@echo off
echo ========================================
echo        WebCurso Backend Startup
echo ========================================
echo.

REM Verificar se estamos no diretório correto
if not exist "app.py" (
    echo Erro: Execute este script no diretorio backend
    echo Exemplo: cd backend && start_server.bat
    pause
    exit /b 1
)

REM Verificar se Python está disponível
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Erro: Python nao encontrado. Instale Python 3.7+ primeiro.
    pause
    exit /b 1
)

echo Verificando dependencias...
python -c "import flask, flask_cors" >nul 2>&1
if %errorlevel% neq 0 (
    echo Instalando dependencias...
    python -m pip install -r requirements.txt
    if %errorlevel% neq 0 (
        echo Erro ao instalar dependencias
        pause
        exit /b 1
    )
)

REM Verificar se o banco de dados existe
if not exist "instance\database.sqlite" (
    echo Inicializando banco de dados...
    python init_db.py
    if %errorlevel% neq 0 (
        echo Erro ao inicializar banco de dados
        pause
        exit /b 1
    )
)

echo.
echo ========================================
echo  Iniciando servidor de desenvolvimento
echo ========================================
echo  API disponivel em: http://localhost:5000
echo  Endpoints principais:
echo    GET    /api/cursos
echo    POST   /api/cursos
echo    GET    /api/health
echo.
echo  Pressione Ctrl+C para parar o servidor
echo ========================================
echo.

REM Iniciar o servidor Flask
python app.py