"""
Enhanced Model Loader for OpthalmoAI
Import enhanced model loader with custom trained model support
"""

from app.models.enhanced_model_loader import OpthalmoAIModelLoader

# For backward compatibility
EnsembleModelLoader = OpthalmoAIModelLoader

# Global model loader instance (uses enhanced loader with custom model support)
model_loader = OpthalmoAIModelLoader()