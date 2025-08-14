#!/bin/bash

# AI FAQ System Auto-Start Script
# 自动启动AI FAQ系统的脚本

echo "🚀 AI FAQ System Auto-Start Script"
echo "=================================="

# 设置工作目录
cd "$(dirname "$0")"
echo "📁 Working directory: $(pwd)"

# 检查必要的服务
check_services() {
    echo "🔍 Checking required services..."
    
    # 检查Python
    if ! command -v python3 &> /dev/null; then
        echo "❌ Python3 not found. Installing..."
        # 这里可以添加自动安装Python的逻辑
        return 1
    fi
    
    # 检查Node.js
    if ! command -v npm &> /dev/null; then
        echo "❌ Node.js not found. Installing..."
        # 这里可以添加自动安装Node.js的逻辑
        return 1
    fi
    
    echo "✅ All required services are available"
    return 0
}

# 启动后端服务
start_backend() {
    echo "🔧 Starting Flask backend..."
    cd faq-backend
    
    # 检查是否已经有后端在运行
    if curl -s http://localhost:5000/api/health > /dev/null 2>&1; then
        echo "✅ Backend is already running on port 5000"
        cd ..
        return 0
    fi
    
    # 启动后端
    nohup python3 app.py > ../logs/backend.log 2>&1 &
    BACKEND_PID=$!
    echo $BACKEND_PID > ../logs/backend.pid
    
    # 等待后端启动
    echo "⏳ Waiting for backend to start..."
    for i in {1..30}; do
        if curl -s http://localhost:5000/api/health > /dev/null 2>&1; then
            echo "✅ Backend started successfully on port 5000"
            cd ..
            return 0
        fi
        sleep 1
        echo -n "."
    done
    
    echo "❌ Backend failed to start"
    cd ..
    return 1
}

# 启动前端服务
start_frontend() {
    echo "🌐 Starting React frontend..."
    cd faq-frontend
    
    # 检查是否已经有前端在运行
    if curl -s http://localhost:3000 > /dev/null 2>&1; then
        echo "✅ Frontend is already running on port 3000"
        cd ..
        return 0
    fi
    
    # 启动前端
    export PORT=3000
    nohup npm start > ../logs/frontend.log 2>&1 &
    FRONTEND_PID=$!
    echo $FRONTEND_PID > ../logs/frontend.pid
    
    # 等待前端启动
    echo "⏳ Waiting for frontend to start..."
    for i in {1..30}; do
        if curl -s http://localhost:3000 > /dev/null 2>&1; then
            echo "✅ Frontend started successfully on port 3000"
            cd ..
            return 0
        fi
        sleep 1
        echo -n "."
    done
    
    echo "❌ Frontend failed to start"
    cd ..
    return 1
}

# 创建日志目录
mkdir -p logs

# 主启动流程
main() {
    echo "🔄 Starting AI FAQ System..."
    
    # 检查服务
    if ! check_services; then
        echo "❌ Service check failed"
        exit 1
    fi
    
    # 启动后端
    if ! start_backend; then
        echo "❌ Backend startup failed"
        exit 1
    fi
    
    # 启动前端
    if ! start_frontend; then
        echo "❌ Frontend startup failed"
        exit 1
    fi
    
    echo ""
    echo "🎉 AI FAQ System started successfully!"
    echo "📱 Frontend: http://localhost:3000"
    echo "🔧 Backend: http://localhost:5000/api"
    echo "📊 Health: http://localhost:5000/api/health"
    echo ""
    echo "📝 Logs are available in the logs/ directory"
    echo "🛑 To stop services, run: ./stop-services.sh"
}

# 运行主函数
main "$@"
