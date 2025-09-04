# WebCurso Frontend Cleanup Script
Write-Host "🧹 Cleaning WebCurso Frontend..." -ForegroundColor Green
Write-Host "==================================================" -ForegroundColor Green

# Get the full path of the current script directory
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RootDir = Split-Path -Parent $ScriptDir
$FrontendDir = "$RootDir\frontend"

Write-Host "Root directory: $RootDir" -ForegroundColor Yellow
Write-Host "Frontend directory: $FrontendDir" -ForegroundColor Yellow

# Change to frontend directory
Set-Location -Path $FrontendDir

# Stop any running processes that might be using node_modules
Write-Host "🛑 Stopping any processes using frontend files..." -ForegroundColor Yellow
try {
    # This is just informational, we can't easily stop processes on Windows
    Get-Process | Where-Object { $_.Path -like "$FrontendDir*" } | Format-Table Name, Id, Path
} catch {
    Write-Host "ℹ️  Could not check for running processes (this is normal)" -ForegroundColor Gray
}

# Remove node_modules with force
Write-Host "🗑️  Removing node_modules directory..." -ForegroundColor Yellow
if (Test-Path -Path "node_modules") {
    try {
        # Try normal removal first
        Remove-Item -Path "node_modules" -Recurse -Force
        Write-Host "✅ node_modules removed successfully" -ForegroundColor Green
    } catch {
        Write-Host "⚠️  Failed to remove node_modules with PowerShell" -ForegroundColor Yellow
        Write-Host "🔧 Trying alternative method..." -ForegroundColor Yellow
        
        # Try using cmd to remove
        try {
            cmd /c "rmdir /s /q node_modules"
            Write-Host "✅ node_modules removed successfully with cmd" -ForegroundColor Green
        } catch {
            Write-Host "❌ Failed to remove node_modules. Please close any applications using these files and try again." -ForegroundColor Red
            Write-Host "💡 You can also manually delete the node_modules folder in explorer" -ForegroundColor Gray
            exit 1
        }
    }
} else {
    Write-Host "✅ node_modules directory not found" -ForegroundColor Green
}

# Clear npm cache
Write-Host "🧹 Clearing npm cache..." -ForegroundColor Yellow
try {
    npm cache clean --force
    Write-Host "✅ npm cache cleared" -ForegroundColor Green
} catch {
    Write-Host "⚠️  Failed to clear npm cache (this is usually not critical)" -ForegroundColor Yellow
}

# Remove package-lock.json
Write-Host "🗑️  Removing package-lock.json..." -ForegroundColor Yellow
if (Test-Path -Path "package-lock.json") {
    try {
        Remove-Item -Path "package-lock.json" -Force
        Write-Host "✅ package-lock.json removed" -ForegroundColor Green
    } catch {
        Write-Host "⚠️  Failed to remove package-lock.json" -ForegroundColor Yellow
    }
} else {
    Write-Host "✅ package-lock.json not found" -ForegroundColor Green
}

Write-Host "✨ Frontend cleanup completed!" -ForegroundColor Green
Write-Host "💡 You can now run the application normally" -ForegroundColor Gray