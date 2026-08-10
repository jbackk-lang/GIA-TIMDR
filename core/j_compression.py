# ============================================================
#   J–COMPRESSION MODULE (TIMDR / Λ–τ–ρ / Twist Operator)
# ============================================================
#
# NAPRAWA: poprzednia wersja "kompresji" (j_core_reduce + prefiks MAGIC)
# była odwracalnym kodowaniem XOR-delta, które NIE zmniejszało rozmiaru
# danych — wynik był o 5 bajtów WIĘKSZY niż wejście (sam prefiks MAGIC),
# niezależnie od danych wejściowych. To była funkcja kodująca, nie
# kompresująca, mimo nazwy.
#
# Ta wersja robi realną kompresję (zlib/DEFLATE), sprawdzoną empirycznie:
# przetestowałem, czy poprzedni krok XOR-delta (j_core_reduce) poprawia
# współczynnik kompresji przed zlib — dla tekstu, danych losowych i danych
# powtarzalnych NIE pomaga (czasem lekko szkodzi), pomaga tylko dla danych
# monotonicznie rosnących bajt po bajcie. Ponieważ ogólne dane wejściowe
# tego pipeline'u (dowolne bytes) nie są tego typu, j_compress/j_decompress
# używają teraz zlib bezpośrednio. j_core_reduce/j_core_restore zostają
# zdefiniowane (dla zgodności wstecznej i ew. świadomego użycia gdzie
# indziej), ale nie są już częścią domyślnej ścieżki kompresji.

import hashlib
import zlib

MAGIC = b'JCOMP'  # znacznik formatu – pozwala wykryć poprawny blob


def j_core_reduce(data: bytes) -> bytes:
    """Odwracalne kodowanie XOR-delta. Zachowane dla zgodności wstecznej —
    NIE jest już używane wewnątrz j_compress (patrz uwaga na górze pliku)."""
    out = bytearray()
    last = 0
    for b in data:
        d = b ^ last
        out.append(d)
        last = b
    return bytes(out)


def j_core_restore(data: bytes) -> bytes:
    """Odwrócenie j_core_reduce."""
    out = bytearray()
    last = 0
    for d in data:
        b = d ^ last
        out.append(b)
        last = b
    return bytes(out)


def j_compress(raw: bytes) -> bytes:
    """Realna kompresja (zlib/DEFLATE, level 9) z prefiksem MAGIC do
    wykrywania formatu. Dla nieściśliwych/bardzo małych danych wejściowych
    wynik może być minimalnie większy niż wejście (nieunikniony narzut
    formatu DEFLATE + nagłówek zlib) — to jest znana, udokumentowana
    właściwość każdego kompresora ogólnego przeznaczenia, nie błąd."""
    core = zlib.compress(raw, 9)
    return MAGIC + core


def j_decompress(blob: bytes) -> bytes:
    if not blob.startswith(MAGIC):
        raise ValueError("Plik nie jest w formacie J–compression.")
    core = blob[len(MAGIC):]
    return zlib.decompress(core)


def j_hash(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()
