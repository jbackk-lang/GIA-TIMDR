# RESULTS 014 — Czy silny impuls zostawia ślad w kolejnym oknie?

Wykonano lokalnie 2026-11-19 na 16 rzeczywistych plikach MAT CWRU z archiwum `CWRU_CHF.zip`. W każdym pliku pierwsze 50 niepokrywających się okien po 2048 próbek. Z 49 możliwych okien zdarzeń wybrano 5 o najwyższym crest factor. Wynik: następne okno, oceniane pod kątem RMS i maksymalnej autokorelacji obwiedni Hilberta dla opóźnień 30–400 próbek. Wyniki standaryzowane osobno dla każdego pliku, następnie uśredniane między 16 plikami. Null: 2000 losowych niezerowych cyklicznych przesunięć etykiet zdarzeń w obrębie pliku, seed 20261119.

| Wynik w następnym oknie | Średnia różnica (SD) | Dwustronne p, przesunięcia | 95% przedział null | Pliki z dodatnim efektem |
|---|---:|---:|---|---:|
| Powtarzalność obwiedni | +0.0237 | 0.8386 | [-0.2128, 0.2219] | 10/16 |
| RMS | -0.2666 | 0.0205 | [-0.2139, 0.2336] | 6/16 |

**Interpretacja:** brak wykrytego śladu w powtarzalności obwiedni. Ujemny efekt RMS jest wstępny i może wynikać z regresji do średniej, zależności od aktualnej amplitudy lub niestacjonarności. Nie jest dowodem pamięci informacji, efektu CHF ani nowej fizyki. Przy prostej korekcie Bonferroniego dla dwóch miar RMS p≈0.041, ale post-selekcja hipotez i zależności czasowe pozostają istotne.

Ograniczenia: wybór zdarzeń i ocena na tych samych nagraniach; 16 plików niekoniecznie jest niezależnymi realizacjami; brak dopasowania poprzedzającego RMS i charakterystyki usterek; null przez przesunięcie cykliczne nie zachowuje pełnej struktury niestacjonarnej; brak testu odczytu historii i brak pełnych cech CHF.

Reprodukcja: `python research/chrono_helix_fusion/after_event_014.py CWRU_CHF.zip --output CHF_AFTER_EVENT_014.json`.

**Następny krok:** kontrola regresji do średniej, porównanie RMS przed/po i dopasowane zdarzenia kontrolne; następnie odczyt historii z późniejszych okien, walidacja między nagraniami oraz porównanie CHF vs obwiednia/STFT.
