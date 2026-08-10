# timdr_complex_stack.py
# TIMDR – COMPLEX-STACK
# Składanka z:
# - STAR-CORE (figura + FFT + gradient)
# - TORUS-MAP (torus energii)
# - FIELD-SHEAR (ścinanie pola)
# - CORE-PULSE (puls jądra)
#
# Wyjście: jeden obraz, dwa panele:
#   góra  – kolejność Λ -> τ -> ρ (od figury do torusa)
#   dół   – kolejność τ -> ρ -> Λ (od torusa do figury)

from PIL import Image
import numpy as np

# --- wspólne pomocnicze ---

def _to_float_rgb(img):
    return np.asarray(img.convert("RGB"), dtype=np.float32) / 255.0

def _to_float_gray(img):
    return np.asarray(img.convert("L"), dtype=np.float32) / 255.0

def _from_float(arr):
    arr = np.clip(arr * 255.0, 0, 255).astype(np.uint8)
    return Image.fromarray(arr)

def _fft_mag(gray):
    F = np.fft.fft2(gray)
    Fshift = np.fft.fftshift(F)
    mag = np.log1p(np.abs(Fshift))
    mag /= mag.max() + 1e-8
    return mag

def _sobel(gray):
    kx = np.array([[-1,0,1],[-2,0,2],[-1,0,1]], dtype=np.float32)
    ky = np.array([[-1,-2,-1],[0,0,0],[1,2,1]], dtype=np.float32)

    def conv(img, k):
        h,w = img.shape
        p = np.pad(img, 1, mode="reflect")
        out = np.zeros_like(img)
        for y in range(h):
            for x in range(w):
                out[y,x] = np.sum(p[y:y+3, x:x+3] * k)
        return out

    gx = conv(gray, kx)
    gy = conv(gray, ky)
    g = np.sqrt(gx*gx + gy*gy)
    g /= g.max() + 1e-8
    return g

# --- warstwy TIMDR ---

def _layer_star_core(base_rgb, gray):
    figura = gray[...,None]              # Λ – jasność
    widmo  = _fft_mag(gray)[...,None]    # τ – widmo
    grad   = _sobel(gray)[...,None]      # ρ – struktura

    out = (
        0.50 * figura +
        0.35 * widmo +
        0.15 * grad
    )
    out = np.repeat(out, 3, axis=-1)
    return out

def _layer_torus_map(gray):
    mag = _fft_mag(gray)
    h, w = mag.shape
    cy, cx = h//2, w//2

    Y, X = np.ogrid[:h, :w]
    R = np.sqrt((Y-cy)**2 + (X-cx)**2)
    Rn = R / (R.max() + 1e-8)

    torus = mag * Rn
    torus /= torus.max() + 1e-8

    torus_rgb = np.stack([torus, torus, torus], axis=-1)
    return torus_rgb

def _layer_field_shear(gray):
    gx = np.gradient(gray, axis=1)
    gy = np.gradient(gray, axis=0)
    shear = np.abs(gx - gy)
    shear /= shear.max() + 1e-8
    rgb = np.stack([shear, shear, shear], axis=-1)
    return rgb

def _layer_core_pulse(gray):
    mag = _fft_mag(gray)
    hfreq = mag - np.mean(mag)
    hfreq = np.clip(hfreq, 0, None)
    hfreq /= hfreq.max() + 1e-8
    rgb = np.stack([hfreq, hfreq, hfreq], axis=-1)
    return rgb

# --- filtr główny ---

def timdr_complex_stack(img):
    base_rgb = _to_float_rgb(img)
    gray = (0.299*base_rgb[...,0] + 0.587*base_rgb[...,1] + 0.114*base_rgb[...,2])

    star_core = _layer_star_core(base_rgb, gray)
    torus     = _layer_torus_map(gray)
    shear     = _layer_field_shear(gray)
    pulse     = _layer_core_pulse(gray)

    # GÓRA: Λ -> τ -> ρ
    top = (
        0.40 * star_core +   # figura + FFT + gradient
        0.30 * torus +       # torus energii
        0.15 * shear +       # ścinanie pola
        0.15 * pulse         # puls jądra
    )

    # DÓŁ: τ -> ρ -> Λ (odwrócona logika)
    bottom = (
        0.40 * torus +
        0.30 * pulse +
        0.15 * shear +
        0.15 * star_core
    )

    top_img    = np.clip(top, 0, 1)
    bottom_img = np.clip(bottom, 0, 1)

    stacked = np.vstack([top_img, bottom_img])
    return _from_float(stacked)
