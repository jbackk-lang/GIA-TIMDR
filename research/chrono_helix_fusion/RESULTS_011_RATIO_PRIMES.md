# RESULTS 011 — Stosunek pi/(sqrt(2)+sqrt(3)) i podział zwojów

2026-11-19. Wykonany eksperyment arytmetyczny, **nie eksperyment na rzeczywistym sygnale**. Hipoteza: fazy zwojów o numerach pierwszych przy kącie 2πnR skupiają się silniej niż fazy losowych zbiorów zwojów o tej samej liczności.

R = π/(√2+√3) ≈ 0.99851515. Testowano N=1000,3000,10000, 999 losowych podzbiorów, seed=20261119.

| N | Skupienie pierwszych | Średnia losowa | Jednostronne p |
|---|---:|---:|---:|
| 1000 | 0.2323 | 0.2195 | 0.371 |
| 3000 | 0.1021 | 0.0796 | 0.216 |
| 10000 | 0.0368 | 0.0259 | 0.188 |

Odwrócony stosunek: p=0.407,0.209,0.210. Kontrole π/(√2+√5), √2, złota proporcja również nie wykazały małych wartości p (najmniejsza 0.231 dla tych trzech).

**Wniosek negatywny:** brak podstaw, by twierdzić, że ten prosty podział wyróżnia zwoje pierwsze. Brak kontroli lokalnej gęstości liczb pierwszych, brak korekty wielokrotnego testowania, brak naturalnego sygnału i odczytu informacji. Efekty mogą zależeć od okresu dudnień wynikającego z R bliskiego 1.

Następny krok: porównać na tych samych naturalnych nagraniach odczyt informacji o historii przez podziały prime, ratio, równomierne i losowe, z kontrolą FFT/STFT/fazy i separacją nagrań trening/test.
