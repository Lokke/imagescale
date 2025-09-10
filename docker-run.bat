@echo off
echo 🎵 Starting Band-Logo Processing Tool deployment...

REM Update from Git repository
echo 📥 Updating from Git repository...
git fetch origin
git reset --hard origin/main

if %ERRORLEVEL% EQU 0 (
    echo ✅ Git update successful!
    echo 🔧 Git update completed...
) else (
    echo ⚠️  Git update failed, continuing with current version...
)

echo 🔨 Building Band-Logo Processing Tool...

REM Build the Docker image with no cache to ensure latest changes
docker build --no-cache -t band-logo-tool .

if %ERRORLEVEL% EQU 0 (
    echo ✅ Build successful! Starting container...
    
    REM Stop existing container if running
    echo 🛑 Stopping existing container...
    docker stop imagescale-app >nul 2>&1
    docker rm imagescale-app >nul 2>&1
    
    REM Run the container on port 8724
    echo 🚀 Starting new container...
    docker run -d -p 8724:8724 --name imagescale-app band-logo-tool
    
    if %ERRORLEVEL% EQU 0 (
        echo.
        echo 🎉 SUCCESS! Application is running!
        echo 📱 Local access: http://localhost:8724
        echo � Server access: http://radio-endstation.de:8724
        echo.
        echo 📋 Container status:
        docker ps | findstr imagescale-app
        echo.
        echo 📝 To check logs: docker logs imagescale-app
        echo 🛑 To stop: docker stop imagescale-app
    ) else (
        echo ❌ Failed to start container
        exit /b 1
    )
) else (
    echo ❌ Build failed
    exit /b 1
)

pause
