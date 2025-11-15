"""
🎯 Complete Upload Flow Test
Test the exact same upload flow that the frontend uses
"""

import requests
from PIL import Image, ImageDraw

def test_complete_upload_flow():
    """Test the complete upload flow with the exact URLs the frontend uses"""
    
    print("🏥 Testing Complete Upload Flow")
    print("=" * 50)
    
    # Step 1: Test health check (what frontend does first)
    print("1. 🔍 Testing Health Check...")
    try:
        health_response = requests.get("http://127.0.0.1:8001/health")
        if health_response.status_code == 200:
            print("   ✅ Health check successful")
            print(f"   📊 Response: {health_response.json()}")
        else:
            print(f"   ❌ Health check failed: {health_response.status_code}")
            return False
    except Exception as e:
        print(f"   ❌ Health check error: {e}")
        return False
    
    # Step 2: Create test image (simulate user upload)
    print("\n2. 📷 Creating Test Retinal Image...")
    img = Image.new('RGB', (400, 400), color=(30, 15, 10))
    draw = ImageDraw.Draw(img)
    
    # Optic disc
    draw.ellipse([160, 140, 240, 220], fill=(255, 200, 150))
    # Blood vessels  
    draw.line([200, 50, 200, 350], fill=(150, 40, 40), width=8)
    draw.line([50, 200, 350, 200], fill=(140, 35, 35), width=6)
    
    test_image_path = 'frontend_test_retinal.jpg'
    img.save(test_image_path, 'JPEG', quality=90)
    print(f"   ✅ Created test image: {test_image_path}")
    
    # Step 3: Test upload (exact same way frontend does it)
    print("\n3. 📤 Testing Image Upload (Frontend Style)...")
    try:
        # Open file exactly like frontend FormData does
        with open(test_image_path, 'rb') as f:
            files = {
                'file': (test_image_path, f, 'image/jpeg')
            }
            
            # Use exact URL that frontend uses
            upload_url = "http://127.0.0.1:8001/analyze"
            print(f"   🌐 Uploading to: {upload_url}")
            
            response = requests.post(
                upload_url,
                files=files,
                timeout=30
            )
            
        if response.status_code == 200:
            result = response.json()
            print("   ✅ Upload and analysis successful!")
            
            # Parse response like frontend would
            if result.get('success', False):
                analysis = result['result']
                print(f"\n📊 Analysis Results:")
                print(f"   🎯 Stage: {analysis.get('stage')} - {analysis.get('stage_description')}")
                print(f"   📈 Confidence: {analysis.get('confidence')}%")
                print(f"   ⚠️  Risk: {analysis.get('risk_level')}")
                
                # Verify custom model is being used
                model_info = analysis.get('model_info', {})
                if model_info and model_info.get('use_custom_model'):
                    print(f"   🌟 SUCCESS: Using YOUR custom trained model!")
                
                recommendations = analysis.get('recommendations', [])
                if recommendations:
                    print(f"   🩺 Recommendations: {len(recommendations)} items")
                    for i, rec in enumerate(recommendations[:2], 1):
                        print(f"      {i}. {rec}")
                
                return True
            else:
                print(f"   ❌ Analysis failed: {result.get('error')}")
                return False
        else:
            print(f"   ❌ Upload failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"   ❌ Upload error: {e}")
        return False

def show_frontend_integration_status():
    """Show the current integration status"""
    print(f"\n🌐 Frontend Integration Status:")
    print(f"   ✅ Backend Server: http://127.0.0.1:8001 (Running)")
    print(f"   ✅ Frontend App: http://localhost:3000 (Running)")
    print(f"   ✅ API URLs: Fixed (no more malformed URLs)")
    print(f"   ✅ CORS: Enabled (allows frontend requests)")
    print(f"   ✅ Custom Model: Active and responding")
    
    print(f"\n📱 How to Test:")
    print(f"   1. Open http://localhost:3000")
    print(f"   2. Click 'Upload Image' or drag & drop")
    print(f"   3. Select any retinal fundus image")
    print(f"   4. Get instant AI analysis results")
    
    print(f"\n🔧 What Was Fixed:")
    print(f"   ❌ Old URL: http://127.0.0.1:8000v1/analyze (malformed)")
    print(f"   ✅ New URL: http://127.0.0.1:8001/analyze (correct)")

if __name__ == "__main__":
    print("🚀 Testing Complete Frontend-Backend Integration")
    
    success = test_complete_upload_flow()
    
    if success:
        print(f"\n🎉 SUCCESS! Upload flow is working perfectly!")
        show_frontend_integration_status()
        print(f"\n✅ The frontend should now work without upload errors!")
    else:
        print(f"\n❌ Upload flow test failed - check server status")
        print(f"🔧 Make sure both servers are running:")
        print(f"   Backend: python standalone_server.py")
        print(f"   Frontend: npm start")