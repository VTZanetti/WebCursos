# WebCurso Startup Script for PowerShell
Write-Host "🎓 Starting WebCurso Application..." -ForegroundColor Green
Write-Host "==================================================" -ForegroundColor Green

# Get the full path of the current script directory
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RootDir = Split-Path -Parent $ScriptDir

Write-Host "Root directory: $RootDir" -ForegroundColor Yellow

# Start backend server
Write-Host "🔧 Starting backend server..." -ForegroundColor Yellow
Set-Location -Path "$RootDir\backend"
$env:FLASK_APP = "app.py"
$env:FLASK_ENV = "development"

# Check if database exists, if not initialize it
if (!(Test-Path -Path "instance/database.sqlite")) {
    Write-Host "💾 Initializing database..." -ForegroundColor Yellow
    python init_db.py
}

Write-Host "🚀 Starting Flask backend on http://localhost:5000..." -ForegroundColor Cyan
# Start backend in background using a job
$job = Start-Job -ScriptBlock {
    Set-Location -Path "$using:RootDir\backend"
    python -m flask run --port 5000 --host 127.0.0.1
}

# Wait a bit for backend to start
Start-Sleep -Seconds 5

# Open browser
Start-Process "http://localhost:5173"

# Start frontend server
Write-Host "🎨 Starting frontend server..." -ForegroundColor Yellow
Set-Location -Path "$RootDir\frontend"

# Check if node_modules exists, if not install dependencies
if (!(Test-Path -Path "node_modules")) {
    Write-Host "📦 Installing frontend dependencies..." -ForegroundColor Yellow
    # Use cmd to bypass PowerShell execution policy issues
    cmd /c "npm install"
}

Write-Host "🚀 Starting Vue.js frontend on http://localhost:5173..." -ForegroundColor Cyan
# Use cmd to bypass PowerShell execution policy issues
cmd /c "npm run dev"