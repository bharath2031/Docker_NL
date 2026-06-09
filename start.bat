@echo off
REM Startup script for AI Docker NL Dashboard (Windows)

echo ========================================
echo AI Docker NL Dashboard - Startup Script
echo ========================================
echo.

REM Check if Docker is running
docker info >nul 2>&1
if errorlevel 1 (
    echo ❌ Docker is not running. Please start Docker Desktop and try again.
    pause
    exit /b 1
)
echo ✅ Docker is running

REM Check if Ollama is running
curl -s http://localhost:11434/api/tags >nul 2>&1
if errorlevel 1 (
    echo ⚠️  Ollama is not running on localhost:11434
    echo    Please start Ollama or use Docker Compose to start all services
    set /p choice="   Continue anyway? (y/N): "
    if /i not "%choice%"=="y" exit /b 1
) else (
    echo ✅ Ollama is running
)

REM Create necessary directories
echo.
echo Creating directories...
if not exist data mkdir data
if not exist logs mkdir logs
if not exist prompts mkdir prompts

REM Check if Python dependencies are installed
python -c "import streamlit" >nul 2>&1
if errorlevel 1 (
    echo.
    echo ⚠️  Python dependencies not found
    set /p choice="   Install dependencies now? (y/N): "
    if /i "%choice%"=="y" (
        echo    Installing dependencies...
        pip install -r requirements.txt
    ) else (
        echo    Please install dependencies with: pip install -r requirements.txt
        pause
        exit /b 1
    )
) else (
    echo ✅ Python dependencies installed
)

REM Start the application
echo.
echo ========================================
echo Starting Dashboard...
echo ========================================
echo.
echo Dashboard will be available at: http://localhost:8501
echo.
echo Press Ctrl+C to stop the dashboard
echo.

streamlit run app.py
