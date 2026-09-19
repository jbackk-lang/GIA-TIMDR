# B4-Kitchen v0.2 — prerejestracja poprawki metody statystycznej

**Status: PREREGISTERED, NOT YET RUN.** Zamrożone przed dotknięciem
jakiegokolwiek nowego wyniku. Osobna prerejestracja od
`B3_KITCHEN_PREREG_v0.1.md`/`B4_KITCHEN_ADDENDUM_v0.1.md` — nie jest ich
edycją ani kontynuacją. `B4_KITCHEN_ADDENDUM_v0.1.md` §"Werdykt" wprost
zabrania kolejnych przebiegów z innym seedem/oknem/mikrofonem/
triangulacją/metodą Q/orientacją hipotezy/filtrowaniem klatek — v0.2 nie
zmienia żadnej z tych rzeczy. Zmienia się **wyłącznie metoda budowy
rozkładu null** dla testu istotności, z jawnie udokumentowanego, uczciwie
zgłoszonego powodu opisanego w §1.

## 0. Zgoda użytkownika

Ta prerejestracja powstaje na wyraźną prośbę użytkownika ("osobna
prerejestracja") po tym, jak druga wiadomość opisująca "kontynuację" B4
Kitchen okazała się (a) opisywać już ukończony przebieg v0.1, (b) używać
nazw plików niezgodnych z realną strukturą repo, i (c) łamać zakaz
kolejnych przebiegów z `B4_KITCHEN_ADDENDUM_v0.1.md`. Użytkownik
potwierdził, że chce nowej, osobnej prerejestracji zamiast kontynuacji
zamrożonego v0.1.

## 1. Dlaczego v0.2 — dokładny, udokumentowany powód

Wynik `B4_KITCHEN_RESULT_v0.1.json` (już w repo, commit z tej sesji):
werdykt **INCONCLUSIVE**, bo prerejestrowana kontrola negatywna
(dwie niezależne serie AR(1), `phi=0.8`, długość 1645, seedy `20260917`/
`20260918`) dała **fałszywie istotną** korelację rangową w pełnym teście
permutacyjnym: `rho=0.115`, `p=0.0002` (próg `alpha=0.05`) — `controls.passed
= false` w zapisanym wyniku.

**Diagnoza:** pełny test permutacyjny (losowa permutacja WSZYSTKICH 1645
wartości jednej serii względem drugiej) zakłada wymienialność
(exchangeability) obserwacji pod hipotezą zerową. Dla serii z krótkozasięgową
autokorelacją (AR(1), i ogólniej — bloków `Λ` licznych z zachodzących na
siebie okien czasowych sygnału ciągłego, jak `lambda_g`/`lambda_meta` w
v0.1) to założenie jest fałszywe: permutacja niszczy autokorelację
WEWNĄTRZ każdej serii, zawężając rozkład null bardziej niż rzeczywista
zmienność uzasadnia, co zawyża odsetek fałszywych detekcji. To znany,
udokumentowany problem testów permutacyjnych na szeregach czasowych (nie
odkrycie tej sesji) — standardowym remedium jest permutacja BLOKOWA
(block permutation / moving block bootstrap), zachowująca strukturę
autokorelacji wewnątrz bloku, niszcząca wyłącznie powiązanie MIĘDZY
dwiema seriami.

## 2. Dane wejściowe — DOKŁADNIE te same co v0.1, bez zmian

Ten sam zbiór, ta sama triangulacja, ten sam alignment czasu, te same
hashe co `docs/geometry/b4_kitchen_manifest_template.json`:

```text
dataset_id: CMU_KITCHEN_S13_BROWNIE_v0.1
mocap_archive_sha256:      77609D7ECF8478C68013F2C040F9D48C7B560B828EF7C27DEFB9CF6B4E93AA9F
microphone_archive_sha256: 27A1AD07AD05CD6C2AEA951B34DD35C029E52D758AABCDC998BBDA6440A8DC15
triangulation_sha256:      9BCDFD51CE489063B2F18A652A31D1882FC7BE52C65100E87F866A91ECFF55E8
window_size: 50
n_blocks: 1645 (Λ_G i Λ_META,disp, tożsame z v0.1)
```

Żadna geometria, żadne audio, żadna triangulacja, żaden alignment nie są
tu ponownie definiowane ani zmieniane — v0.2 startuje z DOKŁADNIE tych
samych 1645 par `(lambda_g, lambda_meta)`, jakie wyprodukował
`core/b4_kitchen_run.py` dla v0.1. Powtórna ekstrakcja geometrii/audio nie
jest częścią v0.2 (bez ryzyka nowego błędu w tej warstwie).

## 3. Poprawka: cyrkularny test permutacji blokowej

Zamiast permutować 1645 pojedynczych wartości niezależnie, permutujemy
**bloki nachodzących sekwencyjnie wartości** (circular block permutation,
Politis & Romano 1992/Hall-Horowitz-Jing 1995 dla statystyk zależnych od
autokorelacji).

**Długość bloku `L`** — zamrożona PRZED uruchomieniem, wyliczona z
heurystyki `L = round(n^(1/3))`, standardowego wyboru rzędu wielkości dla
bootstrapu blokowego (nie dobrana z próby-błędu na tych danych):

```text
n = 1645
L = round(1645^(1/3)) = round(11.83) = 12
```

**Algorytm (frozen, pseudokod):**

```text
wejście: x (lambda_g, dł. n), y (lambda_meta, dł. n), L=12, seed
rho_obs = spearman(x, y)
dla każdej z 10 000 permutacji:
    # cyrkularne przesunięcie y o losowy offset, potem podział na bloki
    # dł. L i losowa permutacja KOLEJNOŚCI bloków (nie zawartości)
    offset = rng.integers(0, n)
    y_shifted = concat(y[offset:], y[:offset])   # cyrkularne przesunięcie
    bloki = podziel y_shifted na ceil(n/L) bloków po L (ostatni krótszy)
    y_perm = konkatenacja bloków w losowej kolejności, przycięta do n
    rho_perm = spearman(x, y_perm)
p_value = (1 + count(|rho_perm| >= |rho_obs|)) / 10001
```

Cyrkularne przesunięcie PRZED podziałem na bloki (nie stały podział) —
żeby granice bloków nie były zawsze w tych samych miejscach szeregu,
zgodnie ze standardową wersją cyrkularnego bootstrapu blokowego.

**Wszystko inne bez zmian względem v0.1:** `N_PERMUTATIONS=10_000`,
`SEED=20_260_919`, `ALPHA=0.05`, definicja `Lambda(x)` (dokładnie ta sama
funkcja `std/(std+|mean|+1e-9)`), test główny to wciąż dwustronny Spearman.

## 4. Kontrole — MUSZĄ przejść obiema metodami naraz

Dokładnie te same dwie syntetyczne kontrole co w
`B4_KITCHEN_ADDENDUM_v0.1.md` (te same generatory, te same seedy), ale
oceniane teraz NOWĄ metodą permutacji blokowej:

- **(+) pozytywna**: dwa identyczne monotoniczne wektory długości 1645,
  seed `20260919` — musi dać `p < 0.05` (metoda blokowa nie może stracić
  czułości na oczywisty sygnał).
- **(−) negatywna**: dwie niezależne serie AR(1), `phi=0.8`, długość 1645,
  seedy `20260917`/`20260918` — **musi teraz dać `p >= 0.05`** (to
  dokładnie ta kontrola, która ujawniła wadę w v0.1; jeśli permutacja
  blokowa dalej daje fałszywie istotny wynik na tej samej kontroli,
  poprawka nie działa i v0.2 kończy się `INCONCLUSIVE` bez uruchamiania
  testu głównego, tak jak v0.1).

Werdykt główny liczy się WYŁĄCZNIE, gdy obie kontrole przejdą — identyczna
brama jak w v0.1 (`controls.passed`).

## 5. Werdykt

- **SUPPORTED** — obie kontrole przechodzą NOWĄ metodą i `p_main < 0.05`.
- **NOT SUPPORTED** — obie kontrole przechodzą i `p_main >= 0.05`.
- **INCONCLUSIVE** — którakolwiek kontrola nie przechodzi (w tym: jeśli
  poprawka blokowa nadal nie naprawia negatywnej kontroli).

## 6. Zasada anty-tuningu (bez zmian względem v0.1)

Po uruchomieniu v0.2 nie wolno zmieniać: `L` (długości bloku), liczby
permutacji, seeda, progu `alpha`, definicji `Lambda`, kierunku hipotezy,
ani wracać do pełnej (niezablokowanej) permutacji, jeśli wynik nie
spodoba się — na podstawie uzyskanego wyniku. Zmiana którejkolwiek z tych
rzeczy po zobaczeniu wyniku oznacza nową prerejestrację (v0.3), nie
edycję v0.2.

## 7. Co v0.2 NIE rozstrzyga

Nawet SUPPORTED w v0.2 nie byłoby niezależnym potwierdzeniem częściej niż
jeden przebieg na jednym zbiorze danych (CMU Kitchen S13 Brownie) —
dokładnie to samo zastrzeżenie o replikacji, jakie dotyczy każdego
pojedynczego wyniku w tym ekosystemie. v0.2 rozstrzyga wyłącznie, czy
wada metody statystycznej z v0.1 była tym, co uniemożliwiło odczytanie
wyniku — nie tworzy nowego aksjomatu w żadnym przypadku.

## 8. Implementacja i dane źródłowe

Implementacja: nowy plik `core/b4_kitchen_run_v0_2.py`, reużywający bez
zmian funkcje ekstrakcji geometrii/audio z `core/b4_kitchen_run.py`
(`_read_times`, `_read_vertices`, `_read_q`, `_h_trace`, `_lambda`,
`_blocks`) — zmienia się wyłącznie `_permutation_test` (nowa wersja
blokowa) i `_controls`. Surowe archiwa (`S13_Brownie_Mocap.zip`,
`S13_Brownie_Audio.zip`) muszą być dostępne lokalnie pod tą samą ścieżką
co w v0.1 (`C:\Users\jback\Downloads\`) — poza folderem połączonym z tą
sesją; uruchomienie wymaga dostępu do tych plików z maszyny, na której
działa skrypt.

## 9. Status końcowy

**Candidate B4-Kitchen v0.2 — preregistered, not run.** Żadna z sekcji
1-8 nie może się zmienić po zobaczeniu wyniku testu głównego ani kontroli.
