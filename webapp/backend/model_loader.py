from tensorflow.keras.models import load_model

def load_segmentation_model(model_path="../model/deeplabv3plus.keras"):
  model = load_model(model_path)
  return model
