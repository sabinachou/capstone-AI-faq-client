#!/bin/bash

# AI FAQ System Stop Script
# Script to stop the AI FAQ system

echo "🛑 Stopping AI FAQ System..."
echo "============================="

# Set working directory
cd "$(dirname "$0")"

# Stop backend service
if [ -f "logs/backend.pid" ]; then
    BACKEND_PID=$(cat logs/backend.pid)
    if kill -0 $BACKEND_PID 2>/dev/null; then
        echo "🔧 Stopping backend (PID: $BACKEND_PID)..."
        kill $BACKEND_PID
        sleep 2
        if kill -0 $BACKEND_PID 2>/dev/null; then
            echo "⚠️  Backend still running, force killing..."
            kill -9 $BACKEND_PID
        fi
        echo "✅ Backend stopped"
    else
        echo "ℹ️  Backend not running"
    fi
    rm -f logs/backend.pid
else
    echo "ℹ️  No backend PID file found"
fi

# Stop frontend service
if [ -f "logs/frontend.pid" ]; then
    FRONTEND_PID=$(cat logs/frontend.pid)
    if kill -0 $FRONTEND_PID 2>/dev/null; then
        echo "🌐 Stopping frontend (PID: $FRONTEND_PID)..."
        kill $FRONTEND_PID
        sleep 2
        if kill -0 $FRONTEND_PID 2>/dev/null; then
            echo "⚠️  Frontend still running, force killing..."
            kill -9 $FRONTEND_PID
        fi
        echo "✅ Frontend stopped"
    else
        echo "ℹ️  Frontend not running"
    fi
    rm -f logs/frontend.pid
else
    echo "ℹ️  No frontend PID file found"
fi

# Check if there are any remaining processes running
echo "🔍 Checking for remaining processes..."
REMAINING_PIDS=$(pgrep -f "python3 app.py\|npm start" | tr '\n' ' ')

if [ -n "$REMAINING_PIDS" ]; then
    echo "⚠️  Found remaining processes: $REMAINING_PIDS"
    echo "🔄 Force killing remaining processes..."
    echo $REMAINING_PIDS | xargs kill -9
    echo "✅ All processes stopped"
else
    echo "✅ No remaining processes found"
fi

echo ""
echo "🎉 AI FAQ System stopped successfully!"
echo "🚀 To restart, run: ./auto-start.sh"
