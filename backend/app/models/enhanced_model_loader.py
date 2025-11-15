"""
Enhanced Model Loader with Custom Trained Model Support
Supports user's trained diabetic retinopathy model alongside ResNet50 and VGG16
"""

import torch
import torch.nn as nn
import torchvision.transforms as transforms
import torchvision.models as models
from PIL import Image
import numpy as np
import cv2
import os
import logging
from typing import Dict, Tuple, Optional, Union
import time

from app.core.config import settings
from app.core.schemas import DiabeticRetinopathyStage, RiskLevel, AnalysisResult
from app.models.resnet50_model import ResNet50Predictor, load_resnet50_model
from app.models.vgg16_model import VGG16Predictor, load_vgg16_model
from app.models.custom_trained_model import (
    CustomTrainedModel, 
    load_custom_trained_model,
    is_trained_model_available,
    get_trained_model_path,
    get_architecture_path
)

logger = logging.getLogger(__name__)

class OpthalmoAIModelLoader:
    """
    Enhanced model loader that prioritizes user's trained model
    Falls back to ResNet50 + VGG16 ensemble if trained model not available
    """
    
    def __init__(self):
        self.custom_model: Optional[CustomTrainedModel] = None
        self.resnet50_model: Optional[ResNet50Predictor] = None
        self.vgg16_model: Optional[VGG16Predictor] = None
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.models_loaded = False
        self.use_custom_model = False
        self.ensemble_mode = True
        
    def load_model(self):
        """Load models with priority: Custom Trained > Ensemble (ResNet50 + VGG16)"""
        return self.load_models()
    
    def load_models(self):
        """Load models with priority: Custom Trained > Ensemble (ResNet50 + VGG16)"""
        try:
            # Check if user's trained model is available
            if is_trained_model_available():
                logger.info("🎯 User's trained model detected! Loading custom model...")
                self._load_custom_trained_model()
            else:
                logger.info("📋 No custom model found. Loading ResNet50 + VGG16 ensemble...")
                self._load_ensemble_models()
            
            self.models_loaded = True
            logger.info(f"✅ Models loaded successfully on {self.device}")
            
        except Exception as e:
            logger.error(f"❌ Error loading models: {str(e)}")
            # Final fallback
            self._load_fallback_model()
    
    def _load_custom_trained_model(self):
        """Load user's custom trained model"""
        try:
            model_path = get_trained_model_path()
            architecture_path = get_architecture_path()
            
            # Check if architecture file exists
            arch_file = architecture_path if os.path.exists(architecture_path) else None
            
            self.custom_model = load_custom_trained_model(
                model_path=model_path,
                architecture_file=arch_file
            )
            
            self.use_custom_model = True
            logger.info("✅ Custom trained model loaded successfully!")
            logger.info(f"   📁 Model weights: {model_path}")
            if arch_file:
                logger.info(f"   📁 Architecture: {arch_file}")
            
        except Exception as e:
            logger.error(f"❌ Failed to load custom model: {e}")
            logger.info("🔄 Falling back to ensemble models...")
            self._load_ensemble_models()
    
    def _load_ensemble_models(self):
        """Load ResNet50 + VGG16 ensemble models"""
        try:
            # Load ResNet50 model
            resnet_weights_path = os.path.join(settings.MODEL_PATH, "resnet50_dr_weights.pth") if hasattr(settings, 'MODEL_PATH') else None
            self.resnet50_model = load_resnet50_model(model_path=resnet_weights_path, device=str(self.device))
            logger.info("✅ ResNet50 model loaded")
            
            # Load VGG16 model  
            vgg_weights_path = os.path.join(settings.MODEL_PATH, "vgg16_dr_weights.pth") if hasattr(settings, 'MODEL_PATH') else None
            self.vgg16_model = load_vgg16_model(model_path=vgg_weights_path, device=str(self.device))
            logger.info("✅ VGG16 model loaded")
            
            self.use_custom_model = False
            logger.info("✅ Ensemble models loaded successfully")
            
        except Exception as e:
            logger.error(f"❌ Failed to load ensemble models: {e}")
            self._load_fallback_model()
    
    def _load_fallback_model(self):
        """Final fallback - load single ResNet50 model"""
        try:
            self.resnet50_model = load_resnet50_model(device=str(self.device))
            self.ensemble_mode = False
            self.use_custom_model = False
            logger.info("✅ Fallback ResNet50 model loaded")
            
        except Exception as e:
            logger.error(f"❌ All model loading failed: {e}")
            raise RuntimeError("Failed to load any models")
    
    def get_model_info(self) -> Dict:
        """Get information about loaded models"""
        info = {
            "models_loaded": self.models_loaded,
            "device": str(self.device),
            "use_custom_model": self.use_custom_model,
            "ensemble_mode": self.ensemble_mode and not self.use_custom_model
        }
        
        if self.use_custom_model and self.custom_model:
            info.update({
                "primary_model": "Custom Trained OpthalmoAI",
                "model_path": get_trained_model_path(),
                "architecture_available": os.path.exists(get_architecture_path()),
                "custom_model_loaded": True
            })
        else:
            info.update({
                "primary_model": "ResNet50 + VGG16 Ensemble" if self.ensemble_mode else "ResNet50",
                "models": {
                    "resnet50": self.resnet50_model is not None,
                    "vgg16": self.vgg16_model is not None,
                    "custom": False
                }
            })
        
        return info
    
    def predict(self, image: Image.Image) -> AnalysisResult:
        """Make prediction using the best available model"""
        if not self.models_loaded:
            raise RuntimeError("Models not loaded")
        
        start_time = time.time()
        
        try:
            if self.use_custom_model and self.custom_model:
                # Use custom trained model
                prediction_result = self.custom_model.predict(image)
                model_name = "Custom Trained OpthalmoAI"
            else:
                # Use ensemble or fallback model
                prediction_result = self._ensemble_predict(image)
                model_name = prediction_result.get("model_name", "Ensemble")
            
            if "error" in prediction_result:
                raise RuntimeError(f"Prediction failed: {prediction_result['error']}")
            
            # Extract results
            predicted_class = prediction_result["predicted_class"]
            confidence = prediction_result["confidence"]
            
            # Create analysis result
            stage = DiabeticRetinopathyStage(predicted_class)
            stage_description = self._get_stage_description(predicted_class)
            risk_level = self._get_risk_level(predicted_class, confidence)
            recommendations = prediction_result.get("recommendations", self._get_recommendations(predicted_class, risk_level))
            processing_time = time.time() - start_time
            
            return AnalysisResult(
                stage=stage,
                stage_description=stage_description,
                confidence=round(confidence, 2),
                risk_level=risk_level,
                recommendations=recommendations,
                processing_time=round(processing_time, 3),
                model_info={
                    "model_name": model_name,
                    "use_custom_model": self.use_custom_model,
                    "model_path": get_trained_model_path() if self.use_custom_model else None,
                    "prediction_details": prediction_result
                }
            )
            
        except Exception as e:
            logger.error(f"Error during prediction: {str(e)}")
            raise
    
    def _ensemble_predict(self, image: Image.Image) -> Dict:
        """Ensemble prediction using ResNet50 and VGG16"""
        predictions = []
        
        # Get ResNet50 prediction
        if self.resnet50_model:
            resnet_result = self.resnet50_model.predict(image)
            if "error" not in resnet_result:
                predictions.append(resnet_result)
        
        # Get VGG16 prediction
        if self.vgg16_model and self.ensemble_mode:
            vgg_result = self.vgg16_model.predict(image)
            if "error" not in vgg_result:
                predictions.append(vgg_result)
        
        if not predictions:
            raise RuntimeError("No successful predictions from any model")
        
        # If only one prediction available, return it
        if len(predictions) == 1:
            return predictions[0]
        
        # Ensemble prediction: Average probabilities
        ensemble_probs = {}
        for pred in predictions:
            for class_name, prob in pred["class_probabilities"].items():
                if class_name not in ensemble_probs:
                    ensemble_probs[class_name] = []
                ensemble_probs[class_name].append(prob / 100.0)  # Convert to 0-1 range
        
        # Average probabilities
        averaged_probs = {}
        for class_name, prob_list in ensemble_probs.items():
            averaged_probs[class_name] = np.mean(prob_list)
        
        # Find predicted class
        predicted_class_name = max(averaged_probs, key=averaged_probs.get)
        
        # Map class names back to IDs
        class_labels = {
            "No DR": 0,
            "Mild": 1,
            "Moderate": 2,
            "Severe": 3,
            "Proliferative DR": 4
        }
        
        predicted_class = class_labels.get(predicted_class_name, 0)
        ensemble_confidence = averaged_probs[predicted_class_name] * 100
        
        return {
            "model_name": "ResNet50 + VGG16 Ensemble",
            "predicted_class": predicted_class,
            "predicted_label": predicted_class_name,
            "confidence": round(ensemble_confidence, 2),
            "class_probabilities": {k: round(v * 100, 2) for k, v in averaged_probs.items()},
            "individual_predictions": predictions,
            "requires_urgent_care": predicted_class >= 3,
            "follow_up_months": min([pred.get("follow_up_months", 6) for pred in predictions])
        }
    
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

# Global model loader instance
model_loader = OpthalmoAIModelLoader()