@echo off
echo 🎵 Building Band-Logo Processing Tool...

REM Build the Docker image
docker build -t band-logo-tool .

if %ERRORLEVEL% EQU 0 (
    echo ✅ Build successful! Starting container...
    
    REM Stop existing container if running
    docker stop imagescale-app >nul 2>&1
    docker rm imagescale-app >nul 2>&1
    
    REM Run the container on port 8724
    docker run -d -p 8724:8724 --name imagescale-app band-logo-tool
    
    if %ERRORLEVEL% EQU 0 (
        echo 🚀 Application is running!
        echo 📱 Access at: http://localhost:8724
        echo 🎯 For radio-endstation.de: http://radio-endstation.de:8724
        echo.
        echo 📋 Container status:
        docker ps | findstr imagescale-app
    ) else (
        echo ❌ Failed to start container
        exit /b 1
    )
) else (
    echo ❌ Build failed
    exit /b 1
)

pause
