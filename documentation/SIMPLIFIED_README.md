# 🎓 WebCurso - Simplified Version

## 📋 Overview

This is a simplified version of the WebCurso application that consolidates the backend and frontend into a single easy-to-run structure. All unnecessary batch files have been removed and replaced with a streamlined startup process.

## 🏗️ Simplified Structure

```
WebCurso/
├── backend/           # Flask API backend
├── frontend/          # Vue.js frontend
├── start.py          # Python script to run everything
├── start.bat         # Windows batch file for easy startup
├── start-backend.ps1 # PowerShell script for backend
├── start-frontend.ps1 # PowerShell script for frontend
└── README.md         # This file
```

## 🚀 Quick Start

### Option 1: Windows Batch File (Easiest)
Double-click on [start.bat](file:///C:/Dev/WebCurso/start.bat) or run:
```cmd
start.bat
```

### Option 2: Python Script
```bash
python start.py
```

### Option 3: PowerShell Scripts
In separate PowerShell windows:
```powershell
.\start-backend.ps1
.\start-frontend.ps1
```

Any of these methods will:
- Set up the Python virtual environment
- Install all backend dependencies
- Initialize the database
- Install all frontend dependencies
- Start both the Flask backend (port 5000) and Vue.js frontend (port 5173)
- Open your browser automatically

## 🧠 How It Works

### Using start.bat (Windows):
1. Opens a new command window for the backend server
2. Waits for the backend to start
3. Opens a new command window for the frontend server
4. Opens your browser to the application

### Using start.py:
1. Creates a Python virtual environment if needed
2. Installs Flask and other backend dependencies
3. Initializes the SQLite database
4. Installs Node.js dependencies for the frontend
5. Starts both servers concurrently
6. Opens your browser to the application

## 🔧 Manual Control (if needed)

If you prefer to run the backend and frontend separately:

### Backend Only:
```bash
cd backend
python -m venv venv
venv\Scripts\activate  # On Windows
# source venv/bin/activate  # On macOS/Linux
pip install -r requirements.txt
python init_db.py
set FLASK_APP=app.py
set FLASK_ENV=development
python -m flask run --port 5000 --host 127.0.0.1
```

### Frontend Only:
```bash
cd frontend
npm install
npm run dev
```

## 🗄️ Database

The application uses SQLite for data storage. The database file is located at:
```
backend/instance/database.sqlite
```

It will be automatically created when you first run the application.

## 🌐 Accessing the Application

After starting the application:
- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:5000/api

## 📦 Dependencies

### Backend:
- Python 3.8+
- Flask
- Flask-CORS
- SQLite (built into Python)

### Frontend:
- Node.js 16+
- Vue.js 3
- Vue Router
- Axios