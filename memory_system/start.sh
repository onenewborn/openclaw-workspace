#!/bin/bash
# 启动记忆系统服务

cd /root/.openclaw/workspace/memory_system

echo "🧠 Starting LightMemoryOS API Server..."
echo ""

# 检查 Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 not found"
    exit 1
fi

# 启动 API 服务
python3 memory_api.py 1996 &
PID=$!

# 等待服务启动
sleep 2

# 检查服务是否正常运行
if curl -s http://localhost:1996/health > /dev/null; then
    echo "✅ Memory API Server is running on port 1996"
    echo "   PID: $PID"
    echo ""
    echo "Test commands:"
    echo "  curl http://localhost:1996/health"
    echo "  curl -X POST http://localhost:1996/store -H 'Content-Type: application/json' -d '{\"content\":\"test\",\"sender\":\"user\"}'"
    echo ""
    echo "To stop: kill $PID"
else
    echo "❌ Failed to start server"
    kill $PID 2>/dev/null
    exit 1
fi

# 保存 PID
echo $PID > /tmp/memory_api.pid
