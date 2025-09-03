@echo off
TITLE Servidor de Desenvolvimento Vue.js - WebCurso

echo ====================================================
echo  INICIANDO SERVIDOR DE DESENVOLVIMENTO VUE.JS
echo ====================================================
echo.

REM Navega para o diretorio onde o script esta localizado
cd /d "%~dp0"
echo Diretorio atual: %CD%
echo.

REM Verifica se o Node.js esta instalado
echo Verificando instalacao do Node.js...
node --version >nul 2>&1
if errorlevel 1 (
    echo ERRO: Node.js nao encontrado no sistema.
    echo Por favor, instale o Node.js antes de continuar.
    echo Download: https://nodejs.org
    echo.
    goto :fim
)

REM Verifica npm usando cmd para evitar problemas de ExecutionPolicy
cmd /c "npm --version" >nul 2>&1
if errorlevel 1 (
    echo ERRO: npm nao encontrado no sistema.
    echo Por favor, reinstale o Node.js com npm incluido.
    echo.
    goto :fim
)

echo Node.js encontrado: 
node --version
echo npm encontrado: 
cmd /c "npm --version"
echo.

REM Verifica se existe package.json
if not exist "package.json" (
    echo ERRO: Arquivo package.json nao encontrado neste diretorio.
    echo Certifique-se de que voce esta no diretorio correto do projeto Vue.js.
    echo Diretorio atual: %CD%
    echo.
    goto :fim
)

echo package.json encontrado.
echo.

REM Verifica se a pasta node_modules existe
if not exist "node_modules" (
    echo A pasta node_modules nao foi encontrada.
    echo Executando 'npm install'. Por favor, aguarde...
    echo.
    cmd /c "npm install"
    if errorlevel 1 (
        echo.
        echo ERRO: Falha ao executar 'npm install'.
        echo Verifique sua conexao com a internet e tente novamente.
        echo Ou tente executar manualmente: npm install
        echo.
        goto :fim
    )
    echo.
    echo Dependencias instaladas com sucesso!
    echo.
) else (
    echo Pasta node_modules encontrada.
    echo.
)

REM Verifica se o script 'dev' existe no package.json
findstr /C:"dev" package.json >nul
if errorlevel 1 (
    echo ERRO: Script 'dev' nao encontrado no package.json.
    echo Verifique se o arquivo package.json contem a entrada 'dev' na secao scripts.
    echo.
    goto :fim
)

echo Script 'dev' encontrado no package.json.
echo.
echo Iniciando o servidor de desenvolvimento...
echo Para parar o servidor, pressione Ctrl+C
echo.
echo ====================================================
echo  Frontend sera disponibilizado em: http://localhost:5173
echo  Backend deve estar em: http://localhost:5000
echo.
echo  IMPORTANTE: Certifique-se que o backend esta rodando!
echo  Execute no diretorio backend: python app.py
echo ====================================================
echo.
echo NOTA: Se o comando falhar devido a restricoes do PowerShell,
echo execute este comando diretamente no prompt de comando (cmd):
echo cmd /c "npm run dev"
echo.

REM Executa o comando de desenvolvimento usando cmd para evitar problemas de ExecutionPolicy
cmd /c "npm run dev"

REM Se chegou aqui, o npm run dev terminou
echo.
echo O servidor foi encerrado.

:fim
echo.
echo ====================================================
echo Pressione qualquer tecla para fechar esta janela.
PAUSE