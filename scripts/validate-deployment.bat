@echo off
REM OpthalmoAI Deployment Validation Script (Windows)
setlocal enabledelayedexpansion

echo 🏥 OpthalmoAI Deployment Validation
echo ===================================

REM Check if Node.js is available
node --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Node.js is required to run validation
    echo Please install Node.js from https://nodejs.org/
    pause
    exit /b 1
)

REM Run the validation script
echo [INFO] Running deployment validation...
node scripts\validate-deployment.js

if errorlevel 1 (
    echo [ERROR] Validation failed
    pause
    exit /b 1
) else (
    echo [SUCCESS] Validation completed
    echo.
    echo Check validation-report.json for detailed results
    pause
)