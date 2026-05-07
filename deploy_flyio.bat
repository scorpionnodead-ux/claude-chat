@echo off
echo ========================================
echo Claude Chat - Fly.io Deployment
echo ========================================
echo.

REM Проверка установки Fly CLI
where fly >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo [!] Fly CLI not found. Installing...
    echo.
    powershell -Command "iwr https://fly.io/install.ps1 -useb | iex"
    echo.
    echo [*] Please restart this script after installation completes.
    pause
    exit /b
)

echo [*] Fly CLI found
echo.

REM Проверка авторизации
fly auth whoami >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo [!] Not logged in to Fly.io
    echo [*] Opening login page...
    fly auth login
    echo.
)

echo [*] Logged in to Fly.io
echo.

REM Переход в директорию проекта
cd /d "%~dp0"

echo [*] Current directory: %CD%
echo.

REM Проверка наличия fly.toml
if not exist "fly.toml" (
    echo [!] fly.toml not found
    echo [*] Creating new app...
    fly launch --no-deploy
    echo.
)

echo [*] Deploying to Fly.io...
echo.
fly deploy

echo.
echo ========================================
echo Deployment complete!
echo ========================================
echo.
echo Your app is available at:
fly status | findstr "Hostname"
echo.
echo Useful commands:
echo   fly open          - Open app in browser
echo   fly logs          - View logs
echo   fly status        - Check status
echo   fly deploy        - Deploy updates
echo.
pause
