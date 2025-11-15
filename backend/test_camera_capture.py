"""
Test camera capture functionality verification
"""
import requests
from PIL import Image
import io
import json

def simulate_camera_capture():
    """Simulate camera capture functionality"""
    print("📸 Testing Camera Capture Simulation...")
    
    try:
        # Simulate a camera-captured retinal image
        # Camera captures are typically lower quality than professional scans
        camera_image = Image.new('RGB', (640, 480), color='maroon')
        
        # Add retinal-like features to simulate camera capture
        from PIL import ImageDraw, ImageFilter
        draw = ImageDraw.Draw(camera_image)
        
        # Simulate optic disc (brighter area)
        draw.ellipse([250, 180, 350, 280], fill='orange')
        
        # Simulate macula (central area)
        draw.ellipse([300, 220, 340, 260], fill='yellow')
        
        # Simulate blood vessels
        draw.line([100, 240, 540, 240], fill='darkred', width=4)
        draw.line([320, 50, 320, 430], fill='darkred', width=3)
        draw.line([200, 150, 440, 330], fill='red', width=2)
        draw.line([440, 150, 200, 330], fill='red', width=2)
        
        # Apply slight blur to simulate camera quality
        camera_image = camera_image.filter(ImageFilter.GaussianBlur(radius=0.5))
        
        print(f"✅ Simulated camera capture: {camera_image.size}, mode: {camera_image.mode}")
        
        return camera_image
        
    except Exception as e:
        print(f"❌ Camera simulation failed: {e}")
        return None

def test_camera_workflow():
    """Test camera capture workflow"""
    print("🔍 Testing Camera Capture Workflow...")
    
    try:
        # Simulate camera capture
        captured_image = simulate_camera_capture()
        if not captured_image:
            return False
        
        # Convert to buffer for upload (simulating frontend behavior)
        buffer = io.BytesIO()
        captured_image.save(buffer, format='JPEG', quality=85)  # Camera quality
        buffer.seek(0)
        
        print("📤 Uploading captured image to backend...")
        
        # Upload to analysis endpoint
        files = {'file': ('camera_capture.jpg', buffer, 'image/jpeg')}
        
        response = requests.post(
            "http://localhost:8004/api/v1/analyze",
            files=files,
            timeout=15
        )
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Camera capture analysis successful!")
            
            # Verify response
            if 'result' in result:
                analysis = result['result']
                print(f"   📊 Analysis ID: {analysis.get('id', 'N/A')}")
                print(f"   🎯 DR Classification: Stage {analysis.get('stage', 'N/A')}")
                print(f"   📈 AI Confidence: {analysis.get('confidence', 'N/A')}%")
                print(f"   ⚠️  Risk Assessment: {analysis.get('riskLevel', 'N/A')}")
                
                recommendations = analysis.get('recommendations', [])
                print(f"   📝 Medical Recommendations: {len(recommendations)}")
                for i, rec in enumerate(recommendations[:2], 1):  # Show first 2
                    print(f"      {i}. {rec}")
                
                return True
            else:
                print("❌ Invalid response structure")
                return False
        else:
            print(f"❌ Camera workflow failed: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Camera workflow test failed: {e}")
        return False

def test_different_image_qualities():
    """Test camera capture with different image qualities"""
    print("\n📱 Testing Different Camera Qualities...")
    
    qualities = [
        ("High Quality", 95, (1024, 768)),
        ("Medium Quality", 75, (640, 480)),
        ("Lower Quality", 50, (320, 240))
    ]
    
    success_count = 0
    
    for quality_name, jpeg_quality, size in qualities:
        try:
            # Create test image of specified size
            test_image = Image.new('RGB', size, color='darkred')
            
            # Add basic retinal features
            from PIL import ImageDraw
            draw = ImageDraw.Draw(test_image)
            center_x, center_y = size[0] // 2, size[1] // 2
            disc_size = min(size) // 8
            draw.ellipse([
                center_x - disc_size, center_y - disc_size,
                center_x + disc_size, center_y + disc_size
            ], fill='orange')
            
            # Save with specified quality
            buffer = io.BytesIO()
            test_image.save(buffer, format='JPEG', quality=jpeg_quality)
            buffer.seek(0)
            
            # Test upload
            files = {'file': (f'{quality_name.lower().replace(" ", "_")}.jpg', buffer, 'image/jpeg')}
            
            response = requests.post(
                "http://localhost:8004/api/v1/analyze",
                files=files,
                timeout=10
            )
            
            if response.status_code == 200:
                print(f"   ✅ {quality_name} ({size[0]}x{size[1]}): Analysis successful")
                success_count += 1
            else:
                print(f"   ❌ {quality_name}: Failed ({response.status_code})")
                
        except Exception as e:
            print(f"   ❌ {quality_name}: Error - {e}")
    
    print(f"\n📊 Quality Test Results: {success_count}/{len(qualities)} passed")
    return success_count == len(qualities)

def main():
    """Run camera capture verification tests"""
    print("📸 Camera Capture Functionality Verification")
    print("=" * 55)
    
    # Test 1: Basic camera workflow
    camera_ok = test_camera_workflow()
    
    # Test 2: Different image qualities
    quality_ok = test_different_image_qualities()
    
    # Summary
    print("\n" + "=" * 55)
    print("📋 CAMERA CAPTURE VERIFICATION SUMMARY")
    print("=" * 55)
    
    tests = [
        ("Camera capture & AI analysis", camera_ok),
        ("Multiple image quality support", quality_ok)
    ]
    
    for test_name, passed in tests:
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{status}: {test_name}")
    
    all_passed = all(passed for _, passed in tests)
    
    print(f"\n🎯 CAMERA STATUS: {'✅ FUNCTIONAL' if all_passed else '❌ NEEDS ATTENTION'}")
    
    if all_passed:
        print("\n📸 Camera capture functionality verified:")
        print("   ✓ Accepts camera-captured images")
        print("   ✓ Handles various image qualities and sizes")
        print("   ✓ AI model processes camera images successfully")
        print("   ✓ Returns diabetic retinopathy analysis")
        print("   ✓ Works with both high and lower quality captures")
    
    return all_passed

if __name__ == "__main__":
    main()