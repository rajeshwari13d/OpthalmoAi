"""
🏥 OpthalmoAI - Complete Retinal Image Analysis Demonstration
This script demonstrates the complete workflow from image upload to results display
"""

import requests
import json
import time
from PIL import Image
import io
import base64
import os

# Server configuration
SERVER_URL = "http://127.0.0.1:8001"
FRONTEND_URL = "https://opthalmoai.web.app"

def create_sample_retinal_image():
    """Create a sample retinal image for testing"""
    # Create a sample 512x512 image that simulates a retinal fundus image
    from PIL import Image, ImageDraw
    import numpy as np
    
    # Create base image with dark background (simulating eye fundus)
    img = Image.new('RGB', (512, 512), color=(20, 10, 10))
    draw = ImageDraw.Draw(img)
    
    # Draw optic disc (bright circular area)
    draw.ellipse([200, 180, 280, 260], fill=(255, 200, 150), outline=(255, 255, 200))
    
    # Draw blood vessels (reddish lines)
    draw.line([256, 100, 256, 400], fill=(150, 50, 50), width=8)
    draw.line([100, 256, 400, 256], fill=(140, 45, 45), width=6)
    draw.line([150, 150, 350, 350], fill=(130, 40, 40), width=4)
    draw.line([150, 350, 350, 150], fill=(125, 38, 38), width=4)
    
    # Add some texture for realism
    pixels = np.array(img)
    noise = np.random.normal(0, 10, pixels.shape).astype(np.int16)
    pixels = np.clip(pixels.astype(np.int16) + noise, 0, 255).astype(np.uint8)
    img = Image.fromarray(pixels)
    
    # Save the sample image
    sample_path = "sample_retinal_image.jpg"
    img.save(sample_path, "JPEG", quality=95)
    print(f"✅ Created sample retinal image: {sample_path}")
    return sample_path

def test_server_health():
    """Test if the OpthalmoAI server is running"""
    try:
        response = requests.get(f"{SERVER_URL}/health", timeout=5)
        if response.status_code == 200:
            health_data = response.json()
            print("✅ Server is running!")
            print(f"   Status: {health_data.get('status', 'Unknown')}")
            print(f"   Models: {health_data.get('models_loaded', 'Unknown')}")
            return True
        else:
            print(f"❌ Server responded with status: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Server not reachable: {e}")
        return False

def upload_and_analyze_image(image_path):
    """Upload retinal image and get AI analysis"""
    print(f"\n🔍 Analyzing retinal image: {image_path}")
    
    try:
        # Prepare the image file for upload
        with open(image_path, 'rb') as f:
            files = {'file': (image_path, f, 'image/jpeg')}
            
            # Send image for analysis
            print("📤 Uploading image to AI model...")
            response = requests.post(
                f"{SERVER_URL}/analyze", 
                files=files,
                timeout=30
            )
        
        if response.status_code == 200:
            analysis_result = response.json()
            display_analysis_results(analysis_result)
            return analysis_result
        else:
            print(f"❌ Analysis failed with status: {response.status_code}")
            print(f"   Error: {response.text}")
            return None
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Upload failed: {e}")
        return None

def display_analysis_results(result):
    """Display the AI analysis results in a formatted way"""
    print("\n" + "="*60)
    print("🏥 OPTHALMO AI - RETINAL ANALYSIS REPORT")
    print("="*60)
    
    # Basic diagnosis info
    stage = result.get('stage', 'Unknown')
    stage_desc = result.get('stage_description', 'Unknown')
    confidence = result.get('confidence', 0)
    risk_level = result.get('risk_level', 'Unknown')
    
    print(f"\n📊 DIAGNOSIS:")
    print(f"   Stage: {stage} - {stage_desc}")
    print(f"   Confidence: {confidence}%")
    print(f"   Risk Level: {risk_level}")
    
    # Processing info
    processing_time = result.get('processing_time', 0)
    model_info = result.get('model_info', {})
    model_name = model_info.get('model_name', 'Unknown')
    
    print(f"\n🤖 AI MODEL INFO:")
    print(f"   Model: {model_name}")
    print(f"   Processing Time: {processing_time}s")
    
    # Check if using custom trained model
    if model_info.get('use_custom_model', False):
        print(f"   🎯 Using YOUR TRAINED MODEL!")
        model_path = model_info.get('model_path', 'Unknown')
        print(f"   Model Path: {model_path}")
    else:
        print(f"   📋 Using Ensemble Models (ResNet50 + VGG16)")
    
    # Clinical recommendations
    recommendations = result.get('recommendations', [])
    print(f"\n🩺 CLINICAL RECOMMENDATIONS:")
    for i, rec in enumerate(recommendations, 1):
        print(f"   {i}. {rec}")
    
    # Urgency assessment
    if risk_level == "HIGH" or stage >= 3:
        print(f"\n🚨 URGENT ATTENTION REQUIRED")
        print(f"   This case requires immediate ophthalmological consultation!")
    elif risk_level == "MODERATE":
        print(f"\n⚠️  MONITORING RECOMMENDED")
        print(f"   Regular follow-up appointments advised.")
    else:
        print(f"\n✅ ROUTINE MONITORING")
        print(f"   Continue regular eye care routine.")
    
    print("\n" + "="*60)
    print("📋 MEDICAL DISCLAIMER:")
    print("This AI analysis is for screening purposes only and should not")
    print("replace professional medical diagnosis. Please consult with a")
    print("qualified ophthalmologist for definitive diagnosis and treatment.")
    print("="*60)

def demonstrate_complete_workflow():
    """Demonstrate the complete retinal image analysis workflow"""
    print("🏥 OpthalmoAI - Complete Retinal Image Analysis Demo")
    print("="*55)
    
    # Step 1: Check server health
    print("\n📡 Step 1: Checking server status...")
    if not test_server_health():
        print("❌ Server not available. Please start the server first:")
        print("   python standalone_server.py")
        return
    
    # Step 2: Create or use sample image
    print("\n🖼️  Step 2: Preparing retinal image...")
    if not os.path.exists("sample_retinal_image.jpg"):
        image_path = create_sample_retinal_image()
    else:
        image_path = "sample_retinal_image.jpg"
        print(f"✅ Using existing sample: {image_path}")
    
    # Step 3: Upload and analyze
    print("\n🤖 Step 3: AI Analysis...")
    result = upload_and_analyze_image(image_path)
    
    if result:
        # Step 4: Show access points
        print(f"\n🌐 Step 4: Access Points:")
        print(f"   • API Documentation: {SERVER_URL}/docs")
        print(f"   • Frontend Application: {FRONTEND_URL}")
        print(f"   • Health Check: {SERVER_URL}/health")
        
        # Step 5: Usage instructions
        print(f"\n📱 Step 5: How to Use:")
        print(f"   1. Open frontend: {FRONTEND_URL}")
        print(f"   2. Click 'Upload Image' or 'Take Photo'")
        print(f"   3. Select/capture retinal fundus image")
        print(f"   4. Wait for AI analysis (2-5 seconds)")
        print(f"   5. View results and recommendations")
        print(f"   6. Download/print report if needed")
        
        print(f"\n✅ Demo completed successfully!")
        print(f"📊 Your OpthalmoAI system is fully operational!")
    else:
        print("❌ Demo failed - check server logs for issues")

def show_api_endpoints():
    """Display available API endpoints"""
    print("\n🔌 Available API Endpoints:")
    print("-" * 40)
    
    endpoints = [
        ("POST", "/analyze", "Upload retinal image for AI analysis"),
        ("GET", "/health", "Check server and model status"),
        ("GET", "/docs", "Interactive API documentation"),
        ("GET", "/openapi.json", "OpenAPI specification")
    ]
    
    for method, endpoint, description in endpoints:
        print(f"   {method:4} {endpoint:15} - {description}")
    
    print(f"\n🌐 Base URL: {SERVER_URL}")
    print(f"📚 Full docs: {SERVER_URL}/docs")

if __name__ == "__main__":
    print("🚀 Starting OpthalmoAI Complete Demo...")
    
    # Show API endpoints first
    show_api_endpoints()
    
    # Run the complete demonstration
    demonstrate_complete_workflow()
    
    print(f"\n🎯 Next Steps:")
    print(f"   • Test with your own retinal images")
    print(f"   • Integrate your trained model (see integration guide)")
    print(f"   • Use the web interface for easier uploads")
    print(f"   • Customize recommendations for your use case")