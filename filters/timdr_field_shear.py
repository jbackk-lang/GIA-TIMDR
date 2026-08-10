# timdr_field_shear.py
# TIMDR – FIELD-SHEAR
# Ścinanie pola: różnica kierunkowa gradientów

from PIL import Image
import numpy as np

def _to_float(img):
    return np.asarray(img.convert("L"), dtype=np.float32) / 255.0

def timdr_field_shear(img):
    g = _to_float(img)

    # gradienty kierunkowe
    gx = np.gradient(g, axis=1)
    gy = np.gradient(g, axis=0)

    # ścinanie = |gx - gy|
    shear = np.abs(gx - gy)
    shear /= shear.max() + 1e-8

    rgb = np.stack([shear, shear, shear], axis=-1)
    rgb = (rgb * 255).astype(np.uint8)
    return Image.fromarray(rgb)
