@echo off
TITLE WebCurso - SQLite Setup

echo ====================================================
echo  CONFIGURACAO SQLITE PARA WEBCURSO
echo ====================================================
echo.

cd /d "%~dp0"

echo Verificando SQLite...
python -c "import sqlite3; print('SQLite version:', sqlite3.sqlite_version)"
echo.

echo Criando pasta instance se necessario...
if not exist "instance" (
    mkdir instance
    echo Pasta instance criada.
) else (
    echo Pasta instance ja existe.
)

echo.
echo Inicializando banco de dados SQLite...
echo.

python init_db.py

echo.
echo ====================================================
echo Banco de dados configurado permanentemente!
echo Para iniciar o servidor:
echo   cd c:\Dev\WebCurso\backend
echo   start_server.bat
echo ====================================================

PAUSE