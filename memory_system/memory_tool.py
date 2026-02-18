#!/usr/bin/env python3
"""
memory_tool.py - OpenClaw 记忆工具
替代内置的 memory_search，使用 LightMemoryOS
"""

import sys
import json
import requests

API_BASE = "http://localhost:1996"

def search(query, max_results=5):
    """搜索记忆"""
    try:
        response = requests.post(
            f"{API_BASE}/search",
            json={"query": query, "max_results": max_results},
            timeout=5
        )
        return response.json()
    except Exception as e:
        return {"error": str(e), "results": []}

def store(content, sender="assistant"):
    """存储记忆"""
    try:
        response = requests.post(
            f"{API_BASE}/store",
            json={"content": content, "sender": sender},
            timeout=5
        )
        return response.json()
    except Exception as e:
        return {"error": str(e)}

def stats():
    """获取统计"""
    try:
        response = requests.get(f"{API_BASE}/stats", timeout=5)
        return response.json()
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python memory_tool.py <command> [args]")
        print("Commands:")
        print("  search <query> [max_results]  - 搜索记忆")
        print("  store <content> [sender]      - 存储记忆")
        print("  stats                         - 查看统计")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == "search" and len(sys.argv) >= 3:
        query = sys.argv[2]
        max_results = int(sys.argv[3]) if len(sys.argv) >= 4 else 5
        result = search(query, max_results)
        print(json.dumps(result, indent=2, ensure_ascii=False))
    
    elif command == "store" and len(sys.argv) >= 3:
        content = sys.argv[2]
        sender = sys.argv[3] if len(sys.argv) >= 4 else "assistant"
        result = store(content, sender)
        print(json.dumps(result, indent=2, ensure_ascii=False))
    
    elif command == "stats":
        result = stats()
        print(json.dumps(result, indent=2, ensure_ascii=False))
    
    else:
        print(f"Unknown command or missing arguments: {command}")
        sys.exit(1)
