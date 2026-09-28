# PREREG — Paderborn: czy TIMDR jako warstwa porządkująca zmniejsza liczbę przykładów potrzebnych do nauki? v0.1

Data: 2026-09-28. Kod: `core/paderborn_lc_io.py` (dane), `core/paderborn_learning_curves.py` (`final`). Zamrożone PRZED
uruchomieniem na pomiarach 11–20. Jedno uruchomienie: `python core/paderborn_learning_curves.py final <wynik.json>`.

## Pytanie (autor)
Uwaga/transformer może uczyć się z sygnału sam. Czy TIMDR jako warstwa porządkująca (pole + kotwica + odniesienie) sprawia,
że ta sama sieć osiąga ten sam wynik na kilka razy mniejszej liczbie przykładów?

## Dane
Paderborn (KAt), 15 łożysk z uszkodzeniami naturalnymi i zdrowe: K002–K006, KA04/15/16/22/30, KI04/14/16/18/21;
4 warunki pracy × pomiary 1–20; 2 s po decymacji do 32 kHz (jak w sicie rezonansowym). **Ponowne użycie:** te pomiary były
używane w testach sita (v0.1–v0.3) — tu nowe pytanie (efektywność uczenia), wynik rozpoznawczy co do danych.
Rozwój: pomiary 1–10 (foldy 0–1). Test: pomiary 11–20, 5 foldów łożysk rozłącznych (w teście po jednym zdrowym,
zewnętrznym, wewnętrznym łożysku; uczenie na pozostałych 4 + 4 + 4).

## Ramiona (ta sama sieć dla trzech pierwszych)
Sieć: osadzenie liniowe tokenu → d = 32 + uczona pozycja → 1 warstwa transformera (2 głowy, FFN 64, dropout 0,1) →
średnia po tokenach → 3 klasy. AdamW lr 1e-3, wd 1e-2, 300 kroków, partia 32, standaryzacja z danych uczących.
Hiperparametry ustalone z góry, bez strojenia (sprawdzone tylko, że uczenie zbiega).
- **raw** — surowy przebieg (125 tokenów × 512 próbek), tylko normalizacja amplitudy nagrania.
- **spec** — standardowa obróbka ML: log-spektrogram (125 ramek × 257 binów). *Dodane w rozwoju po zobaczeniu, że raw
  prawie się nie uczy — jako uczciwe odniesienie „każda obróbka vs TIMDR”.*
- **timdr** — pole TIMDR: 15 pasm nośnych jako tokeny × widmo obwiedni względem tła (mediana = 1), oś w rzędach obrotu
  (kotwica z kinematyki; 0,5–12 rzędów, 230 binów), log.
- **lda** — trzecia kolumna: 12 cech sita TIMDR (walidowanych wcześniej) + LDA ze skurczem 0,1.
Krzywa: N ∈ {4, 8, 16, 32, 64, 128, 160} przykładów na klasę, 3 losowania × 5 foldów; miara macro-F1 na łożyskach testowych.

## Ujawnienia z rozwoju (pomiary 1–10, foldy 0–1, 1 losowanie)
macro-F1 przy N = 8 / 32 / 80: raw 0,31 / 0,33 / 0,39; spec 0,35 / 0,44 / 0,40; timdr 0,65 / 0,64 / 0,76;
lda 0,53 / 0,71 / 0,80. Sieć na raw i spec zapamiętuje dane uczące (strata ~0), ale nie uogólnia na nowe łożyska.
Zakaz technologii Meta zniesiony przez autora (dotyczył jednego repozytorium) — użyty PyTorch (CPU).

## Hipotezy
- **H1 (główna):** cel = macro-F1 ramienia spec przy N = 160. Stosunek N_spec / N_timdr (najmniejsze N, przy którym średnia
  krzywa osiąga cel) ≥ 3 → SUPPORTED; 1,5–3 → MIXED; < 1,5 lub timdr nie osiąga celu → NOT.
- **H1b:** to samo względem raw.
- **H2:** przy N ≤ 32 timdr > spec w ≥ 80% par (fold × N × losowanie) → SUPPORTED.
- **H3:** przy N = 160 samo TIMDR + LDA ≥ timdr-sieć − 0,02 → SUPPORTED (sieć niewiele dokłada do struktury TIMDR).
Wynik do README niezależnie od werdyktu.
