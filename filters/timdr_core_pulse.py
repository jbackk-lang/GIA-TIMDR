# timdr_core_pulse.py
# TIMDR – CORE-PULSE
# Puls jądra: analiza wysokich częstotliwości

from PIL import Image
import numpy as np

def _to_float(img):
    return np.asarray(img.convert("L"), dtype=np.float32) / 255.0

def _fft_mag(gray):
    F = np.fft.fft2(gray)
    Fshift = np.fft.fftshift(F)
    mag = np.log1p(np.abs(Fshift))
    mag /= mag.max() + 1e-8
    return mag

def timdr_core_pulse(img):
    gray = _to_float(img)
    mag = _fft_mag(gray)

    # wysokie częstotliwości = puls
    hfreq = mag - np.mean(mag)
    hfreq = np.clip(hfreq, 0, None)
    hfreq /= hfreq.max() + 1e-8

    rgb = np.stack([hfreq, hfreq, hfreq], axis=-1)
    rgb = (rgb * 255).astype(np.uint8)
    return Image.fromarray(rgb)
