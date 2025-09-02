@echo off
echo ========================================
echo     WebCurso Frontend Development
echo ========================================
echo.

REM Verificar se estamos no diretório correto
if not exist "package.json" (
    echo Erro: Execute este script no diretorio frontend
    echo Exemplo: cd frontend && start_dev.bat
    pause
    exit /b 1
)

REM Verificar se Node.js está disponível
node --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Erro: Node.js nao encontrado.
    echo.
    echo Este projeto Vue.js requer Node.js para funcionar.
    echo Baixe e instale Node.js de: https://nodejs.org
    echo.
    echo Como alternativa, voce pode:
    echo 1. Instalar Node.js
    echo 2. Executar: npm install
    echo 3. Executar: npm run dev
    echo.
    pause
    exit /b 1
)

echo Verificando dependencias...
if not exist "node_modules" (
    echo Instalando dependencias...
    npm install
    if %errorlevel% neq 0 (
        echo Erro ao instalar dependencias
        pause
        exit /b 1
    )
)

echo.
echo ========================================
echo  Iniciando servidor de desenvolvimento
echo ========================================
echo  Frontend disponivel em: http://localhost:3000
echo  Backend deve estar em: http://localhost:5000
echo.
echo  IMPORTANTE: Certifique-se que o backend esta rodando!
echo  Execute no diretorio backend: python app.py
echo.
echo  Pressione Ctrl+C para parar o servidor
echo ========================================
echo.

REM Iniciar o servidor de desenvolvimento
npm run dev