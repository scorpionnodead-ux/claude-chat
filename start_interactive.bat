@echo off
echo ========================================
echo   Claude Code Web Interface v2
echo   Interactive Two-Way Communication
echo ========================================
echo.

REM Останавливаем старые процессы
taskkill /F /IM python.exe /FI "WINDOWTITLE eq Claude*" 2>nul
taskkill /F /IM ngrok.exe 2>nul
timeout /t 2 /nobreak >nul

REM Запускаем новый сервер
echo [1/2] Starting unified server v2...
start "Claude Server v2" python unified_server_v2.py
timeout /t 3 /nobreak >nul

REM Запускаем ngrok
echo [2/2] Starting ngrok tunnel...
start "Claude Ngrok" ngrok http 8080 --log=stdout
timeout /t 5 /nobreak >nul

echo.
echo ========================================
echo   Services Started!
echo ========================================
echo.
echo Available interfaces:
echo   Live View:        http://localhost:8080/live
echo   Interactive Chat: http://localhost:8080/chat
echo.
echo Getting public URL...
timeout /t 3 /nobreak >nul

curl -s http://localhost:4040/api/tunnels 2>nul | findstr "public_url" | findstr "https"

echo.
echo ========================================
echo.
echo To send messages from web to this CLI:
echo 1. Open /chat in browser
echo 2. Type your message
echo 3. It will appear here automatically
echo.
echo Press any key to stop all services...
pause >nul

taskkill /F /IM python.exe /FI "WINDOWTITLE eq Claude*"
taskkill /F /IM ngrok.exe
echo.
echo All services stopped.
pause
