# Git Setup and GitHub Deployment Guide

## 📋 Prerequisites

Before pushing to GitHub, you need to install Git and configure it.

## 🔧 Step 1: Install Git

### Option A: Download Git for Windows
1. Visit: https://git-scm.com/download/win
2. Download the latest version
3. Run the installer with default settings
4. Restart VS Code and PowerShell after installation

### Option B: Install via Package Manager (if you have Chocolatey)
```powershell
choco install git
```

### Option C: Install via Winget (Windows Package Manager)
```powershell
winget install --id Git.Git -e --source winget
```

## 🚀 Step 2: Configure Git (One-time Setup)

After installing Git, configure your identity:

```powershell
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

## 📤 Step 3: Push to GitHub

Once Git is installed, run these commands in the project directory:

```powershell
# Navigate to project root
cd "d:\OpthalmoAi"

# Initialize git repository
git init

# Add all files to staging
git add .

# Create initial commit
git commit -m "Initial commit: OpthalmoAI - AI-driven diabetic retinopathy screening platform

- Complete React frontend with TypeScript and TailwindCSS
- FastAPI backend with Python 3.13 and virtual environment
- Docker configuration for containerized deployment
- Healthcare-compliant design with medical disclaimers
- AI model infrastructure ready for diabetic retinopathy detection
- VS Code tasks and development environment configured
- Comprehensive documentation and README"

# Add remote repository
git remote add origin https://github.com/rajeshwari13d/OpthalmoAi.git

# Push to GitHub main branch
git push -u origin main
```

## 🔐 Step 4: GitHub Authentication

If this is your first time pushing to GitHub from this machine, you'll need to authenticate:

### Option A: Personal Access Token (Recommended)
1. Go to GitHub → Settings → Developer settings → Personal access tokens
2. Generate a new token with repo permissions
3. Use your GitHub username and the token as password when prompted

### Option B: GitHub CLI (Alternative)
```powershell
# Install GitHub CLI first
winget install --id GitHub.cli

# Authenticate
gh auth login
```

## 📁 Project Structure Being Pushed

```
OpthalmoAI/
├── .github/
│   └── copilot-instructions.md
├── .vscode/
│   └── tasks.json
├── backend/
│   ├── app/
│   │   ├── api/endpoints/
│   │   ├── core/
│   │   ├── models/
│   │   └── main.py
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   └── services/
│   ├── public/
│   └── package.json
├── docker-compose.yml
├── Dockerfile.backend
├── Dockerfile.frontend
├── .gitignore
└── README.md
```

## ⚡ Quick Commands (After Git Installation)

```powershell
# All-in-one script
cd "d:\OpthalmoAi"
git init
git add .
git commit -m "Initial commit: Complete OpthalmoAI platform"
git remote add origin https://github.com/rajeshwari13d/OpthalmoAi.git
git push -u origin main
```

## 🔍 Verification

After pushing, verify the upload:
1. Visit: https://github.com/rajeshwari13d/OpthalmoAi
2. Check that all files and folders are present
3. Verify README.md displays correctly

## 🚨 Important Notes

- The `.gitignore` file is already configured to exclude sensitive files
- Virtual environment files (`.venv/`) are ignored for security
- Large AI model files should be tracked with Git LFS if needed
- Patient data and uploads directories are excluded for HIPAA compliance

## 🆘 Troubleshooting

### Common Issues:
1. **"git: command not found"** → Install Git as described above
2. **Authentication failed** → Use Personal Access Token instead of password
3. **Repository already exists** → Use `git remote set-url origin <url>` to change URL
4. **Large files** → Consider Git LFS for model files

### Support Commands:
```powershell
git status          # Check repository status
git log --oneline   # View commit history
git remote -v       # Check remote repositories
```