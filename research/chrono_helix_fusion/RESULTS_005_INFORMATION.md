# RESULTS 005 — Czy sygnał zachowuje informację w czasie?

2026-11-19. Kontrolowany test syntetyczny; **nie jest to odkrycie nowego zjawiska ani walidacja przewagi CHF**.

Wygenerowano 24 niezależne realizacje procesu z losowymi dodatnimi impulsami i wykładniczym wygaszaniem (8192 próbek, seed 1000–1023). Dla każdej 79 surogatów ze zrandomizowaną fazą FFT, przy zachowaniu amplitudy każdego prążka (maksymalny błąd 3.41e-13). Surogaty zachowują pełne widmo mocy i autokorelację liniową, ale **nie zachowują rozkładu amplitud**.

Próbki skwantowano do trzech poziomów kwantylowych. Obliczono informację wzajemną między próbkami oddalonymi o 16 indeksów, informację warunkową I(X_t;X_(t+16)|X_(t+8)) oraz asymetrię trzeciego momentu przyrostów. Zbadano p dwustronne względem 79 surogatów, bez korekty wielokrotnych testów.

| Miara | Oryginał, średnia | Surogaty, średnia | Realizacje z p <= 0.05 |
|---|---:|---:|---:|
| Informacja predykcyjna (bity) | 0.121253 | 0.038457 | 24/24 |
| Warunkowa pamięć (bity) | 0.024235 | 0.003214 | 24/24 |
| Asymetria przyrostów | 1.416989 | -0.000177 | 24/24 |

**Interpretacja:** informacja o kolejności i relacjach między próbkami nie jest w pełni określona przez widmo mocy. To znany ogólny fakt teorii sygnałów, tu odtworzony eksperymentalnie. Obliczona informacja wzajemna oznacza statystyczną przewidywalność, nie ilość semantycznej wiadomości zakodowanej w sygnale.

**Kluczowy problem metodologiczny:** surogaty zmieniają rozkład amplitud, więc różnice mogą wynikać z niegaussowskości, a nie wyłącznie z wyższych zależności czasowych. Kolejne kontrole: IAAFT zachowujące przybliżone widmo i rozkład amplitud; predykcja out-of-sample; zmienne opóźnienia i skale; porównanie z bispektrum, ordinal patterns, transfer entropy; na końcu pomiary helix/trinode/bridges i naturalne nagrania.

Reprodukcja: `python research/chrono_helix_fusion/information_probe.py --output information_probe.json`.
