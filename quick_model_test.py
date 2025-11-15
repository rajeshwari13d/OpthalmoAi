"""
Quick test script for model integration
Tests ResNet50 and VGG16 models individually
"""

import torch
import torch.nn as nn
from torchvision import models, transforms
from PIL import Image, ImageDraw
import numpy as np
import time
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_test_image(width=224, height=224):
    """Create a simple test image"""
    image = Image.new('RGB', (width, height), color=(80, 40, 20))
    draw = ImageDraw.Draw(image)
    
    # Draw a simple circular pattern (simulating retinal structure)
    center = (width//2, height//2)
    for i in range(5):
        radius = 20 + i * 15
        draw.ellipse([center[0]-radius, center[1]-radius,
                      center[0]+radius, center[1]+radius], 
                     outline=(120+i*20, 60+i*10, 40+i*5), width=2)
    
    return image

def test_resnet50():
    """Test ResNet50 model loading and inference"""
    logger.info("Testing ResNet50...")
    
    try:
        # Create model
        model = models.resnet50(pretrained=True)
        model.fc = nn.Sequential(
            nn.Dropout(0.5),
            nn.Linear(model.fc.in_features, 512),
            nn.ReLU(inplace=True),
            nn.Dropout(0.3),
            nn.Linear(512, 5)  # 5 classes for DR
        )
        
        # Set to eval mode
        model.eval()
        
        # Create test transforms
        transform = transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
        ])
        
        # Create test image and preprocess
        test_image = create_test_image()
        input_tensor = transform(test_image).unsqueeze(0)
        
        # Run inference
        start_time = time.time()
        with torch.no_grad():
            outputs = model(input_tensor)
            probabilities = torch.softmax(outputs, dim=1)
            predicted_class = torch.argmax(probabilities, dim=1).item()
            confidence = probabilities[0][predicted_class].item() * 100
        end_time = time.time()
        
        logger.info(f"✅ ResNet50 test passed!")
        logger.info(f"   Predicted class: {predicted_class}")
        logger.info(f"   Confidence: {confidence:.2f}%")
        logger.info(f"   Inference time: {end_time - start_time:.3f}s")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ ResNet50 test failed: {e}")
        return False

def test_vgg16():
    """Test VGG16 model loading and inference"""
    logger.info("Testing VGG16...")
    
    try:
        # Create model
        model = models.vgg16(pretrained=True)
        model.classifier[6] = nn.Sequential(
            nn.Dropout(0.5),
            nn.Linear(model.classifier[6].in_features, 1024),
            nn.ReLU(inplace=True),
            nn.Dropout(0.4),
            nn.Linear(1024, 512),
            nn.ReLU(inplace=True),
            nn.Dropout(0.3),
            nn.Linear(512, 5)  # 5 classes for DR
        )
        
        # Set to eval mode
        model.eval()
        
        # Create test transforms
        transform = transforms.Compose([
            transforms.Resize((256, 256)),
            transforms.CenterCrop(224),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
        ])
        
        # Create test image and preprocess
        test_image = create_test_image()
        input_tensor = transform(test_image).unsqueeze(0)
        
        # Run inference
        start_time = time.time()
        with torch.no_grad():
            outputs = model(input_tensor)
            probabilities = torch.softmax(outputs, dim=1)
            predicted_class = torch.argmax(probabilities, dim=1).item()
            confidence = probabilities[0][predicted_class].item() * 100
        end_time = time.time()
        
        logger.info(f"✅ VGG16 test passed!")
        logger.info(f"   Predicted class: {predicted_class}")
        logger.info(f"   Confidence: {confidence:.2f}%")
        logger.info(f"   Inference time: {end_time - start_time:.3f}s")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ VGG16 test failed: {e}")
        return False

def test_pytorch_installation():
    """Test PyTorch installation and CUDA availability"""
    logger.info("Testing PyTorch installation...")
    
    try:
        logger.info(f"PyTorch version: {torch.__version__}")
        logger.info(f"CUDA available: {torch.cuda.is_available()}")
        if torch.cuda.is_available():
            logger.info(f"CUDA device: {torch.cuda.get_device_name(0)}")
        else:
            logger.info("Using CPU for inference")
        
        # Test basic tensor operations
        x = torch.randn(1, 3, 224, 224)
        logger.info(f"Test tensor created: {x.shape}")
        
        logger.info("✅ PyTorch installation test passed!")
        return True
        
    except Exception as e:
        logger.error(f"❌ PyTorch installation test failed: {e}")
        return False

def main():
    """Run all tests"""
    logger.info("🔬 Starting Model Integration Quick Test")
    logger.info("=" * 50)
    
    # Check PyTorch installation
    pytorch_ok = test_pytorch_installation()
    if not pytorch_ok:
        logger.error("PyTorch installation issues detected!")
        return False
    
    # Test models
    resnet_ok = test_resnet50()
    vgg_ok = test_vgg16()
    
    logger.info("=" * 50)
    logger.info("📊 TEST RESULTS:")
    logger.info(f"   PyTorch: {'✅ PASSED' if pytorch_ok else '❌ FAILED'}")
    logger.info(f"   ResNet50: {'✅ PASSED' if resnet_ok else '❌ FAILED'}")
    logger.info(f"   VGG16: {'✅ PASSED' if vgg_ok else '❌ FAILED'}")
    
    all_passed = pytorch_ok and resnet_ok and vgg_ok
    
    if all_passed:
        logger.info("\n🎉 All basic tests passed!")
        logger.info("✅ Models are ready for integration")
        logger.info("\n🚀 NEXT STEPS:")
        logger.info("1. Start the FastAPI backend server")
        logger.info("2. Test the complete API integration")
        logger.info("3. Train models on real diabetic retinopathy data")
    else:
        logger.error("\n⚠️  Some tests failed. Check the errors above.")
    
    return all_passed

if __name__ == "__main__":
    import sys
    success = main()
    sys.exit(0 if success else 1)