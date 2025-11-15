"""
VGG16 Model for Diabetic Retinopathy Detection
Implements pre-trained VGG16 with custom classifier for 5-class DR classification
"""

import torch
import torch.nn as nn
import torch.nn.functional as F
from torchvision import models, transforms
from PIL import Image
import numpy as np
from typing import Dict, Tuple, Optional
import logging

logger = logging.getLogger(__name__)

class DiabeticRetinopathyVGG16(nn.Module):
    """
    VGG16 model for diabetic retinopathy classification
    Classes: 0=No DR, 1=Mild, 2=Moderate, 3=Severe, 4=Proliferative DR
    """
    
    def __init__(self, num_classes: int = 5, pretrained: bool = True):
        super(DiabeticRetinopathyVGG16, self).__init__()
        
        # Load pre-trained VGG16
        self.backbone = models.vgg16(pretrained=pretrained)
        
        # Replace the classifier
        num_features = self.backbone.classifier[6].in_features
        self.backbone.classifier[6] = nn.Sequential(
            nn.Dropout(0.5),
            nn.Linear(num_features, 1024),
            nn.ReLU(inplace=True),
            nn.Dropout(0.4),
            nn.Linear(1024, 512),
            nn.ReLU(inplace=True),
            nn.Dropout(0.3),
            nn.Linear(512, num_classes)
        )
        
        # Freeze early layers for fine-tuning approach
        self._freeze_early_layers()
        
    def _freeze_early_layers(self):
        """Freeze early convolutional layers to preserve pre-trained features"""
        # Freeze first 3 convolutional blocks
        for i, layer in enumerate(self.backbone.features):
            if i < 15:  # First 3 blocks of VGG16
                for param in layer.parameters():
                    param.requires_grad = False
            
    def forward(self, x):
        return self.backbone(x)

class VGG16Predictor:
    """
    VGG16 predictor for diabetic retinopathy detection
    """
    
    def __init__(self, model_path: Optional[str] = None, device: str = 'cpu'):
        self.device = torch.device(device if torch.cuda.is_available() else 'cpu')
        self.model = DiabeticRetinopathyVGG16(num_classes=5)
        
        # Load pre-trained weights if available
        if model_path and torch.cuda.is_available():
            try:
                self.model.load_state_dict(torch.load(model_path, map_location=self.device))
                logger.info(f"Loaded model weights from {model_path}")
            except Exception as e:
                logger.warning(f"Could not load model weights: {e}. Using pre-trained ImageNet weights.")
        
        self.model.to(self.device)
        self.model.eval()
        
        # Define class labels
        self.class_labels = {
            0: "No DR",
            1: "Mild",
            2: "Moderate", 
            3: "Severe",
            4: "Proliferative DR"
        }
        
        # Define risk levels
        self.risk_levels = {
            0: "No Diabetic Retinopathy",
            1: "Mild Non-proliferative DR",
            2: "Moderate Non-proliferative DR",
            3: "Severe Non-proliferative DR", 
            4: "Proliferative DR"
        }
        
        # Image preprocessing pipeline (VGG16 specific)
        self.transform = transforms.Compose([
            transforms.Resize((256, 256)),
            transforms.CenterCrop(224),
            transforms.ToTensor(),
            transforms.Normalize(
                mean=[0.485, 0.456, 0.406],
                std=[0.229, 0.224, 0.225]
            )
        ])
        
    def preprocess_image(self, image: Image.Image) -> torch.Tensor:
        """
        Preprocess PIL Image for VGG16 model input
        
        Args:
            image: PIL Image of retinal fundus
            
        Returns:
            Preprocessed tensor ready for model
        """
        # Convert to RGB if not already
        if image.mode != 'RGB':
            image = image.convert('RGB')
            
        # Apply transforms
        tensor = self.transform(image)
        
        # Add batch dimension
        tensor = tensor.unsqueeze(0)
        
        return tensor.to(self.device)
    
    def predict(self, image: Image.Image) -> Dict:
        """
        Predict diabetic retinopathy from retinal image using VGG16
        
        Args:
            image: PIL Image of retinal fundus
            
        Returns:
            Dictionary with prediction results
        """
        try:
            # Preprocess image
            input_tensor = self.preprocess_image(image)
            
            # Model inference
            with torch.no_grad():
                outputs = self.model(input_tensor)
                probabilities = F.softmax(outputs, dim=1)
                
            # Get predictions
            predicted_class = torch.argmax(probabilities, dim=1).item()
            confidence = probabilities[0][predicted_class].item()
            
            # Get all class probabilities
            class_probs = {
                self.class_labels[i]: probabilities[0][i].item() 
                for i in range(len(self.class_labels))
            }
            
            # Determine severity and recommendations
            severity = self._get_severity_level(predicted_class)
            recommendations = self._get_recommendations(predicted_class)
            
            return {
                "model_name": "VGG16",
                "predicted_class": predicted_class,
                "predicted_label": self.class_labels[predicted_class],
                "risk_level": self.risk_levels[predicted_class],
                "confidence": round(confidence * 100, 2),
                "severity": severity,
                "class_probabilities": {k: round(v * 100, 2) for k, v in class_probs.items()},
                "recommendations": recommendations,
                "requires_urgent_care": predicted_class >= 3,
                "follow_up_months": self._get_follow_up_period(predicted_class),
                "detailed_analysis": self._get_detailed_analysis(predicted_class, confidence)
            }
            
        except Exception as e:
            logger.error(f"Error during VGG16 prediction: {e}")
            return {
                "error": f"Prediction failed: {str(e)}",
                "model_name": "VGG16"
            }
    
    def _get_severity_level(self, predicted_class: int) -> str:
        """Get severity level description"""
        severity_map = {
            0: "None",
            1: "Mild",
            2: "Moderate",
            3: "Severe",
            4: "Very Severe"
        }
        return severity_map.get(predicted_class, "Unknown")
    
    def _get_recommendations(self, predicted_class: int) -> list:
        """Get medical recommendations based on VGG16 prediction"""
        recommendations_map = {
            0: [
                "Continue routine diabetic care",
                "Annual dilated eye examination",
                "Maintain optimal glycemic control"
            ],
            1: [
                "Schedule ophthalmology follow-up in 12 months",
                "Optimize diabetes management with HbA1c < 7%",
                "Blood pressure control recommended"
            ],
            2: [
                "Ophthalmology referral within 6 months",
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
    
    def _get_follow_up_period(self, predicted_class: int) -> int:
        """Get recommended follow-up period in months"""
        follow_up_map = {
            0: 12,  # Annual screening
            1: 12,  # Annual screening
            2: 6,   # Semi-annual
            3: 2,   # Every 2 months
            4: 1    # Monthly
        }
        return follow_up_map.get(predicted_class, 6)
    
    def _get_detailed_analysis(self, predicted_class: int, confidence: float) -> Dict:
        """Get detailed analysis based on prediction"""
        analysis_map = {
            0: {
                "findings": "No signs of diabetic retinopathy detected",
                "features": "Normal retinal vasculature and absence of DR lesions",
                "risk_factors": "Continue diabetes monitoring"
            },
            1: {
                "findings": "Mild non-proliferative diabetic retinopathy",
                "features": "Microaneurysms present, few retinal hemorrhages",
                "risk_factors": "Early stage DR, manageable with good diabetes control"
            },
            2: {
                "findings": "Moderate non-proliferative diabetic retinopathy",
                "features": "Multiple microaneurysms, hemorrhages, and hard exudates",
                "risk_factors": "Progressive DR requiring closer monitoring"
            },
            3: {
                "findings": "Severe non-proliferative diabetic retinopathy",
                "features": "Extensive hemorrhages, cotton wool spots, venous changes",
                "risk_factors": "High risk of progression to proliferative DR"
            },
            4: {
                "findings": "Proliferative diabetic retinopathy",
                "features": "Neovascularization, fibrous proliferation",
                "risk_factors": "Advanced DR requiring immediate intervention"
            }
        }
        
        analysis = analysis_map.get(predicted_class, {
            "findings": "Unable to determine",
            "features": "Analysis incomplete",
            "risk_factors": "Consult healthcare provider"
        })
        
        analysis["confidence_level"] = "High" if confidence > 0.8 else "Medium" if confidence > 0.6 else "Low"
        return analysis

def load_vgg16_model(model_path: Optional[str] = None, device: str = 'cpu') -> VGG16Predictor:
    """
    Factory function to load VGG16 model
    
    Args:
        model_path: Path to trained model weights (optional)
        device: Device to load model on
        
    Returns:
        VGG16Predictor instance
    """
    return VGG16Predictor(model_path=model_path, device=device)