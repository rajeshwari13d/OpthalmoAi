"""
Direct test of the backend models without uvicorn server
Tests the ResNet50 and VGG16 integration directly
"""

import sys
import os
import logging
from pathlib import Path

# Add the backend directory to Python path
backend_dir = Path(__file__).parent / "backend"
sys.path.insert(0, str(backend_dir))

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_direct_import():
    """Test if we can import the modules directly"""
    try:
        from app.models.resnet50_model import ResNet50Predictor, load_resnet50_model
        from app.models.vgg16_model import VGG16Predictor, load_vgg16_model
        from app.models.model_loader import EnsembleModelLoader
        
        logger.info("✅ All model imports successful")
        return True
        
    except Exception as e:
        logger.error(f"❌ Import failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_model_loading():
    """Test if models can be loaded and initialized"""
    try:
        from app.models.model_loader import EnsembleModelLoader
        
        # Create ensemble loader
        loader = EnsembleModelLoader()
        
        # Load models
        loader.load_models()
        
        logger.info(f"✅ Models loaded successfully")
        logger.info(f"   ResNet50: {'✓' if loader.resnet50_model else '✗'}")
        logger.info(f"   VGG16: {'✓' if loader.vgg16_model else '✗'}")
        logger.info(f"   Ensemble mode: {loader.ensemble_mode}")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Model loading failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_prediction():
    """Test if we can make predictions"""
    try:
        from app.models.model_loader import EnsembleModelLoader
        from PIL import Image, ImageDraw
        
        # Create a simple test image
        test_image = Image.new('RGB', (224, 224), color=(80, 40, 20))
        draw = ImageDraw.Draw(test_image)
        
        # Draw a simple pattern
        center = (112, 112)
        for i in range(3):
            radius = 20 + i * 15
            draw.ellipse([center[0]-radius, center[1]-radius,
                          center[0]+radius, center[1]+radius], 
                         outline=(120+i*20, 60+i*10, 40+i*5), width=2)
        
        # Load models and predict
        loader = EnsembleModelLoader()
        loader.load_models()
        
        # Make prediction
        result = loader.predict(test_image)
        
        logger.info(f"✅ Prediction successful")
        logger.info(f"   Stage: {result.stage} - {result.stage_description}")
        logger.info(f"   Confidence: {result.confidence}%")
        logger.info(f"   Risk Level: {result.risk_level}")
        logger.info(f"   Processing Time: {result.processing_time}s")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Prediction failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run all tests"""
    logger.info("🔬 Testing Backend Model Integration Directly")
    logger.info("=" * 60)
    
    # Check backend directory exists
    if not backend_dir.exists():
        logger.error(f"❌ Backend directory not found: {backend_dir}")
        return False
    
    # Change to backend directory
    os.chdir(backend_dir)
    logger.info(f"Working directory: {os.getcwd()}")
    
    tests = [
        ("Import Test", test_direct_import),
        ("Model Loading Test", test_model_loading),
        ("Prediction Test", test_prediction)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        logger.info(f"\n🧪 Running {test_name}...")
        try:
            if test_func():
                logger.info(f"✅ {test_name} PASSED")
                passed += 1
            else:
                logger.error(f"❌ {test_name} FAILED")
        except Exception as e:
            logger.error(f"❌ {test_name} FAILED with exception: {e}")
    
    logger.info(f"\n📊 Results: {passed}/{total} tests passed")
    
    if passed == total:
        logger.info("🎉 All tests passed! Backend models are working correctly.")
        logger.info("\n🚀 Ready to start the server!")
        logger.info("Run from backend directory: python -m uvicorn app.main:app --reload")
    else:
        logger.error("⚠️  Some tests failed. Check the errors above.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)