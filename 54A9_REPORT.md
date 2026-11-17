# 54A.9 — Zmienna orientacja krawędzi a kompresja

## Protokół
Cztery deterministyczne strumienie syntetyczne po 16384 bajty. Okna 64 zdarzeń. Zmienna geometrii to binarna orientacja krawędzi, a J jest udziałem krawędzi zgodnych z osią w poprzednim zamkniętym oknie. Predyktory: opóźnienia 1, 3 i 64, adaptacja na podstawie błędu, dodatkowa kara zależna od J. Wszystkie dekodowania zgodne. Jedna kompresja gzip poziom 9 dla reszt oraz osobna dla geometrii, tak samo liczona dla każdej metody. Koszt nagłówka formatu nieujęty.

## Wyniki (całkowite bajty wraz z geometrią)
| Dane | gzip | statyczna | adaptacyjna | geometryczna |
|---|---:|---:|---:|---:|
| aligned | 1001 | 156 | 104 | 108 |
| rotating | 1250 | 311 | 236 | 243 |
| switching | 938 | 439 | 223 | 231 |
| random | 19137 | 19137 | 19137 | 19137 |

## Interpretacja
W żadnym zbiorze heurystyka geometryczna nie pokonała adaptacyjnej. Wykorzystanie geometrii z zamkniętego okna zapobiega wyciekowi informacji z przyszłości. Nie jest to pełna instancja META: binarny proxy krawędzi nie reprezentuje geometrii przestrzennej, a inne składowe (Lambda,tau,rho) nie są tu implementowane.

## Reprodukcja
`python 54A9_GEOMETRY.py` (Python standard library).
