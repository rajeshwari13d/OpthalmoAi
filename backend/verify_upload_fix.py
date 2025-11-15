"""
Final Upload Error Fix Verification
Comprehensive test to ensure "Failed to fetch" error is resolved
"""
import requests
from PIL import Image, ImageDraw
import io
import json

def create_realistic_retinal_image():
    """Create a realistic-looking retinal image for testing"""
    # Create base retinal image
    image = Image.new('RGB', (512, 512), color=(139, 0, 0))  # Dark red background
    draw = ImageDraw.Draw(image)
    
    # Add optic disc (bright yellow-orange circle)
    draw.ellipse([200, 200, 280, 280], fill=(255, 165, 0))
    
    # Add macula (central darker area)
    draw.ellipse([240, 240, 270, 270], fill=(139, 69, 19))
    
    # Add blood vessels (red lines)
    draw.line([(256, 100), (256, 400)], fill=(220, 20, 60), width=8)
    draw.line([(100, 256), (400, 256)], fill=(220, 20, 60), width=6)
    draw.line([(150, 150), (350, 350)], fill=(178, 34, 34), width=4)
    draw.line([(350, 150), (150, 350)], fill=(178, 34, 34), width=4)
    
    return image

def test_upload_fix():
    """Test that the upload error is fixed"""
    print("🔧 Testing Upload Error Fix")
    print("=" * 50)
    
    # Test URLs
    test_urls = [
        "http://localhost:8004/api/v1/analyze",
        "http://127.0.0.1:8004/api/v1/analyze"
    ]
    
    for url in test_urls:
        print(f"\n📡 Testing: {url}")
        
        try:
            # Create realistic test image
            retinal_image = create_realistic_retinal_image()
            
            # Convert to bytes
            buffer = io.BytesIO()
            retinal_image.save(buffer, format='JPEG', quality=95)
            buffer.seek(0)
            
            # Prepare upload (mimicking frontend)
            files = {'file': ('retinal_fundus.jpg', buffer, 'image/jpeg')}
            headers = {
                'Origin': 'http://localhost:3000',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            
            print("   📤 Uploading retinal image...")
            response = requests.post(url, files=files, headers=headers, timeout=15)
            
            if response.status_code == 200:
                data = response.json()
                print("   ✅ UPLOAD SUCCESSFUL!")
                
                # Verify response format
                if 'result' in data and 'medical_disclaimer' in data:
                    result = data['result']
                    print(f"      📊 Analysis ID: {result.get('id', 'N/A')}")
                    print(f"      🎯 DR Classification: Stage {result.get('stage', 'N/A')}")
                    print(f"      📈 Confidence: {result.get('confidence', 'N/A')}%")
                    print(f"      ⚠️  Risk Level: {result.get('riskLevel', 'N/A')}")
                    print(f"      📝 Recommendations: {len(result.get('recommendations', []))}")
                    print("      ⚕️  Medical disclaimer: Present")
                    return True
                else:
                    print("   ❌ Invalid response format")
                    print(f"      Response keys: {list(data.keys())}")
                    return False
            else:
                print(f"   ❌ UPLOAD FAILED: HTTP {response.status_code}")
                print(f"      Error: {response.text}")
                return False
                
        except requests.exceptions.ConnectionError:
            print(f"   ❌ CONNECTION ERROR: Cannot reach {url}")
            return False
        except requests.exceptions.Timeout:
            print(f"   ❌ TIMEOUT: Request took too long")
            return False
        except Exception as e:
            print(f"   ❌ UNEXPECTED ERROR: {e}")
            return False

def test_cors_headers():
    """Test CORS headers for frontend compatibility"""
    print("\n🌐 Testing CORS Headers...")
    
    try:
        # Test preflight request
        response = requests.options(
            "http://localhost:8004/api/v1/analyze",
            headers={
                'Origin': 'http://localhost:3000',
                'Access-Control-Request-Method': 'POST',
                'Access-Control-Request-Headers': 'content-type'
            }
        )
        
        cors_headers = {
            'Access-Control-Allow-Origin': response.headers.get('access-control-allow-origin'),
            'Access-Control-Allow-Methods': response.headers.get('access-control-allow-methods'),
            'Access-Control-Allow-Headers': response.headers.get('access-control-allow-headers'),
        }
        
        print(f"   Status: {response.status_code}")
        for header, value in cors_headers.items():
            if value:
                print(f"   ✅ {header}: {value}")
            else:
                print(f"   ❌ {header}: Missing")
        
        return response.status_code == 200
        
    except Exception as e:
        print(f"   ❌ CORS test failed: {e}")
        return False

def test_error_handling():
    """Test error handling for invalid uploads"""
    print("\n🔒 Testing Error Handling...")
    
    test_cases = [
        ("Invalid file type", "test.txt", b"invalid content", "text/plain"),
        ("Empty file", "empty.jpg", b"", "image/jpeg"),
    ]
    
    for test_name, filename, content, content_type in test_cases:
        try:
            buffer = io.BytesIO(content)
            files = {'file': (filename, buffer, content_type)}
            
            response = requests.post(
                "http://localhost:8004/api/v1/analyze",
                files=files,
                headers={'Origin': 'http://localhost:3000'},
                timeout=5
            )
            
            if response.status_code == 400:
                print(f"   ✅ {test_name}: Correctly rejected")
            else:
                print(f"   ❌ {test_name}: Should have been rejected")
                
        except Exception as e:
            print(f"   ⚠️  {test_name}: Error during test - {e}")

def main():
    """Run comprehensive upload fix verification"""
    print("🚀 OpthalmoAI Upload Error Fix Verification")
    print("=" * 60)
    
    # Test 1: Upload functionality
    upload_works = test_upload_fix()
    
    # Test 2: CORS configuration
    cors_works = test_cors_headers()
    
    # Test 3: Error handling
    test_error_handling()
    
    # Final verdict
    print("\n" + "=" * 60)
    print("🏁 UPLOAD FIX VERIFICATION RESULTS")
    print("=" * 60)
    
    if upload_works and cors_works:
        print("🎉 SUCCESS: Upload error has been FIXED!")
        print("")
        print("✅ Backend server responding correctly")
        print("✅ CORS headers properly configured") 
        print("✅ Image upload and analysis working")
        print("✅ Response format matches frontend expectations")
        print("")
        print("🌐 Frontend should now work properly:")
        print("   • Go to http://localhost:3000")
        print("   • Upload a retinal image")
        print("   • Should see analysis results (not 'Failed to fetch')")
        print("")
        print("🔧 Fix applied:")
        print("   • Corrected API URL from port 8000 → 8004")
        print("   • Environment variables updated")
        print("   • Frontend restarted with new configuration")
        
    else:
        print("❌ Upload error still exists")
        if not upload_works:
            print("   • Upload functionality failing")
        if not cors_works:
            print("   • CORS configuration issues")
        print("   • Additional troubleshooting needed")

if __name__ == "__main__":
    main()