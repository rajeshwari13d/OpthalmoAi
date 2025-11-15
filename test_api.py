"""
Test script to verify the backend upload/analysis endpoint is working
"""
import requests
import os

def test_backend_api():
    """Test the backend API endpoints"""
    base_url = "http://127.0.0.1:8006/api/v1"
    
    print("🧪 Testing OpthalmoAI Backend API...")
    
    # Test health endpoint
    try:
        print("\n1️⃣ Testing health endpoint...")
        response = requests.get(f"{base_url}/health", timeout=10)
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.json()}")
        
        if response.status_code == 200:
            print("   ✅ Health endpoint working!")
        else:
            print("   ❌ Health endpoint failed!")
            return False
            
    except Exception as e:
        print(f"   ❌ Health endpoint error: {e}")
        return False
    
    # Test analyze endpoint with test image
    try:
        print("\n2️⃣ Testing analyze endpoint...")
        
        # Check for test image
        test_image_path = "test_image.jpg"
        if not os.path.exists(test_image_path):
            print("   ⚠️  No test image found, creating a simple test...")
            # Create a simple test file for upload
            test_data = b"fake image data for testing"
            
            files = {'file': ('test.jpg', test_data, 'image/jpeg')}
        else:
            print(f"   📸 Using test image: {test_image_path}")
            with open(test_image_path, 'rb') as f:
                files = {'file': ('test.jpg', f.read(), 'image/jpeg')}
        
        response = requests.post(f"{base_url}/analyze", files=files, timeout=30)
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("   ✅ Analyze endpoint working!")
            print(f"   📊 Analysis result: {result.get('message', 'No message')}")
            if 'analysis' in result:
                dr_info = result['analysis'].get('diabetic_retinopathy', {})
                print(f"   🎯 Prediction: {dr_info.get('stage_name', 'Unknown')} ({dr_info.get('confidence', 0):.1%} confidence)")
        else:
            print(f"   ❌ Analyze endpoint failed: {response.text}")
            return False
            
    except Exception as e:
        print(f"   ❌ Analyze endpoint error: {e}")
        return False
    
    print("\n🎉 Backend API is working correctly!")
    print("\n📱 Frontend should now be able to connect and get real AI results!")
    return True

if __name__ == "__main__":
    success = test_backend_api()
    if success:
        print("\n✅ All tests passed! Your OpthalmoAI system is ready!")
        print("\n🌐 Open your browser to: http://localhost:3000")
        print("📸 Upload a retinal image to get real AI analysis!")
    else:
        print("\n❌ Some tests failed. Check the backend server.")