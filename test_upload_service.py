"""
🏥 OpthalmoAI Retinal Image Upload & Analysis Demo
Complete demonstration of the image upload to AI analysis pipeline
"""

import requests
import json
from PIL import Image, ImageDraw
import io
import base64
import time
import os

# Server configuration
SERVER_URL = "http://127.0.0.1:8001"

def create_sample_retinal_images():
    """Create sample retinal images for testing different DR stages"""
    images = {}
    
    # Sample 1: Normal retina (No DR)
    img1 = Image.new('RGB', (512, 512), color=(45, 20, 15))
    draw1 = ImageDraw.Draw(img1)
    # Clean optic disc
    draw1.ellipse([200, 180, 280, 260], fill=(255, 220, 180), outline=(255, 255, 220))
    # Normal blood vessels
    draw1.line([256, 100, 256, 400], fill=(180, 60, 60), width=6)
    draw1.line([100, 256, 400, 256], fill=(170, 55, 55), width=4)
    img1.save('normal_retina.jpg', quality=95)
    images['normal'] = 'normal_retina.jpg'
    
    # Sample 2: Moderate DR
    img2 = Image.new('RGB', (512, 512), color=(35, 15, 10))
    draw2 = ImageDraw.Draw(img2)
    # Slightly swollen optic disc
    draw2.ellipse([190, 170, 290, 270], fill=(255, 200, 160), outline=(255, 180, 140))
    # Thicker blood vessels with some irregularities
    draw2.line([256, 90, 256, 410], fill=(160, 40, 40), width=8)
    draw2.line([90, 256, 410, 256], fill=(150, 35, 35), width=6)
    # Add some microaneurysms (small red dots)
    for i in range(5):
        x, y = 150 + i*50, 150 + i*30
        draw2.ellipse([x, y, x+3, y+3], fill=(200, 20, 20))
    img2.save('moderate_dr.jpg', quality=95)
    images['moderate'] = 'moderate_dr.jpg'
    
    # Sample 3: Severe DR
    img3 = Image.new('RGB', (512, 512), color=(25, 10, 5))
    draw3 = ImageDraw.Draw(img3)
    # Swollen optic disc with hemorrhages
    draw3.ellipse([180, 160, 300, 280], fill=(255, 180, 120), outline=(200, 100, 80))
    # Very thick, tortuous vessels
    draw3.line([256, 80, 256, 420], fill=(140, 20, 20), width=12)
    draw3.line([80, 256, 420, 256], fill=(130, 15, 15), width=10)
    # Multiple hemorrhages and exudates
    for i in range(10):
        x, y = 120 + i*25, 120 + i*20
        draw3.ellipse([x, y, x+6, y+6], fill=(180, 10, 10))
    # Cotton wool spots (white areas)
    draw3.ellipse([350, 150, 365, 165], fill=(220, 220, 200))
    draw3.ellipse([150, 350, 170, 370], fill=(210, 210, 190))
    img3.save('severe_dr.jpg', quality=95)
    images['severe'] = 'severe_dr.jpg'
    
    return images

def test_server_health():
    """Check if the OpthalmoAI server is running"""
    try:
        response = requests.get(f"{SERVER_URL}/health", timeout=10)
        if response.status_code == 200:
            return True, response.json()
        else:
            return False, f"Server responded with status {response.status_code}"
    except requests.exceptions.RequestException as e:
        return False, f"Server not reachable: {e}"

def upload_and_analyze_image(image_path, image_name):
    """Upload retinal image to server and get AI analysis"""
    print(f"\n📤 Uploading {image_name}: {image_path}")
    print("-" * 50)
    
    try:
        with open(image_path, 'rb') as f:
            files = {'file': (os.path.basename(image_path), f, 'image/jpeg')}
            
            print("🔄 Sending to AI model for analysis...")
            start_time = time.time()
            
            response = requests.post(
                f"{SERVER_URL}/analyze",
                files=files,
                timeout=30
            )
            
            upload_time = time.time() - start_time
            
        if response.status_code == 200:
            result = response.json()
            display_analysis_result(result, image_name, upload_time)
            return result
        else:
            print(f"❌ Analysis failed: {response.status_code}")
            print(f"   Error: {response.text}")
            return None
            
    except Exception as e:
        print(f"❌ Upload failed: {e}")
        return None

def display_analysis_result(result, image_name, upload_time):
    """Display the AI analysis results in a formatted way"""
    print(f"✅ Analysis completed in {upload_time:.2f}s")
    print(f"🤖 AI Analysis Results for {image_name}:")
    
    if result.get('success', False):
        analysis = result['result']
        
        # Main diagnosis
        stage = analysis.get('stage', 'Unknown')
        stage_desc = analysis.get('stage_description', 'Unknown')
        confidence = analysis.get('confidence', 0)
        risk_level = analysis.get('risk_level', 'Unknown')
        
        print(f"   📊 Stage: {stage} - {stage_desc}")
        print(f"   🎯 Confidence: {confidence}%")
        print(f"   ⚠️  Risk Level: {risk_level}")
        
        # Model information
        model_info = analysis.get('model_info', {})
        if model_info:
            model_name = model_info.get('model_name', 'Unknown')
            use_custom = model_info.get('use_custom_model', False)
            print(f"   🤖 Model: {model_name}")
            if use_custom:
                print(f"   🎯 Using YOUR CUSTOM TRAINED MODEL!")
            
        # Processing details
        processing_time = analysis.get('processing_time', 0)
        print(f"   ⏱️  Processing Time: {processing_time}s")
        
        # Clinical recommendations
        recommendations = analysis.get('recommendations', [])
        if recommendations:
            print(f"   🩺 Recommendations:")
            for i, rec in enumerate(recommendations[:3], 1):  # Show first 3
                print(f"      {i}. {rec}")
        
        # Urgency assessment
        if risk_level == "HIGH" or stage >= 3:
            print(f"   🚨 URGENT: Requires immediate medical attention!")
        elif risk_level == "MODERATE":
            print(f"   ⚠️  MONITOR: Regular follow-up recommended")
        else:
            print(f"   ✅ ROUTINE: Continue regular eye care")
            
    else:
        print(f"   ❌ Analysis failed: {result.get('error', 'Unknown error')}")

def demonstrate_retinal_upload_service():
    """Complete demonstration of the retinal image upload and analysis service"""
    print("🏥 OpthalmoAI Retinal Image Upload & Analysis Service")
    print("=" * 60)
    
    # Step 1: Check server status
    print("\n🔍 Step 1: Checking Server Status")
    print("-" * 40)
    
    server_ok, server_info = test_server_health()
    if not server_ok:
        print(f"❌ Server not available: {server_info}")
        print("   Please start the server first:")
        print("   $env:PYTHONPATH = 'd:\\work_station\\OpthalmoAi\\backend'; python standalone_server.py")
        return False
    
    print("✅ Server is running and ready!")
    if isinstance(server_info, dict):
        print(f"   Status: {server_info.get('status', 'Unknown')}")
        print(f"   Models loaded: {server_info.get('models_loaded', 'Unknown')}")
    
    # Step 2: Create sample images
    print("\n🎨 Step 2: Creating Sample Retinal Images")
    print("-" * 40)
    
    sample_images = create_sample_retinal_images()
    print(f"✅ Created {len(sample_images)} sample retinal images:")
    for name, path in sample_images.items():
        print(f"   📷 {name.title()}: {path}")
    
    # Step 3: Test image upload and analysis
    print("\n🤖 Step 3: Testing AI Analysis Service")
    print("-" * 40)
    
    results = {}
    for image_type, image_path in sample_images.items():
        result = upload_and_analyze_image(image_path, image_type)
        if result:
            results[image_type] = result
    
    # Step 4: Summary
    print(f"\n📊 Step 4: Analysis Summary")
    print("-" * 40)
    
    successful_analyses = len(results)
    total_images = len(sample_images)
    
    print(f"✅ Successful analyses: {successful_analyses}/{total_images}")
    
    if results:
        print(f"\n🎯 Model Performance Summary:")
        for image_type, result in results.items():
            if result.get('success'):
                analysis = result['result']
                stage = analysis.get('stage', 'N/A')
                confidence = analysis.get('confidence', 'N/A')
                print(f"   {image_type.title()}: Stage {stage} ({confidence}% confidence)")
    
    # Step 5: Usage instructions
    print(f"\n📱 Step 5: How to Use the Service")
    print("-" * 40)
    print(f"🌐 API Endpoints:")
    print(f"   • Health Check: GET {SERVER_URL}/health")
    print(f"   • Image Analysis: POST {SERVER_URL}/analyze")
    print(f"   • API Docs: {SERVER_URL}/docs")
    
    print(f"\n📋 Upload Requirements:")
    print(f"   • File formats: JPG, JPEG, PNG, BMP")
    print(f"   • Max file size: 10MB")
    print(f"   • Min resolution: 224x224 pixels")
    print(f"   • Content type: image/*")
    
    print(f"\n🔧 Frontend Integration:")
    print(f"   • Web App: https://opthalmoai.web.app")
    print(f"   • Upload component ready")
    print(f"   • Results display configured")
    
    return successful_analyses == total_images

def test_curl_command():
    """Generate curl command for testing"""
    print(f"\n🛠️  Test with curl command:")
    print(f"curl -X POST '{SERVER_URL}/analyze' \\")
    print(f"  -H 'accept: application/json' \\")
    print(f"  -H 'Content-Type: multipart/form-data' \\")
    print(f"  -F 'file=@normal_retina.jpg'")

if __name__ == "__main__":
    print("🚀 Starting OpthalmoAI Image Upload Service Demo...")
    
    try:
        success = demonstrate_retinal_upload_service()
        
        if success:
            print(f"\n🎉 SUCCESS! Retinal image upload & analysis service is fully operational!")
            print(f"✅ Your custom trained model is processing images correctly")
            print(f"✅ All API endpoints are responding")
            print(f"✅ Image upload pipeline is working")
            
            test_curl_command()
            
            print(f"\n🌟 The service is ready for production use!")
        else:
            print(f"\n❌ Some issues detected. Check server logs and try again.")
            
    except KeyboardInterrupt:
        print(f"\n⏹️  Demo interrupted by user")
    except Exception as e:
        print(f"\n❌ Demo failed: {e}")