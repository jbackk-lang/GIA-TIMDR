# PREREG — TIMDR na drganiach budynku: rama trzykondygnacyjna LANL, v0.1

Zamrożone PRZED obliczeniem jakiejkolwiek cechy na tych danych (2026-09-26). Kod: `core/real_lanl_3story_bridge.py`.

## 0. Pytanie

Problem monitorowania konstrukcji (SHM): odróżnić **uszkodzenie** od nieszkodliwych zmian eksploatacyjnych (dodana masa,
obniżona sztywność słupów), ucząc się **wyłącznie na stanie nieuszkodzonym**. Czy cechy TIMDR wnoszą coś ponad klasyczne
cechy SHM (współczynniki AR, kurtoza, crest factor)?

## 1. Dane

LANL Engineering Institute, „3-Story Structure”, plik `data3SS.mat` (nagłówek: MATLAB 5.0, 2010-07-29),
SHA-256 `d738160e7d0a2c422a1189e3fe6c47c6e978be068247f55dc5a94ca381773e0f`, pobrany z kopii w repozytorium GitHub
`GautamChandak23/shm-bench` (`data/data3SS.mat`) — oficjalna strona LANL jest z tego środowiska niedostępna.
Tablica `dataset` 8192 × 5 × 170, wektor `states` (17 stanów × 10 pomiarów). Kanał 1 = siła wzbudnika, 2–5 = akcelerometry
(podstawa, piętra 1–3). Stany wg dokumentacji LANL (Figueiredo i in. 2009, LA-14393), w pliku są tylko numery:
1 bazowy; 2–3 dodana masa 1,2 kg; 4–9 obniżona sztywność słupów (zmiana eksploatacyjna, **nie** uszkodzenie);
10–14 zderzak (nieliniowość typu „oddychająca rysa”), szczelina 0,20 / 0,15 / 0,13 / 0,10 / 0,05 mm;
15–17 zderzak + dodana masa. Nieuszkodzone: 1–9, uszkodzone: 10–17.

**Widziane przed zamrożeniem:** nazwy i kształty zmiennych, wektor `states`, README i `shm/data.py`, `shm/simulate.py`
(opis stanów) z repozytorium-kopii. Wyników benchmarku tego repozytorium (`results/`) nie otwierałem.

## 2. Cechy (na pomiar, kanały 2–5)

- **B (klasyczne SHM, 28):** na każdym kanale współczynniki AR(5) (najmniejsze kwadraty, sygnał standaryzowany, cały
  zapis), kurtoza nadwyżkowa, crest factor.
- **T (TIMDR, 13):** `spectral_concentration` macierzy korelacji kanałów 2–5 (cały zapis) + winding / crossing /
  phase_winding na każdym kanale — mediana z 4 kolejnych segmentów po 512 próbek (próbki 0–2047; ograniczenie kosztu
  `crossing`). Funkcje bez zmian (`spectral_family`, `winding_crossing_ms_bridge`, `phase_winding_oam_ms_bridge`).
- **BT:** B ∪ T.

## 3. Detektor i podział

Nowość = średnia odległość euklidesowa do k = 3 najbliższych pomiarów uczących po standaryzacji medianą/MAD
(×1,4826; MAD = 0 → 1) zbioru uczącego. Uczenie tylko na nieuszkodzonych. Fold A: w każdym stanie 1–9 pomiary o parzystym
indeksie (0, 2, …, 8) uczą, nieparzyste testują; fold B odwrotnie. Test: 45 nieuszkodzonych + 80 uszkodzonych.
Miara: AUC (nieuszkodzone testowe vs uszkodzone).

## 4. Hipotezy i kryteria

- **H-główna (wartość dodana):** zysk = AUC(BT) − AUC(B). **SUPPORTED:** ≥ 0,03 w obu foldach. **NOT SUPPORTED:** < 0,03
  w obu. Inaczej **MIESZANY**. **Reguła sufitu:** fold, w którym AUC(B) > 0,97, jest „sufitem”; jeśli oba foldy są sufitem
  → **INCONCLUSIVE (sufit)**. Raport dodatkowy: AUC(T) vs AUC(B).
- **H-ciężkość:** stany 10–14, ciężkość 1–5 (szczelina 0,20 → 0,05 mm), wynik = średnia nowości z obu foldów, 50 pomiarów.
  Dla każdego zestawu: Spearman ρ; **SUPPORTED** dla zestawu, jeśli ρ ≥ 0,5 i p < 0,05.
- **Sztywność/masa (opisowo, bez werdyktu):** próg alarmu = 95. percentyl nowości leave-one-out w zbiorze uczącym;
  odsetek alarmów w testowych pomiarach stanów 2–9 (zmiany masy i sztywności) dla każdego zestawu — niższy = cechy nie mylą
  zmiany sztywności z uszkodzeniem.

## 5. Kontrole (bramka)

- Pozytywna: kopie testowych pomiarów nieuszkodzonych (fold A) z 5 impulsami +5σ w kanale 4 (seed 20260926) vs te same
  pomiary bez impulsów, BT: AUC ≥ 0,8.
- Negatywna: etykiety uszkodzony/nieuszkodzony w teście fold A permutowane (seed 20260926), BT: AUC w [0,35; 0,65].
- Niezaliczona kontrola → INCONCLUSIVE.

## 6. Zasady

Jedno uruchomienie; żadnych zmian cech, k, podziału, progów po zobaczeniu wyników. Właściwości materiałowe (wytrzymałość,
rozciągliwość) nie są mierzone przez te dane — drgania niosą informację o sztywności, masie i nieliniowości kontaktu.
