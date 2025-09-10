# WebCurso Frontend Startup Script for PowerShell
Write-Host "🎨 Starting frontend server..." -ForegroundColor Yellow

# Get the full path of the current script directory
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RootDir = Split-Path -Parent $ScriptDir

Write-Host "Root directory: $RootDir" -ForegroundColor Yellow

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