#!/bin/bash

echo "🚀 Starting AI FAQ Application with unified port 5000..."

# Check if Python and Node.js are installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 is not installed. Please install Python 3.8+ first."
    exit 1
fi

if ! command -v npm &> /dev/null; then
    echo "❌ Node.js/npm is not installed. Please install Node.js first."
    exit 1
fi

# Function to cleanup background processes
cleanup() {
    echo "🛑 Shutting down services..."
    kill $BACKEND_PID $FRONTEND_PID 2>/dev/null
    exit 0
}

# Set trap to cleanup on script exit
trap cleanup SIGINT SIGTERM

# Start backend (Flask) on port 5000
echo "🔧 Starting Flask backend on port 5000..."
cd faq-backend
python3 app.py &
BACKEND_PID=$!
cd ..

# Wait a moment for backend to start
sleep 3

# Check if backend is running
if curl -s http://localhost:5000/api/health > /dev/null; then
    echo "✅ Backend is running on port 5000"
else
    echo "❌ Backend failed to start on port 5000"
    kill $BACKEND_PID 2>/dev/null
    exit 1
fi

# Start frontend (React) on port 5000
echo "🌐 Starting React frontend on port 5000..."
cd faq-frontend

# Set environment variable to override React's default port
export PORT=5000
npm start &
FRONTEND_PID=$!
cd ..

echo "🎉 Both services are starting..."
echo "📱 Frontend will be available at: http://localhost:5000"
echo "🔧 Backend API will be available at: http://localhost:5000/api"
echo "📊 Health check: http://localhost:5000/api/health"
echo ""
echo "Press Ctrl+C to stop all services"

# Wait for both processes
wait

