"""
Test frontend connection with corrected port configuration
"""
import requests
from PIL import Image
import io

def test_corrected_frontend_connection():
    """Test that frontend can now connect to backend on correct port"""
    print("🔧 Testing Corrected Frontend-Backend Connection")
    print("=" * 55)
    
    # Test the exact configuration frontend should now use
    frontend_api_url = "http://127.0.0.1:8004/api/v1/analyze"
    
    try:
        # Create test image
        test_image = Image.new('RGB', (224, 224), color='darkred')
        buffer = io.BytesIO()
        test_image.save(buffer, format='JPEG')
        buffer.seek(0)
        
        # Test upload with frontend headers
        files = {'file': ('retinal_test.jpg', buffer, 'image/jpeg')}
        headers = {
            'Origin': 'http://localhost:3000',
            'Referer': 'http://localhost:3000/'
        }
        
        print(f"📡 Testing: {frontend_api_url}")
        print(f"🌐 Origin: {headers['Origin']}")
        
        response = requests.post(
            frontend_api_url,
            files=files,
            headers=headers,
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Connection successful!")
            print(f"   Response structure: {list(data.keys())}")
            
            if 'result' in data:
                result = data['result']
                print(f"   Analysis ID: {result.get('id', 'N/A')}")
                print(f"   DR Stage: {result.get('stage', 'N/A')}")
                print(f"   Confidence: {result.get('confidence', 'N/A')}%")
                print(f"   Risk Level: {result.get('riskLevel', 'N/A')}")
            
            if 'medical_disclaimer' in data:
                print("   ✅ Medical disclaimer included")
                
            return True
        else:
            print(f"❌ Connection failed: HTTP {response.status_code}")
            print(f"   Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Connection test failed: {e}")
        return False

def test_health_check():
    """Test health endpoint with correct port"""
    print("\n❤️  Testing Health Check...")
    
    try:
        response = requests.get(
            "http://127.0.0.1:8004/api/v1/health",
            headers={'Origin': 'http://localhost:3000'},
            timeout=5
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Health check: {data.get('status', 'unknown')}")
            print(f"   Model loaded: {data.get('model_loaded', False)}")
            return True
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Health check error: {e}")
        return False

def main():
    """Run corrected connection test"""
    
    # Test health first
    health_ok = test_health_check()
    
    # Test image upload
    upload_ok = test_corrected_frontend_connection()
    
    print("\n" + "=" * 55)
    print("🎯 CORRECTED CONNECTION TEST RESULTS")
    print("=" * 55)
    
    if health_ok and upload_ok:
        print("✅ FIXED: Frontend should now connect successfully!")
        print("✅ Backend is responding on correct port (8004)")
        print("✅ Image upload pipeline working")
        print("\n💡 Next steps:")
        print("   1. Refresh the browser page")
        print("   2. Try uploading a retinal image")
        print("   3. Should see 'Analysis successful' instead of 'Failed to fetch'")
    else:
        print("❌ Still having connection issues")
        print("⚠️  May need additional troubleshooting")

if __name__ == "__main__":
    main()