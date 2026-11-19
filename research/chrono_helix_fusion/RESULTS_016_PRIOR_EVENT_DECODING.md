# RESULTS 016 — Predykcja wcześniejszego impulsu z następnego okna

2026-11-19. **Rzeczywiście wykonano** lokalnie na archiwum CWRU_CHF.zip: 16 plików, 50 okien po 2048 próbek, 49 par kolejnych okien na nagranie (784 pary). Etykieta dodatnia: 5 najwyższych wartości crest factor wśród 49 poprzednich okien każdego nagrania (80 dodatnich par). Predyktor: cechy **wyłącznie następnego okna**. Logistyczna regresja regularizowana C=0.1, standaryzacja treningowa, leave-one-recording-out.

**Uwaga:** cechy okien następnych centrowano i skalowano wewnątrz nagrania, w tym testowego, bez etykiet. Jest to *transdukcyjna* normalizacja i może nie być możliwa w zastosowaniu online.

| Cechy następnego okna | Średni AUROC per nagranie | Łączny AUROC |
|---|---:|---:|
| RMS | 0.5878 | 0.5802 |
| FFT: energia w 4 pasmach | 0.5088 | 0.5093 |
| Obwiednia: 4 autokorelacje | 0.5773 | 0.5752 |
| Klasyczne relacje faz Fouriera | 0.6097 | 0.6068 |
| Wszystkie cechy | **0.6301** | **0.6329** |

Bootstrap 10 000 prób po 16 nagraniach: średnia różnica AUROC wszystkie minus RMS = +0.0423, 95% CI [-0.0264, 0.1094]. Faza minus RMS +0.0219, CI [-0.0540,0.1009]. AUROC wszystkie minus 0.5 = +0.1301, CI [+0.0597,+0.1932]. Przedziały opisowe; wybór zadania i cech eksploracyjny, bez niezależnej replikacji.

**Interpretacja:** istnieje umiarkowany sygnał predykcyjny o poprzednim impulsie, lecz nie wiadomo, czy wynika z pamięci fizycznej, korelacji amplitudy, powtarzalności usterek, zależności sąsiednich okien lub niestacjonarności. Różnica względem prostego RMS nie jest przekonująca. To nie dowód nowej struktury, nie pełne cechy CHF i nie test przyczynowości.

Następny krok: odsunąć okno obserwacyjne o 2, 3 i 5 okien; dodać dopasowane kontrole czasu i energii, surogaty IAAFT oraz prawdziwą reprezentację CHF, z zewnętrzną walidacją nagrań.
