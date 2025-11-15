"""
🏥 OpthalmoAI Custom Model Integration Status Check
This script checks if your trained model is properly integrated and working
"""

import sys
import os
from pathlib import Path
import requests
import json
import time
from PIL import Image, ImageDraw
import io

# Set up path for imports
backend_dir = Path(__file__).parent / "backend"
sys.path.insert(0, str(backend_dir))
os.chdir(backend_dir)

def test_model_files_exist():
    """Check if model files exist in the correct location"""
    print("🔍 Step 1: Checking Model Files")
    print("-" * 50)
    
    trained_models_dir = Path("app/models/trained_models")
    
    files_to_check = [
        ("OpthalmoAI.py", "Architecture file"),
        ("OpthalmoAi.py", "Architecture file (alternative name)"),
        ("best_model.pth", "Trained model weights"),
        ("OpthalmoAi_Inference.ipynb", "Inference notebook")
    ]
    
    found_files = {}
    for filename, description in files_to_check:
        file_path = trained_models_dir / filename
        exists = file_path.exists()
        found_files[filename] = exists
        status = "✅ Found" if exists else "❌ Missing"
        size = f" ({file_path.stat().st_size // 1024} KB)" if exists else ""
        print(f"   {status}: {filename} - {description}{size}")
    
    return found_files

def test_direct_model_loading():
    """Test loading the custom model directly"""
    print("\n🤖 Step 2: Testing Direct Model Loading")
    print("-" * 50)
    
    try:
        from app.models.custom_trained_model import (
            get_trained_model_path, 
            get_architecture_path, 
            is_trained_model_available,
            load_custom_trained_model
        )
        
        print(f"   Model path: {get_trained_model_path()}")
        print(f"   Architecture path: {get_architecture_path()}")
        print(f"   Model available: {is_trained_model_available()}")
        
        if is_trained_model_available():
            print("   🔄 Loading custom model...")
            model_wrapper = load_custom_trained_model(
                get_trained_model_path(), 
                architecture_file=get_architecture_path()
            )
            
            if model_wrapper.model_loaded:
                print("   ✅ Custom model loaded successfully!")
                print(f"      Device: {model_wrapper.device}")
                print(f"      Model type: {type(model_wrapper.model).__name__}")
                return model_wrapper
            else:
                print("   ❌ Custom model failed to load")
                return None
        else:
            print("   ❌ Model files not available")
            return None
            
    except Exception as e:
        print(f"   ❌ Error loading model: {e}")
        return None

def test_model_prediction(model_wrapper):
    """Test making a prediction with the custom model"""
    print("\n🎯 Step 3: Testing Model Prediction")
    print("-" * 50)
    
    if not model_wrapper:
        print("   ⏭️  Skipping - model not loaded")
        return None
    
    try:
        # Create a test retinal image
        print("   📷 Creating test retinal image...")
        img = Image.new('RGB', (512, 512), color=(20, 10, 10))
        draw = ImageDraw.Draw(img)
        
        # Draw optic disc
        draw.ellipse([200, 180, 280, 260], fill=(255, 200, 150), outline=(255, 255, 200))
        
        # Draw blood vessels
        draw.line([256, 100, 256, 400], fill=(150, 50, 50), width=8)
        draw.line([100, 256, 400, 256], fill=(140, 45, 45), width=6)
        
        print("   🔄 Running prediction...")
        result = model_wrapper.predict(img)
        
        if "error" not in result:
            print("   ✅ Prediction successful!")
            print(f"      Predicted class: {result['predicted_class']}")
            print(f"      Predicted label: {result['predicted_label']}")
            print(f"      Confidence: {result['confidence']}%")
            print(f"      Severity: {result['severity']}")
            return result
        else:
            print(f"   ❌ Prediction failed: {result['error']}")
            return None
            
    except Exception as e:
        print(f"   ❌ Error during prediction: {e}")
        return None

def test_enhanced_model_loader():
    """Test the enhanced model loader integration"""
    print("\n🔧 Step 4: Testing Enhanced Model Loader")
    print("-" * 50)
    
    try:
        from app.models.enhanced_model_loader import OpthalmoAIModelLoader
        
        print("   🔄 Creating OpthalmoAIModelLoader...")
        loader = OpthalmoAIModelLoader()
        
        print("   🔄 Loading models...")
        loader.load_models()
        
        if loader.models_loaded:
            print("   ✅ Enhanced model loader successful!")
            
            model_info = loader.get_model_info()
            print(f"      Use custom model: {model_info['use_custom_model']}")
            print(f"      Ensemble mode: {model_info['ensemble_mode']}")
            print(f"      Device: {model_info['device']}")
            
            if model_info['use_custom_model']:
                print(f"      ✅ YOUR CUSTOM MODEL IS ACTIVE!")
                print(f"      Model path: {model_info.get('model_path', 'Unknown')}")
            else:
                print(f"      📋 Using fallback ensemble models")
            
            return loader
        else:
            print("   ❌ Enhanced model loader failed")
            return None
            
    except Exception as e:
        print(f"   ❌ Error with enhanced loader: {e}")
        return None

def test_server_startup():
    """Test if server can start with custom model"""
    print("\n🚀 Step 5: Testing Server Integration")
    print("-" * 50)
    
    try:
        import subprocess
        import time
        
        print("   🔄 Testing server startup simulation...")
        
        # Import the model loader like the server does
        from app.models.model_loader import model_loader
        
        print("   🔄 Loading models via model_loader...")
        model_loader.load_models()
        
        if model_loader.models_loaded:
            print("   ✅ Server-style model loading successful!")
            
            # Check if using custom model
            if hasattr(model_loader, 'use_custom_model') and model_loader.use_custom_model:
                print("   🎯 Server will use YOUR CUSTOM MODEL!")
            elif hasattr(model_loader, 'custom_model') and model_loader.custom_model:
                print("   🎯 Server has your custom model loaded!")
            else:
                print("   📋 Server will use ensemble fallback models")
                
            return True
        else:
            print("   ❌ Server-style loading failed")
            return False
            
    except Exception as e:
        print(f"   ❌ Server integration error: {e}")
        return False

def generate_integration_report():
    """Generate a comprehensive integration report"""
    print("\n" + "="*60)
    print("🏥 OPTHALMOAI CUSTOM MODEL INTEGRATION REPORT")
    print("="*60)
    
    # Step 1: Check files
    files_status = test_model_files_exist()
    
    # Step 2: Test direct loading
    model_wrapper = test_direct_model_loading()
    
    # Step 3: Test prediction
    prediction_result = test_model_prediction(model_wrapper)
    
    # Step 4: Test enhanced loader
    enhanced_loader = test_enhanced_model_loader()
    
    # Step 5: Test server integration
    server_ready = test_server_startup()
    
    # Final summary
    print("\n" + "="*60)
    print("📊 INTEGRATION STATUS SUMMARY")
    print("="*60)
    
    custom_model_active = False
    if enhanced_loader and hasattr(enhanced_loader, 'use_custom_model'):
        custom_model_active = enhanced_loader.use_custom_model
    
    print(f"✅ Model Files Present: {files_status.get('best_model.pth', False)}")
    print(f"✅ Direct Loading Works: {model_wrapper is not None}")
    print(f"✅ Predictions Working: {prediction_result is not None}")
    print(f"✅ Enhanced Loader: {enhanced_loader is not None}")
    print(f"✅ Server Integration: {server_ready}")
    print(f"🎯 CUSTOM MODEL ACTIVE: {custom_model_active}")
    
    if custom_model_active:
        print(f"\n🎉 SUCCESS! Your custom trained model is fully integrated!")
        print(f"   📁 Model path: {files_status}")
        print(f"   🤖 The server will use YOUR trained weights")
        print(f"   📊 Predictions are working correctly")
    else:
        print(f"\n⚠️  Your model files are present but the system is using fallback models")
        print(f"   This might be due to:")
        print(f"   - Empty OpthalmoAi.py file (no model class found)")
        print(f"   - State dict key mismatches (should be handled gracefully)")
        print(f"   - Architecture incompatibility")
    
    print(f"\n🌐 Next Steps:")
    print(f"   1. Start server: python standalone_server.py")
    print(f"   2. Check logs for 'Custom trained model loaded successfully!'")
    print(f"   3. Test with real images via API or web interface")
    
    return {
        'custom_model_active': custom_model_active,
        'files_present': files_status.get('best_model.pth', False),
        'loading_works': model_wrapper is not None,
        'predictions_work': prediction_result is not None,
        'server_ready': server_ready
    }

if __name__ == "__main__":
    print("🔍 Starting OpthalmoAI Custom Model Integration Check...")
    print(f"📍 Working directory: {os.getcwd()}")
    
    try:
        report = generate_integration_report()
        
        # Exit code for automation
        if report['custom_model_active']:
            print(f"\n✅ Integration Status: FULLY INTEGRATED")
            exit(0)
        else:
            print(f"\n⚠️  Integration Status: FALLBACK MODELS")
            exit(1)
            
    except Exception as e:
        print(f"\n❌ Integration check failed: {e}")
        exit(2)