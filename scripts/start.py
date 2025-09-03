#!/usr/bin/env python3
"""
Simplified WebCurso Application
Single file to run both backend and frontend
"""

import os
import sys
import subprocess
import threading
import time
import webbrowser
from pathlib import Path


def setup_backend():
    """Setup and run the Flask backend"""
    print("🔧 Setting up backend...")
    
    # Change to backend directory
    backend_dir = Path("backend")
    if not backend_dir.exists():
        print("❌ Backend directory not found!")
        return False
    
    original_dir = os.getcwd()
    os.chdir(backend_dir)
    
    try:
        # Create virtual environment if it doesn't exist
        venv_dir = Path("venv")
        if not venv_dir.exists():
            print("🐍 Creating virtual environment...")
            subprocess.run([sys.executable, "-m", "venv", "venv"], check=True)
        
        # Activate virtual environment and install requirements
        if sys.platform == "win32":
            pip_path = venv_dir / "Scripts" / "pip.exe"
            python_path = venv_dir / "Scripts" / "python.exe"
        else:
            pip_path = venv_dir / "bin" / "pip"
            python_path = venv_dir / "bin" / "python"
        
        print("📦 Installing backend dependencies...")
        subprocess.run([str(pip_path), "install", "-r", "requirements.txt"], check=True)
        
        # Initialize database if needed
        instance_path = Path("instance")
        if not instance_path.exists():
            instance_path.mkdir()
            
        db_path = instance_path / "database.sqlite"
        if not db_path.exists():
            print("💾 Initializing database...")
            subprocess.run([str(python_path), "init_db.py"], check=True)
        
        # Set environment variables for Flask
        os.environ["FLASK_APP"] = "app.py"
        os.environ["FLASK_ENV"] = "development"
        
        # Run Flask app
        print("🚀 Starting Flask backend on http://localhost:5000...")
        subprocess.run([str(python_path), "-m", "flask", "run", "--port", "5000", "--host", "127.0.0.1"], check=True)
            
    except subprocess.CalledProcessError as e:
        print(f"❌ Error running backend: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error in backend: {e}")
        return False
    finally:
        os.chdir(original_dir)  # Return to root directory
    
    return True


def setup_frontend():
    """Setup and run the Vue.js frontend"""
    print("🎨 Setting up frontend...")
    
    # Change to frontend directory
    frontend_dir = Path("frontend")
    if not frontend_dir.exists():
        print("❌ Frontend directory not found!")
        return False
    
    original_dir = os.getcwd()
    os.chdir(frontend_dir)
    
    try:
        # Install npm dependencies if node_modules doesn't exist
        node_modules_dir = Path("node_modules")
        if not node_modules_dir.exists():
            print("📦 Installing frontend dependencies...")
            subprocess.run(["npm", "install"], check=True)
        
        # Run development server
        print("🚀 Starting Vue.js frontend on http://localhost:5173...")
        subprocess.run(["npm", "run", "dev"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ Error running frontend: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error in frontend: {e}")
        return False
    finally:
        os.chdir(original_dir)  # Return to root directory
    
    return True


def start_servers():
    """Start both backend and frontend servers"""
    print("🎓 Starting WebCurso Application...")
    print("=" * 50)
    
    # Start backend in a separate thread
    print("🔧 Starting backend server...")
    backend_thread = threading.Thread(target=setup_backend)
    backend_thread.daemon = True
    backend_thread.start()
    
    # Give backend some time to start
    print("⏳ Waiting for backend to start...")
    time.sleep(8)
    
    # Open browser to frontend
    print("🌐 Opening browser...")
    webbrowser.open("http://localhost:5173")
    
    # Start frontend in main thread
    print("🎨 Starting frontend server...")
    setup_frontend()


def main():
    """Main function to start both backend and frontend"""
    try:
        start_servers()
    except KeyboardInterrupt:
        print("\n🛑 Shutting down servers...")
        sys.exit(0)
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()