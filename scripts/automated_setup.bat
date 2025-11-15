@echo off
REM OpthalmoAI Automated Setup and Health Check Script for Windows
REM This script automatically sets up the project and fixes common issues

echo ========================================
echo OpthalmoAI Automated Setup Script
echo ========================================
echo.

REM Check if we're in the right directory
if not exist "package.json" (
    echo ERROR: Please run this script from the OpthalmoAI root directory
    pause
    exit /b 1
)

REM Check if Node.js is installed
echo Checking Node.js installation...
node --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Node.js is not installed or not in PATH
    echo Please install Node.js from https://nodejs.org/
    pause
    exit /b 1
) else (
    echo ✅ Node.js is installed
)

REM Check if Python is installed
echo Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python from https://python.org/
    pause
    exit /b 1
) else (
    echo ✅ Python is installed
)

REM Install root dependencies
echo.
echo Installing root project dependencies...
npm install
if errorlevel 1 (
    echo ERROR: Failed to install root dependencies
    pause
    exit /b 1
) else (
    echo ✅ Root dependencies installed successfully
)

REM Install frontend dependencies
echo.
echo Installing frontend dependencies...
cd frontend
npm install
if errorlevel 1 (
    echo ERROR: Failed to install frontend dependencies
    cd ..
    pause
    exit /b 1
) else (
    echo ✅ Frontend dependencies installed successfully
)

REM Build frontend
echo.
echo Building frontend for production...
npm run build
if errorlevel 1 (
    echo WARNING: Frontend build failed, but continuing...
) else (
    echo ✅ Frontend built successfully
)

cd ..

REM Set up backend virtual environment
echo.
echo Setting up backend Python environment...
cd backend

REM Create virtual environment if it doesn't exist
if not exist "venv" (
    echo Creating Python virtual environment...
    python -m venv venv
    if errorlevel 1 (
        echo ERROR: Failed to create virtual environment
        cd ..
        pause
        exit /b 1
    ) else (
        echo ✅ Virtual environment created
    )
)

REM Activate virtual environment and install dependencies
echo Installing backend dependencies...
call venv\Scripts\activate
pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: Failed to install backend dependencies
    cd ..
    pause
    exit /b 1
) else (
    echo ✅ Backend dependencies installed successfully
)

deactivate
cd ..

REM Copy environment files
echo.
echo Setting up environment files...

if not exist "backend\.env" (
    if exist "backend\.env.example" (
        copy "backend\.env.example" "backend\.env" >nul
        echo ✅ Created backend/.env from example
    ) else (
        echo WARNING: No backend/.env.example found
    )
) else (
    echo ✅ Backend/.env already exists
)

REM Run health check
echo.
echo Running project health check...
python scripts/health_check.py
if errorlevel 1 (
    echo WARNING: Health check found some issues (see above)
) else (
    echo ✅ Project health check passed!
)

REM Final summary
echo.
echo ========================================
echo Setup Complete!
echo ========================================
echo.
echo Next steps:
echo 1. Start frontend: cd frontend && npm start
echo 2. Start backend: cd backend && venv\Scripts\activate && python -m uvicorn app.main:app --reload
echo 3. Open browser: http://localhost:3000
echo.
echo For production deployment:
echo 1. Train AI model with real dataset
echo 2. Deploy backend to Google Cloud Run
echo 3. Update frontend API endpoints
echo.

REM Ask if user wants to start development servers
echo.
set /p start_dev="Start development servers now? (y/n): "
if /i "%start_dev%"=="y" (
    echo Starting development servers...
    echo.
    echo Starting backend server...
    start "OpthalmoAI Backend" cmd /k "cd backend && venv\Scripts\activate && python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000"
    
    timeout /t 3 /nobreak >nul
    
    echo Starting frontend server...
    start "OpthalmoAI Frontend" cmd /k "cd frontend && npm start"
    
    echo.
    echo ✅ Development servers starting...
    echo Frontend: http://localhost:3000
    echo Backend: http://localhost:8000
    echo API Docs: http://localhost:8000/docs
) else (
    echo.
    echo To start development servers manually:
    echo Frontend: cd frontend && npm start
    echo Backend: cd backend && venv\Scripts\activate && python -m uvicorn app.main:app --reload
)

echo.
echo Project setup complete! 🎉
pause