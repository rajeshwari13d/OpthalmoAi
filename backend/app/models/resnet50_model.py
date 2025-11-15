"""
ResNet50 Model for Diabetic Retinopathy Detection
Implements pre-trained ResNet50 with custom classifier for 5-class DR classification
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

class DiabeticRetinopathyResNet50(nn.Module):
    """
    ResNet50 model for diabetic retinopathy classification
    Classes: 0=No DR, 1=Mild, 2=Moderate, 3=Severe, 4=Proliferative DR
    """
    
    def __init__(self, num_classes: int = 5, pretrained: bool = True):
        super(DiabeticRetinopathyResNet50, self).__init__()
        
        # Load pre-trained ResNet50
        self.backbone = models.resnet50(pretrained=pretrained)
        
        # Replace the final fully connected layer
        num_features = self.backbone.fc.in_features
        self.backbone.fc = nn.Sequential(
            nn.Dropout(0.5),
            nn.Linear(num_features, 512),
            nn.ReLU(inplace=True),
            nn.Dropout(0.3),
            nn.Linear(512, num_classes)
        )
        
        # Freeze early layers for fine-tuning approach
        self._freeze_early_layers()
        
    def _freeze_early_layers(self):
        """Freeze early layers to preserve pre-trained features"""
        # Freeze conv1, bn1, and first 2 residual blocks
        for param in self.backbone.conv1.parameters():
            param.requires_grad = False
        for param in self.backbone.bn1.parameters():
            param.requires_grad = False
        for param in self.backbone.layer1.parameters():
            param.requires_grad = False
        for param in self.backbone.layer2.parameters():
            param.requires_grad = False
            
    def forward(self, x):
        return self.backbone(x)

class ResNet50Predictor:
    """
    ResNet50 predictor for diabetic retinopathy detection
    """
    
    def __init__(self, model_path: Optional[str] = None, device: str = 'cpu'):
        self.device = torch.device(device if torch.cuda.is_available() else 'cpu')
        self.model = DiabeticRetinopathyResNet50(num_classes=5)
        
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
        
        # Image preprocessing pipeline
        self.transform = transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.CenterCrop(224),
            transforms.ToTensor(),
            transforms.Normalize(
                mean=[0.485, 0.456, 0.406],
                std=[0.229, 0.224, 0.225]
            )
        ])
        
    def preprocess_image(self, image: Image.Image) -> torch.Tensor:
        """
        Preprocess PIL Image for model input
        
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
        Predict diabetic retinopathy from retinal image
        
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
                "model_name": "ResNet50",
                "predicted_class": predicted_class,
                "predicted_label": self.class_labels[predicted_class],
                "risk_level": self.risk_levels[predicted_class],
                "confidence": round(confidence * 100, 2),
                "severity": severity,
                "class_probabilities": {k: round(v * 100, 2) for k, v in class_probs.items()},
                "recommendations": recommendations,
                "requires_urgent_care": predicted_class >= 3,
                "follow_up_months": self._get_follow_up_period(predicted_class)
            }
            
        except Exception as e:
            logger.error(f"Error during ResNet50 prediction: {e}")
            return {
                "error": f"Prediction failed: {str(e)}",
                "model_name": "ResNet50"
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
        """Get medical recommendations based on prediction"""
        recommendations_map = {
            0: [
                "Continue regular eye exams",
                "Maintain good diabetes control",
                "Monitor blood sugar levels regularly"
            ],
            1: [
                "Schedule follow-up in 12 months",
                "Optimize diabetes management",
                "Monitor blood pressure and cholesterol"
            ],
            2: [
                "Schedule follow-up in 6-12 months",
                "Consider ophthalmologist referral",
                "Strict diabetes control recommended"
            ],
            3: [
                "Urgent ophthalmologist referral needed",
                "Follow-up in 2-4 months",
                "Intensive diabetes management required"
            ],
            4: [
                "Immediate ophthalmologist consultation required",
                "Consider laser therapy or surgery",
                "Monthly monitoring recommended"
            ]
        }
        return recommendations_map.get(predicted_class, ["Consult healthcare provider"])
    
    def _get_follow_up_period(self, predicted_class: int) -> int:
        """Get recommended follow-up period in months"""
        follow_up_map = {
            0: 12,  # Annual screening
            1: 12,  # Annual screening
            2: 6,   # Semi-annual
            3: 3,   # Quarterly
            4: 1    # Monthly
        }
        return follow_up_map.get(predicted_class, 6)

def load_resnet50_model(model_path: Optional[str] = None, device: str = 'cpu') -> ResNet50Predictor:
    """
    Factory function to load ResNet50 model
    
    Args:
        model_path: Path to trained model weights (optional)
        device: Device to load model on
        
    Returns:
        ResNet50Predictor instance
    """
    return ResNet50Predictor(model_path=model_path, device=device)