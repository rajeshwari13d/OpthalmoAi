#!/usr/bin/env python3
"""
Simple Backend Server for OpthalmoAI
Minimal server setup to test the API connection and model loading
"""

import uvicorn
import sys
import os
from pathlib import Path

# Add backend to Python path
backend_path = Path(__file__).parent / "backend"
sys.path.insert(0, str(backend_path))

def main():
    print("🚀 Starting OpthalmoAI Backend Server...")
    print(f"📁 Backend path: {backend_path}")
    print(f"🐍 Python path: {sys.path[0]}")
    
    try:
        # Set environment variable for backend path
        os.environ["PYTHONPATH"] = str(backend_path)
        
        # Start the server
        uvicorn.run(
            "app.main:app",
            host="0.0.0.0",
            port=8002,
            reload=False,  # Disable reload for stability
            log_level="info"
        )
    except Exception as e:
        print(f"❌ Failed to start server: {e}")
        return 1

if __name__ == "__main__":
    exit(main())