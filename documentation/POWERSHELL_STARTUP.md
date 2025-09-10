# 🚀 PowerShell Startup Guide for WebCurso

This guide explains how to start the WebCurso application using PowerShell on Windows.

## 📋 Prerequisites

Before starting, make sure you have these installed:
- Python 3.8 or higher
- Node.js 16 or higher
- PowerShell 5.1 or higher

## ▶️ Starting the Application

### Option 1: Using the PowerShell Scripts (Recommended)

1. **Start the backend server** in a new PowerShell window:
   ```powershell
   .\start-backend.ps1
   ```

2. **Start the frontend server** in another PowerShell window:
   ```powershell
   .\start-frontend.ps1
   ```

3. **Open your browser** to:
   - Frontend: http://localhost:5173
   - Backend API: http://localhost:5000

### Option 2: Manual Startup

1. **Start the backend**:
   ```powershell
   cd backend
   $env:FLASK_APP = "app.py"
   $env:FLASK_ENV = "development"
   python -m flask run --port 5000 --host 127.0.0.1
   ```

2. **Start the frontend** (in another terminal):
   ```powershell
   cd frontend
   npm run dev
   ```

## 🛠️ PowerShell Scripts

### start-backend.ps1
This script:
- Sets the required environment variables
- Initializes the database if needed
- Starts the Flask backend server on port 5000

### start-frontend.ps1
This script:
- Installs npm dependencies if needed
- Starts the Vue.js frontend development server on port 5173

## 🌐 Access the Application

After starting both servers:
- **Main Application**: http://localhost:5173
- **API Endpoints**: http://localhost:5000/api

## ⚠️ Common PowerShell Issues

### Execution Policy Errors
If you get an error about script execution being disabled:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Running Scripts
To run the PowerShell scripts:

```powershell
.\start-backend.ps1
```

If you get an execution error, try:

```powershell
PowerShell -File .\start-backend.ps1
```

## 🔄 Development Workflow

1. Make backend changes in `backend/app.py`
2. Make frontend changes in `frontend/src/`
3. Both servers support hot-reloading
4. No build step needed for development

## 📛 Stopping the Servers

Press `Ctrl + C` in each PowerShell window to stop the servers.