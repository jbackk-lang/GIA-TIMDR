# Audyt TIMDR: dowody, luki i benchmark sekwencyjny — 2026-11-17

Status: AUDYT CZĘŚCIOWY; bez nowych uruchomień eksperymentalnych.

## Zweryfikowane źródła
- README.md, STAN_PROJEKTU.md, REPOZYTORIUM.md, ARCHITEKTURA_TIMDR.md
- docs/geometry/RESULT_PADERBORN_LEARNING_CURVES_v0.1.md
- docs/geometry/RESULT_PADERBORN_RESONANCE_SIEVE_CONFIRM_v0.3.md
- docs/theory/TIMDR_CALIBRATION_FREEZE_RULE.md
- docs/theory/TIMDR_EventGraph_Branch_Construction.md

## Ustalenia
1. TIMDR jest frameworkiem konstrukcyjnym, a nie pojedynczym predyktorem; benchmark musi określić implementację i zadanie.
2. Paderborn learning curves (5 foldów rozłącznych łożysk × 3 losowania; 3 klasy): przy 4 przykładach na klasę macro-F1 raw 0.34, spec 0.43, TIMDR field 0.63, sieve+LDA 0.55; przy 160: raw 0.44, spec 0.43, TIMDR field 0.68, sieve+LDA 0.74. Autorzy raportują jedną małą sieć i stałe hiperparametry; brak porównania z mocnymi, strojeniowymi HMM/LSTM/Transformer.
3. Paderborn resonance sieve: 15 foldów, przewaga nad klasycznymi +0.081 (12/15), nad obwiednią +0.042 (10/15) poniżej progu 0.05; rezerwa pomiarów wyczerpana.
4. TRM/GIA EventGraph v0.1: selekcja przez zamrożoną referencję PCA i próg odległości; idempotencja i stabilność wymagają stałych c,u,a i marginesu. Nie są dowodem przewagi predykcyjnej ani rezonansu fazowego.
5. Reguła freeze zabrania optymalizacji pod wynik holdoutu; już oglądany Paderborn nadaje się do development, nie do nowej niezależnej konfirmacji.
6. W README nadal otwarty niezależny checker LRAT dla osobnej linii badań 51B.16.

## Protokół do wykonania
- Inwentaryzacja kodu właściwego dla sita i jego zależności oraz zestawów danych; zamrożenie konkretnego commit SHA.
- Odrębny publiczny holdout grupowany po fizycznym łożysku/urządzeniu, bez leakage; manifest i hashe.
- TIMDR-sieve+LDA, klasyczne cechy+LDA, HMM, LSTM, Transformer: identyczne foldy i metryka macro-F1; wejścia adekwatne do modelu, ale ta sama informacja źródłowa, jawne budżety strojenia.
- Co najmniej 5 seedów i przedziały ufności na poziomie łożysk; dodatkowo balanced accuracy, kalibracja, koszt treningu i inferencji.
- Ablacje: brak sita, brak kotwicy modalnej, brak odniesienia do tła; negatywna kontrola shuffle labels.
- Przed otwarciem nowego holdoutu prerejestracja progu sukcesu, testu sparowanego i korekty wielokrotności.
- Wyniki, także negatywne, zapisać w nowym RESULT; nie modyfikować starych werdyktów.

## Ograniczenia audytu
Nie zinwentaryzowano jeszcze wszystkich plików kodu, nie uruchomiono testów, nie zweryfikowano surowych danych i nie przeprowadzono niezależnej replikacji. Twierdzenie TIMDR > HMM/LSTM/Transformer pozostaje niepotwierdzone.
