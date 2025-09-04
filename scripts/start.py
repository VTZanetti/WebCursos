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
import shutil


def setup_backend():
    """Setup and run the Flask backend"""
    print("🔧 Setting up backend...")
    
    # Change to backend directory - using absolute path
    script_dir = Path(__file__).parent
    root_dir = script_dir.parent
    backend_dir = root_dir / "backend"
    
    if not backend_dir.exists():
        print("❌ Backend directory not found!")
        return False
    
    original_dir = os.getcwd()
    os.chdir(backend_dir)
    
    try:
        # Remove existing virtual environment if it has broken paths
        venv_dir = Path("venv")
        if venv_dir.exists():
            # Check if the venv has broken paths by trying to run pip
            try:
                if sys.platform == "win32":
                    pip_path = venv_dir / "Scripts" / "pip.exe"
                else:
                    pip_path = venv_dir / "bin" / "pip"
                
                if pip_path.exists():
                    # Test if pip works
                    result = subprocess.run([str(pip_path), "--version"], 
                                          capture_output=True, text=True, timeout=10)
                    if result.returncode != 0:
                        print("⚠️  Virtual environment appears to be corrupted, recreating...")
                        shutil.rmtree(venv_dir)
                else:
                    print("⚠️  Virtual environment missing pip, recreating...")
                    shutil.rmtree(venv_dir)
            except (subprocess.TimeoutExpired, subprocess.SubprocessError, FileNotFoundError):
                print("⚠️  Virtual environment appears to be corrupted, recreating...")
                shutil.rmtree(venv_dir)
        
        # Create virtual environment if it doesn't exist
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
    
    # Change to frontend directory - using absolute path
    script_dir = Path(__file__).parent
    root_dir = script_dir.parent
    frontend_dir = root_dir / "frontend"
    
    if not frontend_dir.exists():
        print("❌ Frontend directory not found!")
        return False
    
    original_dir = os.getcwd()
    os.chdir(frontend_dir)
    
    try:
        # Check if node_modules exists but might be corrupted
        node_modules_dir = Path("node_modules")
        package_lock = Path("package-lock.json")
        
        # If node_modules exists but package-lock.json doesn't, or if there are issues, reinstall
        if node_modules_dir.exists():
            try:
                # Test if npm works by checking version using cmd to bypass PowerShell issues
                result = subprocess.run(["cmd", "/c", "npm", "--version"], 
                                      capture_output=True, text=True, timeout=10)
                if result.returncode != 0:
                    print("⚠️  Node modules appear to be corrupted or npm not available, reinstalling...")
                    # Try to remove node_modules, handle permission errors
                    try:
                        shutil.rmtree(node_modules_dir)
                    except PermissionError:
                        print("⚠️  Permission denied while removing node_modules. Trying alternative approach...")
                        # Try using npm to clean cache
                        try:
                            subprocess.run(["cmd", "/c", "npm", "cache", "clean", "--force"], 
                                         capture_output=True, text=True, timeout=30)
                        except:
                            pass
                        # Try to remove with a different approach
                        try:
                            subprocess.run(["cmd", "/c", "rmdir", "/s", "/q", "node_modules"], 
                                         capture_output=True, text=True, timeout=30)
                        except:
                            print("❌ Could not remove node_modules. Please manually delete the folder and try again.")
                            return False
            except (subprocess.TimeoutExpired, subprocess.SubprocessError, FileNotFoundError):
                print("⚠️  Node modules appear to be corrupted or npm not available, reinstalling...")
                try:
                    shutil.rmtree(node_modules_dir)
                except PermissionError:
                    print("⚠️  Permission denied while removing node_modules. Trying alternative approach...")
                    try:
                        subprocess.run(["cmd", "/c", "rmdir", "/s", "/q", "node_modules"], 
                                     capture_output=True, text=True, timeout=30)
                    except:
                        print("❌ Could not remove node_modules. Please manually delete the folder and try again.")
                        return False
        
        # Install npm dependencies if node_modules doesn't exist
        if not node_modules_dir.exists():
            print("📦 Installing frontend dependencies...")
            # Clear npm cache first to avoid issues
            try:
                subprocess.run(["cmd", "/c", "npm", "cache", "clean", "--force"], 
                             capture_output=True, text=True, timeout=30)
            except:
                pass
            
            # Try to run npm install using cmd to bypass PowerShell issues
            try:
                subprocess.run(["cmd", "/c", "npm", "install"], check=True)
            except subprocess.CalledProcessError as e:
                print(f"❌ Error running npm install: {e}")
                print("💡 Troubleshooting tips:")
                print("   1. Make sure Node.js and npm are installed correctly")
                print("   2. Try running 'npm install' manually in the frontend directory")
                print("   3. If using PowerShell, try using Command Prompt instead")
                print("   4. Check if npm is in your system PATH")
                return False
            except FileNotFoundError:
                print("❌ npm not found. Please make sure Node.js is installed and npm is in your system PATH")
                print("💡 Download Node.js from https://nodejs.org/")
                return False
        
        # Run development server using cmd to bypass PowerShell issues
        print("🚀 Starting Vue.js frontend on http://localhost:5173...")
        subprocess.run(["cmd", "/c", "npm", "run", "dev"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ Error running frontend: {e}")
        print("💡 Tip: If you see permission errors, try:")
        print("   1. Closing any applications that might be using the frontend files")
        print("   2. Running this script as Administrator")
        print("   3. Manually deleting the node_modules folder and trying again")
        return False
    except Exception as e:
        print(f"❌ Unexpected error in frontend: {e}")
        print("💡 Tip: If you see permission errors, try:")
        print("   1. Closing any applications that might be using the frontend files")
        print("   2. Running this script as Administrator")
        print("   3. Manually deleting the node_modules folder and trying again")
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