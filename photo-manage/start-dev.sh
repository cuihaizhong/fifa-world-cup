#!/bin/bash

# 时光胶囊 - 开发环境启动脚本
# 支持离线环境，无需npm/node.js

echo "🚀 时光胶囊 - 开发环境启动脚本"
echo "====================================="

# 检查Python是否可用
if ! command -v python3 &> /dev/null; then
    echo "❌ 错误: Python3 未找到"
    echo "请安装Python3: https://www.python.org/downloads/"
    exit 1
fi

echo "✅ Python3 已找到: $(python3 --version)"

# 检查前端目录是否存在
if [ ! -d "frontend" ]; then
    echo "❌ 错误: frontend 目录不存在"
    exit 1
fi

echo "📁 前端项目目录: $(pwd)/frontend"

# 启动Python API服务器（端口3001）
echo "🌐 启动时光胶囊服务器 (端口 3000)..."
python3 server.py &
SERVER_PID=$!
echo "✅ 服务器PID: $SERVER_PID"

# 等待一秒让服务器启动
sleep 1

# 检查服务器是否成功启动
if ! kill -0 $SERVER_PID 2>/dev/null; then
    echo "❌ 服务器启动失败"
    exit 1
fi

echo "🎉 静态文件服务器已启动: http://localhost:3000"

# 检查Node.js环境（可选）
if command -v node &> /dev/null && command -v npm &> /dev/null; then
    echo "📦 检测到Node.js环境"
    echo "💡 提示: 可使用 npm run dev 获得热重载体验"
else
    echo "⚠️  未检测到Node.js/npm，使用纯Python服务器模式"
    echo "📝 提示: 安装Node.js可获得更好的开发体验"
fi

echo ""
echo "🎉 开发环境启动成功!"
echo "====================================="
echo "🌐 前端访问地址: http://localhost:3000"
echo "📊 API服务: 集成在同一服务器中"
echo ""
echo "📋 支持的功能:"
echo "  • 相册管理 (创建、查看、编辑)"
echo "  • 旅行足迹 (地理位置管理)"
echo "  • 照片浏览 (网格布局)"
echo "  • 搜索过滤 (实时搜索)"
echo "  • 响应式设计 (移动端适配)"
echo ""
echo "❌ 停止服务: Ctrl+C 或者 kill $SERVER_PID"

# 等待用户中断
wait
