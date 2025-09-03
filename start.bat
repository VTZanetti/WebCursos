@echo off
echo 🎓 WebCurso - Simplified Startup
echo ==================================================
echo.
echo 🔧 Starting backend server in a new window...
echo 🎨 Starting frontend server in a new window...
echo.
echo 🌐 Frontend will be available at: http://localhost:5173
echo 🌐 Backend API will be available at: http://localhost:5000
echo.
echo Press any key to start both servers...
pause >nul

REM Start backend server
start "WebCurso Backend" cmd /k "cd backend && set FLASK_APP=app.py && set FLASK_ENV=development && python -m flask run --port 5000 --host 127.0.0.1"

REM Wait a few seconds for backend to start
timeout /t 5 /nobreak >nul

REM Start frontend server
start "WebCurso Frontend" cmd /k "cd frontend && npm run dev"

REM Open browser
timeout /t 3 /nobreak >nul
start http://localhost:5173

echo.
echo ✅ Servers started! Check the new command windows for details.
echo 🌐 Browser opened to http://localhost:5173
echo.
echo Press any key to close this window...
pause >nul