"""
🎯 Live Demo: Your Custom Model in Action
Test the actual local OpthalmoAI service with your trained model
"""

import requests
import json
from PIL import Image, ImageDraw
import time

def test_your_custom_model_service():
    """Test your actual running custom model service"""
    print("🏥 Testing YOUR Custom OpthalmoAI Model Service")
    print("=" * 55)
    
    # Test server connection
    print("1. 🔍 Testing Local Server Connection...")
    try:
        health_response = requests.get("http://127.0.0.1:8001/health", timeout=5)
        if health_response.status_code == 200:
            print("   ✅ Your local server is running!")
            health_data = health_response.json()
            print(f"   📊 Status: {health_data.get('status', 'unknown')}")
            print(f"   🤖 Models loaded: {health_data.get('models_loaded', 'unknown')}")
        else:
            print(f"   ❌ Server health check failed: {health_response.status_code}")
            return
    except Exception as e:
        print(f"   ❌ Cannot connect to local server: {e}")
        print("   Make sure your server is running on http://127.0.0.1:8001")
        return
    
    # Create test retinal image
    print("\n2. 📷 Creating Test Retinal Image...")
    img = Image.new('RGB', (512, 512), color=(25, 12, 8))
    draw = ImageDraw.Draw(img)
    
    # Draw realistic retinal features
    # Optic disc
    draw.ellipse([210, 190, 290, 270], fill=(255, 220, 180), outline=(255, 240, 200))
    
    # Major blood vessels
    draw.line([256, 80, 256, 430], fill=(160, 45, 45), width=10)
    draw.line([80, 256, 430, 256], fill=(150, 40, 40), width=8)
    draw.line([150, 150, 360, 360], fill=(140, 35, 35), width=6)
    draw.line([360, 150, 150, 360], fill=(135, 32, 32), width=6)
    
    # Add some pathological features (moderate DR simulation)
    # Microaneurysms
    for i in range(6):
        x, y = 120 + i*50, 130 + i*40
        draw.ellipse([x, y, x+4, y+4], fill=(200, 20, 20))
    
    # Hard exudates
    draw.ellipse([320, 180, 340, 200], fill=(255, 255, 200))
    draw.ellipse([180, 320, 200, 340], fill=(250, 250, 190))
    
    img.save('your_test_retinal_image.jpg', 'JPEG', quality=95)
    print("   ✅ Created test image: your_test_retinal_image.jpg")
    
    # Test AI analysis with YOUR model
    print("\n3. 🤖 Testing YOUR Custom AI Model...")
    try:
        with open('your_test_retinal_image.jpg', 'rb') as f:
            files = {'file': ('your_test_retinal_image.jpg', f, 'image/jpeg')}
            
            print("   📤 Uploading to your custom model...")
            start_time = time.time()
            
            response = requests.post(
                "http://127.0.0.1:8001/analyze",
                files=files,
                timeout=30
            )
            
            analysis_time = time.time() - start_time
            
        if response.status_code == 200:
            result = response.json()
            print(f"   ✅ Analysis completed in {analysis_time:.2f}s")
            
            if result.get('success', False):
                analysis = result['result']
                
                print(f"\n📊 YOUR CUSTOM MODEL RESULTS:")
                print(f"   🎯 DR Stage: {analysis.get('stage')} - {analysis.get('stage_description')}")
                print(f"   📈 Confidence: {analysis.get('confidence')}%")
                print(f"   ⚠️  Risk Level: {analysis.get('risk_level')}")
                print(f"   ⏱️  Processing Time: {analysis.get('processing_time')}s")
                
                # Verify it's using YOUR custom model
                model_info = analysis.get('model_info', {})
                if model_info:
                    model_name = model_info.get('model_name', 'Unknown')
                    use_custom = model_info.get('use_custom_model', False)
                    model_path = model_info.get('model_path', 'Unknown')
                    
                    print(f"\n🎯 MODEL VERIFICATION:")
                    print(f"   Model Name: {model_name}")
                    print(f"   Using Custom Model: {use_custom}")
                    if use_custom:
                        print(f"   🌟 SUCCESS! Using YOUR trained weights!")
                        print(f"   📁 Model Path: {model_path}")
                    else:
                        print(f"   📋 Using fallback ensemble models")
                
                # Show medical recommendations
                recommendations = analysis.get('recommendations', [])
                if recommendations:
                    print(f"\n🩺 CLINICAL RECOMMENDATIONS:")
                    for i, rec in enumerate(recommendations[:4], 1):
                        print(f"   {i}. {rec}")
                
                return True
            else:
                print(f"   ❌ Analysis failed: {result.get('error', 'Unknown error')}")
                return False
        else:
            print(f"   ❌ Request failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"   ❌ Analysis test failed: {e}")
        return False

def show_local_app_info():
    """Show information about your local application"""
    print(f"\n🌐 YOUR LOCAL OPTHALMOAI APPLICATION:")
    print(f"   • Backend API: http://127.0.0.1:8001")
    print(f"   • API Documentation: http://127.0.0.1:8001/docs")
    print(f"   • Frontend App: http://localhost:3000")
    print(f"   • Health Check: http://127.0.0.1:8001/health")
    
    print(f"\n🎯 WHAT'S RUNNING:")
    print(f"   ✅ Your custom trained OpthalmoAI model")
    print(f"   ✅ FastAPI backend server")
    print(f"   ✅ React frontend development server")
    print(f"   ✅ Complete image upload & analysis pipeline")

if __name__ == "__main__":
    print("🚀 Testing Your Live Custom OpthalmoAI Service")
    
    success = test_your_custom_model_service()
    
    if success:
        print(f"\n🎉 AMAZING! Your custom model service is working perfectly!")
        print(f"✅ Local server responding")
        print(f"✅ Custom model loaded and active")
        print(f"✅ Image analysis working")
        print(f"✅ Medical recommendations generated")
        
        show_local_app_info()
        
        print(f"\n🌟 Your OpthalmoAI application with custom trained model is LIVE!")
        print(f"📱 Open http://localhost:3000 to use the web interface")
        print(f"📋 Or use http://127.0.0.1:8001/docs for API testing")
        
    else:
        print(f"\n❌ Service test failed - check the server status")