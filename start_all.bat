@echo off
echo ========================================
echo   Claude Code Web Interface
echo ========================================
echo.
echo Starting services...
echo.

REM Останавливаем старые процессы
taskkill /F /IM python.exe /FI "WINDOWTITLE eq Claude*" 2>nul
taskkill /F /IM ngrok.exe 2>nul
timeout /t 2 /nobreak >nul

REM Запускаем Flask сервер
echo [1/2] Starting Flask server...
start "Claude Web Server" python unified_server.py
timeout /t 3 /nobreak >nul

REM Запускаем ngrok
echo [2/2] Starting ngrok tunnel...
start "Claude Ngrok" ngrok http 8080 --log=stdout

timeout /t 5 /nobreak >nul

REM Получаем URL от ngrok
echo.
echo ========================================
echo   Services Started!
echo ========================================
echo.
echo Local access:
echo   Live view:  http://localhost:8080
echo   Chat:       http://localhost:8080/chat
echo.
echo Getting public URL from ngrok...
timeout /t 3 /nobreak >nul

curl -s http://localhost:4040/api/tunnels | findstr "public_url" | findstr "https"

echo.
echo ========================================
echo Press any key to stop all services...
pause >nul

taskkill /F /IM python.exe /FI "WINDOWTITLE eq Claude*"
taskkill /F /IM ngrok.exe
echo.
echo All services stopped.
pause
