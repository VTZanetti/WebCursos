# 🚀 Batch File Startup Guide for WebCurso

This guide explains how to start the WebCurso application using the batch file on Windows.

## 📋 Prerequisites

Before starting, make sure you have these installed:
- Python 3.8 or higher
- Node.js 16 or higher

## ▶️ Starting the Application

### Using the Batch File (Recommended)

Simply double-click on [start.bat](file:///C:/Dev/WebCurso/start.bat) or run it from the command line:

```cmd
start.bat
```

This will:
1. Open a new command window for the backend server
2. Wait 5 seconds for the backend to start
3. Open a new command window for the frontend server
4. Open your browser to http://localhost:5173

## 🛠️ What the Batch File Does

The [start.bat](file:///C:/Dev/WebCurso/start.bat) file performs these actions:

1. **Starts the backend server** in a new command window:
   - Changes to the `backend` directory
   - Sets the required environment variables
   - Starts the Flask server on port 5000

2. **Waits 5 seconds** for the backend to initialize

3. **Starts the frontend server** in another command window:
   - Changes to the `frontend` directory
   - Starts the Vue.js development server on port 5173

4. **Opens your browser** to the frontend application

## 🌐 Access the Application

After starting the servers:
- **Main Application**: http://localhost:5173
- **API Endpoints**: http://localhost:5000/api

## ⚠️ Common Issues

### Port Already in Use
If you see an error about ports being in use:
1. Close any existing command windows running the servers
2. Or change the ports in the batch file

### Dependencies Not Found
If you get errors about missing dependencies:
1. Make sure Python and Node.js are installed
2. Check that you can run `python --version` and `npm --version` in a command prompt

### Database Issues
If there are database errors:
1. Delete the `backend/instance/database.sqlite` file
2. Run the batch file again to reinitialize the database

## 🔄 Development Workflow

1. Make backend changes in `backend/app.py`
2. Make frontend changes in `frontend/src/`
3. Both servers support hot-reloading
4. No build step needed for development

## 📛 Stopping the Servers

Close both command windows that were opened by the batch file, or press `Ctrl + C` in each window.

## 🛠️ Manual Batch Commands

If you want to understand what the batch file does, here are the individual commands:

### Start Backend:
```cmd
cd backend
set FLASK_APP=app.py
set FLASK_ENV=development
python -m flask run --port 5000 --host 127.0.0.1
```

### Start Frontend:
```cmd
cd frontend
npm run dev
```