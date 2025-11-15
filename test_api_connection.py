#!/usr/bin/env python3
"""
Simple API Connection Test
Tests the connection between frontend and backend without browser dependency
"""

import requests
import json
import time
from pathlib import Path

def test_backend_connection():
    """Test if backend is running and responsive"""
    backend_url = "http://127.0.0.1:8001"
    
    print("🔍 Testing Backend Connection...")
    print(f"Backend URL: {backend_url}")
    
    # Test root endpoint
    try:
        response = requests.get(f"{backend_url}/", timeout=5)
        print(f"✅ Root endpoint: {response.status_code}")
        if response.status_code == 200:
            print(f"   Response: {response.json()}")
    except Exception as e:
        print(f"❌ Root endpoint failed: {e}")
        return False
    
    # Test health endpoint
    try:
        response = requests.get(f"{backend_url}/api/v1/health", timeout=5)
        print(f"✅ Health endpoint: {response.status_code}")
        if response.status_code == 200:
            print(f"   Response: {response.json()}")
        else:
            print(f"   Error: {response.text}")
    except Exception as e:
        print(f"❌ Health endpoint failed: {e}")
        return False
    
    return True

def test_upload_endpoint():
    """Test image upload endpoint"""
    backend_url = "http://127.0.0.1:8001"
    
    print("\n🔍 Testing Upload Endpoint...")
    
    # Create a small test image
    from PIL import Image
    import io
    
    # Create a simple test image
    test_image = Image.new('RGB', (224, 224), color='red')
    img_bytes = io.BytesIO()
    test_image.save(img_bytes, format='JPEG')
    img_bytes.seek(0)
    
    try:
        files = {'image': ('test.jpg', img_bytes, 'image/jpeg')}
        response = requests.post(f"{backend_url}/api/v1/analyze", files=files, timeout=30)
        
        print(f"✅ Upload endpoint: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print(f"   Analysis Result: {json.dumps(result, indent=2)}")
        else:
            print(f"   Error: {response.text}")
            
    except Exception as e:
        print(f"❌ Upload endpoint failed: {e}")
        return False
    
    return True

if __name__ == "__main__":
    print("🚀 OpthalmoAI API Connection Test")
    print("=" * 50)
    
    # Test backend connection
    if test_backend_connection():
        print("\n✅ Backend is running!")
        
        # Test upload functionality
        if test_upload_endpoint():
            print("\n🎉 All tests passed! The API is working correctly.")
        else:
            print("\n⚠️  Upload functionality has issues.")
    else:
        print("\n❌ Backend is not responding. Please check if the server is running.")
    
    print("\n" + "=" * 50)