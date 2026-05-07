@echo off
echo ============================================================
echo Claude Live Chat - Starting Server
echo ============================================================
echo.

cd /d C:\scripts\WebControl

echo [1/2] Starting Flask server...
start /B python server.py

timeout /t 3 /nobreak >nul

echo [2/2] Starting ngrok tunnel...
start ngrok http 5000

timeout /t 5 /nobreak >nul

echo.
echo ============================================================
echo Server is running!
echo ============================================================
echo.
echo Local access:
echo   http://localhost:5000
echo.
echo Remote access:
echo   Open http://localhost:4040 to get your public URL
echo   Or check the ngrok window
echo.
echo Press any key to stop servers...
pause >nul

echo.
echo Stopping servers...
taskkill /F /IM python.exe /FI "WINDOWTITLE eq *server.py*" 2>nul
taskkill /F /IM ngrok.exe 2>nul

echo Done!
