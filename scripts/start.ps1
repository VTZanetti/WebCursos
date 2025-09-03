# WebCurso Startup Script for PowerShell
Write-Host "🎓 Starting WebCurso Application..." -ForegroundColor Green
Write-Host "==================================================" -ForegroundColor Green

# Start backend server
Write-Host "🔧 Starting backend server..." -ForegroundColor Yellow
Set-Location -Path "backend"
$env:FLASK_APP = "app.py"
$env:FLASK_ENV = "development"

# Check if database exists, if not initialize it
if (!(Test-Path -Path "instance/database.sqlite")) {
    Write-Host "💾 Initializing database..." -ForegroundColor Yellow
    python init_db.py
}

Write-Host "🚀 Starting Flask backend on http://localhost:5000..." -ForegroundColor Cyan
python -m flask run --port 5000 --host 127.0.0.1