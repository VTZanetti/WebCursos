# How to Run the WebCurso Application

This document explains the different ways to run the WebCurso application and troubleshoot common issues.

## Prerequisites

Before running the application, ensure you have the following installed:
- Python 3.8 or higher
- Node.js 16 or higher
- npm (comes with Node.js)

## Method 1: Using the Python Startup Script (Recommended)

This is the easiest way to start both the backend and frontend servers simultaneously.

### Steps:
1. Open Command Prompt (not PowerShell)
2. Navigate to the scripts directory:
   ```
   cd /d c:\Users\vitor\OneDrive\Documentos\Dev\WebCursos\scripts
   ```
3. Run the Python startup script:
   ```
   python start.py
   ```

This will:
- Automatically create virtual environments for backend and frontend
- Install all required dependencies
- Start both servers
- Open your browser to the application

## Method 2: Using the Batch File

### Steps:
1. Open Command Prompt (not PowerShell)
2. Navigate to the scripts directory:
   ```
   cd /d c:\Users\vitor\OneDrive\Documentos\Dev\WebCursos\scripts
   ```
3. Run the batch file:
   ```
   start.bat
   ```

## Method 3: Using PowerShell Scripts

### Steps:
1. Open PowerShell
2. Navigate to the scripts directory:
   ```
   cd c:\Users\vitor\OneDrive\Documentos\Dev\WebCursos\scripts
   ```
3. Run one of the following:
   - For both backend and frontend:
     ```
     PowerShell -ExecutionPolicy Bypass -File "start.ps1"
     ```
   - For backend only:
     ```
     PowerShell -ExecutionPolicy Bypass -File "start-backend.ps1"
     ```
   - For frontend only:
     ```
     PowerShell -ExecutionPolicy Bypass -File "start-frontend.ps1"
     ```

## Method 4: Manual Startup

If you prefer to start the servers manually:

### Backend:
1. Open Command Prompt
2. Navigate to the backend directory:
   ```
   cd /d c:\Users\vitor\OneDrive\Documentos\Dev\WebCursos\backend
   ```
3. Create a virtual environment:
   ```
   python -m venv venv
   ```
4. Activate the virtual environment:
   ```
   venv\Scripts\activate
   ```
5. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
6. Start the Flask server:
   ```
   python app.py
   ```

### Frontend:
1. Open a new Command Prompt window
2. Navigate to the frontend directory:
   ```
   cd /d c:\Users\vitor\OneDrive\Documentos\Dev\WebCursos\frontend
   ```
3. Install dependencies:
   ```
   npm install
   ```
4. Start the development server:
   ```
   npm run dev
   ```

## Troubleshooting Common Issues

### 1. Virtual Environment Issues
If you encounter errors related to the virtual environment:
1. Delete the existing `venv` folder in the backend directory
2. The startup scripts will automatically recreate it

### 2. Node Modules Issues
If you encounter errors with node_modules:
1. Run the cleanup script:
   - For Command Prompt: `clean_frontend.bat`
   - For PowerShell: `PowerShell -ExecutionPolicy Bypass -File "clean_frontend.ps1"`
2. The startup scripts will automatically reinstall dependencies

### 3. Port Conflicts
If the default ports (5000 for backend, 5173 for frontend) are in use:
- The application will show an error
- Either close the applications using those ports or modify the startup scripts

### 4. Path Issues
If you see errors about file paths:
- Make sure you're running the scripts from the correct directory
- Use the full path method: `cd /d c:\Users\vitor\OneDrive\Documentos\Dev\WebCursos\scripts`

### 5. Permission Errors (Windows)
If you see "Access is denied" errors:
1. Close any applications that might be using the frontend files (especially file explorers or editors with files open)
2. Run the command prompt as Administrator
3. Use the cleanup scripts provided:
   - `clean_frontend.bat` (for Command Prompt)
   - `clean_frontend.ps1` (for PowerShell)

### 6. PowerShell Execution Policy Issues
If you see errors like "running scripts is disabled on this system":
1. Use Command Prompt instead of PowerShell for running the scripts
2. Or use the `-ExecutionPolicy Bypass` parameter when running PowerShell scripts
3. Or temporarily change the execution policy (not recommended for production):
   ```powershell
   Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
   ```

### 7. npm Not Found Errors
If you see "npm not found" or similar errors:
1. Make sure Node.js is installed correctly
2. Make sure npm is in your system PATH
3. Try using Command Prompt instead of PowerShell
4. Restart your terminal/command prompt after installing Node.js

## Important Notes

1. **Do NOT run batch files (.bat) with Python**: 
   - ❌ Wrong: `python start.bat`
   - ✅ Correct: `start.bat` (in Command Prompt)

2. **Use Command Prompt for batch files**: 
   - Batch files work best in Command Prompt, not PowerShell

3. **First-time setup takes longer**: 
   - The first time you run the application, it needs to install dependencies
   - Subsequent runs will be faster

4. **Keep both servers running**: 
   - The application requires both backend and frontend servers to function properly
   - Closing one will affect the functionality of the other

## Accessing the Application

Once both servers are running:
- Frontend: http://localhost:5173
- Backend API: http://localhost:5000

The application should automatically open your browser to the frontend.