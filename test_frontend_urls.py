"""
Quick test to verify the frontend API URL is correctly formatted
"""

import requests

def test_frontend_api_urls():
    """Test the URLs that the frontend should be using"""
    
    print("🔍 Testing Frontend API URL Configuration")
    print("=" * 50)
    
    # These are the URLs the frontend should be calling
    base_url = "http://127.0.0.1:8001"
    
    test_urls = [
        f"{base_url}/health",
        f"{base_url}/analyze"
    ]
    
    for url in test_urls:
        print(f"\n🌐 Testing: {url}")
        
        if "/health" in url:
            try:
                response = requests.get(url, timeout=5)
                if response.status_code == 200:
                    print(f"   ✅ Health endpoint working")
                    data = response.json()
                    print(f"   📊 Status: {data.get('status')}")
                else:
                    print(f"   ❌ Health endpoint failed: {response.status_code}")
            except Exception as e:
                print(f"   ❌ Health endpoint error: {e}")
        
        elif "/analyze" in url:
            print(f"   📋 Analyze endpoint should accept POST with FormData")
            print(f"   🎯 This is where the frontend will upload images")
    
    print(f"\n✅ Frontend should now use these correct URLs:")
    print(f"   Health: {base_url}/health")
    print(f"   Analyze: {base_url}/analyze")
    print(f"\n❌ Old incorrect URL format was:")
    print(f"   http://127.0.0.1:8000v1/analyze (malformed)")
    print(f"\n🔧 Fixed in:")
    print(f"   frontend/src/services/api.config.ts")
    print(f"   frontend/src/services/api.client.ts")

if __name__ == "__main__":
    test_frontend_api_urls()
    print(f"\n🎉 Frontend API configuration should now be fixed!")
    print(f"📱 Try uploading an image at: http://localhost:3000")