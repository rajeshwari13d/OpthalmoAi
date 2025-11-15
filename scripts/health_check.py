#!/usr/bin/env python3
"""
OpthalmoAI - Automated Project Health Check and Setup
This script automatically checks and fixes common issues in the project.
"""

import os
import sys
import json
import subprocess
import requests
from pathlib import Path
from typing import Dict, List, Tuple

class ProjectHealthChecker:
    def __init__(self):
        self.project_root = Path(__file__).parent
        self.frontend_dir = self.project_root / "frontend"
        self.backend_dir = self.project_root / "backend"
        self.issues_found = []
        self.fixes_applied = []
        
    def log_status(self, message: str, status: str = "INFO"):
        """Log status messages with color coding"""
        colors = {
            "INFO": "\033[94m",    # Blue
            "SUCCESS": "\033[92m", # Green
            "WARNING": "\033[93m", # Yellow
            "ERROR": "\033[91m",   # Red
            "RESET": "\033[0m"     # Reset
        }
        
        print(f"{colors.get(status, '')}{status}: {message}{colors['RESET']}")
    
    def run_command(self, command: str, cwd: Path = None) -> Tuple[bool, str]:
        """Run shell command and return success status and output"""
        try:
            cwd = cwd or self.project_root
            result = subprocess.run(
                command, 
                shell=True, 
                cwd=cwd, 
                capture_output=True, 
                text=True,
                timeout=60
            )
            return result.returncode == 0, result.stdout + result.stderr
        except subprocess.TimeoutExpired:
            return False, "Command timed out"
        except Exception as e:
            return False, str(e)
    
    def check_file_exists(self, file_path: Path, description: str) -> bool:
        """Check if a file exists and log the result"""
        if file_path.exists():
            self.log_status(f"✅ {description} exists: {file_path}", "SUCCESS")
            return True
        else:
            self.log_status(f"❌ {description} missing: {file_path}", "ERROR")
            self.issues_found.append(f"Missing {description}")
            return False
    
    def check_directory_structure(self):
        """Check if all required directories exist"""
        self.log_status("Checking directory structure...", "INFO")
        
        required_dirs = [
            (self.frontend_dir, "Frontend directory"),
            (self.backend_dir, "Backend directory"),
            (self.frontend_dir / "src", "Frontend source directory"),
            (self.backend_dir / "app", "Backend app directory"),
        ]
        
        for dir_path, description in required_dirs:
            self.check_file_exists(dir_path, description)
    
    def check_package_files(self):
        """Check if package configuration files exist"""
        self.log_status("Checking package configuration files...", "INFO")
        
        required_files = [
            (self.project_root / "package.json", "Root package.json"),
            (self.frontend_dir / "package.json", "Frontend package.json"),
            (self.backend_dir / "requirements.txt", "Backend requirements.txt"),
            (self.frontend_dir / ".env.development", "Frontend dev environment"),
            (self.frontend_dir / ".env.production", "Frontend prod environment"),
            (self.backend_dir / ".env", "Backend environment file"),
        ]
        
        for file_path, description in required_files:
            self.check_file_exists(file_path, description)
    
    def check_frontend_dependencies(self):
        """Check if frontend dependencies are installed"""
        self.log_status("Checking frontend dependencies...", "INFO")
        
        node_modules = self.frontend_dir / "node_modules"
        if not node_modules.exists():
            self.log_status("❌ Frontend dependencies not installed", "ERROR")
            self.issues_found.append("Frontend dependencies missing")
            return False
        
        # Check if key dependencies exist
        key_deps = ["react", "typescript", "@types/react"]
        for dep in key_deps:
            dep_path = node_modules / dep
            if not dep_path.exists():
                self.log_status(f"❌ Key dependency missing: {dep}", "ERROR")
                self.issues_found.append(f"Missing dependency: {dep}")
                return False
        
        self.log_status("✅ Frontend dependencies installed", "SUCCESS")
        return True
    
    def check_backend_dependencies(self):
        """Check if backend dependencies can be imported"""
        self.log_status("Checking backend dependencies...", "INFO")
        
        try:
            # Change to backend directory and check imports
            original_path = sys.path.copy()
            sys.path.insert(0, str(self.backend_dir))
            
            # Try importing key backend dependencies
            import fastapi
            import uvicorn
            import pydantic
            
            self.log_status("✅ Backend dependencies available", "SUCCESS")
            return True
            
        except ImportError as e:
            self.log_status(f"❌ Backend dependency missing: {e}", "ERROR")
            self.issues_found.append(f"Backend dependency missing: {e}")
            return False
        finally:
            sys.path = original_path
    
    def check_api_endpoints(self):
        """Check if backend API endpoints are accessible"""
        self.log_status("Checking API endpoints...", "INFO")
        
        try:
            # Try to check if backend is running
            response = requests.get("http://127.0.0.1:8000/health", timeout=5)
            if response.status_code == 200:
                self.log_status("✅ Backend API is accessible", "SUCCESS")
                return True
            else:
                self.log_status(f"⚠️ Backend API returned status {response.status_code}", "WARNING")
                return False
        except requests.exceptions.ConnectionError:
            self.log_status("⚠️ Backend API not running (this is OK for setup)", "WARNING")
            return False
        except Exception as e:
            self.log_status(f"❌ Error checking API: {e}", "ERROR")
            return False
    
    def auto_fix_dependencies(self):
        """Attempt to automatically fix dependency issues"""
        self.log_status("Attempting to auto-fix dependencies...", "INFO")
        
        # Install root dependencies
        if (self.project_root / "package.json").exists():
            self.log_status("Installing root dependencies...", "INFO")
            success, output = self.run_command("npm install", self.project_root)
            if success:
                self.log_status("✅ Root dependencies installed", "SUCCESS")
                self.fixes_applied.append("Installed root dependencies")
            else:
                self.log_status(f"❌ Failed to install root dependencies: {output}", "ERROR")
        
        # Install frontend dependencies
        if not (self.frontend_dir / "node_modules").exists():
            self.log_status("Installing frontend dependencies...", "INFO")
            success, output = self.run_command("npm install", self.frontend_dir)
            if success:
                self.log_status("✅ Frontend dependencies installed", "SUCCESS")
                self.fixes_applied.append("Installed frontend dependencies")
            else:
                self.log_status(f"❌ Failed to install frontend dependencies: {output}", "ERROR")
        
        # Check Python virtual environment
        if not (self.backend_dir / "venv").exists():
            self.log_status("Creating Python virtual environment...", "INFO")
            success, output = self.run_command("python -m venv venv", self.backend_dir)
            if success:
                self.log_status("✅ Python virtual environment created", "SUCCESS")
                self.fixes_applied.append("Created Python virtual environment")
            else:
                self.log_status(f"❌ Failed to create virtual environment: {output}", "ERROR")
    
    def check_build_capability(self):
        """Check if the project can be built successfully"""
        self.log_status("Checking build capability...", "INFO")
        
        # Test frontend build
        self.log_status("Testing frontend build...", "INFO")
        success, output = self.run_command("npm run build", self.frontend_dir)
        if success:
            self.log_status("✅ Frontend builds successfully", "SUCCESS")
            return True
        else:
            self.log_status(f"❌ Frontend build failed: {output[:200]}...", "ERROR")
            self.issues_found.append("Frontend build fails")
            return False
    
    def generate_health_report(self):
        """Generate a comprehensive health report"""
        self.log_status("Generating health report...", "INFO")
        
        report = {
            "timestamp": str(subprocess.run(["date"], capture_output=True, text=True).stdout.strip()),
            "overall_status": "HEALTHY" if not self.issues_found else "ISSUES_FOUND",
            "issues_found": self.issues_found,
            "fixes_applied": self.fixes_applied,
            "recommendations": [],
            "next_steps": []
        }
        
        # Add recommendations based on issues
        if "Frontend dependencies missing" in self.issues_found:
            report["recommendations"].append("Run 'npm install' in the frontend directory")
        
        if "Backend dependency missing" in [i for i in self.issues_found if "Backend dependency" in i]:
            report["recommendations"].append("Install backend dependencies with 'pip install -r requirements.txt'")
        
        if "Frontend build fails" in self.issues_found:
            report["recommendations"].append("Check frontend code for TypeScript errors")
        
        # Add next steps for production
        if report["overall_status"] == "HEALTHY":
            report["next_steps"] = [
                "Train AI model with real diabetic retinopathy dataset",
                "Deploy backend to Google Cloud Run",
                "Update frontend API endpoints for production",
                "Set up production database",
                "Configure monitoring and analytics"
            ]
        
        # Write report to file
        report_file = self.project_root / "HEALTH_CHECK_REPORT.json"
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2)
        
        self.log_status(f"✅ Health report saved to: {report_file}", "SUCCESS")
        return report
    
    def run_full_check(self):
        """Run complete project health check"""
        self.log_status("🏥 Starting OpthalmoAI Project Health Check...", "INFO")
        self.log_status("=" * 60, "INFO")
        
        # Run all checks
        self.check_directory_structure()
        self.check_package_files()
        self.check_frontend_dependencies()
        self.check_backend_dependencies()
        self.check_api_endpoints()
        
        # Auto-fix if issues found
        if self.issues_found:
            self.log_status(f"Found {len(self.issues_found)} issues. Attempting auto-fixes...", "WARNING")
            self.auto_fix_dependencies()
        
        # Test build capability
        self.check_build_capability()
        
        # Generate report
        report = self.generate_health_report()
        
        # Final summary
        self.log_status("=" * 60, "INFO")
        if report["overall_status"] == "HEALTHY":
            self.log_status("🎉 PROJECT STATUS: HEALTHY! Ready for development.", "SUCCESS")
        else:
            self.log_status(f"⚠️ PROJECT STATUS: {len(self.issues_found)} issues found", "WARNING")
            self.log_status("Check the health report for details and recommendations.", "INFO")
        
        return report

if __name__ == "__main__":
    checker = ProjectHealthChecker()
    report = checker.run_full_check()
    
    # Exit with error code if issues found
    sys.exit(0 if report["overall_status"] == "HEALTHY" else 1)