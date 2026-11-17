# 54A.4 — predykcja między blokami: wynik negatywny

Wykonano lokalnie Python 2026-11-17; seed 5404, 128 bloków po 1024 B, gzip.compress(level=9,mtime=0). Cztery zbiory: identical, slow_drift, independent_variants, random. Testowano prev, three_loop (lag 3) i J2 (predykcja b-2c mod 256 z trzech poprzednich bloków). Residual XOR, gzip osobno dla każdego bloku, 4 bajty długości na blok i 1 bajt nagłówka. Pełne roundtrip sprawdzone asercjami.

| Dane | gzip whole | prev | lag3 | J2 |
|---|---:|---:|---:|---:|
| identical | 1852 | 5243 | 5243 | 48493 |
| slow_drift | 4832 | 8409 | 14176 | 55035 |
| independent_variants | 5286 | 11355 | 11356 | 55324 |
| random | 131130 | 134529 | 134529 | 134529 |

Wszystkie predyktory przegrywają. Porównanie jest konserwatywne wobec gzip (whole stream) i karze predyktory osobną kompresją bloków; kolejny test powinien izolować tę różnicę, kompresując cały strumień residuali jedną instancją gzip. Predyktor J2 jest konstrukcją inspirowaną trójkanałowością, **nie** bezpośrednim zastosowaniem całego J(lambda) ani walidacją TIMDR. Bez zmian w Helix-Lock/AES.
