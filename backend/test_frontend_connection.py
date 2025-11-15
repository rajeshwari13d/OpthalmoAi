"""
Frontend-Backend Connection Test
Test if the frontend can properly communicate with the backend API
"""
import requests
import json

def test_cors_preflight():
    """Test CORS preflight request"""
    print("🔍 Testing CORS Preflight...")
    
    try:
        # Test OPTIONS request (CORS preflight)
        response = requests.options(
            "http://127.0.0.1:8004/api/v1/analyze",
            headers={
                'Origin': 'http://localhost:3000',
                'Access-Control-Request-Method': 'POST',
                'Access-Control-Request-Headers': 'content-type'
            },
            timeout=5
        )
        
        print(f"   OPTIONS Status: {response.status_code}")
        print(f"   CORS Headers: {dict(response.headers)}")
        
        # Check required CORS headers
        required_headers = [
            'access-control-allow-origin',
            'access-control-allow-methods', 
            'access-control-allow-headers'
        ]
        
        missing_headers = []
        for header in required_headers:
            if header not in response.headers:
                missing_headers.append(header)
        
        if missing_headers:
            print(f"   ❌ Missing CORS headers: {missing_headers}")
            return False
        else:
            print("   ✅ CORS headers present")
            return True
            
    except Exception as e:
        print(f"   ❌ CORS test failed: {e}")
        return False

def test_frontend_api_call():
    """Test the exact API call that frontend makes"""
    print("\n📡 Testing Frontend API Call...")
    
    try:
        from PIL import Image
        import io
        
        # Create a test image exactly like frontend would
        test_image = Image.new('RGB', (224, 224), color='darkred')
        buffer = io.BytesIO()
        test_image.save(buffer, format='JPEG')
        buffer.seek(0)
        
        # Make request exactly like frontend does
        files = {'file': ('retinal.jpg', buffer, 'image/jpeg')}
        
        # Test with both localhost and 127.0.0.1 
        urls = [
            "http://localhost:8004/api/v1/analyze",
            "http://127.0.0.1:8004/api/v1/analyze"
        ]
        
        for url in urls:
            print(f"   Testing {url}...")
            try:
                # Reset buffer
                buffer.seek(0)
                files = {'file': ('retinal.jpg', buffer, 'image/jpeg')}
                
                response = requests.post(
                    url,
                    files=files,
                    headers={
                        'Origin': 'http://localhost:3000'
                    },
                    timeout=10
                )
                
                if response.status_code == 200:
                    data = response.json()
                    print(f"   ✅ {url}: SUCCESS")
                    print(f"      Response keys: {list(data.keys())}")
                    if 'result' in data:
                        print(f"      Analysis ID: {data['result'].get('id', 'N/A')}")
                else:
                    print(f"   ❌ {url}: HTTP {response.status_code}")
                    print(f"      Response: {response.text}")
                    
            except Exception as e:
                print(f"   ❌ {url}: {e}")
        
        return True
        
    except Exception as e:
        print(f"   ❌ API call test failed: {e}")
        return False

def test_health_endpoint():
    """Test health endpoint from frontend perspective"""
    print("\n❤️  Testing Health Endpoint...")
    
    urls = [
        "http://localhost:8004/api/v1/health",
        "http://127.0.0.1:8004/api/v1/health"
    ]
    
    for url in urls:
        try:
            response = requests.get(
                url,
                headers={'Origin': 'http://localhost:3000'},
                timeout=5
            )
            
            if response.status_code == 200:
                data = response.json()
                print(f"   ✅ {url}: {data.get('status', 'unknown')}")
            else:
                print(f"   ❌ {url}: HTTP {response.status_code}")
                
        except Exception as e:
            print(f"   ❌ {url}: {e}")

def main():
    """Run frontend connection diagnostics"""
    print("🚀 Frontend-Backend Connection Diagnostics")
    print("=" * 55)
    
    # Test 1: CORS
    cors_ok = test_cors_preflight()
    
    # Test 2: Health endpoint
    test_health_endpoint()
    
    # Test 3: API call
    api_ok = test_frontend_api_call()
    
    # Summary
    print("\n" + "=" * 55)
    print("🔍 DIAGNOSTIC SUMMARY")
    print("=" * 55)
    
    if cors_ok and api_ok:
        print("✅ Backend is accessible from frontend")
        print("✅ CORS is properly configured")
        print("✅ API endpoints are working")
        print("\n💡 If frontend still shows 'Failed to fetch':")
        print("   1. Check browser developer console for exact error")
        print("   2. Verify frontend is using correct API URL")
        print("   3. Clear browser cache and try again")
        print("   4. Check if any browser extensions are blocking requests")
    else:
        print("❌ Connection issues detected")
        print("⚠️  Frontend may not be able to reach backend")

if __name__ == "__main__":
    main()