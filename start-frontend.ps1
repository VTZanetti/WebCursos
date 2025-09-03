# WebCurso Frontend Startup Script for PowerShell
Write-Host "🎨 Starting frontend server..." -ForegroundColor Yellow
Set-Location -Path "frontend"

# Check if node_modules exists, if not install dependencies
if (!(Test-Path -Path "node_modules")) {
    Write-Host "📦 Installing frontend dependencies..." -ForegroundColor Yellow
    npm install
}

Write-Host "🚀 Starting Vue.js frontend on http://localhost:5173..." -ForegroundColor Cyan
npm run dev