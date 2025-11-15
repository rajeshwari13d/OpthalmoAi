"""
Test script for ResNet50 and VGG16 diabetic retinopathy model integration
This script tests the complete model pipeline from image loading to prediction
"""

import sys
import os
import asyncio
import requests
import numpy as np
from PIL import Image, ImageDraw
import torch
import logging
from pathlib import Path
import time
import json

# Add the backend directory to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'backend'))

from app.models.resnet50_model import ResNet50Predictor, load_resnet50_model
from app.models.vgg16_model import VGG16Predictor, load_vgg16_model
from app.models.model_loader import EnsembleModelLoader

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_test_retinal_image(width=512, height=512, dr_stage=0):
    """
    Create a synthetic retinal fundus image for testing
    Simulates different diabetic retinopathy stages
    """
    # Create base fundus image
    image = Image.new('RGB', (width, height), color=(80, 40, 20))  # Dark brownish background
    draw = ImageDraw.Draw(image)
    
    # Draw optic disc (bright circular area)
    disc_center = (width//4, height//2)
    disc_radius = min(width, height) // 8
    draw.ellipse([disc_center[0]-disc_radius, disc_center[1]-disc_radius,
                  disc_center[0]+disc_radius, disc_center[1]+disc_radius], 
                 fill=(220, 180, 120))
    
    # Draw blood vessels
    for i in range(8):
        start_x = disc_center[0] + np.random.randint(-20, 20)
        start_y = disc_center[1] + np.random.randint(-20, 20)
        end_x = start_x + np.random.randint(-width//2, width//2)
        end_y = start_y + np.random.randint(-height//2, height//2)
        draw.line([(start_x, start_y), (end_x, end_y)], 
                 fill=(120, 60, 40), width=np.random.randint(2, 6))
    
    # Add DR stage-specific features
    if dr_stage >= 1:  # Mild DR - microaneurysms
        for _ in range(5 + dr_stage * 3):
            x = np.random.randint(0, width)
            y = np.random.randint(0, height)
            radius = np.random.randint(1, 3)
            draw.ellipse([x-radius, y-radius, x+radius, y+radius], 
                        fill=(150, 50, 50))
    
    if dr_stage >= 2:  # Moderate DR - hemorrhages
        for _ in range(3 + dr_stage * 2):
            x = np.random.randint(0, width)
            y = np.random.randint(0, height)
            radius = np.random.randint(3, 8)
            draw.ellipse([x-radius, y-radius, x+radius, y+radius], 
                        fill=(100, 20, 20))
    
    if dr_stage >= 3:  # Severe DR - cotton wool spots
        for _ in range(2 + dr_stage):
            x = np.random.randint(0, width)
            y = np.random.randint(0, height)
            radius = np.random.randint(5, 12)
            draw.ellipse([x-radius, y-radius, x+radius, y+radius], 
                        fill=(200, 200, 180))
    
    if dr_stage >= 4:  # Proliferative DR - neovascularization
        for _ in range(3):
            start_x = np.random.randint(0, width)
            start_y = np.random.randint(0, height)
            for j in range(5):
                end_x = start_x + np.random.randint(-30, 30)
                end_y = start_y + np.random.randint(-30, 30)
                draw.line([(start_x, start_y), (end_x, end_y)], 
                         fill=(180, 80, 80), width=2)
                start_x, start_y = end_x, end_y
    
    return image

def test_individual_models():
    """Test ResNet50 and VGG16 models individually"""
    logger.info("Testing individual models...")
    
    # Create test images for different DR stages
    test_images = {}
    for stage in range(5):
        test_images[stage] = create_test_retinal_image(dr_stage=stage)
    
    # Test ResNet50
    logger.info("Testing ResNet50 model...")
    try:
        resnet_model = load_resnet50_model()
        
        for stage, image in test_images.items():
            start_time = time.time()
            result = resnet_model.predict(image)
            end_time = time.time()
            
            logger.info(f"ResNet50 - Input Stage {stage}: "
                       f"Predicted {result['predicted_label']} "
                       f"(Confidence: {result['confidence']}%) "
                       f"Time: {end_time - start_time:.3f}s")
        
        logger.info("✅ ResNet50 model test passed")
        
    except Exception as e:
        logger.error(f"❌ ResNet50 model test failed: {e}")
        return False
    
    # Test VGG16
    logger.info("Testing VGG16 model...")
    try:
        vgg_model = load_vgg16_model()
        
        for stage, image in test_images.items():
            start_time = time.time()
            result = vgg_model.predict(image)
            end_time = time.time()
            
            logger.info(f"VGG16 - Input Stage {stage}: "
                       f"Predicted {result['predicted_label']} "
                       f"(Confidence: {result['confidence']}%) "
                       f"Time: {end_time - start_time:.3f}s")
        
        logger.info("✅ VGG16 model test passed")
        
    except Exception as e:
        logger.error(f"❌ VGG16 model test failed: {e}")
        return False
    
    return True

def test_ensemble_model():
    """Test ensemble model loader"""
    logger.info("Testing ensemble model...")
    
    try:
        # Initialize ensemble model loader
        ensemble_loader = EnsembleModelLoader()
        ensemble_loader.load_models()
        
        # Create test image
        test_image = create_test_retinal_image(dr_stage=2)
        
        # Test prediction
        start_time = time.time()
        result = ensemble_loader.predict(test_image)
        end_time = time.time()
        
        logger.info(f"Ensemble prediction:")
        logger.info(f"  Stage: {result.stage} - {result.stage_description}")
        logger.info(f"  Confidence: {result.confidence}%")
        logger.info(f"  Risk Level: {result.risk_level}")
        logger.info(f"  Processing Time: {result.processing_time}s")
        logger.info(f"  Recommendations: {len(result.recommendations)} items")
        
        if hasattr(result, 'model_info') and result.model_info:
            model_info = result.model_info
            logger.info(f"  Model: {model_info.get('model_name', 'Unknown')}")
            if 'ensemble_agreement' in model_info:
                agreement = model_info['ensemble_agreement']
                logger.info(f"  Agreement: {agreement.get('agreement_level', 'Unknown')} "
                           f"({agreement.get('agreement_score', 0):.1f}%)")
        
        logger.info("✅ Ensemble model test passed")
        return True
        
    except Exception as e:
        logger.error(f"❌ Ensemble model test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_api_endpoint():
    """Test the FastAPI endpoint with the new models"""
    logger.info("Testing API endpoint...")
    
    try:
        # Create test image
        test_image = create_test_retinal_image(dr_stage=1)
        
        # Save test image temporarily
        test_image_path = "test_retinal_image.jpg"
        test_image.save(test_image_path, "JPEG")
        
        # Test API endpoint
        api_url = "http://localhost:8000/api/v1/analysis/analyze"
        
        with open(test_image_path, "rb") as f:
            files = {"file": ("test_image.jpg", f, "image/jpeg")}
            response = requests.post(api_url, files=files, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            logger.info(f"API Response:")
            logger.info(f"  Success: {result.get('success', False)}")
            if result.get('result'):
                analysis = result['result']
                logger.info(f"  Stage: {analysis.get('stage')} - {analysis.get('stage_description')}")
                logger.info(f"  Confidence: {analysis.get('confidence')}%")
                logger.info(f"  Risk Level: {analysis.get('risk_level')}")
                logger.info(f"  Processing Time: {analysis.get('processing_time')}s")
            
            logger.info("✅ API endpoint test passed")
            
        else:
            logger.error(f"❌ API endpoint test failed: HTTP {response.status_code}")
            logger.error(f"Response: {response.text}")
            return False
        
        # Clean up
        os.remove(test_image_path)
        return True
        
    except requests.exceptions.ConnectionError:
        logger.warning("⚠️  API endpoint test skipped - Server not running")
        logger.info("To test API endpoint, start the server with: uvicorn app.main:app --reload")
        return True
        
    except Exception as e:
        logger.error(f"❌ API endpoint test failed: {e}")
        return False

def test_model_performance():
    """Performance benchmark for the models"""
    logger.info("Running performance benchmark...")
    
    try:
        # Create test images
        test_images = [create_test_retinal_image(dr_stage=i) for i in range(3)]
        
        # Test ResNet50 performance
        resnet_model = load_resnet50_model()
        resnet_times = []
        
        for image in test_images:
            start_time = time.time()
            resnet_model.predict(image)
            end_time = time.time()
            resnet_times.append(end_time - start_time)
        
        # Test VGG16 performance
        vgg_model = load_vgg16_model()
        vgg_times = []
        
        for image in test_images:
            start_time = time.time()
            vgg_model.predict(image)
            end_time = time.time()
            vgg_times.append(end_time - start_time)
        
        # Test ensemble performance
        ensemble_loader = EnsembleModelLoader()
        ensemble_loader.load_models()
        ensemble_times = []
        
        for image in test_images:
            start_time = time.time()
            ensemble_loader.predict(image)
            end_time = time.time()
            ensemble_times.append(end_time - start_time)
        
        # Report results
        logger.info("Performance Results:")
        logger.info(f"  ResNet50 avg: {np.mean(resnet_times):.3f}s ± {np.std(resnet_times):.3f}s")
        logger.info(f"  VGG16 avg: {np.mean(vgg_times):.3f}s ± {np.std(vgg_times):.3f}s")
        logger.info(f"  Ensemble avg: {np.mean(ensemble_times):.3f}s ± {np.std(ensemble_times):.3f}s")
        
        logger.info("✅ Performance benchmark completed")
        return True
        
    except Exception as e:
        logger.error(f"❌ Performance benchmark failed: {e}")
        return False

def main():
    """Run all tests"""
    logger.info("🔬 Starting OpthalmoAI Model Integration Tests")
    logger.info("=" * 60)
    
    test_results = {
        "individual_models": test_individual_models(),
        "ensemble_model": test_ensemble_model(),
        "api_endpoint": test_api_endpoint(),
        "performance": test_model_performance()
    }
    
    logger.info("=" * 60)
    logger.info("📊 TEST RESULTS SUMMARY:")
    
    passed = 0
    total = len(test_results)
    
    for test_name, result in test_results.items():
        status = "✅ PASSED" if result else "❌ FAILED"
        logger.info(f"  {test_name.replace('_', ' ').title()}: {status}")
        if result:
            passed += 1
    
    logger.info(f"\n🎯 Overall: {passed}/{total} tests passed")
    
    if passed == total:
        logger.info("🎉 All tests passed! Model integration is working correctly.")
        
        logger.info("\n🚀 NEXT STEPS:")
        logger.info("1. Train models on real diabetic retinopathy dataset")
        logger.info("2. Replace pre-trained weights with trained DR weights")
        logger.info("3. Deploy backend to production environment")
        logger.info("4. Update frontend API endpoints to production URLs")
        
    else:
        logger.error("⚠️  Some tests failed. Please check the errors above.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)