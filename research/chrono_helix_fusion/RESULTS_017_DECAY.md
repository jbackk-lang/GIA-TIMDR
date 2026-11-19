# RESULTS 017 — Zanik przewidywalności wcześniejszego impulsu

Data: 2026-11-19. **Wykonano lokalnie** na rzeczywistych danych CWRU_CHF.zip: 16 nagrań, pierwsze 50 okien po 2048 próbek. Zdarzenie: pięć najwyższych wartości crest factor spośród możliwych okien początkowych *dla każdego opóźnienia*. Odczyt cech z okna oddalonego o 1, 2, 3, 5 lub 8 okien. Logistyczna regresja (C=0.1, class_weight=balanced), leave-one-recording-out, transdukcyjne centrowanie cech wewnątrz każdego nagrania.

| Odstęp (okna) | Pary | RMS | FFT | Obwiednia | Faza | Wszystkie |
|---|---:|---:|---:|---:|---:|---:|
| 1 | 784 | 0.5878 | 0.506 | 0.577 | 0.611 | **0.630** |
| 2 | 768 | 0.576 | 0.536 | 0.549 | 0.568 | **0.593** |
| 3 | 752 | 0.441 | 0.526 | 0.534 | 0.535 | 0.509 |
| 5 | 720 | 0.526 | 0.504 | 0.431 | 0.573 | 0.501 |
| 8 | 672 | 0.539 | 0.493 | 0.495 | 0.509 | 0.483 |

Wartości to średnie AUROC z 16 nagrań; 0.5 oznacza poziom losowy. Wyniki zaokrąglone.

**Interpretacja:** łączny model wykazuje sygnał predykcyjny po 1–2 oknach, ale nie po 3–8. Pojedynczy wynik fazy 0.573 przy opóźnieniu 5 może być przypadkowy przy wielu testach. Nie można mówić o potwierdzonej trwałej pamięci sygnału ani o nowym mechanizmie helikalnym.

**Ograniczenia:** wiele eksploracyjnych porównań, brak przedziałów niepewności dla opóźnień, definicja zdarzeń zmienia się nieznacznie z opóźnieniem, normalizacja testowego nagrania jest transdukcyjna, możliwe zależności między oknami i powtarzalne usterki, brak kontroli dopasowanych energią, brak surogatów i brak rzeczywistych cech CHF.

Reprodukcja: `python research/chrono_helix_fusion/chf_stage_017.py CWRU_CHF.zip`.

Następny test: stały zbiór impulsów dla wszystkich opóźnień, bez normalizacji testowego nagrania, bootstrap po nagraniach, matched controls i porównanie z rzeczywistymi deskryptorami CHF.
