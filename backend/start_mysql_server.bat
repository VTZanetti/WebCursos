@echo off
TITLE WebCurso Backend - MySQL

echo ====================================================
echo  INICIANDO SERVIDOR BACKEND - MySQL Database
echo ====================================================
echo.

cd /d "%~dp0"

echo Verificando ambiente...
python --version
echo.

echo Iniciando servidor...
set DATABASE_TYPE=mysql
python app.py

echo.
echo ====================================================
echo  Servidor finalizado
echo ====================================================
PAUSE