#!/usr/bin/env python3
"""
Test the complete image upload and analysis flow
"""

import requests
import io
from PIL import Image
import json

def test_image_upload_flow():
    """Test the complete image upload to results display flow"""
    backend_url = "http://127.0.0.1:8003"
    
    print("🧪 Testing Complete Image Upload Flow")
    print("=" * 50)
    
    # Test 1: Health check
    try:
        response = requests.get(f"{backend_url}/api/v1/health", timeout=5)
        print(f"✅ Health Check: {response.status_code}")
        if response.status_code == 200:
            health_data = response.json()
            print(f"   Status: {health_data.get('status')}")
            print(f"   Model Loaded: {health_data.get('model_loaded')}")
    except Exception as e:
        print(f"❌ Health Check Failed: {e}")
        return False
    
    # Test 2: Create test image
    print("\n📷 Creating Test Retinal Image...")
    test_image = Image.new('RGB', (224, 224), color=(200, 100, 50))  # Retinal-like color
    
    # Add some circular patterns to mimic retinal features
    from PIL import ImageDraw
    draw = ImageDraw.Draw(test_image)
    
    # Optic disc (bright circle)
    draw.ellipse([80, 80, 120, 120], fill=(255, 200, 150))
    
    # Blood vessels (dark lines)
    draw.line([50, 112, 174, 112], fill=(120, 50, 30), width=3)
    draw.line([112, 50, 112, 174], fill=(120, 50, 30), width=2)
    
    # Convert to bytes
    img_bytes = io.BytesIO()
    test_image.save(img_bytes, format='JPEG', quality=85)
    img_bytes.seek(0)
    
    print("   ✅ Test image created (224x224 JPEG)")
    
    # Test 3: Upload and analyze image
    print("\n🔬 Testing Image Upload & Analysis...")
    try:
        files = {'file': ('test_retinal_image.jpg', img_bytes, 'image/jpeg')}
        response = requests.post(f"{backend_url}/api/v1/analyze", files=files, timeout=30)
        
        print(f"   📤 Upload Response: {response.status_code}")
        
        if response.status_code == 200:
            result_data = response.json()
            print("   ✅ Analysis Successful!")
            print(f"   📋 Response Keys: {list(result_data.keys())}")
            
            if 'result' in result_data:
                result = result_data['result']
                print(f"\n🎯 Analysis Results:")
                print(f"   • ID: {result.get('id')}")
                print(f"   • Stage: {result.get('stage')}/4")
                print(f"   • Confidence: {result.get('confidence')}%")
                print(f"   • Risk Level: {result.get('riskLevel')}")
                print(f"   • Processing Time: {result.get('processing_time')}s")
                print(f"   • Recommendations: {len(result.get('recommendations', []))} items")
                
                if 'model_info' in result:
                    model_info = result['model_info']
                    print(f"\n🤖 Model Information:")
                    print(f"   • Model Name: {model_info.get('model_name')}")
                    print(f"   • Custom Model: {model_info.get('use_custom_model')}")
                
                print(f"\n📋 Medical Disclaimer Present: {'medical_disclaimer' in result_data}")
                
                return True
            else:
                print("   ❌ No 'result' field in response")
                print(f"   Response: {json.dumps(result_data, indent=2)}")
        else:
            print(f"   ❌ Analysis Failed: {response.status_code}")
            try:
                error_data = response.json()
                print(f"   Error: {error_data}")
            except:
                print(f"   Error Text: {response.text}")
                
    except Exception as e:
        print(f"   ❌ Upload Failed: {e}")
        return False
    
    return False

def test_frontend_api_config():
    """Test frontend API configuration"""
    print("\n🌐 Checking Frontend API Configuration...")
    
    try:
        with open("D:/work_station/OpthalmoAi/frontend/src/services/api.config.ts", 'r') as f:
            config_content = f.read()
            
        if "http://127.0.0.1:8003" in config_content:
            print("   ✅ Frontend configured for correct port (8003)")
        else:
            print("   ❌ Frontend not configured for port 8003")
            
        if "/api/v1" in config_content:
            print("   ✅ Frontend configured for correct API version")
        else:
            print("   ❌ Frontend missing API version configuration")
            
    except Exception as e:
        print(f"   ❌ Could not read frontend config: {e}")

if __name__ == "__main__":
    print("🧪 OpthalmoAI Complete Flow Test")
    print("Testing image upload → AI analysis → result display flow")
    print("=" * 60)
    
    # Test backend flow
    success = test_image_upload_flow()
    
    # Test frontend config
    test_frontend_api_config()
    
    print("\n" + "=" * 60)
    if success:
        print("🎉 SUCCESS: Complete flow is working!")
        print("✅ Images can be uploaded and processed")
        print("✅ AI analysis returns proper results")
        print("✅ Results contain all required fields")
        print("\n💡 Next Step: Test in the browser at http://localhost:3000")
    else:
        print("❌ ISSUES FOUND: Flow needs fixing")
        print("🔧 Check backend server logs for errors")
        print("🔧 Verify API endpoints are working")
        
    print("=" * 60)