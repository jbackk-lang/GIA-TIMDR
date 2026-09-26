# Wynik — diagnostyka wielokanałowa TIMDR na SEU (bearingset), v0.1 (2026-09-26)

Pre-rejestracja: `PREREG_SEU_MULTICHANNEL_DIAGNOSTIC_v0.1.md` (commit a361e8d, przed obliczeniem cech). Liczby:
`RESULT_SEU_MULTICHANNEL_DIAGNOSTIC_v0.1.json`; analizy po fakcie: `POSTHOC_SEU_MULTICHANNEL_v0.1.json`
(`core/real_seu_multichannel_posthoc.py`).

**Poprawka techniczna po zamrożeniu (ujawnienie):** parser nie rozpoznawał linii `Data,,,,,,,,` w jedynym pliku
rozdzielanym przecinkami (`ball_20_0.csv`) i przerwał się błędem przed policzeniem jakiejkolwiek cechy tego pliku.
Zmieniono jedynie rozpoznanie tej linii; metoda bez zmian.

## Werdykty wg pre-rejestracji

- Bramka: kontrole syntetyczne 6/6, kontrola negatywna (permutacja etykiet) macro-F1 0,04 / 0,09 ≤ 0,35 — **przeszła**.
- **H1 — SUPPORTED** (6/8 komórek, kierunek jak na CWRU: zdrowy > uszkodzony w `spectral_concentration`).
  Ball/inner/outer w obu warunkach r = 0,68–0,98. Wyjątek: `comb` — w 20_0 nierozróżnialny (r = −0,08), w 30_2 odwrotnie
  (r = −0,81).
- **H2 — SUPPORTED** (przeniesienie między warunkami): macro-F1 B / T / BT = 0,23 / 0,69 / 0,32 (20_0→30_2)
  i 0,26 / 0,68 / 0,51 (30_2→20_0). Zysk BT − B = +0,08 i +0,25. Sufit w obrębie warunku: wszystkie zestawy 0,89–1,00.

## Co to znaczy — analizy po fakcie (nie zmieniają werdyktu)

1. **Przewaga nad baseline'em wynika głównie ze słabego baseline'u.** Zestaw B zawiera `std`, które zmienia się z
   prędkością/obciążeniem; przy standaryzacji statystykami zbioru uczącego klasyczne cechy zapadają się do poziomu losowego.
   Gdy każdy warunek jest standaryzowany własnymi statystykami (bez etykiet), B osiąga 0,66 / 0,79, a T 0,70 / 0,67 —
   **TIMDR sam nie jest lepszy od uczciwie znormalizowanego baseline'u.**
2. **Ale łącznie coś dodaje:** przy tej samej normalizacji BT = 0,95 / 0,81 wobec B = 0,66 / 0,79 — duży zysk w jednym
   kierunku (+0,29), znikomy w drugim (+0,02). Wynik mieszany, po fakcie, wymaga własnej pre-rejestracji do potwierdzenia.
3. **Pracuje trójka topologiczna, nie membrana.** Sama `spectral_concentration` daje 0,36 / 0,32; T bez niej 0,68 / 0,68.
   Membrana to praktycznie średnia |korelacja| kanałów (Spearman 0,96; sama średnia |r| daje 0,37 / 0,36).
4. **Możliwe zakłócenie akwizycją w H1.** Pliki `health` i `comb` mają wspólną, inną konfigurację (przesunięcie DC), a
   membrana nie odróżnia właśnie `comb` od `health`. Część rozdzielenia w H1 może oznaczać „inna sesja nagrania”, a nie
   „uszkodzenie”. Przy jednej jednostce na klasę nie da się tego rozstrzygnąć.
5. T nie rozpoznaje `outer` po zmianie warunków (0–1 na 100 okien).

## Wniosek

Kierunek membrany z CWRU powtórzył się na innym stanowisku, ale membrana okazuje się średnią korelacją między kanałami i
może być zakłócona sesją nagrania. Wartość dodana TIMDR przy zmianie warunków formalnie przeszła, lecz po uczciwej
normalizacji baseline'u sam TIMDR nie wygrywa; w połączeniu z klasycznymi cechami pomaga niejednoznacznie (+0,29 / +0,02).
Następny rzetelny krok: nowa pre-rejestracja z baseline'em standaryzowanym per warunek i danymi z więcej niż jedną
jednostką na klasę.
