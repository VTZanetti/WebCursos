@echo off
TITLE WebCurso Backend - SQLite

echo ====================================================
echo  INICIANDO SERVIDOR BACKEND - SQLite Database
echo ====================================================
echo.

cd /d "%~dp0"

echo Verificando ambiente...
python --version
echo.

echo Verificando banco de dados...
if not exist "instance\database.sqlite" (
    echo Inicializando banco de dados SQLite...
    python init_db.py
)

echo.
echo Iniciando servidor...
set DATABASE_TYPE=sqlite
python app.py

echo.
echo ====================================================
echo  Servidor finalizado
echo ====================================================
PAUSE