import torch
import torch.nn as nn
import torchvision.transforms as transforms
import torchvision.models as models
from PIL import Image
import numpy as np
import cv2
import os
import logging
from typing import Dict, Tuple, Optional
import time

from app.core.config import settings
from app.core.schemas import DiabeticRetinopathyStage, RiskLevel, AnalysisResult

logger = logging.getLogger(__name__)

class ModelLoader:
    def __init__(self):
        self.model = None
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.transform = self._get_transform()
        self.model_loaded = False
        
    def _get_transform(self):
        """Get image preprocessing transform"""
        return transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], 
                               std=[0.229, 0.224, 0.225])
        ])
    
    def _create_model(self) -> nn.Module:
        """Create the model architecture"""
        if settings.MODEL_TYPE.lower() == "resnet50":
            model = models.resnet50(pretrained=True)
            model.fc = nn.Linear(model.fc.in_features, 5)  # 5 classes for DR stages
        elif settings.MODEL_TYPE.lower() == "vgg16":
            model = models.vgg16(pretrained=True)
            model.classifier[6] = nn.Linear(model.classifier[6].in_features, 5)
        else:
            raise ValueError(f"Unsupported model type: {settings.MODEL_TYPE}")
        
        return model
    
    def load_model(self):
        """Load the trained model"""
        try:
            self.model = self._create_model()
            
            # Try to load pre-trained weights if available
            if os.path.exists(settings.MODEL_PATH):
                state_dict = torch.load(settings.MODEL_PATH, map_location=self.device)
                self.model.load_state_dict(state_dict)
                logger.info(f"Loaded model weights from {settings.MODEL_PATH}")
            else:
                logger.warning(f"Model weights not found at {settings.MODEL_PATH}. Using pretrained ImageNet weights.")
            
            self.model.to(self.device)
            self.model.eval()
            self.model_loaded = True
            logger.info(f"Model loaded successfully on {self.device}")
            
        except Exception as e:
            logger.error(f"Error loading model: {str(e)}")
            raise
    
    def _preprocess_image(self, image: Image.Image) -> torch.Tensor:
        """Preprocess image for model inference"""
        # Convert to RGB if necessary
        if image.mode != 'RGB':
            image = image.convert('RGB')
        
        # Apply transforms
        tensor = self.transform(image)
        return tensor.unsqueeze(0)  # Add batch dimension
    
    def _get_stage_description(self, stage: int) -> str:
        """Get human-readable description for DR stage"""
        descriptions = {
            0: "No Diabetic Retinopathy",
            1: "Mild Non-proliferative Diabetic Retinopathy",
            2: "Moderate Non-proliferative Diabetic Retinopathy", 
            3: "Severe Non-proliferative Diabetic Retinopathy",
            4: "Proliferative Diabetic Retinopathy"
        }
        return descriptions.get(stage, "Unknown Stage")
    
    def _get_risk_level(self, stage: int, confidence: float) -> RiskLevel:
        """Determine risk level based on stage and confidence"""
        if stage == 0:
            return RiskLevel.LOW
        elif stage in [1, 2]:
            return RiskLevel.MODERATE if confidence > 70 else RiskLevel.LOW
        else:  # stage 3 or 4
            return RiskLevel.HIGH
    
    def _get_recommendations(self, stage: int, risk_level: RiskLevel) -> list:
        """Get clinical recommendations based on stage and risk"""
        base_recommendations = [
            "Maintain optimal blood glucose control",
            "Monitor blood pressure and cholesterol levels",
            "Follow a healthy diet and exercise regularly"
        ]
        
        stage_specific = {
            0: ["Continue regular eye exams annually"],
            1: [
                "Schedule eye exams every 6-12 months",
                "Monitor for progression"
            ],
            2: [
                "Schedule eye exams every 3-6 months",
                "Consider consultation with retinal specialist",
                "Monitor for signs of progression"
            ],
            3: [
                "Urgent consultation with retinal specialist required",
                "Schedule eye exams every 2-4 months",
                "May require laser treatment"
            ],
            4: [
                "Immediate referral to retinal specialist required",
                "May require urgent treatment (laser or surgery)",
                "Monitor closely for complications"
            ]
        }
        
        recommendations = base_recommendations + stage_specific.get(stage, [])
        
        if risk_level == RiskLevel.HIGH:
            recommendations.insert(0, "URGENT: Seek immediate ophthalmological consultation")
        
        return recommendations
    
    def predict(self, image: Image.Image) -> AnalysisResult:
        """Make prediction on image"""
        if not self.model_loaded:
            raise RuntimeError("Model not loaded")
        
        start_time = time.time()
        
        try:
            # Preprocess image
            input_tensor = self._preprocess_image(image).to(self.device)
            
            # Make prediction
            with torch.no_grad():
                outputs = self.model(input_tensor)
                probabilities = torch.softmax(outputs, dim=1)
                predicted_class = torch.argmax(probabilities, dim=1).item()
                confidence = probabilities[0][predicted_class].item() * 100
            
            # Create analysis result
            stage = DiabeticRetinopathyStage(predicted_class)
            stage_description = self._get_stage_description(predicted_class)
            risk_level = self._get_risk_level(predicted_class, confidence)
            recommendations = self._get_recommendations(predicted_class, risk_level)
            processing_time = time.time() - start_time
            
            return AnalysisResult(
                stage=stage,
                stage_description=stage_description,
                confidence=round(confidence, 2),
                risk_level=risk_level,
                recommendations=recommendations,
                processing_time=round(processing_time, 3)
            )
            
        except Exception as e:
            logger.error(f"Error during prediction: {str(e)}")
            raise

# Global model loader instance
model_loader = ModelLoader()