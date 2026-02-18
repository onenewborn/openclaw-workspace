#!/usr/bin/env python3
"""
LightMemoryOS - 轻量级记忆操作系统
为 OpenClaw 设计的简化版 EverMemOS
"""

import os
import json
import sqlite3
import re
from datetime import datetime
from typing import List, Dict, Any, Optional

# 尝试导入 ChromaDB，如果失败则使用纯 SQLite
try:
    import chromadb
    from chromadb.utils import embedding_functions
    CHROMA_AVAILABLE = True
except ImportError:
    CHROMA_AVAILABLE = False
    print("Warning: ChromaDB not available, using SQLite fallback")

class LightMemoryOS:
    """轻量级记忆操作系统"""
    
    def __init__(self, persist_dir: str = "/root/.openclaw/memory_db"):
        """
        初始化记忆系统
        
        Args:
            persist_dir: 数据持久化目录
        """
        self.persist_dir = persist_dir
        os.makedirs(persist_dir, exist_ok=True)
        
        if CHROMA_AVAILABLE:
            # 使用 ChromaDB 向量存储
            self.client = chromadb.PersistentClient(path=persist_dir)
            self.collection = self.client.get_or_create_collection(
                name="memories",
                metadata={"description": "OpenClaw conversation memories"}
            )
        else:
            # 使用 SQLite 回退方案
            self.db_path = os.path.join(persist_dir, "memories.db")
            self._init_sqlite()
        
        # 记忆统计
        self.stats = {"stored": 0, "retrieved": 0}
    
    def _init_sqlite(self):
        """初始化 SQLite 数据库"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # 创建记忆表
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS memories (
                id TEXT PRIMARY KEY,
                content TEXT NOT NULL,
                timestamp TEXT NOT NULL,
                sender TEXT,
                facts TEXT,  -- JSON 数组
                preferences TEXT,  -- JSON 数组
                relations TEXT,  -- JSON 数组
                topics TEXT,  -- JSON 数组
                importance REAL DEFAULT 0.5
            )
        """)
        
        # 创建全文检索索引
        cursor.execute("""
            CREATE VIRTUAL TABLE IF NOT EXISTS memories_fts USING fts5(
                content, sender, topics,
                content_rowid=rowid
            )
        """)
        
        conn.commit()
        conn.close()
    
    def store(self, 
              content: str, 
              sender: str = "user",
              timestamp: Optional[str] = None,
              metadata: Optional[Dict] = None) -> str:
        """
        存储一条记忆
        
        Args:
            content: 记忆内容
            sender: 发送者 (user/assistant)
            timestamp: 时间戳 (ISO格式)
            metadata: 额外元数据
            
        Returns:
            memory_id: 记忆唯一ID
        """
        if timestamp is None:
            timestamp = datetime.now().isoformat()
        
        memory_id = f"mem_{datetime.now().timestamp()}"
        
        # 提取结构化信息 (简化版)
        facts = self._extract_facts(content)
        preferences = self._extract_preferences(content)
        relations = self._extract_relations(content)
        topics = self._extract_topics(content)
        importance = self._calculate_importance(content)
        
        if CHROMA_AVAILABLE:
            # 使用 ChromaDB
            self.collection.add(
                documents=[content],
                metadatas=[{
                    "timestamp": timestamp,
                    "sender": sender,
                    "facts": json.dumps(facts),
                    "preferences": json.dumps(preferences),
                    "relations": json.dumps(relations),
                    "topics": json.dumps(topics),
                    "importance": importance
                }],
                ids=[memory_id]
            )
        else:
            # 使用 SQLite
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT INTO memories 
                (id, content, timestamp, sender, facts, preferences, relations, topics, importance)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                memory_id, content, timestamp, sender,
                json.dumps(facts), json.dumps(preferences),
                json.dumps(relations), json.dumps(topics), importance
            ))
            
            cursor.execute("""
                INSERT INTO memories_fts (content, sender, topics)
                VALUES (?, ?, ?)
            """, (content, sender, json.dumps(topics)))
            
            conn.commit()
            conn.close()
        
        self.stats["stored"] += 1
        return memory_id
    
    def retrieve(self, 
                 query: str, 
                 n_results: int = 5,
                 memory_type: Optional[str] = None) -> List[Dict]:
        """
        检索相关记忆
        
        Args:
            query: 查询文本
            n_results: 返回结果数量
            memory_type: 记忆类型过滤 (可选)
            
        Returns:
            List[Dict]: 相关记忆列表
        """
        if CHROMA_AVAILABLE:
            # ChromaDB 向量检索
            results = self.collection.query(
                query_texts=[query],
                n_results=n_results
            )
            
            memories = []
            for i in range(len(results["ids"][0])):
                memories.append({
                    "id": results["ids"][0][i],
                    "content": results["documents"][0][i],
                    "metadata": results["metadatas"][0][i],
                    "distance": results["distances"][0][i] if "distances" in results else None
                })
        else:
            # SQLite 全文检索
            memories = self._search_sqlite(query, n_results)
        
        self.stats["retrieved"] += len(memories)
        return memories
    
    def _search_sqlite(self, query: str, n_results: int) -> List[Dict]:
        """SQLite 检索实现 - 使用 LIKE 匹配"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # 提取查询关键词
        keywords = [w for w in query.split() if len(w) > 1]
        if not keywords:
            keywords = [query]
        
        # 构建 LIKE 查询
        conditions = []
        params = []
        for kw in keywords:
            conditions.append("(content LIKE ? OR topics LIKE ?)")
            params.extend([f"%{kw}%", f"%{kw}%"])
        
        where_clause = " OR ".join(conditions) if conditions else "1=1"
        
        cursor.execute(f"""
            SELECT * FROM memories
            WHERE {where_clause}
            ORDER BY importance DESC, timestamp DESC
            LIMIT ?
        """, params + [n_results])
        
        results = []
        for row in cursor.fetchall():
            results.append({
                "id": row[0],
                "content": row[1],
                "metadata": {
                    "timestamp": row[2],
                    "sender": row[3],
                    "facts": json.loads(row[4]) if row[4] else [],
                    "preferences": json.loads(row[5]) if row[5] else [],
                    "relations": json.loads(row[6]) if row[6] else [],
                    "topics": json.loads(row[7]) if row[7] else [],
                    "importance": row[8]
                }
            })
        
        conn.close()
        return results
    
    def _extract_facts(self, content: str) -> List[str]:
        """提取事实性信息 (简化版规则)"""
        facts = []
        # 简单规则：包含"是"、"在"、"有"的句子可能是事实
        sentences = content.split("。")
        for sent in sentences:
            if any(kw in sent for kw in ["是", "在", "有", "喜欢", "讨厌", "叫"]):
                if len(sent) > 5 and len(sent) < 100:
                    facts.append(sent.strip())
        return facts[:3]  # 最多提取3个事实
    
    def _extract_preferences(self, content: str) -> List[str]:
        """提取偏好信息"""
        prefs = []
        keywords = ["喜欢", "讨厌", "不爱", "想", "希望", "习惯"]
        sentences = content.split("。")
        for sent in sentences:
            if any(kw in sent for kw in keywords):
                prefs.append(sent.strip())
        return prefs[:2]
    
    def _extract_relations(self, content: str) -> List[Dict]:
        """提取关系信息"""
        relations = []
        # 简单模式匹配："X是Y的Z"
        import re
        patterns = [
            r"(\w+)是(\w+)的(\w+)",
            r"(\w+)和(\w+)是(\w+)"
        ]
        for pattern in patterns:
            matches = re.findall(pattern, content)
            for match in matches:
                relations.append({
                    "subject": match[0],
                    "relation": match[2],
                    "object": match[1]
                })
        return relations[:2]
    
    def _extract_topics(self, content: str) -> List[str]:
        """提取主题关键词"""
        # 简单关键词提取
        words = content.split()
        # 过滤停用词并返回前5个较长的词
        stopwords = set(["的", "了", "是", "我", "你", "在", "和", "就", "都", "要"])
        keywords = [w for w in words if len(w) > 1 and w not in stopwords]
        return list(set(keywords))[:5]
    
    def _calculate_importance(self, content: str) -> float:
        """计算记忆重要性分数"""
        importance = 0.5  # 基础分
        
        # 长度因子
        if len(content) > 50:
            importance += 0.1
        if len(content) > 100:
            importance += 0.1
        
        # 关键词因子
        important_keywords = ["决定", "重要", "关键", "计划", "目标", "喜欢", "讨厌"]
        for kw in important_keywords:
            if kw in content:
                importance += 0.05
        
        return min(importance, 1.0)
    
    def get_stats(self) -> Dict:
        """获取记忆系统统计信息"""
        if CHROMA_AVAILABLE:
            count = self.collection.count()
        else:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM memories")
            count = cursor.fetchone()[0]
            conn.close()
        
        return {
            "total_memories": count,
            "stored_this_session": self.stats["stored"],
            "retrieved_this_session": self.stats["retrieved"],
            "storage_backend": "ChromaDB" if CHROMA_AVAILABLE else "SQLite"
        }
    
    def consolidate(self):
        """
        记忆整合 (简化版)
        合并相似记忆，清理低重要性记忆
        """
        # TODO: 实现记忆整合逻辑
        pass


# CLI 接口
if __name__ == "__main__":
    import sys
    
    memory = LightMemoryOS()
    
    if len(sys.argv) < 2:
        print("Usage: python light_memory_os.py <command> [args]")
        print("Commands: store <content> | retrieve <query> | stats")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == "store" and len(sys.argv) >= 3:
        content = sys.argv[2]
        sender = sys.argv[3] if len(sys.argv) >= 4 else "user"
        mid = memory.store(content, sender)
        print(f"Stored memory: {mid}")
    
    elif command == "retrieve" and len(sys.argv) >= 3:
        query = sys.argv[2]
        n = int(sys.argv[3]) if len(sys.argv) >= 4 else 5
        results = memory.retrieve(query, n)
        print(json.dumps(results, indent=2, ensure_ascii=False))
    
    elif command == "stats":
        print(json.dumps(memory.get_stats(), indent=2))
    
    else:
        print(f"Unknown command: {command}")
