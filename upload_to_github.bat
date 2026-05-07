@echo off
echo ========================================
echo Claude Chat - GitHub Upload Helper
echo ========================================
echo.
echo Git repository is ready!
echo.
echo Next steps:
echo.
echo 1. Create GitHub repository:
echo    - Go to: https://github.com/new
echo    - Repository name: claude-chat
echo    - Make it Public
echo    - DO NOT initialize with README
echo    - Click "Create repository"
echo.
echo 2. Copy the commands GitHub shows you under:
echo    "...or push an existing repository from the command line"
echo.
echo 3. Run those commands in this directory:
echo    cd C:\scripts\WebControl
echo.
echo Example commands (replace YOUR_USERNAME):
echo    git remote add origin https://github.com/YOUR_USERNAME/claude-chat.git
echo    git branch -M main
echo    git push -u origin main
echo.
echo 4. After pushing to GitHub:
echo    - Go to: https://dashboard.render.com
echo    - Click "New +" -^> "Web Service"
echo    - Connect your GitHub repository
echo    - Select "claude-chat"
echo    - Choose "Free" plan
echo    - Click "Create Web Service"
echo.
echo 5. Wait 3-5 minutes for deployment
echo.
echo 6. Your app will be available at:
echo    https://claude-chat-xxxx.onrender.com
echo.
echo ========================================
echo.
pause
