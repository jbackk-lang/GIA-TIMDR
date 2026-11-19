# RESULTS 015 — Czy niższy RMS po impulsie wynika z wcześniejszego RMS?

2026-11-19. Rzeczywiste CWRU_CHF.zip, 16 plików, pierwsze 50 okien po 2048 próbek na plik. Z 49 możliwych okien zdarzeń wybrano 5 z najwyższym crest factor. Analiza wyłącznie RMS. Standaryzacja wewnątrz nagrania. Test null: 5000 losowych niezerowych przesunięć cyklicznych zdarzeń w obrębie pliku, seed=20261119. Regresja liniowa post_RMS na pre_RMS z centrowaniem wewnątrz nagrania: współczynnik 0.11616.

| Miara | Różnica SD | Dwustronne p przesunięć | 95% bootstrap po nagraniach |
|---|---:|---:|---|
| RMS przed zdarzeniem | -0.0290 | 0.8042 | [-0.2205,0.1666] |
| RMS po zdarzeniu | -0.2662 | 0.0308 | [-0.4377,-0.1014] |
| RMS po korekcie o RMS przed | -0.2628 | 0.0306 | [-0.4460,-0.0836] |
| Różnica (po-przed) | -0.2372 | 0.1444 | [-0.5527,0.0704] |

**Wniosek:** prosta korekta liniowa o RMS przed impulsem nie usuwa obserwowanej różnicy RMS w następnym oknie. Nie dowodzi to przyczynowości, informacji o przeszłości, helisy ani CHF. Wskaźnik zmiany po-przed nie przeszedł testu przesunięć.

**Ograniczenia:** eksploracja po selekcji hipotez, brak kontroli wielokrotnych testów, 16 nagrań z powiązanymi oknami, brak niezależnego zbioru testowego, cykliczny null może być nieadekwatny przy niestacjonarności, nie testowano cech CHF. Nie należy interpretować p=0.031 jako potwierdzonego odkrycia.

Reprodukcja: `python research/chrono_helix_fusion/chf_after_event_015.py` (wymaga CWRU_CHF.zip; ścieżkę źródłową w kodzie należy dostosować do środowiska).

Następny eksperyment: dopasowanie zdarzeń do kontroli o podobnym RMS i crest factor, kontrola wpływu uszkodzenia i czasu, odczyt historii z kolejnych okien i walidacja leave-one-recording-out, porównanie CHF ze STFT/obwiednią.
