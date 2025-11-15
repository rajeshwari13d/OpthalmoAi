"""
Stable Test Backend for Model Response Testing
A simple backend that stays running for testing
"""
import uvicorn
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, Any
import torch
import torch.nn as nn
import torchvision.transforms as transforms
from torchvision import models
from PIL import Image
import io
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(title="OpthalmoAI Stable Test Backend", version="1.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for testing
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global variables
model_instance = None
device = None
transform = None

class HealthResponse(BaseModel):
    status: str
    message: str
    model_loaded: bool

class AnalysisResult(BaseModel):
    success: bool
    analysis: Dict[str, Any]
    message: str

def load_model():
    """Load the trained model"""
    global model_instance, device, transform
    
    try:
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        logger.info(f"Using device: {device}")
        
        # Load model architecture
        model = models.resnet50(pretrained=False)
        model.fc = nn.Linear(model.fc.in_features, 5)  # 5 DR classes
        
        # Load weights
        model_path = "app/models/trained_models/best_model.pth"
        checkpoint = torch.load(model_path, map_location=device)
        
        # Handle different checkpoint formats
        if isinstance(checkpoint, dict):
            state_dict = checkpoint
        else:
            state_dict = checkpoint.state_dict() if hasattr(checkpoint, 'state_dict') else checkpoint
        
        # Remove 'module.' prefix if present
        new_state_dict = {}
        for k, v in state_dict.items():
            name = k[7:] if k.startswith('module.') else k
            new_state_dict[name] = v
        
        model.load_state_dict(new_state_dict, strict=False)
        model.to(device)
        model.eval()
        
        # Create transform
        transform = transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
        ])
        
        model_instance = model
        logger.info("✅ Model loaded successfully!")
        return True
        
    except Exception as e:
        logger.error(f"❌ Model loading failed: {e}")
        return False

# Load model on startup
@app.on_event("startup")
async def startup_event():
    load_model()

@app.get("/api/v1/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    return HealthResponse(
        status="healthy",
        message="Stable Test Backend Running",
        model_loaded=model_instance is not None
    )

@app.post("/api/v1/analyze", response_model=AnalysisResult)
async def analyze_image(file: UploadFile = File(...)):
    """Analyze uploaded retinal image"""
    try:
        logger.info(f"🔍 Analyzing image: {file.filename}")
        
        if model_instance is None:
            raise HTTPException(status_code=503, detail="Model not loaded")
        
        # Read and process image
        content = await file.read()
        image = Image.open(io.BytesIO(content))
        
        if image.mode != 'RGB':
            image = image.convert('RGB')
        
        # Preprocess and predict
        input_tensor = transform(image).unsqueeze(0).to(device)
        
        with torch.no_grad():
            outputs = model_instance(input_tensor)
            probabilities = torch.softmax(outputs, dim=1)
        
        predicted_class = torch.argmax(probabilities, dim=1).item()
        confidence = probabilities[0][predicted_class].item()
        
        # Class labels
        class_labels = {0: "No DR", 1: "Mild", 2: "Moderate", 3: "Severe", 4: "Proliferative DR"}
        
        # Get all probabilities
        all_probs = {
            class_labels[i]: float(probabilities[0][i].item() * 100)
            for i in range(5)
        }
        
        # Create response
        analysis = {
            "patient_id": f"TEST_{hash(file.filename) % 1000:03d}",
            "analysis_timestamp": "2024-01-15T10:30:00Z",
            "image_quality": {"score": 0.95, "assessment": "Good quality"},
            "diabetic_retinopathy": {
                "stage": predicted_class,
                "stage_name": class_labels[predicted_class],
                "confidence": confidence,
                "description": f"AI analysis: {class_labels[predicted_class]} ({confidence*100:.1f}% confidence)"
            },
            "risk_assessment": {
                "progression_risk": "Low" if predicted_class < 2 else "Moderate" if predicted_class < 4 else "High",
                "recommended_followup": "12 months" if predicted_class < 2 else "6 months" if predicted_class < 4 else "1 month",
                "urgent_referral": predicted_class >= 3
            },
            "recommendations": [
                "Continue regular diabetic care",
                "Annual eye examination" if predicted_class < 2 else "Semi-annual examination" if predicted_class < 4 else "Urgent ophthalmology referral"
            ],
            "technical_details": {
                "model_version": "Custom Trained OpthalmoAI",
                "processing_time": "Real-time analysis",
                "image_resolution": f"{image.size[0]}x{image.size[1]}",
                "all_class_probabilities": all_probs
            }
        }
        
        logger.info(f"✅ Analysis complete: {class_labels[predicted_class]} ({confidence*100:.1f}%)")
        
        return AnalysisResult(
            success=True,
            analysis=analysis,
            message="Analysis completed using trained OpthalmoAI model"
        )
        
    except Exception as e:
        logger.error(f"❌ Analysis failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    print("🚀 Starting Stable Test Backend...")
    print("Server: http://localhost:8007")
    print("Health: http://localhost:8007/api/v1/health")
    print("Analysis: http://localhost:8007/api/v1/analyze")
    print("=" * 50)
    
    uvicorn.run(app, host="0.0.0.0", port=8007, log_level="info")