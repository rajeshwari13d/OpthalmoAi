# PowerShell Script to Auto-Download and Install Node.js for OpthalmoAI
# This script will automatically download and install Node.js LTS version

Write-Host "🚀 OpthalmoAI - Automated Node.js Installation Script" -ForegroundColor Green
Write-Host "=================================================" -ForegroundColor Green

# Check if running as Administrator
$isAdmin = ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)

if (-not $isAdmin) {
    Write-Host "⚠️  This script should be run as Administrator for best results" -ForegroundColor Yellow
    Write-Host "   Right-click PowerShell and select 'Run as Administrator'" -ForegroundColor Yellow
    Write-Host ""
}

# Function to check if Node.js is already installed
function Test-NodeInstallation {
    try {
        $nodeVersion = node --version 2>$null
        if ($nodeVersion) {
            Write-Host "✅ Node.js is already installed: $nodeVersion" -ForegroundColor Green
            return $true
        }
    }
    catch {
        return $false
    }
    return $false
}

# Check current installation
if (Test-NodeInstallation) {
    Write-Host "✅ Node.js is already installed and ready for OpthalmoAI development!" -ForegroundColor Green
    Write-Host ""
    Write-Host "🎯 Next steps for OpthalmoAI:" -ForegroundColor Cyan
    Write-Host "   1. cd D:\OpthalmoAi\frontend" -ForegroundColor White
    Write-Host "   2. npm install" -ForegroundColor White
    Write-Host "   3. npm start" -ForegroundColor White
    Write-Host ""
    exit 0
}

Write-Host "📥 Starting Node.js installation for OpthalmoAI healthcare platform..." -ForegroundColor Cyan
Write-Host ""

# Method 1: Try Windows Package Manager (winget)
Write-Host "🔄 Attempting installation via Windows Package Manager..." -ForegroundColor Yellow

try {
    # Check if winget is available
    $wingetVersion = winget --version 2>$null
    if ($wingetVersion) {
        Write-Host "   Found winget version: $wingetVersion" -ForegroundColor Gray
        
        # Install Node.js via winget
        Write-Host "   Installing Node.js LTS via winget..." -ForegroundColor Gray
        $wingetResult = winget install OpenJS.NodeJS --silent --accept-package-agreements --accept-source-agreements 2>$null
        
        # Wait for installation
        Start-Sleep -Seconds 10
        
        # Refresh environment variables
        $env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")
        
        if (Test-NodeInstallation) {
            Write-Host "✅ Node.js successfully installed via winget!" -ForegroundColor Green
            Write-Host ""
            Write-Host "🎉 Ready for OpthalmoAI development!" -ForegroundColor Green
            exit 0
        }
    }
}
catch {
    Write-Host "   winget installation failed, trying alternative method..." -ForegroundColor Yellow
}

# Method 2: Direct Download and Install
Write-Host "🔄 Downloading Node.js LTS directly from nodejs.org..." -ForegroundColor Yellow

try {
    # Create temp directory
    $tempDir = "$env:TEMP\nodejs_install"
    New-Item -ItemType Directory -Force -Path $tempDir | Out-Null
    
    # Download Node.js LTS installer
    $nodeUrl = "https://nodejs.org/dist/v20.17.0/node-v20.17.0-x64.msi"
    $installerPath = "$tempDir\nodejs_installer.msi"
    
    Write-Host "   Downloading from: $nodeUrl" -ForegroundColor Gray
    Write-Host "   Please wait... (this may take a few minutes)" -ForegroundColor Gray
    
    # Download with progress
    $webClient = New-Object System.Net.WebClient
    $webClient.DownloadFile($nodeUrl, $installerPath)
    
    Write-Host "✅ Download completed!" -ForegroundColor Green
    
    # Install Node.js silently
    Write-Host "🔧 Installing Node.js (silent installation)..." -ForegroundColor Yellow
    $installProcess = Start-Process -FilePath "msiexec.exe" -ArgumentList "/i `"$installerPath`" /quiet /norestart" -Wait -PassThru
    
    if ($installProcess.ExitCode -eq 0) {
        Write-Host "✅ Node.js installation completed!" -ForegroundColor Green
        
        # Refresh environment variables
        $env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")
        
        # Clean up temp files
        Remove-Item -Recurse -Force $tempDir -ErrorAction SilentlyContinue
        
        Write-Host ""
        Write-Host "🔄 Verifying installation..." -ForegroundColor Yellow
        Start-Sleep -Seconds 5
        
        if (Test-NodeInstallation) {
            Write-Host "✅ Node.js successfully installed and verified!" -ForegroundColor Green
        } else {
            Write-Host "⚠️  Installation completed but verification failed." -ForegroundColor Yellow
            Write-Host "   Please restart PowerShell and try: node --version" -ForegroundColor Yellow
        }
    } else {
        Write-Host "❌ Installation failed with exit code: $($installProcess.ExitCode)" -ForegroundColor Red
    }
}
catch {
    Write-Host "❌ Direct download failed: $($_.Exception.Message)" -ForegroundColor Red
    Write-Host ""
    Write-Host "🔧 Manual Installation Instructions:" -ForegroundColor Yellow
    Write-Host "   1. Visit: https://nodejs.org/" -ForegroundColor White
    Write-Host "   2. Download LTS version (Recommended)" -ForegroundColor White
    Write-Host "   3. Run the installer with default settings" -ForegroundColor White
    Write-Host "   4. Restart PowerShell after installation" -ForegroundColor White
}

Write-Host ""
Write-Host "🎯 Next Steps for OpthalmoAI Development:" -ForegroundColor Cyan
Write-Host "   1. Restart PowerShell (or VS Code)" -ForegroundColor White
Write-Host "   2. cd D:\OpthalmoAi\frontend" -ForegroundColor White
Write-Host "   3. npm install" -ForegroundColor White
Write-Host "   4. npm start" -ForegroundColor White
Write-Host ""
Write-Host "🏥 Your clinical-grade AI healthcare platform will be ready!" -ForegroundColor Green
Write-Host "   Frontend: http://localhost:3000" -ForegroundColor White
Write-Host "   Backend:  http://localhost:8000" -ForegroundColor White