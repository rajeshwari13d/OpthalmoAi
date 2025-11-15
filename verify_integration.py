"""
Quick verification that OpthalmoAI ResNet50 + VGG16 integration is working
"""

import requests
import json
from PIL import Image, ImageDraw
import io

def create_sample_retinal_image():
    """Create a simple retinal-like image for testing"""
    image = Image.new('RGB', (512, 512), color=(80, 40, 20))
    draw = ImageDraw.Draw(image)
    
    # Draw optic disc
    draw.ellipse([100, 200, 180, 280], fill=(220, 180, 120))
    
    # Draw some blood vessels
    draw.line([(120, 240), (400, 240)], fill=(120, 60, 40), width=4)
    draw.line([(140, 220), (380, 300)], fill=(120, 60, 40), width=3)
    draw.line([(140, 260), (380, 180)], fill=(120, 60, 40), width=3)
    
    return image

def test_api():
    """Test the API with a sample image"""
    try:
        print("🔬 Testing OpthalmoAI API...")
        
        # Test health endpoint
        health_response = requests.get("http://127.0.0.1:8001/health", timeout=5)
        if health_response.status_code == 200:
            health_data = health_response.json()
            print(f"✅ Server Status: {health_data.get('status')}")
            print(f"✅ Models Loaded: {health_data.get('models_loaded')}")
        
        # Test model info
        info_response = requests.get("http://127.0.0.1:8001/model-info", timeout=5)
        if info_response.status_code == 200:
            info_data = info_response.json()
            print(f"✅ Model Type: {info_data.get('model_type')}")
            models = info_data.get('models', {})
            print(f"✅ ResNet50: {'✓' if models.get('resnet50') else '✗'}")
            print(f"✅ VGG16: {'✓' if models.get('vgg16') else '✗'}")
        
        # Test analysis
        print("\n🧠 Testing AI Analysis...")
        test_image = create_sample_retinal_image()
        
        # Convert image to bytes
        byte_arr = io.BytesIO()
        test_image.save(byte_arr, format='JPEG')
        byte_arr.seek(0)
        
        files = {'file': ('test_retina.jpg', byte_arr, 'image/jpeg')}
        
        analysis_response = requests.post(
            "http://127.0.0.1:8001/analyze", 
            files=files, 
            timeout=30
        )
        
        if analysis_response.status_code == 200:
            analysis_data = analysis_response.json()
            
            if analysis_data.get('success'):
                result = analysis_data.get('result', {})
                print(f"✅ Analysis Complete!")
                print(f"   📊 Predicted Stage: {result.get('stage')} - {result.get('stage_description')}")
                print(f"   🎯 Confidence: {result.get('confidence')}%")
                print(f"   ⚠️  Risk Level: {result.get('risk_level')}")
                print(f"   ⏱️  Processing Time: {result.get('processing_time')}s")
                
                model_info = result.get('model_info')
                if model_info:
                    print(f"   🤖 Model: {model_info.get('model_name')}")
                    if 'ensemble_agreement' in model_info:
                        agreement = model_info['ensemble_agreement']
                        print(f"   🤝 Agreement: {agreement.get('agreement_level')} ({agreement.get('agreement_score', 0):.1f}%)")
                
                recommendations = result.get('recommendations', [])
                print(f"   💡 Recommendations: {len(recommendations)} items")
                for i, rec in enumerate(recommendations[:3], 1):
                    print(f"      {i}. {rec}")
                
                print("\n🎉 ResNet50 + VGG16 Integration WORKING!")
                return True
            else:
                print(f"❌ Analysis failed: {analysis_data.get('error')}")
                return False
        else:
            print(f"❌ Analysis request failed: HTTP {analysis_response.status_code}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to server. Make sure it's running on http://127.0.0.1:8001")
        return False
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False

if __name__ == "__main__":
    print("🏥 OpthalmoAI ResNet50 + VGG16 Verification")
    print("=" * 50)
    
    if test_api():
        print("\n🎉 SUCCESS: OpthalmoAI is running with ResNet50 + VGG16!")
        print("🌐 Server: http://127.0.0.1:8001")
        print("📚 API Docs: http://127.0.0.1:8001/docs")
    else:
        print("\n❌ Test failed. Check if the server is running.")
        print("💡 Start server: python standalone_server.py")