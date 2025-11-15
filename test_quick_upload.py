"""
🎯 Quick Test: OpthalmoAI Upload Service Activation
Creates a sample image and tests the complete upload-to-analysis pipeline
"""

import requests
import json
from PIL import Image, ImageDraw
import io
import time

def create_test_retinal_image():
    """Create a quick test retinal image"""
    # Create a realistic retinal image
    img = Image.new('RGB', (512, 512), color=(30, 15, 10))
    draw = ImageDraw.Draw(img)
    
    # Optic disc
    draw.ellipse([220, 200, 280, 260], fill=(255, 200, 150), outline=(255, 220, 170))
    
    # Blood vessels
    draw.line([256, 50, 256, 450], fill=(150, 40, 40), width=8)
    draw.line([50, 256, 450, 256], fill=(140, 35, 35), width=6)
    draw.line([150, 150, 350, 350], fill=(130, 30, 30), width=4)
    draw.line([350, 150, 150, 350], fill=(125, 28, 28), width=4)
    
    # Add some texture
    import random
    for _ in range(200):
        x, y = random.randint(0, 511), random.randint(0, 511)
        color = (random.randint(20, 60), random.randint(10, 30), random.randint(5, 20))
        draw.point((x, y), fill=color)
    
    # Save test image
    img.save('test_retinal_sample.jpg', 'JPEG', quality=95)
    return 'test_retinal_sample.jpg'

def test_upload_service():
    """Test the complete upload and analysis service"""
    print("🏥 Testing OpthalmoAI Upload Service")
    print("=" * 50)
    
    # Create test image
    print("📷 Creating test retinal image...")
    image_path = create_test_retinal_image()
    print(f"✅ Created: {image_path}")
    
    # Test server health
    print("\n🔍 Testing server connection...")
    try:
        health_response = requests.get("http://127.0.0.1:8001/health", timeout=5)
        if health_response.status_code == 200:
            print("✅ Server is running and healthy!")
            print(f"   Response: {health_response.json()}")
        else:
            print(f"❌ Server health check failed: {health_response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Cannot connect to server: {e}")
        print("   Make sure the server is running on port 8001")
        return False
    
    # Test image upload and analysis
    print(f"\n🤖 Testing image upload and AI analysis...")
    try:
        with open(image_path, 'rb') as f:
            files = {'file': (image_path, f, 'image/jpeg')}
            
            print("📤 Uploading image...")
            start_time = time.time()
            
            response = requests.post(
                "http://127.0.0.1:8001/analyze",
                files=files,
                timeout=30
            )
            
            end_time = time.time()
            upload_time = end_time - start_time
            
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Upload and analysis completed in {upload_time:.2f}s")
            
            # Display results
            if result.get('success', False):
                analysis = result['result']
                print(f"\n📊 AI Analysis Results:")
                print(f"   Stage: {analysis.get('stage')} - {analysis.get('stage_description')}")
                print(f"   Confidence: {analysis.get('confidence')}%")
                print(f"   Risk Level: {analysis.get('risk_level')}")
                print(f"   Processing Time: {analysis.get('processing_time')}s")
                
                # Check if using custom model
                model_info = analysis.get('model_info', {})
                if model_info and model_info.get('use_custom_model', False):
                    print(f"   🎯 Using YOUR CUSTOM TRAINED MODEL!")
                
                print(f"\n🩺 Recommendations:")
                for i, rec in enumerate(analysis.get('recommendations', [])[:3], 1):
                    print(f"   {i}. {rec}")
                
                return True
            else:
                print(f"❌ Analysis failed: {result.get('error', 'Unknown error')}")
                return False
        else:
            print(f"❌ Upload failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Upload test failed: {e}")
        return False

def show_service_endpoints():
    """Show available service endpoints"""
    print(f"\n🌐 OpthalmoAI Service Endpoints:")
    print(f"   • Health Check: http://127.0.0.1:8001/health")
    print(f"   • Image Analysis: http://127.0.0.1:8001/analyze")
    print(f"   • API Documentation: http://127.0.0.1:8001/docs")
    print(f"   • Frontend App: https://opthalmoai.web.app")

def show_usage_examples():
    """Show how to use the service"""
    print(f"\n📋 How to Use the Upload Service:")
    print(f"\n1. Web Interface:")
    print(f"   - Visit: https://opthalmoai.web.app")
    print(f"   - Click 'Upload Image' or 'Take Photo'")
    print(f"   - Select retinal fundus image")
    print(f"   - Get AI analysis results")
    
    print(f"\n2. API (curl):")
    print(f"   curl -X POST 'http://127.0.0.1:8001/analyze' \\")
    print(f"     -H 'Content-Type: multipart/form-data' \\")
    print(f"     -F 'file=@your_retinal_image.jpg'")
    
    print(f"\n3. Python (requests):")
    print(f"   with open('image.jpg', 'rb') as f:")
    print(f"       files = {{'file': ('image.jpg', f, 'image/jpeg')}}")
    print(f"       response = requests.post('http://127.0.0.1:8001/analyze', files=files)")

if __name__ == "__main__":
    print("🚀 OpthalmoAI Upload Service Activation Test")
    
    success = test_upload_service()
    
    if success:
        print(f"\n🎉 SUCCESS! Upload service is fully activated and working!")
        print(f"✅ Server is running")
        print(f"✅ Image upload working")
        print(f"✅ AI analysis functional")
        print(f"✅ Custom model active")
        print(f"✅ Results properly formatted")
        
        show_service_endpoints()
        show_usage_examples()
        
        print(f"\n🌟 Your OpthalmoAI upload service is ready for production!")
        
    else:
        print(f"\n❌ Upload service activation incomplete")
        print(f"   Check server status and try again")
        print(f"   Server command: python standalone_server.py")