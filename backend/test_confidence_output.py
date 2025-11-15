"""
Test AI Model Output Format - Check Confidence Percentage Issue
"""
import requests
from PIL import Image
import io

def test_ai_confidence_output():
    """Test AI model confidence output to check for percentage issues"""
    print("🔍 Testing AI Model Confidence Output")
    print("=" * 50)
    
    try:
        # Create test retinal image
        test_image = Image.new('RGB', (224, 224), color='darkred')
        buffer = io.BytesIO()
        test_image.save(buffer, format='JPEG')
        buffer.seek(0)
        
        # Upload to backend
        files = {'file': ('test_retinal.jpg', buffer, 'image/jpeg')}
        
        print("📤 Uploading test image...")
        response = requests.post(
            "http://localhost:8004/api/v1/analyze",
            files=files,
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Response received")
            
            # Check the exact format
            print("\n📊 Full Response Structure:")
            print(f"   Keys: {list(data.keys())}")
            
            if 'result' in data:
                result = data['result']
                print(f"\n🎯 Result Keys: {list(result.keys())}")
                
                confidence = result.get('confidence', 'N/A')
                stage = result.get('stage', 'N/A')
                risk = result.get('riskLevel', 'N/A')
                
                print(f"\n📈 Confidence Analysis:")
                print(f"   Raw confidence value: {confidence}")
                print(f"   Type: {type(confidence)}")
                
                # Check if it's a percentage issue
                if isinstance(confidence, (int, float)):
                    print(f"   As integer: {int(confidence)}")
                    print(f"   As percentage: {confidence}%")
                    print(f"   Divided by 100: {confidence/100}")
                    
                    # Check if it should be displayed differently
                    if confidence > 100:
                        print(f"   ⚠️  WARNING: Confidence > 100% ({confidence})")
                        print(f"   🔧 Corrected: {confidence/100}% or {confidence/1000}%")
                    elif confidence < 1:
                        print(f"   ⚠️  WARNING: Confidence < 1% ({confidence})")
                        print(f"   🔧 Corrected: {confidence*100}%")
                    else:
                        print(f"   ✅ Confidence looks normal: {confidence}%")
                
                print(f"\n🎯 Other Analysis Values:")
                print(f"   DR Stage: {stage}")
                print(f"   Risk Level: {risk}")
                
            # Check raw response
            print(f"\n📄 Raw JSON Response:")
            import json
            print(json.dumps(data, indent=2))
            
            return data
        else:
            print(f"❌ Request failed: {response.status_code}")
            print(f"Response: {response.text}")
            return None
            
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return None

def check_backend_source():
    """Check the backend source code for confidence calculation"""
    print("\n🔍 Checking Backend Source Code...")
    
    try:
        with open('simple_backend.py', 'r') as f:
            content = f.read()
        
        # Look for confidence-related code
        lines = content.split('\n')
        confidence_lines = []
        
        for i, line in enumerate(lines, 1):
            if 'confidence' in line.lower():
                confidence_lines.append(f"Line {i}: {line.strip()}")
        
        if confidence_lines:
            print("📋 Confidence-related code found:")
            for line in confidence_lines:
                print(f"   {line}")
        else:
            print("❌ No confidence-related code found")
            
    except Exception as e:
        print(f"❌ Could not read backend source: {e}")

def main():
    """Run confidence output test"""
    # Test current output
    result = test_ai_confidence_output()
    
    # Check source code
    check_backend_source()
    
    # Analysis
    print("\n" + "=" * 50)
    print("🎯 CONFIDENCE OUTPUT ANALYSIS")
    print("=" * 50)
    
    if result and 'result' in result:
        confidence = result['result'].get('confidence')
        
        if confidence == 87:
            print("✅ Confidence shows as 87% - This is normal")
        elif confidence == 8700:
            print("❌ Confidence shows as 8700% - This is wrong!")
            print("🔧 Fix needed: Divide by 100 or adjust calculation")
        elif confidence == 0.87:
            print("⚠️  Confidence shows as 0.87 - Needs *100 for percentage")
        else:
            print(f"🔍 Confidence shows as {confidence} - Check if this is correct")

if __name__ == "__main__":
    main()