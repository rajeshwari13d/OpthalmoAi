"""
Test the confidence percentage fix
"""
import requests
from PIL import Image
import io

def test_confidence_fix():
    """Test that confidence is now showing correctly as 87% instead of 8700%"""
    print("🔧 Testing Confidence Percentage Fix")
    print("=" * 45)
    
    try:
        # Create test image
        test_image = Image.new('RGB', (224, 224), color='darkred')
        buffer = io.BytesIO()
        test_image.save(buffer, format='JPEG')
        buffer.seek(0)
        
        # Upload to backend
        files = {'file': ('test_retinal.jpg', buffer, 'image/jpeg')}
        
        print("📤 Testing AI model output...")
        response = requests.post(
            "http://localhost:8004/api/v1/analyze",
            files=files,
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            result = data['result']
            
            confidence = result.get('confidence')
            
            print(f"✅ Response received")
            print(f"📊 Raw confidence value: {confidence}")
            print(f"🧮 Type: {type(confidence)}")
            
            # Test how frontend would display it
            if isinstance(confidence, (int, float)):
                frontend_display = confidence * 100
                print(f"🌐 Frontend will display: {frontend_display}%")
                
                if frontend_display == 87:
                    print("🎉 SUCCESS: Will show 87% (correct!)")
                elif frontend_display == 8700:
                    print("❌ STILL BROKEN: Will show 8700% (wrong!)")
                else:
                    print(f"⚠️  UNEXPECTED: Will show {frontend_display}%")
                
                # Test different scenarios
                print(f"\n📐 Value analysis:")
                print(f"   If confidence = 0.87 → display = {0.87 * 100}% ✅")
                print(f"   If confidence = 87 → display = {87 * 100}% ❌")
                print(f"   Current confidence = {confidence} → display = {confidence * 100}%")
                
            return confidence
        else:
            print(f"❌ Request failed: {response.status_code}")
            return None
            
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return None

if __name__ == "__main__":
    confidence = test_confidence_fix()
    
    print("\n" + "=" * 45)
    print("🎯 FIX VERIFICATION")
    print("=" * 45)
    
    if confidence == 0.87:
        print("✅ FIXED: Backend now sends 0.87")
        print("✅ Frontend will display: 87%")
        print("🎉 Confidence percentage issue resolved!")
    elif confidence == 87:
        print("❌ NOT FIXED: Backend still sends 87")
        print("❌ Frontend will display: 8700%") 
        print("⚠️  Need to fix backend to send 0.87 instead of 87")
    else:
        print(f"🤔 UNEXPECTED: Backend sends {confidence}")
        print("🔍 Need to investigate further")