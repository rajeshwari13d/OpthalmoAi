@echo off
cls
echo ========================================
echo OpthalmoAI - Project Status Checker
echo ========================================
echo.

set "PROJECT_ROOT=%~dp0.."
cd /d "%PROJECT_ROOT%"

echo [INFO] Checking OpthalmoAI project status...
echo Project Directory: %CD%
echo.

echo [1/7] System Requirements
echo ========================================

REM Check Node.js
where node >nul 2>&1
if %errorlevel% neq 0 (
    echo [❌] Node.js - NOT INSTALLED
    set "MISSING_DEPS=1"
) else (
    for /f "tokens=*" %%i in ('node --version') do echo [✅] Node.js %%i
)

REM Check Python
where python >nul 2>&1
if %errorlevel% neq 0 (
    echo [❌] Python - NOT INSTALLED
    set "MISSING_DEPS=1"
) else (
    for /f "tokens=*" %%i in ('python --version') do echo [✅] Python %%i
)

REM Check Docker
where docker >nul 2>&1
if %errorlevel% neq 0 (
    echo [⚠️] Docker - NOT INSTALLED (optional for deployment)
) else (
    echo [✅] Docker - Available for containerization
)

REM Check Firebase CLI
where firebase >nul 2>&1
if %errorlevel% neq 0 (
    echo [⚠️] Firebase CLI - NOT INSTALLED (needed for frontend deployment)
) else (
    echo [✅] Firebase CLI - Ready for deployment
)

echo.
echo [2/7] Backend Status
echo ========================================

cd backend

REM Check virtual environment
if exist "venv" (
    echo [✅] Python virtual environment exists
) else (
    echo [❌] Python virtual environment missing
    echo       Run: python -m venv venv
)

REM Check .env file
if exist ".env" (
    echo [✅] Backend .env configuration exists
) else (
    echo [❌] Backend .env file missing
    echo       Run: copy .env.example .env
)

REM Check if dependencies are installed
if exist "venv\Lib\site-packages\fastapi" (
    echo [✅] Backend dependencies installed
) else (
    echo [❌] Backend dependencies missing
    echo       Run: pip install -r requirements.txt
)

REM Check for model file
if exist "app\models\diabetic_retinopathy_model.pth" (
    echo [✅] AI Model file found
) else (
    echo [⚠️] AI Model file missing (using demo mode)
    echo       Train and place model at: app\models\diabetic_retinopathy_model.pth
)

echo.
echo [3/7] Frontend Status  
echo ========================================

cd ..\frontend

REM Check node_modules
if exist "node_modules" (
    echo [✅] Frontend dependencies installed
) else (
    echo [❌] Frontend dependencies missing
    echo       Run: npm install
)

REM Check build directory
if exist "build" (
    echo [✅] Production build exists
) else (
    echo [⚠️] Production build missing
    echo       Run: npm run build
)

REM Check environment files
if exist ".env.development" (
    echo [✅] Development environment configured
) else (
    echo [❌] Development environment missing
)

if exist ".env.production" (
    echo [✅] Production environment configured
) else (
    echo [❌] Production environment missing
)

echo.
echo [4/7] Configuration Status
echo ========================================

REM Check Firebase config
if exist "firebase.json" (
    echo [✅] Firebase hosting configuration
) else (
    echo [❌] Firebase configuration missing
)

REM Check Docker configs
cd ..
if exist "docker-compose.yml" (
    echo [✅] Docker Compose configuration
) else (
    echo [❌] Docker Compose configuration missing
)

if exist "backend\Dockerfile" (
    echo [✅] Backend Dockerfile
) else (
    echo [❌] Backend Dockerfile missing
)

echo.
echo [5/7] Deployment Scripts
echo ========================================

if exist "scripts\setup-project.bat" (
    echo [✅] Project setup script
) else (
    echo [❌] Setup script missing
)

if exist "scripts\deploy-backend.bat" (
    echo [✅] Backend deployment script
) else (
    echo [❌] Backend deployment script missing
)

if exist "scripts\test-api.bat" (
    echo [✅] API testing script
) else (
    echo [❌] API testing script missing
)

echo.
echo [6/7] Development Tools
echo ========================================

if exist "start-dev.bat" (
    echo [✅] Development startup script
) else (
    echo [⚠️] Development startup script missing
)

REM Check if processes are running
tasklist /fi "imagename eq python.exe" 2>nul | find /i "python.exe" >nul
if %errorlevel% equ 0 (
    echo [✅] Backend server appears to be running
) else (
    echo [⚠️] Backend server not running
)

tasklist /fi "imagename eq node.exe" 2>nul | find /i "node.exe" >nul
if %errorlevel% equ 0 (
    echo [✅] Frontend development server may be running
) else (
    echo [⚠️] Frontend development server not running
)

echo.
echo [7/7] Code Quality & Documentation
echo ========================================

if exist "README.md" (
    echo [✅] Project README
) else (
    echo [❌] README documentation missing
)

if exist "PENDING_COMPLETION_STATUS.md" (
    echo [✅] Project completion status documented
) else (
    echo [❌] Completion status documentation missing
)

REM Check for key frontend components
if exist "frontend\src\components\ImageUpload.tsx" (
    echo [✅] Core frontend components present
) else (
    echo [❌] Frontend components missing
)

REM Check for backend API endpoints
if exist "backend\app\api\endpoints\analysis.py" (
    echo [✅] Backend API endpoints implemented
) else (
    echo [❌] Backend API missing
)

echo.
echo ========================================
echo 📊 PROJECT STATUS SUMMARY
echo ========================================
echo.

REM Calculate completion percentage
set "TOTAL_CHECKS=20"
set "COMPLETED=0"

REM Count completed items (simplified)
if exist "backend\venv" set /a COMPLETED+=1
if exist "backend\.env" set /a COMPLETED+=1
if exist "frontend\node_modules" set /a COMPLETED+=1
if exist "frontend\build" set /a COMPLETED+=1
if exist "firebase.json" set /a COMPLETED+=1
if exist "docker-compose.yml" set /a COMPLETED+=1
if exist "backend\Dockerfile" set /a COMPLETED+=1
if exist "scripts\setup-project.bat" set /a COMPLETED+=1
if exist "scripts\deploy-backend.bat" set /a COMPLETED+=1
if exist "README.md" set /a COMPLETED+=1
if exist "frontend\src\components\ImageUpload.tsx" set /a COMPLETED+=1
if exist "backend\app\api\endpoints\analysis.py" set /a COMPLETED+=1

set /a PERCENTAGE=COMPLETED*100/12

echo 🎯 Completion Status: %COMPLETED%/12 major components (%PERCENTAGE%%%)
echo.

if %PERCENTAGE% gtr 90 (
    echo ✅ PROJECT STATUS: EXCELLENT - Ready for deployment
    echo.
    echo 🚀 Ready For:
    echo   • Local development and testing
    echo   • Production deployment to cloud platforms
    echo   • Healthcare professional demonstrations
    echo   • Real AI model integration
) else if %PERCENTAGE% gtr 70 (
    echo ⚠️ PROJECT STATUS: GOOD - Minor items need attention
    echo.
    echo 🔧 Quick Fixes Needed:
    echo   • Run setup-project.bat to auto-fix most issues
    echo   • Install missing dependencies
    echo   • Create missing configuration files
) else (
    echo ❌ PROJECT STATUS: NEEDS SETUP
    echo.
    echo 🛠️ Action Required:
    echo   • Run scripts\setup-project.bat for automated setup
    echo   • Install required system dependencies
    echo   • Complete project configuration
)

echo.
echo 📋 Next Steps:
echo.
echo For Development:
echo   1. Run: scripts\setup-project.bat (if not done)
echo   2. Run: start-dev.bat (starts both servers)
echo   3. Open: http://localhost:3000
echo.
echo For Production:
echo   1. Backend: scripts\deploy-backend.bat
echo   2. Frontend: firebase deploy --only hosting
echo   3. Update API URLs in production config
echo.
echo 🔍 Detailed Analysis:
echo   • Check PENDING_COMPLETION_STATUS.md for full project roadmap
echo   • Run scripts\test-api.bat to validate backend functionality
echo   • See individual component README files for specific guidance
echo.
pause