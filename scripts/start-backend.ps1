# WebCurso Backend Startup Script for PowerShell
Write-Host "🎓 Starting WebCurso Backend..." -ForegroundColor Green
Write-Host "==================================================" -ForegroundColor Green

# Get the full path of the current script directory
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RootDir = Split-Path -Parent $ScriptDir

Write-Host "Script directory: $ScriptDir" -ForegroundColor Yellow
Write-Host "Root directory: $RootDir" -ForegroundColor Yellow

# Change to backend directory
Set-Location -Path "$RootDir\backend"

# Set environment variables for Flask
$env:FLASK_APP = "app.py"
$env:FLASK_ENV = "development"

Write-Host "🔧 Checking database..." -ForegroundColor Yellow

# Check if instance directory exists, if not create it
if (!(Test-Path -Path "instance")) {
    New-Item -ItemType Directory -Name "instance" | Out-Null
}

# Check if database exists, if not initialize it
if (!(Test-Path -Path "instance/database.sqlite")) {
    Write-Host "💾 Initializing database..." -ForegroundColor Yellow
    python init_db.py
}

Write-Host "🚀 Starting Flask backend on http://localhost:5000..." -ForegroundColor Cyan
Write-Host "Press CTRL+C to stop the server" -ForegroundColor Gray

python -m flask run --port 5000 --host 127.0.0.1