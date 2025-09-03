# WebCurso Backend Startup Script for PowerShell
Write-Host "🎓 Starting WebCurso Backend..." -ForegroundColor Green
Write-Host "==================================================" -ForegroundColor Green

# Change to backend directory
Set-Location -Path "backend"

# Set environment variables for Flask
$env:FLASK_APP = "app.py"
$env:FLASK_ENV = "development"

Write-Host "🔧 Checking database..." -ForegroundColor Yellow

# Check if instance directory exists, if not create it
if (!(Test-Path -Path "instance")) {
    New-Item -ItemType Directory -Name "instance"
}

# Check if database exists, if not initialize it
if (!(Test-Path -Path "instance/database.sqlite")) {
    Write-Host "💾 Initializing database..." -ForegroundColor Yellow
    python init_db.py
}

Write-Host "🚀 Starting Flask backend on http://localhost:5000..." -ForegroundColor Cyan
Write-Host "Press CTRL+C to stop the server" -ForegroundColor Gray

python -m flask run --port 5000 --host 127.0.0.1