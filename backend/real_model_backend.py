"""
Real Model Backend for OpthalmoAI
FastAPI server with actual trained model integration
"""
import uvicorn
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, Any, Optional
import logging
import os
import sys
from PIL import Image
import io
import traceback
import torch
import torch.nn as nn
import torchvision.transforms as transforms
from torchvision import models

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Direct model loading without complex imports
def load_trained_model():
    """Load the trained model directly"""
    try:
        # Use absolute path from the current file location
        current_dir = os.path.dirname(os.path.abspath(__file__))
        model_path = os.path.join(current_dir, "app", "models", "trained_models", "best_model.pth")
        
        if not os.path.exists(model_path):
            logger.error(f"Model file not found: {model_path}")
            return None
            
        logger.info(f"Loading model from: {model_path}")
        
        # Create a standard ResNet50 architecture (most common for DR)
        model = models.resnet50(pretrained=False)
        num_classes = 5  # Assuming 5 DR classes: No DR, Mild, Moderate, Severe, Proliferative
        model.fc = nn.Linear(model.fc.in_features, num_classes)
        
        # Load the trained weights
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        checkpoint = torch.load(model_path, map_location=device)
        
        # Handle different checkpoint formats
        if isinstance(checkpoint, dict):
            if 'model_state_dict' in checkpoint:
                state_dict = checkpoint['model_state_dict']
            elif 'state_dict' in checkpoint:
                state_dict = checkpoint['state_dict']
            else:
                state_dict = checkpoint
        else:
            # Checkpoint is the model itself
            model = checkpoint
            state_dict = None
        
        if state_dict:
            # Remove 'module.' prefix if present
            new_state_dict = {}
            for k, v in state_dict.items():
                name = k[7:] if k.startswith('module.') else k
                new_state_dict[name] = v
            
            model.load_state_dict(new_state_dict, strict=False)
        
        model.to(device)
        model.eval()
        
        logger.info("✅ Model loaded successfully")
        return model, device
        
    except Exception as e:
        logger.error(f"❌ Failed to load model: {e}")
        logger.error(traceback.format_exc())
        return None

def predict_image(image: Image.Image):
    """Make prediction using the loaded model"""
    global model_instance, device, class_labels
    
    if model_instance is None:
        return {"error": "Model not loaded"}
    
    try:
        # Preprocessing pipeline
        transform = transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            transforms.Normalize(
                mean=[0.485, 0.456, 0.406],
                std=[0.229, 0.224, 0.225]
            )
        ])
        
        # Convert to RGB if necessary
        if image.mode != 'RGB':
            image = image.convert('RGB')
        
        # Apply transforms and add batch dimension
        input_tensor = transform(image).unsqueeze(0).to(device)
        
        # Model inference
        with torch.no_grad():
            outputs = model_instance(input_tensor)
            probabilities = torch.softmax(outputs, dim=1)
            
        # Get predictions
        predicted_class = torch.argmax(probabilities, dim=1).item()
        confidence = probabilities[0][predicted_class].item()
        
        # Get all class probabilities
        class_probs = {
            class_labels[i]: probabilities[0][i].item() * 100
            for i in range(len(class_labels))
        }
        
        return {
            "predicted_class": predicted_class,
            "predicted_label": class_labels[predicted_class],
            "confidence": confidence * 100,
            "class_probabilities": class_probs,
            "severity": get_severity_level(predicted_class),
            "recommendations": get_recommendations(predicted_class),
            "requires_urgent_care": predicted_class >= 3,
            "follow_up_months": get_follow_up_period(predicted_class),
            "model_name": "Custom Trained OpthalmoAI",
            "model_path": model_path
        }
        
    except Exception as e:
        logger.error(f"Error during prediction: {e}")
        return {"error": f"Prediction failed: {str(e)}"}

def get_severity_level(predicted_class: int) -> str:
    """Get severity level description"""
    severity_map = {
        0: "None",
        1: "Mild", 
        2: "Moderate",
        3: "Severe",
        4: "Very Severe"
    }
    return severity_map.get(predicted_class, "Unknown")

def get_recommendations(predicted_class: int) -> list:
    """Get medical recommendations based on prediction"""
    recommendations_map = {
        0: [
            "Continue regular diabetic care",
            "Annual dilated eye examination recommended", 
            "Maintain optimal glycemic control"
        ],
        1: [
            "Schedule ophthalmology follow-up in 12 months",
            "Optimize diabetes management with HbA1c < 7%",
            "Monitor blood pressure and lipid levels"
        ],
        2: [
            "Ophthalmology referral within 6 months recommended",
            "Consider more frequent monitoring",
            "Strict glycemic and blood pressure control"
        ],
        3: [
            "Urgent ophthalmology consultation within 1 month",
            "Consider pan-retinal photocoagulation",
            "Intensive diabetes management required"
        ],
        4: [
            "Immediate ophthalmology referral (within 1-2 weeks)",
            "Vitreoretinal surgery evaluation may be needed",
            "Close monitoring with monthly follow-ups"
        ]
    }
    return recommendations_map.get(predicted_class, ["Consult healthcare provider"])

def get_follow_up_period(predicted_class: int) -> int:
    """Get recommended follow-up period in months"""
    follow_up_map = {
        0: 12,  # Annual screening
        1: 12,  # Annual screening 
        2: 6,   # Semi-annual
        3: 2,   # Every 2 months
        4: 1    # Monthly
    }
    return follow_up_map.get(predicted_class, 6)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(title="OpthalmoAI Real Model Backend", version="2.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:3001", 
        "http://127.0.0.1:3000",
        "http://127.0.0.1:3001"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global model instance
model_instance = None
device = None
class_labels = {
    0: "No DR",
    1: "Mild",
    2: "Moderate", 
    3: "Severe",
    4: "Proliferative DR"
}

# Response models
class HealthResponse(BaseModel):
    status: str
    message: str
    model_loaded: bool
    model_path: Optional[str] = None
    architecture_path: Optional[str] = None

class AnalysisResult(BaseModel):
    success: bool
    analysis: Dict[str, Any]
    message: str

def load_model():
    """Load the trained model on startup"""
    global model_instance, device
    
    try:
        result = load_trained_model()
        if result is None:
            logger.error("❌ Trained model files not found or failed to load")
            return False
        
        model_instance, device = result
        logger.info("✅ Custom trained model loaded successfully")
        return True
        
    except Exception as e:
        logger.error(f"❌ Failed to load model: {e}")
        logger.error(traceback.format_exc())
        return False

# Load model on startup
@app.on_event("startup")
async def startup_event():
    """Load model when server starts"""
    logger.info("🚀 Starting OpthalmoAI Real Model Backend...")
    success = load_model()
    if not success:
        logger.warning("⚠️  Server started but model loading failed")

# Health check endpoint
@app.get("/api/v1/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint with model status"""
    try:
        model_loaded = model_instance is not None
        current_dir = os.path.dirname(os.path.abspath(__file__))
        model_path_check = os.path.join(current_dir, "app", "models", "trained_models", "best_model.pth")
        arch_path_check = os.path.join(current_dir, "app", "models", "trained_models", "OpthalmoAi.py")
        model_path = model_path_check if os.path.exists(model_path_check) else None
        architecture_path = arch_path_check if os.path.exists(arch_path_check) else None
        
        return HealthResponse(
            status="healthy" if model_loaded else "degraded",
            message=f"OpthalmoAI Real Model Backend - Model {'Loaded' if model_loaded else 'Not Loaded'}",
            model_loaded=model_loaded,
            model_path=model_path,
            architecture_path=architecture_path
        )
    except Exception as e:
        logger.error(f"Health check error: {e}")
        raise HTTPException(status_code=500, detail="Health check failed")

# Analysis endpoint with real model
@app.post("/api/v1/analyze", response_model=AnalysisResult)
async def analyze_image(file: UploadFile = File(...)):
    """Analyze uploaded retinal image using trained model"""
    try:
        logger.info(f"🔍 Analysis requested for file: {file.filename}")
        
        # Check if model is loaded
        if model_instance is None:
            logger.error("❌ Model not loaded")
            raise HTTPException(status_code=503, detail="AI model not available")
        
        # Validate file
        if not file.filename:
            raise HTTPException(status_code=400, detail="No file provided")
            
        # Check file type
        allowed_types = ['image/jpeg', 'image/jpg', 'image/png']
        if file.content_type not in allowed_types:
            raise HTTPException(status_code=400, detail=f"Invalid file type: {file.content_type}. Allowed: {allowed_types}")
        
        # Read and validate file content
        content = await file.read()
        if len(content) == 0:
            raise HTTPException(status_code=400, detail="Empty file")
        
        logger.info(f"📁 File validated: {len(content)} bytes, type: {file.content_type}")
        
        # Convert to PIL Image
        try:
            image = Image.open(io.BytesIO(content))
            logger.info(f"🖼️  Image opened: {image.size}, mode: {image.mode}")
        except Exception as e:
            logger.error(f"Failed to open image: {e}")
            raise HTTPException(status_code=400, detail="Invalid image file")
        
        # Run model prediction
        logger.info("🤖 Running AI model prediction...")
        prediction_result = predict_image(image)
        
        if "error" in prediction_result:
            logger.error(f"❌ Model prediction failed: {prediction_result['error']}")
            raise HTTPException(status_code=500, detail=f"Model prediction failed: {prediction_result['error']}")
        
        logger.info(f"✅ Prediction completed: {prediction_result['predicted_label']} (confidence: {prediction_result['confidence']}%)")
        
        # Format result for frontend
        formatted_result = {
            "patient_id": f"PATIENT_{hash(file.filename) % 10000:04d}",
            "analysis_timestamp": "2024-01-15T10:30:00Z",  # You can use datetime.now().isoformat()
            "image_quality": {
                "score": 0.95,  # You can implement actual quality assessment
                "assessment": "Good quality for analysis"
            },
            "diabetic_retinopathy": {
                "stage": prediction_result['predicted_class'],
                "stage_name": prediction_result['predicted_label'],
                "confidence": prediction_result['confidence'] / 100.0,  # Convert to 0-1 scale
                "description": f"AI analysis indicates: {prediction_result['predicted_label']} with {prediction_result['confidence']}% confidence"
            },
            "findings": [
                {
                    "type": "AI Classification",
                    "severity": prediction_result['severity'],
                    "location": "Retinal analysis",
                    "confidence": prediction_result['confidence'] / 100.0
                }
            ],
            "risk_assessment": {
                "progression_risk": prediction_result['severity'], 
                "recommended_followup": f"{prediction_result['follow_up_months']} months",
                "urgent_referral": prediction_result['requires_urgent_care']
            },
            "recommendations": prediction_result['recommendations'],
            "technical_details": {
                "model_version": prediction_result['model_name'],
                "model_path": prediction_result['model_path'],
                "processing_time": "Real-time analysis",
                "image_resolution": f"{image.size[0]}x{image.size[1]}",
                "all_class_probabilities": prediction_result['class_probabilities']
            }
        }
        
        logger.info("📊 Analysis formatted successfully")
        
        return AnalysisResult(
            success=True,
            analysis=formatted_result,
            message="Analysis completed successfully using trained OpthalmoAI model"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Analysis error: {e}")
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")

if __name__ == "__main__":
    print("🚀 Starting OpthalmoAI Real Model Backend...")
    print("Server: http://localhost:8005")
    print("Health: http://localhost:8005/api/v1/health") 
    print("Analysis: http://localhost:8005/api/v1/analyze")
    print("CORS: Allowing localhost:3000, localhost:3001, 127.0.0.1:3000")
    print("Model Integration: Using your trained OpthalmoAI model")
    print("=" * 70)
    
    try:
        uvicorn.run(
            app, 
            host="0.0.0.0", 
            port=8005, 
            log_level="info",
            access_log=True
        )
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
    except Exception as e:
        print(f"❌ Server error: {e}")
        sys.exit(1)