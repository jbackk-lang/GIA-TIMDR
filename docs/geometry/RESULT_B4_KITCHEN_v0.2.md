# Wynik B4-Kitchen v0.2 (2026-09-19) — nadal INCONCLUSIVE, ale bliżej progu

Zgodnie z `PREREG_B4_KITCHEN_v0.2.md`, zamrożonym PRZED tym wynikiem. Dane,
triangulacja, alignment czasu, definicja `Lambda` — identyczne z v0.1
(zweryfikowane: `h_summary`/`q_summary`/`lambda_g_summary`/
`lambda_meta_summary` w `B4_KITCHEN_RESULT_v0.2.json` są bit-do-bitu
identyczne z `B4_KITCHEN_RESULT_v0.1.json` — jedyna zmiana to metoda
budowy rozkładu null). Pełny surowy wynik: `B4_KITCHEN_RESULT_v0.2.json`.

## Wynik surowy

| | v0.1 (pełna permutacja) | v0.2 (permutacja blokowa, L=12) |
|---|---|---|
| Kontrola pozytywna | p=0.0001 (przeszła) | p=0.0001 (przeszła) |
| Kontrola negatywna (AR(1)) | **p=0.0002** (nie przeszła) | **p=0.0173** (nie przeszła) |
| `controls.passed` | false | false |
| Werdykt | INCONCLUSIVE | **INCONCLUSIVE** |
| Test główny uruchomiony? | nie | nie |

## Uczciwa interpretacja

**Poprawka pomogła, ale nie wystarczająco.** Permutacja blokowa (L=12)
zmniejszyła fałszywą istotność kontroli negatywnej o ok. 86× (p: 0.0002 →
0.0173, liczba przekroczeń: 1/10000 → 172/10000) — dokładnie w
przewidywanym kierunku, bo blokowanie chroni krótkozasięgową
autokorelację AR(1) lepiej niż pełna permutacja. Ale przy progu
`alpha=0.05` kontrola WCIĄŻ nie przechodzi (`0.0173 < 0.05` — to wciąż
fałszywa istotność, nie brak efektu). Zgodnie z `PREREG_B4_KITCHEN_v0.2.md`
§5 werdykt pozostaje **INCONCLUSIVE**, a test główny (Spearman na
`lambda_g`/`lambda_meta`) NIE został uruchomiony — brama kontrolna
(`controls.passed`) go blokuje, dokładnie tak jak zaprojektowano.

**Dlaczego L=12 mogło nie wystarczyć — hipoteza, nie ustalony fakt.** Dla
AR(1) z `phi=0.8` czas autokorelacji (`1/(1-phi)=5`) jest krótszy niż
L=12, więc blok tej długości POWINIEN w teorii uchwycić większość
struktury zależności. Że mimo to kontrola nie przechodzi, sugeruje że albo
(a) sama granica cyrkularnego przesunięcia+przetasowania bloków wciąż
wprowadza pewną resztkową niezależność silniejszą niż zakładana, albo (b)
heurystyka `n^(1/3)` jest zbyt konserwatywna dla tego konkretnego `phi`, albo
(c) 1645-elementowa sekwencja bloków Λ (a nie surowe AR(1)) ma inną
strukturę zależności niż czysty AR(1) z kontroli. Rozstrzygnięcie
któregokolwiek z tych wymagałoby OSOBNEJ analizy diagnostycznej — nie
retuningu L na tych samych danych.

## Zgodnie z zasadą anty-tuningu (PREREG §6)

**`L=12` NIE zostanie zmienione na podstawie tego wyniku.** Nie
uruchomiono, nie uruchomi się w ramach v0.2, żadnej wersji z innym `L`
"żeby zobaczyć czy przejdzie". Jeśli dalsza praca nad tym pytaniem ma sens,
wymaga to nowej, osobnej prerejestracji (v0.3) z jawnie innym, z góry
uzasadnionym wyborem metody (np. inna heurystyka długości bloku
zdecydowana przed jakimkolwiek kolejnym uruchomieniem, albo całkiem inna
rodzina testu — surogaty z randomizacją fazy, Theiler i in. 1992 — zamiast
permutacji blokowej).

## Co to pokazuje, uczciwie

1. Diagnoza z v0.1 (pełna permutacja jest niepoprawna dla autoskorelowanych
   serii) była trafna — poprawka poszła we właściwym kierunku i dała
   mierzalną, dużą poprawę (86×).
2. Ale sama trafna diagnoza nie gwarantuje, że pierwsza wypróbowana
   poprawka w pełni rozwiąże problem — to wciąż wynik negatywny, zgłoszony
   uczciwie, nie ukryty ani nie "dociągnięty" zmianą parametru po fakcie.
3. Pytanie "czy `Lambda_G` koreluje z `Lambda_META,disp` w danych Kitchen"
   pozostaje **nierozstrzygnięte** po dwóch niezależnych próbach
   metodologicznych — nie potwierdzone, nie odrzucone, INCONCLUSIVE w obu
   przypadkach, z różnych, jawnie nazwanych powodów statystycznych.

## Status: INCONCLUSIVE (v0.2, jak v0.1, z innego, jawnie zmierzonego powodu)
