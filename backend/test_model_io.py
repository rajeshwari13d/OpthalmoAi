"""
Model Input/Output Test for OpthalmoAI
Test script to verify model loading, input processing, and output format
"""
import sys
import os
import torch
import torch.nn as nn
import torchvision.transforms as transforms
from PIL import Image
import numpy as np
from pathlib import Path
import traceback
import requests
import time

# Add the app directory to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

def test_model_files():
    """Test if model files exist and are accessible"""
    print("🔍 Testing Model Files...")
    
    model_path = "app/models/trained_models/best_model.pth"
    architecture_path = "app/models/trained_models/OpthalmoAi.py"
    
    print(f"Model weights: {model_path}")
    print(f"Exists: {os.path.exists(model_path)}")
    if os.path.exists(model_path):
        size = os.path.getsize(model_path)
        print(f"Size: {size / (1024*1024):.1f} MB")
    
    print(f"\nArchitecture: {architecture_path}")
    print(f"Exists: {os.path.exists(architecture_path)}")
    if os.path.exists(architecture_path):
        try:
            with open(architecture_path, 'r', encoding='utf-8') as f:
                content = f.read().strip()
                print(f"Content length: {len(content)} chars")
                if content:
                    print(f"First 200 chars: {content[:200]}...")
                else:
                    print("File is empty - using fallback architecture")
        except UnicodeDecodeError:
            try:
                with open(architecture_path, 'r', encoding='latin1') as f:
                    content = f.read().strip()
                    print(f"Content length: {len(content)} chars (latin1)")
                    if content:
                        print("File contains binary data or non-UTF8 content")
                    else:
                        print("File is empty - using fallback architecture")
            except Exception as e:
                print(f"Cannot read architecture file: {e}")
                print("Using fallback architecture")
    
    return os.path.exists(model_path)

def test_model_loading():
    """Test loading the trained model"""
    print("\n🤖 Testing Model Loading...")
    
    try:
        from torchvision import models
        
        # Load model architecture (same as in backend)
        model = models.resnet50(pretrained=False)
        num_classes = 5  # DR classes: No DR, Mild, Moderate, Severe, Proliferative
        model.fc = nn.Linear(model.fc.in_features, num_classes)
        
        print(f"✅ Model architecture created: ResNet50 with {num_classes} classes")
        
        # Load trained weights
        model_path = "app/models/trained_models/best_model.pth"
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        
        checkpoint = torch.load(model_path, map_location=device)
        print(f"✅ Checkpoint loaded from: {model_path}")
        print(f"Device: {device}")
        
        # Handle different checkpoint formats
        if isinstance(checkpoint, dict):
            print("Checkpoint is a dictionary")
            print(f"Keys: {list(checkpoint.keys())}")
            
            if 'model_state_dict' in checkpoint:
                state_dict = checkpoint['model_state_dict']
                print("Using 'model_state_dict'")
            elif 'state_dict' in checkpoint:
                state_dict = checkpoint['state_dict']
                print("Using 'state_dict'")
            else:
                state_dict = checkpoint
                print("Using entire checkpoint as state_dict")
        else:
            print("Checkpoint is not a dictionary - might be the model itself")
            model = checkpoint
            state_dict = None
        
        if state_dict:
            # Remove 'module.' prefix if present
            new_state_dict = {}
            module_keys = []
            normal_keys = []
            
            for k, v in state_dict.items():
                if k.startswith('module.'):
                    module_keys.append(k)
                    new_key = k[7:]  # Remove 'module.'
                else:
                    normal_keys.append(k)
                    new_key = k
                new_state_dict[new_key] = v
            
            print(f"State dict keys: {len(state_dict)} total")
            print(f"Module keys: {len(module_keys)}")
            print(f"Normal keys: {len(normal_keys)}")
            
            # Show some example keys
            example_keys = list(new_state_dict.keys())[:5]
            print(f"Example keys: {example_keys}")
            
            # Try to load state dict
            missing_keys, unexpected_keys = model.load_state_dict(new_state_dict, strict=False)
            print(f"✅ State dict loaded")
            print(f"Missing keys: {len(missing_keys)}")
            print(f"Unexpected keys: {len(unexpected_keys)}")
            
            if missing_keys:
                print(f"Missing keys sample: {missing_keys[:3]}")
            if unexpected_keys:
                print(f"Unexpected keys sample: {unexpected_keys[:3]}")
        
        model.to(device)
        model.eval()
        
        # Test model inference with dummy input
        dummy_input = torch.randn(1, 3, 224, 224).to(device)
        with torch.no_grad():
            output = model(dummy_input)
        
        print(f"✅ Model inference test successful")
        print(f"Output shape: {output.shape}")
        print(f"Output sample: {output[0][:3].cpu().numpy()}")
        
        # Test softmax probabilities
        probabilities = torch.softmax(output, dim=1)
        print(f"Probabilities shape: {probabilities.shape}")
        print(f"Probabilities sum: {probabilities.sum().item():.3f}")
        print(f"Max probability: {probabilities.max().item():.3f}")
        
        return model, device
        
    except Exception as e:
        print(f"❌ Model loading failed: {e}")
        print(traceback.format_exc())
        return None, None

def test_image_preprocessing():
    """Test image preprocessing pipeline"""
    print("\n🖼️  Testing Image Preprocessing...")
    
    try:
        # Create preprocessing pipeline (same as in backend)
        transform = transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            transforms.Normalize(
                mean=[0.485, 0.456, 0.406],
                std=[0.229, 0.224, 0.225]
            )
        ])
        
        # Test with a dummy image
        dummy_image = Image.new('RGB', (512, 512), color='red')
        print(f"Created dummy image: {dummy_image.size}, mode: {dummy_image.mode}")
        
        # Apply preprocessing
        tensor = transform(dummy_image)
        print(f"✅ Preprocessing successful")
        print(f"Tensor shape: {tensor.shape}")
        print(f"Tensor dtype: {tensor.dtype}")
        print(f"Tensor range: [{tensor.min():.3f}, {tensor.max():.3f}]")
        
        # Add batch dimension
        batch_tensor = tensor.unsqueeze(0)
        print(f"Batch tensor shape: {batch_tensor.shape}")
        
        return transform
        
    except Exception as e:
        print(f"❌ Preprocessing failed: {e}")
        print(traceback.format_exc())
        return None

def test_full_prediction_pipeline(model, device, transform):
    """Test the complete prediction pipeline"""
    print("\n🔮 Testing Full Prediction Pipeline...")
    
    if model is None or transform is None:
        print("❌ Cannot test - model or transform not available")
        return
    
    try:
        # Create test image
        test_image = Image.new('RGB', (300, 300), color='blue')
        print(f"Test image: {test_image.size}, mode: {test_image.mode}")
        
        # Preprocess
        input_tensor = transform(test_image).unsqueeze(0).to(device)
        print(f"Input tensor ready: {input_tensor.shape}")
        
        # Model inference
        with torch.no_grad():
            outputs = model(input_tensor)
            probabilities = torch.softmax(outputs, dim=1)
        
        # Get predictions
        predicted_class = torch.argmax(probabilities, dim=1).item()
        confidence = probabilities[0][predicted_class].item()
        
        # Class labels
        class_labels = {
            0: "No DR",
            1: "Mild",
            2: "Moderate", 
            3: "Severe",
            4: "Proliferative DR"
        }
        
        print(f"✅ Prediction successful")
        print(f"Predicted class: {predicted_class}")
        print(f"Predicted label: {class_labels[predicted_class]}")
        print(f"Confidence: {confidence * 100:.2f}%")
        
        # All class probabilities
        class_probs = {
            class_labels[i]: probabilities[0][i].item() * 100
            for i in range(len(class_labels))
        }
        
        print("All class probabilities:")
        for label, prob in class_probs.items():
            print(f"  {label}: {prob:.2f}%")
        
        return {
            "predicted_class": predicted_class,
            "predicted_label": class_labels[predicted_class],
            "confidence": confidence * 100,
            "class_probabilities": class_probs
        }
        
    except Exception as e:
        print(f"❌ Prediction pipeline failed: {e}")
        print(traceback.format_exc())
        return None

def test_backend_api():
    """Test if backend API is responding"""
    print("\n🌐 Testing Backend API...")
    
    api_base = "http://127.0.0.1:8006"
    
    try:
        # Test health endpoint
        health_url = f"{api_base}/api/v1/health"
        print(f"Testing: {health_url}")
        
        response = requests.get(health_url, timeout=5)
        print(f"✅ Health check successful: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"Status: {data.get('status')}")
            print(f"Message: {data.get('message')}")
            print(f"Model loaded: {data.get('model_loaded')}")
        
        return True
        
    except requests.exceptions.ConnectionError:
        print("❌ Backend not running or not accessible")
        return False
    except Exception as e:
        print(f"❌ API test failed: {e}")
        return False

def start_backend_server():
    """Start the backend server"""
    print("\n🚀 Starting Backend Server...")
    
    try:
        # Start in background
        import subprocess
        process = subprocess.Popen([
            "python", "working_backend.py"
        ], cwd=".", stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        print("Backend server starting...")
        time.sleep(3)  # Wait for server to start
        
        return process
        
    except Exception as e:
        print(f"❌ Failed to start backend: {e}")
        return None

def main():
    """Run all tests"""
    print("=" * 60)
    print("🔬 OpthalmoAI Model Input/Output Testing")
    print("=" * 60)
    
    # Test 1: Check files
    files_ok = test_model_files()
    
    if not files_ok:
        print("\n❌ Model files not found - cannot proceed")
        return
    
    # Test 2: Load model
    model, device = test_model_loading()
    
    # Test 3: Test preprocessing
    transform = test_image_preprocessing()
    
    # Test 4: Test full pipeline
    if model and transform:
        result = test_full_prediction_pipeline(model, device, transform)
    
    # Test 5: Test backend API
    api_ok = test_backend_api()
    
    if not api_ok:
        print("\n🚀 Backend not running - attempting to start...")
        # Note: This would need to be run in a separate process in reality
    
    print("\n" + "=" * 60)
    print("🏁 Testing Complete")
    print("=" * 60)

if __name__ == "__main__":
    main()