#!/usr/bin/env python3
"""
Memory API Server - 为 OpenClaw 提供记忆服务
轻量级 HTTP API，替代 memory_search 工具
"""

import json
import sys
import os
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

# 添加父目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from light_memory_os import LightMemoryOS

# 全局记忆实例
memory = LightMemoryOS()

class MemoryHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        """处理 GET 请求"""
        parsed = urlparse(self.path)
        path = parsed.path
        query = parse_qs(parsed.query)
        
        if path == "/health":
            self._send_json({"status": "healthy", "service": "memory-api"})
        
        elif path == "/stats":
            stats = memory.get_stats()
            self._send_json(stats)
        
        else:
            self._send_error(404, "Not found")
    
    def do_POST(self):
        """处理 POST 请求"""
        content_length = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(content_length).decode('utf-8')
        
        try:
            data = json.loads(post_data) if post_data else {}
        except json.JSONDecodeError:
            self._send_error(400, "Invalid JSON")
            return
        
        parsed = urlparse(self.path)
        path = parsed.path
        
        if path == "/store":
            # 存储记忆
            content = data.get("content", "")
            sender = data.get("sender", "user")
            timestamp = data.get("timestamp")
            
            if not content:
                self._send_error(400, "Missing 'content' field")
                return
            
            memory_id = memory.store(content, sender, timestamp)
            self._send_json({"success": True, "memory_id": memory_id})
        
        elif path == "/retrieve":
            # 检索记忆
            query = data.get("query", "")
            n_results = data.get("n_results", 5)
            
            if not query:
                self._send_error(400, "Missing 'query' field")
                return
            
            results = memory.retrieve(query, n_results)
            self._send_json({
                "success": True,
                "query": query,
                "results": results,
                "count": len(results)
            })
        
        elif path == "/search":
            # 兼容 OpenClaw 的 memory_search 接口
            query = data.get("query", "")
            max_results = data.get("max_results", 5)
            
            results = memory.retrieve(query, max_results)
            
            # 转换为 OpenClaw 期望的格式
            formatted_results = []
            for r in results:
                formatted_results.append({
                    "path": "memory_db",
                    "startLine": 1,
                    "endLine": 1,
                    "score": r["metadata"].get("importance", 0.5),
                    "snippet": r["content"][:200],
                    "source": "memory",
                    "citation": f"memory://{r['id']}"
                })
            
            self._send_json({
                "results": formatted_results,
                "provider": "LightMemoryOS",
                "model": "local-sqlite"
            })
        
        else:
            self._send_error(404, "Not found")
    
    def _send_json(self, data):
        """发送 JSON 响应"""
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(data, ensure_ascii=False).encode())
    
    def _send_error(self, code, message):
        """发送错误响应"""
        self.send_response(code)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps({"error": message}).encode())
    
    def log_message(self, format, *args):
        """简化日志输出"""
        print(f"[MemoryAPI] {args[0]}")

def run_server(port=1996):
    """启动记忆 API 服务"""
    server = HTTPServer(('localhost', port), MemoryHandler)
    print(f"🧠 Memory API Server running at http://localhost:{port}")
    print(f"   - Health check: GET http://localhost:{port}/health")
    print(f"   - Store memory: POST http://localhost:{port}/store")
    print(f"   - Retrieve:     POST http://localhost:{port}/retrieve")
    print(f"   - Stats:        GET http://localhost:{port}/stats")
    print("\nPress Ctrl+C to stop")
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n👋 Shutting down...")
        server.shutdown()

if __name__ == "__main__":
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 1996
    run_server(port)
