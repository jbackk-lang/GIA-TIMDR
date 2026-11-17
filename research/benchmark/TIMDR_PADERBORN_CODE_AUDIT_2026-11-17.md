# Audyt kodu Paderborn — 2026-11-17
Status: inspekcja statyczna, bez nowego uruchomienia.

## Zweryfikowane pliki
- core/paderborn_learning_curves.py
- core/paderborn_lc_io.py
- docs/geometry/PREREG_PADERBORN_LEARNING_CURVES_v0_1.md
- docs/geometry/RESULT_PADERBORN_LEARNING_CURVES_v0_1.json
- core/trm_gia_projections.py i tests/test_trm_gia_projections.py (osobna referencja syntetyczna)

## Ustalenia
1. Model sieciowy: liniowy embedding d=32, jedna warstwa TransformerEncoder (2 głowy, FFN64), średnia tokenów, klasyfikacja 3 klas; 300 kroków AdamW, stałe hiperparametry.
2. Foldy rozłączne po łożysku: pięć foldów, trzy losowania, N=4..160 przykładów na klasę; metryka macro-F1.
3. Raw: 125x512; spec: 125x257; TIMDR: 15x230, cechy sita + LDA: 12 cech.
4. KRYTYCZNE DLA FAIRNESS: tokenizacja TIMDR wykorzystuje rpm(cd), a raw i spec nie otrzymują jawnie tej samej prędkości obrotowej. Nie można przypisać całej przewagi wyłącznie reprezentacji bez kontroli RPM.
5. Ten sam mały Transformer, lecz różne liczby tokenów i reprezentacje oznaczają inny koszt i inductive bias; brak mocnego strojenia modeli.
6. W badanym skrypcie nie ma HMM ani LSTM. Brak dowodu przewagi nad tymi modelami.
7. Wejścia zależą od lokalnego LC_DATA, plików npz i rs_feats_all.json; nie ma samowystarczalnego odtwarzania w tym skrypcie.
8. Paderborn jest historycznie używany wielokrotnie; nowa hipoteza wymaga nowego holdoutu.

## Dalszy eksperyment
Porównać raw/spec bez i z RPM, TIMDR z RPM oraz ablacją kotwicy, a także dostrojone HMM/LSTM/Transformer. Zapewnić identyczną informację źródłową, grupowy split, prerejestrację, zamrożenie i statystykę na poziomie fizycznego łożyska.

Nie uruchomiono jeszcze benchmarku; status wyłącznie audyt kodu.