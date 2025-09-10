#!/bin/bash

# WebCurso Startup Script for Linux
echo "🎓 Starting WebCurso Application..."
echo "=================================================="

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" &>/dev/null && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"

echo "Project directory: $PROJECT_DIR"

# Function to start backend
start_backend() {
    echo "🔧 Starting backend server..."
    cd "$PROJECT_DIR/backend"
    
    # Check if virtual environment exists
    if [ ! -d "venv" ]; then
        echo "🐍 Creating virtual environment..."
        python3 -m venv venv
    fi
    
    # Activate virtual environment
    source venv/bin/activate
    
    # Install dependencies
    echo "📦 Installing backend dependencies..."
    pip install -r requirements.txt
    
    # Initialize database if needed
    if [ ! -d "instance" ]; then
        mkdir instance
    fi
    
    if [ ! -f "instance/database.sqlite" ]; then
        echo "💾 Initializing database..."
        python init_db.py
    fi
    
    # Start Flask app
    echo "🚀 Starting Flask backend on http://0.0.0.0:5001..."
    export FLASK_APP=app.py
    export FLASK_ENV=production
    python -m flask run --port 5001 --host 0.0.0.0
}

# Function to start frontend
start_frontend() {
    echo "🎨 Starting frontend server..."
    cd "$PROJECT_DIR/frontend"
    
    # Install dependencies if node_modules doesn't exist
    if [ ! -d "node_modules" ]; then
        echo "📦 Installing frontend dependencies..."
        npm install
    fi
    
    # Build and serve the application
    echo "🚀 Starting Vue.js frontend on http://0.0.0.0:3001..."
    npm run build
    npx serve -s dist -l 3001 -n
}

# Check if we should start both, backend only, or frontend only
if [ "$1" = "backend" ]; then
    start_backend
elif [ "$1" = "frontend" ]; then
    start_frontend
else
    # Start both in background
    echo "🔧 Starting backend server in background..."
    start_backend &
    BACKEND_PID=$!
    
    # Wait a bit for backend to start
    sleep 5
    
    echo "🎨 Starting frontend server..."
    start_frontend
    
    # Kill backend when frontend exits
    kill $BACKEND_PID
fi