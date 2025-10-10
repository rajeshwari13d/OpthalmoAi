@echo off
REM OpthalmoAI Frontend Firebase Deployment Script (Windows)
REM Healthcare-compliant deployment with security validation

setlocal enabledelayedexpansion

echo 🏥 OpthalmoAI Frontend Deployment to Firebase Hosting
echo ====================================================

REM Configuration variables (replace with actual values)
set PROJECT_ID=OPTHALMOAI_PROJECT_ID
set SITE_ID=OPTHALMOAI_SITE_ID
set FRONTEND_DIR=frontend

REM Check prerequisites
echo [INFO] Checking prerequisites...

REM Check Node.js
node --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Node.js is not installed. Please install Node.js 18+
    exit /b 1
)

REM Check npm
npm --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] npm is not installed
    exit /b 1
)

REM Check Firebase CLI
firebase --version >nul 2>&1
if errorlevel 1 (
    echo [WARNING] Firebase CLI not found. Installing...
    npm install -g firebase-tools
)

echo [SUCCESS] Prerequisites check completed

REM Validate configuration
echo [INFO] Validating configuration...

if not exist "%FRONTEND_DIR%" (
    echo [ERROR] Frontend directory not found: %FRONTEND_DIR%
    exit /b 1
)

if not exist "%FRONTEND_DIR%\package.json" (
    echo [ERROR] package.json not found in %FRONTEND_DIR%
    exit /b 1
)

if not exist "%FRONTEND_DIR%\firebase.json" (
    echo [ERROR] firebase.json not found in %FRONTEND_DIR%
    exit /b 1
)

echo [SUCCESS] Configuration validation completed

REM Build frontend
echo [INFO] Building OpthalmoAI frontend...

cd "%FRONTEND_DIR%"

REM Install dependencies
echo [INFO] Installing dependencies...
call npm ci
if errorlevel 1 (
    echo [ERROR] Failed to install dependencies
    exit /b 1
)

REM Build production version
echo [INFO] Building production version...
call npm run build
if errorlevel 1 (
    echo [ERROR] Build failed
    exit /b 1
)

if not exist "build" (
    echo [ERROR] Build directory not created
    exit /b 1
)

echo [SUCCESS] Frontend built successfully

REM Deploy to Firebase
echo [INFO] Deploying to Firebase Hosting...

REM Check Firebase authentication
firebase projects:list >nul 2>&1
if errorlevel 1 (
    echo [WARNING] Not authenticated with Firebase. Please run: firebase login
    exit /b 1
)

REM Deploy hosting
echo [INFO] Deploying to Firebase Hosting...
call firebase deploy --only hosting --project %PROJECT_ID%
if errorlevel 1 (
    echo [ERROR] Deployment failed
    exit /b 1
)

echo [SUCCESS] Deployment completed successfully!
echo [SUCCESS] OpthalmoAI is now live at: https://%SITE_ID%.web.app

cd ..

echo.
echo 🏥 OpthalmoAI Frontend Deployment Complete!
echo.
echo Healthcare Platform URL: https://%SITE_ID%.web.app
echo Firebase Console: https://console.firebase.google.com/project/%PROJECT_ID%
echo.
echo Next Steps:
echo   1. Test medical image upload functionality
echo   2. Verify API connectivity to Cloud Run backend
echo   3. Validate healthcare compliance features
echo   4. Monitor application performance
echo.
echo Remember: This platform requires medical professional supervision for clinical use

pause