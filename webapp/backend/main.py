from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from PIL import Image
import io
import base64
# import numpy as np

from model_loader import *
from predict import *

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

model = load_segmentation_model();

@app.post("/predict/")
async def predict_image(file: UploadFile = File(...), opacity: int = Form(...)):
  image_bytes = await file.read()
  image = Image.open(io.BytesIO(image_bytes)).convert("RGB")

  # Convertim imaginea originală (redimensionată) la PNG
  original_io = io.BytesIO()
  image.resize((256, 256)).save(original_io, format="PNG")
  original_base64 = base64.b64encode(original_io.getvalue()).decode()

  input_array = preprocess_image(image)
  prediction = model.predict(input_array)

  # Generăm mască simplă
  mask_img = postprocess_mask(prediction)
  mask_io = io.BytesIO()
  mask_img.save(mask_io, format="PNG")
  mask_base64 = base64.b64encode(mask_io.getvalue()).decode()

  # Suprapunere
  overlay_img = overlay_mask_on_image(prediction, image, opacity)
  overlay_io = io.BytesIO()
  overlay_img.save(overlay_io, format="PNG")
  overlay_base64 = base64.b64encode(overlay_io.getvalue()).decode()

  return JSONResponse({
    "original": original_base64,
    "mask": mask_base64,
    "overlay": overlay_base64
  })

