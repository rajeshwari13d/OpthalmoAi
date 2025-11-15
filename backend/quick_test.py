"""
Quick Model Response Test
Test the model response with the stable backend
"""
import requests
from PIL import Image
import io

def test_model_response():
    print("🧪 Testing Model Response on Port 8007...")
    
    # Create a test image
    img = Image.new('RGB', (512, 512), color=(120, 60, 30))  # Retinal-like color
    
    # Convert to bytes
    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format='JPEG')
    img_byte_arr = img_byte_arr.getvalue()
    
    # Prepare request
    files = {'file': ('test_retina.jpg', img_byte_arr, 'image/jpeg')}
    url = "http://127.0.0.1:8007/api/v1/analyze"
    
    try:
        print(f"Sending image to: {url}")
        response = requests.post(url, files=files, timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            print("✅ SUCCESS! Model is generating output response!")
            
            analysis = data['analysis']
            dr = analysis['diabetic_retinopathy']
            
            print(f"\n📊 Model Response:")
            print(f"Stage: {dr['stage']}")
            print(f"Classification: {dr['stage_name']}")
            print(f"Confidence: {dr['confidence']*100:.1f}%")
            
            print(f"\n🎯 All Class Probabilities:")
            for class_name, prob in analysis['technical_details']['all_class_probabilities'].items():
                print(f"  {class_name}: {prob:.1f}%")
            
            print(f"\n💡 Recommendations:")
            for rec in analysis['recommendations']:
                print(f"  - {rec}")
            
            print("\n🎉 YOUR MODEL IS WORKING CORRECTLY!")
            return True
        else:
            print(f"❌ Error: {response.status_code}")
            print(response.text)
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    test_model_response()