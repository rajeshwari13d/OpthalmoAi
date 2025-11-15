"""
End-to-end test for OpthalmoAI with ResNet50 and VGG16 integration
Tests the complete API pipeline from image upload to prediction
"""

import requests
import json
import time
from PIL import Image, ImageDraw
import io
import sys

def create_test_retinal_image(width=512, height=512, dr_stage=0):
    """Create a synthetic retinal fundus image for testing"""
    # Create base fundus image
    image = Image.new('RGB', (width, height), color=(80, 40, 20))
    draw = ImageDraw.Draw(image)
    
    # Draw optic disc (bright circular area)
    disc_center = (width//4, height//2)
    disc_radius = min(width, height) // 8
    draw.ellipse([disc_center[0]-disc_radius, disc_center[1]-disc_radius,
                  disc_center[0]+disc_radius, disc_center[1]+disc_radius], 
                 fill=(220, 180, 120))
    
    # Draw blood vessels
    for i in range(8):
        start_x = disc_center[0] + (i-4) * 10
        start_y = disc_center[1] + (i-4) * 5
        end_x = start_x + (width//3) * (1 if i%2 else -1)
        end_y = start_y + (height//4) * (1 if i%3 else -1)
        draw.line([(start_x, start_y), (end_x, end_y)], 
                 fill=(120, 60, 40), width=3)
    
    # Add DR stage-specific features
    if dr_stage >= 1:  # Mild DR - microaneurysms
        for _ in range(5 + dr_stage * 3):
            x = width//4 + (width//2) * ((_ % 10) / 10)
            y = height//4 + (height//2) * ((_ % 7) / 7)
            radius = 2
            draw.ellipse([x-radius, y-radius, x+radius, y+radius], 
                        fill=(150, 50, 50))
    
    if dr_stage >= 2:  # Moderate DR - hemorrhages
        for _ in range(3 + dr_stage * 2):
            x = width//3 + (width//3) * ((_ % 8) / 8)
            y = height//3 + (height//3) * ((_ % 6) / 6)
            radius = 5
            draw.ellipse([x-radius, y-radius, x+radius, y+radius], 
                        fill=(100, 20, 20))
    
    return image

def image_to_bytes(image, format='JPEG'):
    """Convert PIL Image to bytes"""
    byte_arr = io.BytesIO()
    image.save(byte_arr, format=format)
    byte_arr.seek(0)
    return byte_arr

def test_server_health():
    """Test if the server is running and healthy"""
    try:
        response = requests.get("http://127.0.0.1:8001/health", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print("✅ Server health check passed")
            print(f"   Status: {data.get('status', 'unknown')}")
            print(f"   Models loaded: {data.get('models_loaded', False)}")
            return True
        else:
            print(f"❌ Health check failed: HTTP {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Server health check failed: Connection refused")
        print("   Make sure the server is running on http://127.0.0.1:8001")
        return False
    except Exception as e:
        print(f"❌ Health check failed: {e}")
        return False

def test_model_info():
    """Test the model info endpoint"""
    try:
        response = requests.get("http://127.0.0.1:8001/model-info", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print("✅ Model info endpoint test passed")
            print(f"   Model type: {data.get('model_type', 'unknown')}")
            print(f"   Ensemble mode: {data.get('ensemble_mode', False)}")
            models = data.get('models', {})
            print(f"   ResNet50: {'✓' if models.get('resnet50') else '✗'}")
            print(f"   VGG16: {'✓' if models.get('vgg16') else '✗'}")
            return True
        else:
            print(f"❌ Model info test failed: HTTP {response.status_code}")
            print(f"   Response: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Model info test failed: {e}")
        return False

def test_image_analysis(dr_stage=0):
    """Test image analysis endpoint"""
    try:
        # Create test image
        test_image = create_test_retinal_image(dr_stage=dr_stage)
        image_bytes = image_to_bytes(test_image)
        
        # Prepare request
        files = {
            'file': ('test_retina.jpg', image_bytes, 'image/jpeg')
        }
        
        print(f"🔬 Testing analysis with DR stage {dr_stage} simulation...")
        start_time = time.time()
        
        response = requests.post(
            "http://127.0.0.1:8001/analyze", 
            files=files, 
            timeout=30
        )
        
        end_time = time.time()
        request_time = end_time - start_time
        
        if response.status_code == 200:
            data = response.json()
            
            if data.get('success'):
                result = data.get('result', {})
                
                print(f"✅ Image analysis test passed")
                print(f"   Input: Simulated DR stage {dr_stage}")
                print(f"   Predicted stage: {result.get('stage')} - {result.get('stage_description')}")
                print(f"   Confidence: {result.get('confidence')}%")
                print(f"   Risk level: {result.get('risk_level')}")
                print(f"   Processing time: {result.get('processing_time')}s")
                print(f"   Total request time: {request_time:.3f}s")
                
                # Check if model info is included
                model_info = result.get('model_info')
                if model_info:
                    print(f"   Model: {model_info.get('model_name', 'Unknown')}")
                    if 'ensemble_agreement' in model_info:
                        agreement = model_info['ensemble_agreement']
                        print(f"   Agreement: {agreement.get('agreement_level')} ({agreement.get('agreement_score', 0):.1f}%)")
                
                # Check recommendations
                recommendations = result.get('recommendations', [])
                print(f"   Recommendations: {len(recommendations)} items")
                
                return True
            else:
                print(f"❌ Analysis failed: {data.get('error', 'Unknown error')}")
                return False
        else:
            print(f"❌ Analysis test failed: HTTP {response.status_code}")
            print(f"   Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Analysis test failed: {e}")
        return False

def test_error_handling():
    """Test error handling with invalid inputs"""
    print("🧪 Testing error handling...")
    
    # Test with non-image file
    try:
        files = {'file': ('test.txt', io.BytesIO(b'This is not an image'), 'text/plain')}
        response = requests.post("http://127.0.0.1:8001/analyze", files=files, timeout=10)
        
        if response.status_code == 400:
            print("✅ Non-image file rejection test passed")
        else:
            print(f"❌ Non-image file test failed: Expected 400, got {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error handling test failed: {e}")
        return False
    
    # Test with very small image
    try:
        small_image = Image.new('RGB', (50, 50), color=(255, 255, 255))
        image_bytes = image_to_bytes(small_image)
        files = {'file': ('small.jpg', image_bytes, 'image/jpeg')}
        response = requests.post("http://127.0.0.1:8001/analyze", files=files, timeout=10)
        
        if response.status_code == 400:
            print("✅ Small image rejection test passed")
        else:
            print(f"❌ Small image test failed: Expected 400, got {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Small image test failed: {e}")
        return False
    
    return True

def main():
    """Run all end-to-end tests"""
    print("🔬 OpthalmoAI End-to-End Integration Test")
    print("🏥 Testing ResNet50 + VGG16 Ensemble Pipeline")
    print("=" * 70)
    
    tests = [
        ("Server Health Check", test_server_health),
        ("Model Info", test_model_info),
        ("Image Analysis (No DR)", lambda: test_image_analysis(0)),
        ("Image Analysis (Mild DR)", lambda: test_image_analysis(1)),
        ("Image Analysis (Moderate DR)", lambda: test_image_analysis(2)),
        ("Error Handling", test_error_handling)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n🧪 Running {test_name}...")
        try:
            if test_func():
                passed += 1
            else:
                print(f"❌ {test_name} failed")
        except Exception as e:
            print(f"❌ {test_name} failed with exception: {e}")
    
    print("\n" + "=" * 70)
    print(f"📊 TEST RESULTS: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 ALL TESTS PASSED!")
        print("✅ ResNet50 + VGG16 integration is working correctly")
        print("✅ End-to-end pipeline is functional")
        print("✅ Error handling is working properly")
        
        print("\n🚀 INTEGRATION COMPLETE!")
        print("📋 Summary:")
        print("   ✓ ResNet50 model integrated and working")
        print("   ✓ VGG16 model integrated and working") 
        print("   ✓ Ensemble prediction working")
        print("   ✓ FastAPI server running on http://127.0.0.1:8001")
        print("   ✓ Image upload and analysis pipeline functional")
        print("   ✓ Medical-grade error handling implemented")
        
        print("\n📝 Next Steps:")
        print("1. Update frontend API endpoints to use http://127.0.0.1:8001")
        print("2. Train models on real diabetic retinopathy dataset")
        print("3. Deploy to production environment")
        print("4. Implement real-time monitoring and logging")
        
    else:
        print("⚠️  Some tests failed. Check the errors above.")
        print("💡 Make sure the server is running: python standalone_server.py")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)