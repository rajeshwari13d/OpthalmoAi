@echo off
cls
echo ========================================
echo OpthalmoAI - Development Environment
echo ========================================
echo.

echo [INFO] Starting OpthalmoAI development servers...
echo.

REM Check if we're in the right directory
if not exist "backend" (
    echo [ERROR] Please run this script from the OpthalmoAI project root directory
    echo Current directory: %CD%
    pause
    exit /b 1
)

echo [1/3] Checking prerequisites...
echo ========================================

REM Check if backend virtual environment exists
if not exist "backend\venv" (
    echo [ERROR] Backend virtual environment not found
    echo Please run: scripts\setup-project.bat
    pause
    exit /b 1
)

REM Check if frontend dependencies are installed
if not exist "frontend\node_modules" (
    echo [ERROR] Frontend dependencies not installed
    echo Please run: scripts\setup-project.bat
    pause
    exit /b 1
)

echo [OK] Prerequisites verified
echo.

echo [2/3] Starting Backend Server...
echo ========================================

echo [INFO] Activating Python virtual environment...
echo [INFO] Starting FastAPI server on http://localhost:8000...

start "OpthalmoAI Backend" cmd /c "title OpthalmoAI Backend && cd backend && call venv\Scripts\activate.bat && echo [INFO] Backend server starting... && echo [INFO] API will be available at: http://localhost:8000 && echo [INFO] Health check: http://localhost:8000/api/v1/health && echo [INFO] Interactive docs: http://localhost:8000/docs && echo. && python main.py"

REM Wait for backend to start
echo [INFO] Waiting for backend to initialize...
timeout /t 8 /nobreak >nul

echo [3/3] Starting Frontend Development Server...
echo ========================================

echo [INFO] Starting React development server on http://localhost:3000...

start "OpthalmoAI Frontend" cmd /c "title OpthalmoAI Frontend && cd frontend && echo [INFO] Frontend server starting... && echo [INFO] React app will be available at: http://localhost:3000 && echo [INFO] Hot reloading enabled for development && echo. && npm start"

REM Wait a moment for frontend to start
timeout /t 3 /nobreak >nul

echo.
echo ========================================
echo ✅ DEVELOPMENT ENVIRONMENT STARTED!
echo ========================================
echo.
echo 🌐 Application URLs:
echo   • Frontend (React):     http://localhost:3000
echo   • Backend (FastAPI):    http://localhost:8000  
echo   • API Documentation:    http://localhost:8000/docs
echo   • Health Check:         http://localhost:8000/api/v1/health
echo.
echo 🔧 Development Features:
echo   • Hot Module Reloading: Frontend auto-refreshes on code changes
echo   • API Auto-reload:      Backend restarts on Python file changes
echo   • Debug Mode:           Detailed error messages in development
echo   • CORS Enabled:         Frontend can call backend APIs
echo.
echo 📱 Testing Instructions:
echo   1. Open http://localhost:3000 in your browser
echo   2. Try the image upload functionality
echo   3. Test the analysis workflow (demo mode)
echo   4. Check mobile responsiveness
echo   5. Verify all navigation links work
echo.
echo 🏥 Demo Mode Features:
echo   • Simulated AI analysis results
echo   • Realistic confidence scores
echo   • Medical recommendations
echo   • Professional report generation
echo   • All UI/UX workflows functional
echo.
echo 🛑 To Stop Development Servers:
echo   • Close the terminal windows, or
echo   • Press Ctrl+C in each terminal, or
echo   • Run: taskkill /f /im python.exe /im node.exe
echo.
echo 📋 Next Steps for Production:
echo   1. Train real AI model for diabetic retinopathy
echo   2. Deploy backend with: scripts\deploy-backend.bat
echo   3. Update API URLs in frontend production config
echo   4. Deploy frontend with: firebase deploy --only hosting
echo.

REM Check if servers started successfully
timeout /t 5 /nobreak >nul

echo [INFO] Checking server status...
powershell -Command "try { $response = Invoke-RestMethod -Uri 'http://localhost:8000/api/v1/health' -TimeoutSec 5; Write-Host '[✅] Backend server is responding'; Write-Host '    Status:' $response.status } catch { Write-Host '[⚠️] Backend server may still be starting...' }"

echo.
echo 🎯 Happy Coding! Both servers are now running in separate windows.
echo.
pause