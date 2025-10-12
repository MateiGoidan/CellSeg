import os
import random
from PIL import Image
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import numpy as np

# === CONFIG ===

IMG_DIR = "../../microscopy/ds1/train/img/cls/"
MASK_DIR = "../../microscopy/ds1/train/mult_mask/cls/"
OUTPUT_PDF = "urinary_cell_grid.pdf"
NUM_SAMPLES = 3

# === SELECT RANDOM SAMPLES ===
image_files = sorted([f for f in os.listdir(IMG_DIR) if f.endswith(".tif")])
mask_files = sorted([f for f in os.listdir(MASK_DIR) if f.endswith(".tif")])
paired = list(zip(image_files, mask_files))

if len(paired) < NUM_SAMPLES:
  raise ValueError("Not enough samples found.")

samples = random.sample(paired, NUM_SAMPLES)

# === PLOT IN GRID ===
fig, axes = plt.subplots(2, NUM_SAMPLES, figsize=(4 * NUM_SAMPLES, 8))

for i, (img_name, mask_name) in enumerate(samples):
  img_path = os.path.join(IMG_DIR, img_name)
  mask_path = os.path.join(MASK_DIR, mask_name)

  img = Image.open(img_path).convert("L")
  mask = Image.open(mask_path)
  mask_np = np.array(mask)

  # Imagine originală
  axes[0, i].imshow(img, cmap='gray')
  axes[0, i].set_title(f"Image {i+1}")
  axes[0, i].axis('off')

  # Masca cu colormap și interpolare clară
  im = axes[1, i].imshow(mask_np, cmap='nipy_spectral', interpolation='nearest')
  axes[1, i].set_title(f"Multiclass Mask {i+1}")
  axes[1, i].axis('off')

# Adaugă bara de culoare pentru întreaga linie de măști
cbar_ax = fig.add_axes([0.92, 0.1, 0.02, 0.35])
fig.colorbar(im, cax=cbar_ax)

plt.tight_layout(rect=[0, 0, 0.9, 1])
plt.savefig(OUTPUT_PDF)
print(f"PDF saved as: {OUTPUT_PDF}")
