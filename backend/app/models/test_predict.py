from app.models.custom_trained_model import get_trained_model_path, get_architecture_path, load_custom_trained_model
from PIL import Image, ImageDraw
import numpy as np

# Create sample retinal image
img = Image.new('RGB', (512,512), color=(20,10,10))
draw = ImageDraw.Draw(img)
draw.ellipse([200,180,280,260], fill=(255,200,150), outline=(255,255,200))
draw.line([256,100,256,400], fill=(150,50,50), width=8)

# Save for reference
img.save('tmp_sample_retinal.jpg')

# Load model
model_wrapper = load_custom_trained_model(get_trained_model_path(), architecture_file=get_architecture_path())
print('Model loaded:', model_wrapper.model_loaded)

# Predict
res = model_wrapper.predict(img)
print('Prediction result:')
print(res)
