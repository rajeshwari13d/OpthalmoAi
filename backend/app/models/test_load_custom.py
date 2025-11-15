from app.models.custom_trained_model import get_trained_model_path, get_architecture_path, load_custom_trained_model

print('Model path:', get_trained_model_path())
print('Arch path:', get_architecture_path())

try:
    model_wrapper = load_custom_trained_model(get_trained_model_path(), architecture_file=get_architecture_path())
    print('Model loaded:', model_wrapper.model_loaded)
    print('Model device:', model_wrapper.device)
except Exception as e:
    print('Error loading model:', e)
