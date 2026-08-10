# timdr_star_core.py
# TIMDR – STAR‑CORE
# Filtr do analizy pojedynczego źródła światła (gwiazdy)
# Wyciąga: figura (jasność), widmo (FFT), struktura (gradient)

from PIL import Image
import numpy as np

def _to_float(img):
    return np.asarray(img.convert("RGB"), dtype=np.float32) / 255.0

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

def timdr_star_core(img):
    base = _to_float(img)
    gray = (0.299*base[...,0] + 0.587*base[...,1] + 0.114*base[...,2])

    figura = gray[...,None]              # jasność gwiazdy
    widmo = _fft_mag(gray)[...,None]     # widmo częstotliwości
    struktura = _sobel(gray)[...,None]   # gradient pola

    out = (
        0.50 * figura +
        0.35 * widmo +
        0.15 * struktura
    )

    return _from_float(out)
