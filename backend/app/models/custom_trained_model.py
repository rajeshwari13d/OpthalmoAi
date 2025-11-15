"""
Custom Trained Model Integration for OpthalmoAI
This module handles loading and integration of user's trained diabetic retinopathy model
"""

import torch
import torch.nn as nn
import torchvision.transforms as transforms
from PIL import Image
import numpy as np
from typing import Dict, Tuple, Optional, List
import logging
import os
from pathlib import Path

logger = logging.getLogger(__name__)

class CustomTrainedModel:
    """
    Wrapper for user's custom trained diabetic retinopathy model
    """
    
    def __init__(self, model_path: str, architecture_file: Optional[str] = None):
        self.model_path = model_path
        self.architecture_file = architecture_file
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model = None
        self.model_loaded = False
        
        # Default DR classification labels (can be customized)
        self.class_labels = {
            0: "No DR",
            1: "Mild",
            2: "Moderate", 
            3: "Severe",
            4: "Proliferative DR"
        }
        
        # Default image preprocessing (can be customized)
        self.transform = transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            transforms.Normalize(
                mean=[0.485, 0.456, 0.406],
                std=[0.229, 0.224, 0.225]
            )
        ])
    
    def load_custom_architecture(self):
        """
        Load custom model architecture from OpthalmoAI.py
        Override this method based on your model architecture
        """
        try:
            if self.architecture_file and os.path.exists(self.architecture_file):
                # Import the custom architecture
                # This is a placeholder - you'll need to adapt based on your OpthalmoAI.py structure
                logger.info(f"Loading architecture from {self.architecture_file}")
                # Dynamically import the architecture module by path so we don't need package imports
                import importlib.util

                spec = importlib.util.spec_from_file_location("user_opthalmo_model", self.architecture_file)
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)

                # Try common class names
                for cls_name in ("OpthalmoAI", "OpthalmoAi", "OpthalmoModel", "Model", "Net", "DRModel"):
                    if hasattr(module, cls_name):
                        ModelClass = getattr(module, cls_name)
                        try:
                            model = ModelClass()
                            logger.info(f"Instantiated model class '{cls_name}' from architecture file")
                            return model
                        except TypeError:
                            # Try with num_classes argument
                            try:
                                model = ModelClass(num_classes=len(self.class_labels))
                                logger.info(f"Instantiated model class '{cls_name}' with num_classes from architecture file")
                                return model
                            except Exception:
                                logger.warning(f"Failed to instantiate '{cls_name}' with/without num_classes")

                logger.warning("No recognized model class found in architecture file; falling back to default architecture")
            
            # Fallback: Create a standard architecture that matches common trained models
            # This assumes your model follows a common pattern
            return self._create_default_architecture()
            
        except Exception as e:
            logger.error(f"Failed to load custom architecture: {e}")
            return self._create_default_architecture()
    
    def _create_default_architecture(self):
        """
        Create a default model architecture for diabetic retinopathy classification
        Modify this based on your actual model architecture
        """
        # This is a common architecture for DR classification
        # Replace with your actual model architecture
        
        # Example ResNet50-based model
        from torchvision import models
        model = models.resnet50(pretrained=False)
        # Use a simple final linear layer to match common saved checkpoints that use `fc.weight` / `fc.bias`
        in_features = model.fc.in_features
        model.fc = nn.Linear(in_features, len(self.class_labels))
        
        return model
    
    def load_model(self):
        """Load the trained model weights"""
        try:
            # Load model architecture
            self.model = self.load_custom_architecture()
            
            # Load trained weights
            if os.path.exists(self.model_path):
                checkpoint = torch.load(self.model_path, map_location=self.device)

                # Unpack checkpoint to state_dict where necessary
                state_dict = None
                if isinstance(checkpoint, dict):
                    if 'model_state_dict' in checkpoint:
                        state_dict = checkpoint['model_state_dict']
                    elif 'state_dict' in checkpoint:
                        state_dict = checkpoint['state_dict']
                    else:
                        # Could be a raw state_dict
                        state_dict = checkpoint
                elif hasattr(checkpoint, 'state_dict') and not isinstance(checkpoint, dict):
                    # It might be a saved nn.Module instance
                    try:
                        self.model = checkpoint
                        state_dict = None
                    except Exception:
                        state_dict = None

                # If we have a state_dict, try to load it with several fallbacks
                if isinstance(state_dict, dict):
                    # Strip 'module.' prefix from keys if present (DataParallel wrapper)
                    new_state = {}
                    for k, v in state_dict.items():
                        new_key = k
                        if k.startswith('module.'):
                            new_key = k[len('module.'):]
                        new_state[new_key] = v

                    # Try strict load first, then strict=False fallback
                    try:
                        self.model.load_state_dict(new_state, strict=True)
                        logger.info(f"✅ Loaded trained model weights (strict) from {self.model_path}")
                    except Exception as strict_err:
                        logger.warning(f"Strict load failed: {strict_err}. Trying non-strict load...")
                        try:
                            load_res = self.model.load_state_dict(new_state, strict=False)
                            logger.info(f"✅ Loaded trained model weights (non-strict) from {self.model_path}")
                            if hasattr(load_res, 'missing_keys') or hasattr(load_res, 'unexpected_keys'):
                                logger.debug(f"Load result: {load_res}")
                        except Exception as non_strict_err:
                            logger.error(f"Non-strict load also failed: {non_strict_err}")
                            # Give a helpful error message showing keys
                            model_keys = set(self.model.state_dict().keys())
                            ckpt_keys = set(new_state.keys())
                            missing = model_keys - ckpt_keys
                            unexpected = ckpt_keys - model_keys
                            logger.error(f"Missing keys in checkpoint: {sorted(list(missing))[:10]}{'...' if len(missing)>10 else ''}")
                            logger.error(f"Unexpected keys in checkpoint: {sorted(list(unexpected))[:10]}{'...' if len(unexpected)>10 else ''}")
                            raise RuntimeError(f"Failed to load state_dict for model. See logs for key differences.")
                else:
                    # If checkpoint was a full model (nn.Module), we already assigned it
                    if hasattr(self, 'model') and self.model is not None and not isinstance(state_dict, dict):
                        logger.info(f"✅ Loaded full model object from checkpoint {self.model_path}")
                    else:
                        logger.error(f"Checkpoint format not recognized for {self.model_path}")
                        raise RuntimeError("Unrecognized checkpoint format")

                logger.info(f"Loaded trained model weights from {self.model_path}")
            else:
                logger.error(f"❌ Model weights file not found: {self.model_path}")
                raise FileNotFoundError(f"Model file not found: {self.model_path}")
            
            self.model.to(self.device)
            self.model.eval()
            self.model_loaded = True
            
            logger.info(f"✅ Custom trained model loaded successfully on {self.device}")
            
        except Exception as e:
            logger.error(f"❌ Failed to load trained model: {e}")
            raise
    
    def preprocess_image(self, image: Image.Image) -> torch.Tensor:
        """
        Preprocess image for model input
        Customize this based on your model's preprocessing requirements
        """
        # Convert to RGB if necessary
        if image.mode != 'RGB':
            image = image.convert('RGB')
        
        # Apply transforms
        tensor = self.transform(image)
        
        # Add batch dimension
        tensor = tensor.unsqueeze(0)
        
        return tensor.to(self.device)
    
    def predict(self, image: Image.Image) -> Dict:
        """
        Make prediction using the trained model
        """
        if not self.model_loaded:
            raise RuntimeError("Model not loaded. Call load_model() first.")
        
        try:
            # Preprocess image
            input_tensor = self.preprocess_image(image)
            
            # Model inference
            with torch.no_grad():
                outputs = self.model(input_tensor)
                probabilities = torch.softmax(outputs, dim=1)
                
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
                "model_name": "Custom Trained OpthalmoAI",
                "model_path": self.model_path,
                "predicted_class": predicted_class,
                "predicted_label": self.class_labels[predicted_class],
                "confidence": round(confidence * 100, 2),
                "severity": severity,
                "class_probabilities": {k: round(v * 100, 2) for k, v in class_probs.items()},
                "recommendations": recommendations,
                "requires_urgent_care": predicted_class >= 3,
                "follow_up_months": self._get_follow_up_period(predicted_class)
            }
            
        except Exception as e:
            logger.error(f"Error during prediction: {e}")
            return {
                "error": f"Prediction failed: {str(e)}",
                "model_name": "Custom Trained OpthalmoAI"
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
    
    def _get_recommendations(self, predicted_class: int) -> List[str]:
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
    
    def update_class_labels(self, new_labels: Dict[int, str]):
        """Update class labels to match your training data"""
        self.class_labels = new_labels
        logger.info(f"Updated class labels: {new_labels}")
    
    def update_preprocessing(self, new_transform: transforms.Compose):
        """Update preprocessing pipeline"""
        self.transform = new_transform
        logger.info("Updated preprocessing pipeline")

def load_custom_trained_model(
    model_path: str, 
    architecture_file: Optional[str] = None,
    class_labels: Optional[Dict[int, str]] = None,
    preprocessing: Optional[transforms.Compose] = None
) -> CustomTrainedModel:
    """
    Factory function to load custom trained model
    
    Args:
        model_path: Path to your best_model.pth file
        architecture_file: Path to your OpthalmoAI.py file (optional)
        class_labels: Custom class labels (optional)
        preprocessing: Custom preprocessing pipeline (optional)
    
    Returns:
        CustomTrainedModel instance
    """
    model = CustomTrainedModel(model_path, architecture_file)
    
    if class_labels:
        model.update_class_labels(class_labels)
    
    if preprocessing:
        model.update_preprocessing(preprocessing)
    
    model.load_model()
    return model

# Configuration for trained models directory
TRAINED_MODELS_DIR = Path(__file__).parent / "trained_models"

def get_trained_model_path() -> str:
    """Get path to the trained model weights"""
    model_path = TRAINED_MODELS_DIR / "best_model.pth"
    return str(model_path)

def get_architecture_path() -> str:
    """Get path to the model architecture file"""
    # Support multiple possible filename capitalizations
    candidates = [
        TRAINED_MODELS_DIR / "OpthalmoAI.py",
        TRAINED_MODELS_DIR / "OpthalmoAi.py",
        TRAINED_MODELS_DIR / "opthalmoai.py",
    ]
    for c in candidates:
        if c.exists():
            return str(c)
    # Default to the canonical name
    return str(TRAINED_MODELS_DIR / "OpthalmoAI.py")

def is_trained_model_available() -> bool:
    """Check if trained model files are available"""
    model_path = Path(get_trained_model_path())
    return model_path.exists()