# timdr_migotowiec_heavy.py
# TIMDR „Migotowiec” – ciężki filtr strukturalno‑widmowy
# Uwaga: wymaga dużej mocy obliczeniowej (FFT + gradienty na całym obrazie)

from PIL import Image
import numpy as np
import sys
from pathlib import Path


def _to_float_array(img: Image.Image) -> np.ndarray:
    arr = np.asarray(img.convert("RGB"), dtype=np.float32) / 255.0
    return arr


def _from_float_array(arr: np.ndarray) -> Image.Image:
    arr = np.clip(arr * 255.0, 0, 255).astype(np.uint8)
    return Image.fromarray(arr)


def _fft_layer(arr: np.ndarray) -> np.ndarray:
    # widmo amplitudowe per kanał
    fft = np.fft.fft2(arr, axes=(0, 1))
    fft_shift = np.fft.fftshift(fft, axes=(0, 1))
    mag = np.log1p(np.abs(fft_shift))
    mag /= (mag.max(axis=(0, 1), keepdims=True) + 1e-8)
    return mag


def _sobel_gradients(gray: np.ndarray) -> np.ndarray:
    # proste Sobele 3x3
    kx = np.array([[-1, 0, 1],
                   [-2, 0, 2],
                   [-1, 0, 1]], dtype=np.float32)
    ky = np.array([[-1, -2, -1],
                   [ 0,  0,  0],
                   [ 1,  2,  1]], dtype=np.float32)

    def conv2(img, k):
        h, w = img.shape
        kh, kw = k.shape
        pad_h, pad_w = kh // 2, kw // 2
        padded = np.pad(img, ((pad_h, pad_h), (pad_w, pad_w)), mode="reflect")
        out = np.zeros_like(img, dtype=np.float32)
        for y in range(h):
            ys = y
            ye = y + kh
            for x in range(w):
                xs = x
                xe = x + kw
                region = padded[ys:ye, xs:xe]
                out[y, x] = np.sum(region * k)
        return out

    gx = conv2(gray, kx)
    gy = conv2(gray, ky)
    g = np.sqrt(gx * gx + gy * gy)
    g /= (g.max() + 1e-8)
    return g


def _laplace(gray: np.ndarray) -> np.ndarray:
    k = np.array([[0,  1, 0],
                  [1, -4, 1],
                  [0,  1, 0]], dtype=np.float32)

    def conv2(img, k):
        h, w = img.shape
        kh, kw = k.shape
        pad_h, pad_w = kh // 2, kw // 2
        padded = np.pad(img, ((pad_h, pad_h), (pad_w, pad_w)), mode="reflect")
        out = np.zeros_like(img, dtype=np.float32)
        for y in range(h):
            ys = y
            ye = y + kh
            for x in range(w):
                xs = x
                xe = x + kw
                region = padded[ys:ye, xs:xe]
                out[y, x] = np.sum(region * k)
        return out

    l = conv2(gray, k)
    l = np.abs(l)
    l /= (l.max() + 1e-8)
    return l


def timdr_migotowiec(img: Image.Image) -> Image.Image:
    base = _to_float_array(img)
    h, w, _ = base.shape

    # figura – samo wejście
    figura = base.copy()

    # widmo – FFT per kanał
    widmo = _fft_layer(base)

    # liczba – jasność (luminancja)
    gray = (0.299 * base[..., 0] +
            0.587 * base[..., 1] +
            0.114 * base[..., 2])
    liczba = gray[..., None]

    # dynamika – normalizowana lokalna rozpiętość (min/max w oknie)
    # uproszczona: globalny kontrast
    dyn = (base - base.min(axis=(0, 1), keepdims=True)) / (
        base.max(axis=(0, 1), keepdims=True) - base.min(axis=(0, 1), keepdims=True) + 1e-8
    )

    # gradient + laplace – struktura krawędziowa
    grad = _sobel_gradients(gray)
    lap = _laplace(gray)
    struktura = np.stack([grad, lap, grad], axis=-1)

    # miks warstw – „migotowiec”
    # wagi można korygować
    w_fig = 0.35
    w_fft = 0.25
    w_num = 0.10
    w_dyn = 0.15
    w_str = 0.15

    out = (
        w_fig * figura +
        w_fft * widmo +
        w_num * liczba +
        w_dyn * dyn +
        w_str * struktura
    )

    return _from_float_array(out)


def main():
    if len(sys.argv) < 3:
        print("Użycie: python timdr_migotowiec_heavy.py wejście.jpg wyjście.png")
        sys.exit(1)

    in_path = Path(sys.argv[1])
    out_path = Path(sys.argv[2])

    img = Image.open(in_path)
    out = timdr_migotowiec(img)
    out.save(out_path)
    print(f"Zapisano migotowca do: {out_path}")


if __name__ == "__main__":
    main()
