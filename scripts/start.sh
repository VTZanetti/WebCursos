#!/bin/bash

# WebCurso Startup Script for Linux/macOS
echo "🎓 Starting WebCurso Application..."
echo "=================================================="

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" &>/dev/null && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"

echo "Project directory: $PROJECT_DIR"

# Function to check if port is available
check_port() {
    local port=$1
    if lsof -Pi :$port -sTCP:LISTEN -t >/dev/null 2>&1; then
        return 1
    else
        return 0
    fi
}

# Function to find available port
find_available_port() {
    local start_port=$1
    local port=$start_port
    while ! check_port $port; do
        ((port++))
        if [ $port -gt $((start_port + 10)) ]; then
            echo "Couldn't find available port starting from $start_port"
            return 1
        fi
    done
    echo $port
}

# Find available ports
BACKEND_PORT=$(find_available_port 5001)
FRONTEND_PORT=$(find_available_port 3001)

if [ -z "$BACKEND_PORT" ] || [ -z "$FRONTEND_PORT" ]; then
    echo "❌ Could not find available ports"
    exit 1
fi

echo "📋 Using ports:"
echo "   Backend: $BACKEND_PORT"
echo "   Frontend: $FRONTEND_PORT"

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
    echo "🚀 Starting Flask backend on http://0.0.0.0:$BACKEND_PORT..."
    export FLASK_APP=app.py
    export FLASK_ENV=production
    python -m flask run --port $BACKEND_PORT --host 0.0.0.0
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
    
    # Update vite config with backend port
    echo "🔧 Updating Vite config for backend port $BACKEND_PORT..."
    cat > vite.config.js << EOF
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [vue()],
  server: {
    port: $FRONTEND_PORT,
    host: true,
    proxy: {
      '/api': {
        target: 'http://localhost:$BACKEND_PORT',
        changeOrigin: true,
        secure: false,
        rewrite: (path) => path
      }
    }
  }
})
EOF
    
    # Start development server
    echo "🚀 Starting Vue.js frontend on http://0.0.0.0:$FRONTEND_PORT..."
    npm run dev
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