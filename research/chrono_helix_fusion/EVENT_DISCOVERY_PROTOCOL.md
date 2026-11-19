# CHF — poszukiwanie impulsów, zaników i reorganizacji

**Cel:** bez nadzoru wyszukiwać kandydatów na powtarzalne zdarzenia i zaniki relacji w sygnałach, nie tylko klasyfikować uszkodzenia.

Pierwszy skrypt `event_discovery.py` daje **kontrole wstępne**, a nie dowód odkrycia: RMS, energię pasma, koncentrację różnicy faz oraz niestabilność tej relacji. Obecna miara fazowa nie jest pełnym CHF; jest prostą sondą pomagającą sprawdzić, czy w ogóle warto budować detektor helisy/trinode.

Przebieg:
1. Syntetyczny sygnał z pięcioma **jawnie wstrzykniętymi** krótkimi zanikami składnika; wynik nie jest odkryciem.
2. Niezależny sygnał ECG z SciPy — **bez etykiet** i bez interpretacji medycznej.
3. Wyłonienie kandydatów oraz ocena stabilności czasu zdarzenia przy zmianie parametrów.
4. Porównanie z klasycznymi metodami: matrix profile (motifs/discords), STFT, energia pasma, PLV, change-point detection i surogaty z randomizacją fazy.
5. Dopiero po kontroli artefaktów: cechy helix/trinode/bridges z CHF, walidacja na niezależnych nagraniach i poszukiwanie interpretacji fizycznej.

**Nie wolno** nazywać anomalii nową własnością fizyczną bez replikacji i porównania ze znanymi miarami.
