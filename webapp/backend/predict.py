import numpy as np
import matplotlib.cm as cm
from PIL import Image

def preprocess_image(image: Image.Image) -> np.ndarray:
    image = image.resize((256, 256))  # trebuie să corespundă dimensiunii de input
    img_array = (np.array(image) / 255.0) * 2.0 - 1.0  # Normalizează în [-1, 1]
    if img_array.ndim == 2:  # grayscale
        img_array = np.expand_dims(img_array, axis=-1)
    img_array = np.expand_dims(img_array, axis=0)  # (1, H, W, C)
    return img_array

def postprocess_mask(mask: np.ndarray) -> Image.Image:
    mask = np.argmax(mask[0], axis=-1).astype(np.uint8)
    print("[DEBUG] Mask unique values:", np.unique(mask))

    colormap = cm.get_cmap("viridis")
    colored_mask = colormap(mask / 7.0)[..., :3]  # RGB, fără alpha
    colored_mask = (colored_mask * 255).astype(np.uint8)
    return Image.fromarray(colored_mask)

def overlay_mask_on_image(mask: np.ndarray, original_image: Image.Image, opacity: int) -> Image.Image:
    pred_mask = np.argmax(mask[0], axis=-1).astype(np.uint8)

    colormap = cm.get_cmap("tab10")  
    mask_rgb = (colormap(pred_mask / 7.0)[..., :3] * 255).astype(np.uint8)

    alpha = (pred_mask > 0).astype(np.uint8) * 255  
    mask_rgba = np.dstack((mask_rgb, alpha))

    mask_img = Image.fromarray(mask_rgba, mode="RGBA")
    image_resized = original_image.resize((256, 256)).convert("RGBA")

    faded = image_resized.copy()
    faded_np = np.array(faded)
    faded_np[..., 3] = opacity
    faded = Image.fromarray(faded_np, mode="RGBA")

    overlay = Image.alpha_composite(faded, mask_img)

    return overlay
