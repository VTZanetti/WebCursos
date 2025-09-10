@echo off
echo 🧹 Cleaning WebCurso Frontend...
echo ==================================================

REM Calculate the root directory
set "ROOT_DIR=%~dp0.."

echo Root directory: %ROOT_DIR%
echo Frontend directory: %ROOT_DIR%\frontend

REM Change to frontend directory
cd /d "%ROOT_DIR%\frontend"

REM Stop any running processes that might be using node_modules
echo 🛑 Stopping any processes using frontend files...
echo (Note: On Windows, you'll need to manually close any applications using these files)

REM Remove node_modules with force
echo 🗑️  Removing node_modules directory...
if exist "node_modules" (
    echo Removing node_modules...
    rmdir /s /q node_modules
    if errorlevel 1 (
        echo ⚠️  Failed to remove node_modules
        echo 💡 Try closing any applications using these files and run this script again
        echo 💡 Or manually delete the node_modules folder in Explorer
        pause
        exit /b 1
    ) else (
        echo ✅ node_modules removed successfully
    )
) else (
    echo ✅ node_modules directory not found
)

REM Clear npm cache
echo 🧹 Clearing npm cache...
npm cache clean --force
if errorlevel 1 (
    echo ⚠️  Failed to clear npm cache (this is usually not critical)
) else (
    echo ✅ npm cache cleared
)

REM Remove package-lock.json
echo 🗑️  Removing package-lock.json...
if exist "package-lock.json" (
    del /f "package-lock.json"
    if errorlevel 1 (
        echo ⚠️  Failed to remove package-lock.json
    ) else (
        echo ✅ package-lock.json removed
    )
) else (
    echo ✅ package-lock.json not found
)

echo ✨ Frontend cleanup completed!
echo 💡 You can now run the application normally
pause