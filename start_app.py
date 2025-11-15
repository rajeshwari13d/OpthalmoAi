#!/usr/bin/env python3
"""
Start both backend and frontend servers for OpthalmoAI
"""

import subprocess
import time
import sys
import os
import signal
import threading
from pathlib import Path

# Global process variables
backend_process = None
frontend_process = None

def signal_handler(signum, frame):
    """Handle shutdown signals"""
    print("\n🛑 Shutting down servers...")
    
    if backend_process:
        backend_process.terminate()
        print("   Backend stopped")
        
    if frontend_process:
        frontend_process.terminate() 
        print("   Frontend stopped")
        
    sys.exit(0)

def start_backend():
    """Start the backend server"""
    global backend_process
    
    print("🚀 Starting Backend Server...")
    
    backend_dir = Path("D:/work_station/OpthalmoAi")
    
    try:
        backend_process = subprocess.Popen(
            [sys.executable, "simple_backend.py"],
            cwd=backend_dir,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1
        )
        
        # Monitor backend output in a separate thread
        def monitor_backend():
            for line in iter(backend_process.stdout.readline, ''):
                print(f"[BACKEND] {line.rstrip()}")
                
        threading.Thread(target=monitor_backend, daemon=True).start()
        
        print("✅ Backend server starting...")
        return True
        
    except Exception as e:
        print(f"❌ Failed to start backend: {e}")
        return False

def start_frontend():
    """Start the frontend server"""
    global frontend_process
    
    print("🌐 Starting Frontend Server...")
    
    frontend_dir = Path("D:/work_station/OpthalmoAi/frontend")
    
    try:
        frontend_process = subprocess.Popen(
            ["npm", "start"],
            cwd=frontend_dir,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1
        )
        
        # Monitor frontend output in a separate thread
        def monitor_frontend():
            for line in iter(frontend_process.stdout.readline, ''):
                if "webpack compiled" in line.lower() or "compiled successfully" in line.lower():
                    print(f"[FRONTEND] ✅ {line.rstrip()}")
                elif "error" in line.lower() and "deprecation" not in line.lower():
                    print(f"[FRONTEND] ❌ {line.rstrip()}")
                elif "starting" in line.lower() or "server" in line.lower():
                    print(f"[FRONTEND] 🔄 {line.rstrip()}")
                
        threading.Thread(target=monitor_frontend, daemon=True).start()
        
        print("✅ Frontend server starting...")
        return True
        
    except Exception as e:
        print(f"❌ Failed to start frontend: {e}")
        return False

def wait_for_servers():
    """Wait for servers to be ready"""
    import requests
    
    print("\n⏳ Waiting for servers to be ready...")
    
    # Wait for backend
    backend_ready = False
    for i in range(30):  # 30 second timeout
        try:
            response = requests.get("http://127.0.0.1:8003/api/v1/health", timeout=2)
            if response.status_code == 200:
                print("✅ Backend is ready!")
                backend_ready = True
                break
        except:
            pass
        time.sleep(1)
    
    if not backend_ready:
        print("⚠️  Backend may not be ready yet")
    
    # Wait a bit for frontend
    print("⏳ Waiting for frontend to compile...")
    time.sleep(10)  # Give frontend time to compile
    
    return backend_ready

def main():
    """Main startup function"""
    print("🎯 OpthalmoAI Application Launcher")
    print("=" * 50)
    
    # Set up signal handlers for clean shutdown
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    try:
        # Start backend
        if not start_backend():
            print("❌ Failed to start backend server")
            return 1
        
        time.sleep(3)  # Give backend time to start
        
        # Start frontend  
        if not start_frontend():
            print("❌ Failed to start frontend server")
            return 1
        
        # Wait for servers to be ready
        servers_ready = wait_for_servers()
        
        if servers_ready:
            print("\n🎉 OpthalmoAI is ready!")
            print("📍 Frontend: http://localhost:3000")
            print("📍 Backend:  http://localhost:8003")
            print("📋 API Docs: http://localhost:8003/docs")
            print("\n💡 Open http://localhost:3000 in your browser")
            print("🔧 Upload a retinal image to test the AI analysis")
        else:
            print("\n⚠️  Servers may not be fully ready yet")
            print("💡 Try accessing http://localhost:3000 in a few moments")
        
        print("\n" + "=" * 50)
        print("🔴 Press Ctrl+C to stop all servers")
        print("=" * 50)
        
        # Keep the main process running
        try:
            while True:
                time.sleep(1)
                # Check if processes are still running
                if backend_process and backend_process.poll() is not None:
                    print("❌ Backend process died")
                    break
                if frontend_process and frontend_process.poll() is not None:
                    print("❌ Frontend process died") 
                    break
        except KeyboardInterrupt:
            pass
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return 1
    
    finally:
        signal_handler(None, None)
    
    return 0

if __name__ == "__main__":
    sys.exit(main())