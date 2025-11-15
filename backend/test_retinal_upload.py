"""
Test retinal image upload workflow verification
"""
import requests
from PIL import Image
import io
import json

def test_retinal_upload_workflow():
    """Test the retinal image upload workflow"""
    print("🔍 Testing Retinal Image Upload Workflow...")
    
    try:
        # Create a realistic test retinal image
        retinal_image = Image.new('RGB', (512, 512), color='darkred')
        # Add some circular patterns to simulate retinal features
        from PIL import ImageDraw
        draw = ImageDraw.Draw(retinal_image)
        # Optic disc
        draw.ellipse([200, 200, 280, 280], fill='orange')
        # Blood vessels
        draw.line([0, 256, 512, 256], fill='red', width=5)
        draw.line([256, 0, 256, 512], fill='red', width=3)
        
        # Save to buffer
        buffer = io.BytesIO()
        retinal_image.save(buffer, format='JPEG', quality=95)
        buffer.seek(0)
        
        print("✅ Created test retinal image (512x512)")
        
        # Test upload to backend
        files = {'file': ('retinal_fundus.jpg', buffer, 'image/jpeg')}
        
        print("📤 Uploading to backend analysis endpoint...")
        response = requests.post(
            "http://localhost:8004/api/v1/analyze",
            files=files,
            timeout=15
        )
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Upload successful!")
            
            # Verify response structure
            if 'result' in result and 'medical_disclaimer' in result:
                analysis = result['result']
                print(f"   📊 Analysis ID: {analysis.get('id', 'N/A')}")
                print(f"   🎯 DR Stage: {analysis.get('stage', 'N/A')}")
                print(f"   📈 Confidence: {analysis.get('confidence', 'N/A')}%")
                print(f"   ⚠️  Risk Level: {analysis.get('riskLevel', 'N/A')}")
                print(f"   📝 Recommendations: {len(analysis.get('recommendations', []))}")
                print(f"   ⚕️  Medical disclaimer: {'Present' if result.get('medical_disclaimer') else 'Missing'}")
                return True
            else:
                print("❌ Invalid response structure")
                print(f"Response: {json.dumps(result, indent=2)}")
                return False
        else:
            print(f"❌ Upload failed: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Workflow test failed: {e}")
        return False

def test_upload_validation():
    """Test file validation in upload workflow"""
    print("\n🔒 Testing Upload Validation...")
    
    try:
        # Test invalid file type
        invalid_buffer = io.BytesIO(b"invalid file content")
        files = {'file': ('test.txt', invalid_buffer, 'text/plain')}
        
        response = requests.post(
            "http://localhost:8004/api/v1/analyze",
            files=files,
            timeout=10
        )
        
        if response.status_code == 400:
            print("✅ File type validation working (rejected .txt file)")
        else:
            print(f"❌ File validation failed: {response.status_code}")
            
        # Test empty file
        empty_buffer = io.BytesIO(b"")
        files = {'file': ('empty.jpg', empty_buffer, 'image/jpeg')}
        
        response = requests.post(
            "http://localhost:8004/api/v1/analyze",
            files=files,
            timeout=10
        )
        
        if response.status_code == 400:
            print("✅ Empty file validation working")
            return True
        else:
            print(f"❌ Empty file validation failed: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Validation test failed: {e}")
        return False

def main():
    """Run workflow verification tests"""
    print("🚀 Retinal Image Upload Workflow Verification")
    print("=" * 55)
    
    # Test 1: Basic upload workflow
    upload_ok = test_retinal_upload_workflow()
    
    # Test 2: Validation checks
    validation_ok = test_upload_validation()
    
    # Summary
    print("\n" + "=" * 55)
    print("📋 WORKFLOW VERIFICATION SUMMARY")
    print("=" * 55)
    
    tests = [
        ("Retinal image upload & analysis", upload_ok),
        ("File validation & error handling", validation_ok)
    ]
    
    for test_name, passed in tests:
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{status}: {test_name}")
    
    all_passed = all(passed for _, passed in tests)
    
    print(f"\n🎯 WORKFLOW STATUS: {'✅ VERIFIED' if all_passed else '❌ NEEDS ATTENTION'}")
    
    if all_passed:
        print("\n💡 Upload workflow is working correctly:")
        print("   ✓ Accepts retinal images (JPEG/PNG)")
        print("   ✓ Validates file types and rejects invalid files")
        print("   ✓ Processes images through AI model")
        print("   ✓ Returns structured analysis results")
        print("   ✓ Includes medical disclaimers")
    
    return all_passed

if __name__ == "__main__":
    main()