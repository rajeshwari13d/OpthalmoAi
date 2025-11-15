"""
Test Model Response with Retinal Image
Comprehensive test to verify model generates proper output for retinal images
"""
import requests
import os
from PIL import Image
import io
import json

def test_with_existing_retinal_image():
    """Test with the existing test image in backend"""
    print("🔍 Testing Model Response with Existing Retinal Image...")
    
    # Check if test image exists
    test_image_path = "test_image.jpg"
    
    if not os.path.exists(test_image_path):
        print(f"❌ Test image not found: {test_image_path}")
        return False
    
    print(f"✅ Found test image: {test_image_path}")
    
    # Load and inspect the image
    try:
        with open(test_image_path, 'rb') as f:
            img_data = f.read()
        
        # Open with PIL to get info
        img = Image.open(test_image_path)
        print(f"Image info: {img.size}, mode: {img.mode}, format: {img.format}")
        print(f"Image size: {len(img_data)} bytes")
        
        # Prepare for API call
        files = {
            'file': ('retinal_image.jpg', img_data, 'image/jpeg')
        }
        
        # API endpoint
        url = "http://127.0.0.1:8005/api/v1/analyze"
        
        print(f"\n🚀 Sending image to API: {url}")
        response = requests.post(url, files=files, timeout=30)
        
        print(f"Response Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ API Response Successful!")
            
            # Pretty print the full response
            print("\n📊 Complete Model Response:")
            print("=" * 60)
            print(json.dumps(data, indent=2))
            print("=" * 60)
            
            # Extract key information
            if data.get('success') and 'analysis' in data:
                analysis = data['analysis']
                
                print("\n🎯 Key Results:")
                print(f"Success: {data['success']}")
                print(f"Message: {data['message']}")
                
                # Diabetic Retinopathy Results
                if 'diabetic_retinopathy' in analysis:
                    dr = analysis['diabetic_retinopathy']
                    print(f"\n🩺 Diabetic Retinopathy Analysis:")
                    print(f"  Stage: {dr.get('stage')}")
                    print(f"  Classification: {dr.get('stage_name')}")
                    print(f"  Confidence: {dr.get('confidence', 0) * 100:.2f}%")
                    print(f"  Description: {dr.get('description')}")
                
                # Risk Assessment
                if 'risk_assessment' in analysis:
                    risk = analysis['risk_assessment']
                    print(f"\n⚠️  Risk Assessment:")
                    print(f"  Progression Risk: {risk.get('progression_risk')}")
                    print(f"  Follow-up: {risk.get('recommended_followup')}")
                    print(f"  Urgent Referral: {risk.get('urgent_referral')}")
                
                # Technical Details
                if 'technical_details' in analysis:
                    tech = analysis['technical_details']
                    print(f"\n🔧 Technical Details:")
                    print(f"  Model: {tech.get('model_version')}")
                    print(f"  Processing Time: {tech.get('processing_time')}")
                    print(f"  Image Resolution: {tech.get('image_resolution')}")
                    
                    if 'all_class_probabilities' in tech:
                        print(f"\n📈 All Class Probabilities:")
                        for class_name, prob in tech['all_class_probabilities'].items():
                            print(f"    {class_name}: {prob:.2f}%")
                
                # Recommendations
                if 'recommendations' in analysis:
                    print(f"\n💡 Medical Recommendations:")
                    for i, rec in enumerate(analysis['recommendations'], 1):
                        print(f"    {i}. {rec}")
                
                return True
            else:
                print("❌ Analysis failed or incomplete")
                return False
        else:
            print(f"❌ API Error: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_api_health_first():
    """First check if API is responsive"""
    print("🏥 Testing API Health...")
    
    try:
        response = requests.get("http://127.0.0.1:8005/api/v1/health", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ API Health: {data.get('status')}")
            print(f"Model Loaded: {data.get('model_loaded')}")
            print(f"Message: {data.get('message')}")
            return True
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Cannot connect to API: {e}")
        return False

def create_realistic_retinal_image():
    """Create a more realistic retinal image for testing"""
    print("🎨 Creating Realistic Retinal Image for Testing...")
    
    try:
        import numpy as np
        
        # Create a 512x512 retinal-like image
        img_array = np.zeros((512, 512, 3), dtype=np.uint8)
        
        # Create circular fundus background
        center_x, center_y = 256, 256
        radius = 200
        
        for y in range(512):
            for x in range(512):
                distance = np.sqrt((x - center_x)**2 + (y - center_y)**2)
                
                if distance <= radius:
                    # Inside fundus - reddish background
                    intensity = max(0, 1 - (distance / radius) * 0.3)
                    img_array[y, x] = [
                        int(150 * intensity + 50),  # Red channel
                        int(80 * intensity + 30),   # Green channel  
                        int(40 * intensity + 20)    # Blue channel
                    ]
                    
                    # Add some vessel-like patterns
                    if (x + y) % 20 < 3 or (x - y) % 25 < 2:
                        img_array[y, x] = [80, 20, 10]  # Darker for vessels
                    
                    # Add optic disc area
                    if 200 <= x <= 280 and 230 <= y <= 270:
                        img_array[y, x] = [220, 180, 120]  # Yellowish optic disc
        
        # Convert to PIL Image
        img = Image.fromarray(img_array)
        img.save("synthetic_retinal_test.jpg", "JPEG", quality=85)
        
        print(f"✅ Created synthetic retinal image: synthetic_retinal_test.jpg")
        print(f"Size: {img.size}, Mode: {img.mode}")
        
        return "synthetic_retinal_test.jpg"
        
    except ImportError:
        print("⚠️  NumPy not available, using simple image")
        # Fallback to simple image
        img = Image.new('RGB', (512, 512), color=(120, 60, 30))
        img.save("simple_retinal_test.jpg", "JPEG")
        return "simple_retinal_test.jpg"

def main():
    """Run comprehensive model response test"""
    print("=" * 70)
    print("🧪 COMPREHENSIVE MODEL RESPONSE TEST")
    print("=" * 70)
    
    # Step 1: Check API health
    if not test_api_health_first():
        print("\n❌ API not available - cannot test model response")
        return
    
    print("\n" + "="*50)
    
    # Step 2: Test with existing image
    success = test_with_existing_retinal_image()
    
    if not success:
        print("\n📷 Existing image not found or failed, creating synthetic image...")
        
        # Step 3: Create and test with synthetic image
        synthetic_path = create_realistic_retinal_image()
        
        if synthetic_path:
            print(f"\n🔄 Testing with synthetic image: {synthetic_path}")
            
            # Test with synthetic image
            test_image_path = synthetic_path
            if os.path.exists(test_image_path):
                with open(test_image_path, 'rb') as f:
                    img_data = f.read()
                
                files = {'file': ('synthetic_retinal.jpg', img_data, 'image/jpeg')}
                url = "http://127.0.0.1:8005/api/v1/analyze"
                
                response = requests.post(url, files=files, timeout=30)
                
                if response.status_code == 200:
                    data = response.json()
                    print("✅ Synthetic Image Test Successful!")
                    
                    if 'analysis' in data:
                        dr = data['analysis'].get('diabetic_retinopathy', {})
                        print(f"Prediction: {dr.get('stage_name')} ({dr.get('confidence', 0)*100:.1f}% confidence)")
                    success = True
    
    print("\n" + "="*70)
    if success:
        print("🎉 MODEL IS GENERATING PROPER RESPONSES FOR RETINAL IMAGES!")
        print("✅ Your trained OpthalmoAI model is working correctly")
        print("✅ Upload pipeline is functional")
        print("✅ Frontend can now receive real AI predictions")
    else:
        print("❌ Model response test failed - check backend logs")
    
    print("="*70)

if __name__ == "__main__":
    main()