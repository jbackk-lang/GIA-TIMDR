# RESULTS 006 — Faza jako nośnik informacji o wcześniejszym stanie

Data: 2026-11-19. **Eksperyment syntetyczny, kontrola pozytywna. Nie jest to odkrycie nowego zjawiska.**

W 80 niezależnych parach sygnałów 2-sekundowych przy fs=256 Hz użyto harmonicznych 8 Hz i 16 Hz. Losowano wspólną fazę oraz amplitudę drugiej harmonicznej dla każdej pary. Bit wcześniejszego stanu 0/1 zapisano jako względną fazę drugiej harmonicznej -π/2 lub +π/2. Każda para miała identyczne amplitudy FFT do dokładności numerycznej; maksymalna różnica bezwzględna wszystkich prążków: 1.7053e-13.

Cechy: (1) pełny wektor amplitud FFT, (2) sin i cos fazy względnej arg(X(16 Hz) conj(X(8 Hz))²). LogisticRegression + StandardScaler, 10 podziałów GroupShuffleSplit, 25% par na test, pary nierozdzielane między trening i test.

| Cechy | AUROC średnia | SD |
|---|---:|---:|
| Amplitudy FFT | 0.50 | 0.00 |
| Relacja faz harmonicznych | 1.00 | 0.00 |

**Wniosek ograniczony:** dwa przebiegi mogą mieć identyczne widmo mocy i energię, ale nieść różną informację w fazie. To jest znane z teorii sygnałów; nie oznacza odkrycia nowej fizyki, rzeczywistej pamięci układu ani przewagi CHF. Stan został celowo zakodowany. Klasyczna analiza fazowa odzyskuje go bez CHF.

**Kolejny eksperyment:** zbudować układ dynamiczny, w którym wcześniejszy impuls pozostawia wewnętrzny stan, a po zaniku przejściowego impulsu mierzyć informację o historii przy wyrównanej energii, rozkładzie amplitud i widmie; porównać pełne CHF z fazą harmonicznych, bispektrum, STFT, matrix profile i surogatami IAAFT. Dopiero niezależne nagrania rzeczywiste pozwolą szukać naturalnego zjawiska.

Odtwarzanie: `python research/chrono_helix_fusion/phase_memory_probe.py`.
