# RESULTS 008 — Zwinięcie sygnału, widmo i kierunek dynamiki

2026-11-19. **Eksperyment syntetyczny wykonany lokalnie.** Wygenerowano 80 losowanych liniowych chirpów (fs=256 Hz, 1024 próbek, 4 s), z szumem i losową fazą. Każdy sparowano z dokładnie odwróconym w czasie przebiegiem. Maksymalna różnica amplitud globalnego FFT: 3.552713678800501e-14. Porównano amplitudy globalnego FFT z nachyleniem centroidu widma STFT w czasie (nperseg=128, noverlap=96). LogisticRegression, StandardScaler, 20 podziałów GroupShuffleSplit z parami pozostającymi w tej samej grupie.

| Metoda | Średni AUROC | SD |
|---|---:|---:|
| Globalne amplitudy FFT | 0.50 | 0.00 |
| Kierunek przesunięcia centroidu STFT | 1.00 | 0.00 |

**Interpretacja:** odwrócenie czasu zachowuje globalne widmo amplitudowe, ale zmienia znak kierunku ewolucji częstotliwości. STFT to znana metoda, więc nie wykazano przewagi CHF ani nowego zjawiska. Użyty klasyfikator jedynie ilustruje rozdzielność cechy.

**Hipoteza badawcza:** bardziej złożone struktury mogą przechowywać historię w kolejności przejść między stanami (np. kierunkowe cykle w przestrzeni opóźnień) nawet po wyrównaniu energii, widma i znanych cech STFT. Dalszy test: trajectory embedding, recurrence plots, permutation entropy, time irreversibility i porównanie z pełnym CHF helix/trinode/bridges. Następnie realne nagrania i surogaty IAAFT.

Reprodukcja: `python research/chrono_helix_fusion/dynamic_direction.py`.
