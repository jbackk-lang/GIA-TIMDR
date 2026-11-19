# RESULTS 018 — Stałe zdarzenia i normalizacja tylko na treningu

Wykonano 2026-11-19 na CWRU_CHF.zip: 16 nagrań, 50 okien × 2048 próbek. W każdym nagraniu **te same 5 najwyższych crest factor z pierwszych 42 okien** stanowi zdarzenia dla wszystkich opóźnień. Każde opóźnienie ma 672 pary (80 dodatnich). Logistyczna regresja leave-one-recording-out, StandardScaler dopasowany wyłącznie na treningu, bez normalizacji nagrania testowego.

| Opóźnienie | RMS | FFT | Obwiednia | Faza | Wszystkie |
|---|---:|---:|---:|---:|---:|
| 1 | 0.5831 | 0.4084 | 0.5571 | 0.6030 | 0.6135 |
| 2 | 0.5713 | 0.4811 | 0.5530 | 0.5186 | 0.5466 |
| 3 | 0.5078 | 0.4250 | 0.5226 | 0.5169 | 0.4966 |
| 5 | 0.5203 | 0.5453 | 0.4659 | 0.5672 | 0.5574 |
| 8 | 0.5389 | 0.5547 | 0.4902 | 0.5297 | 0.5328 |

Średnia AUROC z 16 nagrań. Bootstrap 10 000 próbek po nagraniach: różnica wszystkie minus RMS przy lag 1 = +0.0304, CI95% [-0.0510,0.1176], przy lag 5 = +0.0372, CI95% [-0.0547,0.1331]. Eksploracyjne CI bez korekty wielokrotnych testów.

**Wniosek:** predykcja wcześniejszego impulsu z najbliższego okna utrzymuje się słabo bez transdukcyjnej normalizacji. Brak przekonującej przewagi wszystkich cech nad RMS, brak potwierdzenia długiej pamięci, brak pełnych cech CHF. Efekt fazy przy lag 5 jest niepotwierdzony.

Ograniczenia: post-hoc dobór hipotez, korelacje okien, brak niezależnej replikacji i surogatów, możliwy wpływ charakterystyki nagrania. Kod wykonywalny i pełne wyniki dostępne jako artefakty rozmowy: chf_stage_018.py i CHF_AFTER_EVENT_018.json. Następny test: dopasowane energetycznie i czasowo kontrole, niezależne nagrania, właściwe cechy CHF.