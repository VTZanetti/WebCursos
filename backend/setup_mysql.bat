@echo off
TITLE WebCurso - MySQL Setup

echo ====================================================
echo  CONFIGURACAO MYSQL PARA WEBCURSO
echo ====================================================
echo.

cd /d "%~dp0"

echo Instalando dependencias MySQL...
echo.

pip install mysql-connector-python==8.2.0
pip install pymysql==1.1.0

echo.
echo ====================================================
echo Dependencias MySQL instaladas!
echo.
echo Para configurar o banco de dados:
echo 1. Certifique-se que MySQL esta rodando
echo 2. Execute: python init_mysql_db.py
echo.
echo Configuracao para Navicat:
echo   Host: localhost
echo   Port: 3306
echo   Username: root
echo   Password: (deixe em branco)
echo   Database: webcurso
echo ====================================================

PAUSE