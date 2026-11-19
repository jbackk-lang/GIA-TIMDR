# RESULTS 025 — Echo i okresowość obwiedni po impulsie

Uruchomiono lokalnie 2026-11-19: 16 rzeczywistych nagrań CWRU, po 50 okien × 2048 próbek; 48 par zdarzenie–kontrola (3 na nagranie). Wybór 5 najwyższych crest factor z pierwszych 42 okien; dopasowanie po log RMS i słabej karze czasowej. Mediana luki RMS 0.0004374.

**Echo proxy:** maksimum bezwzględnej znormalizowanej korelacji kolejnych okien przy przesunięciach ±128 próbek.

**Beat proxy:** maksimum znormalizowanej autokorelacji obwiedni Hilberta w następnym oknie dla opóźnień 64–512 próbek. To miara okresowości, nie bezpośredni dowód fizycznego dudnienia.

| Miara | Różnica impuls–kontrola | 95% bootstrap po nagraniach | Dwustronne p (20 000 sign-flips nagrań) | Dodatnie pary |
|---|---:|---|---:|---:|
| Echo proxy | +0.015331 | [-0.003831,0.042439] | 0.25079 | 30/48 |
| Okresowość obwiedni | +0.014604 | [0.005317,0.023199] | **0.01080** | 32/48 |
| Log RMS następnego okna | -0.010102 | [-0.020911,-0.001002] | 0.06075 | 15/48 |

Bonferroni w obrębie tych trzech metryk daje p≈0.0324 dla okresowości, lecz nie uwzględnia wieloetapowej eksploracji. Wynik jest **hipotezą do replikacji**, nie odkryciem nowego zjawiska. Zwykła okresowość uszkodzonych łożysk i niestacjonarność mogą wyjaśniać obserwację. Brak dowodu CHF lub informacji na helisie.

Następny test: czy obserwowane modulacje mają dwa bliskie stabilne składniki częstotliwościowe, których różnica odpowiada okresowi obwiedni; kontrole lokalnej niestacjonarności, niezależne nagrania, porównanie CHF i klasycznych metod.

Reprodukcja: `python chf_stage_025.py CWRU_CHF.zip`. Kod i JSON w artefaktach rozmowy.