"""
Test API Upload with Real Image
Test the complete image upload and analysis pipeline
"""
import requests
from PIL import Image
import io
import base64

# Create test image
def create_test_image():
    # Create a test retinal-like image
    img = Image.new('RGB', (512, 512))
    # Add some simple patterns that might look like a fundus image
    pixels = []
    for y in range(512):
        for x in range(512):
            # Create a circular pattern with some variation
            center_x, center_y = 256, 256
            distance = ((x - center_x) ** 2 + (y - center_y) ** 2) ** 0.5
            
            if distance < 200:
                # Inner retina area
                r = int(120 + (distance / 200) * 80)
                g = int(60 + (distance / 200) * 40) 
                b = int(20 + (distance / 200) * 30)
            else:
                # Outer area
                r = g = b = 20
                
            pixels.extend([r, g, b])
    
    # Convert to bytes
    img.putdata([(pixels[i], pixels[i+1], pixels[i+2]) for i in range(0, len(pixels), 3)])
    return img

def test_upload_api():
    """Test the upload API with real image"""
    print("🧪 Testing Image Upload API...")
    
    # Create test image
    test_image = create_test_image()
    print(f"Created test image: {test_image.size}")
    
    # Convert to bytes
    img_byte_arr = io.BytesIO()
    test_image.save(img_byte_arr, format='PNG')
    img_byte_arr = img_byte_arr.getvalue()
    
    print(f"Image size: {len(img_byte_arr)} bytes")
    
    # Prepare multipart form data
    files = {
        'file': ('test_retina.png', img_byte_arr, 'image/png')
    }
    
    # API endpoint
    url = "http://127.0.0.1:8006/api/v1/analyze"
    
    try:
        print(f"Sending POST request to: {url}")
        response = requests.post(url, files=files, timeout=30)
        
        print(f"Response status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Upload successful!")
            print(f"Success: {data.get('success')}")
            print(f"Message: {data.get('message')}")
            
            if 'analysis' in data:
                analysis = data['analysis']
                print("\n📊 Analysis Results:")
                
                # DR Results
                if 'diabetic_retinopathy' in analysis:
                    dr = analysis['diabetic_retinopathy']
                    print(f"Stage: {dr.get('stage')}")
                    print(f"Stage Name: {dr.get('stage_name')}")
                    print(f"Confidence: {dr.get('confidence', 0) * 100:.1f}%")
                    print(f"Description: {dr.get('description')}")
                
                # Technical Details
                if 'technical_details' in analysis:
                    tech = analysis['technical_details']
                    print(f"\n🔧 Technical Details:")
                    print(f"Model: {tech.get('model_version')}")
                    print(f"Processing time: {tech.get('processing_time')}")
                    if 'all_class_probabilities' in tech:
                        print("Class Probabilities:")
                        for class_name, prob in tech['all_class_probabilities'].items():
                            print(f"  {class_name}: {prob:.1f}%")
                
                # Recommendations
                if 'recommendations' in analysis:
                    print(f"\n💡 Recommendations:")
                    for rec in analysis['recommendations']:
                        print(f"  - {rec}")
        else:
            print(f"❌ Upload failed: {response.status_code}")
            print(f"Response: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to backend server")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_upload_api()