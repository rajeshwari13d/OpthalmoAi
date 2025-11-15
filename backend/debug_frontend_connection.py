"""
Debug Frontend Connection Issue
Test the exact same request the frontend makes to backend
"""
import requests
import os
from PIL import Image
import io

def test_frontend_backend_connection():
    """Test the exact connection from frontend perspective"""
    print("🔍 Debugging Frontend -> Backend Connection...")
    
    # Test 1: Health check (same as frontend would do)
    try:
        health_url = "http://127.0.0.1:8004/api/v1/health"
        print(f"Testing health: {health_url}")
        
        response = requests.get(health_url, timeout=10)
        print(f"✅ Health Status: {response.status_code}")
        
        if response.status_code == 200:
            print(f"Response: {response.json()}")
        else:
            print(f"❌ Health failed: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Health check failed: {e}")
        return False
    
    # Test 2: Upload request (exactly like frontend)
    try:
        upload_url = "http://127.0.0.1:8004/api/v1/analyze" 
        print(f"\nTesting upload: {upload_url}")
        
        # Create a small test image (same as frontend would send)
        img = Image.new('RGB', (100, 100), color='red')
        img_bytes = io.BytesIO()
        img.save(img_bytes, format='JPEG')
        img_bytes.seek(0)
        
        # Prepare files exactly like frontend FormData
        files = {
            'file': ('test.jpg', img_bytes.getvalue(), 'image/jpeg')
        }
        
        # Add headers that frontend might send
        headers = {
            'Accept': 'application/json',
            'Origin': 'http://localhost:3000',
            'Referer': 'http://localhost:3000'
        }
        
        print("Sending upload request...")
        response = requests.post(
            upload_url, 
            files=files, 
            headers=headers,
            timeout=30
        )
        
        print(f"Upload Status: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ Upload successful!")
            data = response.json()
            print(f"Response keys: {list(data.keys())}")
            return True
        else:
            print(f"❌ Upload failed: {response.status_code}")
            print(f"Response: {response.text}")
            print(f"Headers: {response.headers}")
            return False
            
    except requests.exceptions.ConnectionError as e:
        print(f"❌ Connection Error: {e}")
        print("This is the same error frontend sees: 'Failed to fetch'")
        return False
    except Exception as e:
        print(f"❌ Upload error: {e}")
        return False

def check_cors_issue():
    """Check if it's a CORS issue"""
    print("\n🔍 Checking CORS Configuration...")
    
    try:
        # Test with CORS preflight
        options_url = "http://127.0.0.1:8004/api/v1/analyze"
        headers = {
            'Origin': 'http://localhost:3000',
            'Access-Control-Request-Method': 'POST',
            'Access-Control-Request-Headers': 'content-type'
        }
        
        response = requests.options(options_url, headers=headers)
        print(f"CORS Preflight Status: {response.status_code}")
        print(f"CORS Headers: {dict(response.headers)}")
        
        if 'access-control-allow-origin' in response.headers:
            print(f"✅ CORS Allow Origin: {response.headers['access-control-allow-origin']}")
        else:
            print("❌ No CORS headers found")
            
    except Exception as e:
        print(f"❌ CORS test failed: {e}")

if __name__ == "__main__":
    print("=" * 60)
    print("🐛 DEBUGGING FRONTEND 'Failed to fetch' ERROR")
    print("=" * 60)
    
    success = test_frontend_backend_connection()
    check_cors_issue()
    
    print("\n" + "=" * 60)
    if success:
        print("✅ Connection works - Issue might be in frontend code")
    else:
        print("❌ Connection failed - This is why frontend shows 'Failed to fetch'")
    print("=" * 60)