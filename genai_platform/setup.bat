@echo off
REM GenAI Platform - Quick Setup Script for Windows
REM This script installs dependencies and initializes the platform

echo ============================================================
echo GenAI Platform - Quick Setup
echo ============================================================
echo.

echo Step 1: Installing Python dependencies...
echo This may take a few minutes...
echo.

python -m pip install -r requirements.txt

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo ERROR: Failed to install dependencies
    echo Please check your Python installation and internet connection
    pause
    exit /b 1
)

echo.
echo Step 2: Running platform initialization...
echo.

python scripts\initialize.py

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo WARNING: Initialization encountered issues
    echo The platform may still work, but some features might be limited
)

echo.
echo ============================================================
echo Setup Complete!
echo ============================================================
echo.
echo Next steps:
echo 1. Edit .env file with your API keys (optional)
echo 2. Launch the platform: python gui\main_window.py
echo 3. Login with username: admin, password: Admin@123
echo.
echo For local models, install Ollama: https://ollama.ai
echo.

pause
