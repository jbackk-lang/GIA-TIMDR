# PREREG — lokalne uszkodzenie jako przerwanie ciągłości (K → G → M/S), Hell Bridge Test Arena, v0.3

Data: 2026-09-27. Kod: `core/hbta_discontinuity.py`. Zamrożone przed uruchomieniem. Idea J. Kielicha: lokalne uszkodzenie
to przerwa na czymś ciągłym.

## Ujawnienia
Czwarte użycie tych danych (v0.1, v0.2 i widma uczenia) — wynik rozpoznawczy, nie rozstrzygający. Kotwice, siatka, okna,
uczenie (UDS_01) i test (UDS_02 vs DS1–DS8) jak v0.2.

## Konstrukcja
Kształt modu z fazą (jak v0.2) → aksjomat M/S „defekt = skok” zastosowany w przestrzeni:
- **(a) wzdłuż podłużnicy:** odchyłka punktu od kubicznej interpolacji z sąsiadów i±1, i±2 (gapped smoothing, Ratcliffe 1997);
  rozstaw 3,5 m, połączenia leżą między czujnikami — ograniczenie rozdzielczości.
- **(b) w poprzek:** różnica kształtu między sąsiednimi podłużnicami w tym samym x (zerwana współbieżność pomostu).
Cecha: dla każdej kotwicy **maksimum** |z| zmiany względem uczenia (mediana/MAD po oknach) po położeniach — osobliwość, nie suma
(v0.2 sumował krzywiznę i rozmywał lokalny sygnał). DISC = (a) + (b), 12 cech. Detektor kNN jak wcześniej.

## Hipotezy
- **H1:** średnie AUC(DISC) > AR (0,80, v0.2).
- **H2:** średnie AUC(DISC) dla DS1–DS2 (połączenia podłużnica–poprzecznica) > kształt z fazą v0.2 (0,87).
- **H3:** średnie AUC(w poprzek) > średnie AUC(wzdłuż) — ograniczenie rozdzielczości wzdłuż linii.
- Rozpoznawczo: para podłużnic i x maksimum zmiany w poprzek dla każdego DS.
