"""Strumieniowy czytnik MAT v5 z obiektem MCOS (tabela MATLAB) -- bez ladowania calosci do pamieci.
Szuka duzych tablic numerycznych (double, zespolone) w __function_workspace__ i oddaje je kawalkami."""
import struct, zlib

class Raw:
    def __init__(self, f): self.f = f
    def read(self, n):
        b = self.f.read(n)
        if len(b) < n: raise EOFError
        return b

class Bounded:
    def __init__(self, src, n): self.src, self.left = src, n
    def read(self, n):
        if n > self.left: raise EOFError
        self.left -= n; return self.src.read(n)


class Z:
    """Strumien zdekompresowany z innego strumienia (miCOMPRESSED o dlugosci nbytes)."""
    def __init__(self, src, nbytes):
        self.src, self.left, self.d, self.buf = src, nbytes, zlib.decompressobj(), bytearray()
    def read(self, n):
        while len(self.buf) < n:
            if self.left <= 0:
                self.buf += self.d.flush()
                if len(self.buf) < n: raise EOFError
                break
            k = min(1 << 20, self.left); self.left -= k; self.buf += self.d.decompress(self.src.read(k))
        out = bytes(self.buf[:n]); del self.buf[:n]; return out

LAST_SMALL = [b""]


def tag(s):
    raw = s.read(8); t, n = struct.unpack('<II', raw)
    if t >> 16:                      # maly element: 8 bajtow = znacznik (2+2) + dane (4), nic wiecej do czytania
        LAST_SMALL[0] = raw[4:]
        return t & 0xffff, t >> 16, True
    return t, n, False

def skip(s, n):
    while n > 0:
        k = min(1 << 22, n); s.read(k); n -= k

def pad(n): return (8 - n % 8) % 8

def matrix(s, nbytes, on_array, depth=0):
    """Parsuje miMATRIX generycznie: flagi, potem podelementy; duze tablice double -> on_array."""
    used = 0; cplx = False; dims = None; first = True
    while used < nbytes:
        t, n, small = tag(s); used += 8
        if small:
            b = LAST_SMALL[0]
            if t == 5 and dims is None and not first: dims = struct.unpack('<%di' % (n // 4), b[:n])
            first = False; continue
        body = n + pad(n); used += body
        if first and t == 6:                    # array flags (miUINT32)
            b = s.read(body); cplx = bool(b[1] & 0x08); first = False; continue
        first = False
        if t == 5 and dims is None:
            b = s.read(body); dims = struct.unpack('<%di' % (n // 4), b[:n]); continue
        if t == 14:
            matrix(s, n, on_array, depth + 1); skip(s, pad(n))
        elif t == 15:
            walk_stream(Z(s, n), on_array, depth + 1); skip(s, pad(n))
        elif t == 9 and n >= 8_000_000:
            on_array(s, dims, cplx, n); skip(s, pad(n))
        elif t == 2 and n > 1_000_000:          # uint8 = zagniezdzony workspace MAT
            b = Bounded(s, n); b.read(8); walk_stream(b, on_array, depth + 1); skip(s, b.left + pad(n))
        else:
            skip(s, body)

def walk_stream(s, on_array, depth=0):
    while True:
        try:
            t, n, small = tag(s)
        except EOFError:
            return
        if small:
            continue
        if t == 14:
            matrix(s, n, on_array, depth); skip(s, pad(n))
        elif t == 15:
            walk_stream(Z(s, n), on_array, depth + 1)
        elif t == 2 and n > 1_000_000:          # uint8: zagniezdzony workspace MAT
            s.read(8); walk_stream(s, on_array, depth + 1)   # 8 bajtow naglowka wersji
        else:
            skip(s, n + pad(n))
