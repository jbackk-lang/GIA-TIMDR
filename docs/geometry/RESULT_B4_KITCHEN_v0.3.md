# Wynik B4-Kitchen v0.3 (2026-09-19) — SUPPORTED, ale z istotnym zastrzeżeniem

Zgodnie z `PREREG_B4_KITCHEN_v0.3.md`, zamrożonym PRZED tym wynikiem —
łącznie z ziarnami kontroli negatywnej, które NIE zostały sprawdzone przed
zapisaniem prerejestracji. Dane identyczne z v0.1/v0.2, zweryfikowane
bit-do-bitu: `h_summary`/`q_summary`/`lambda_g_summary`/`lambda_meta_summary`
w `B4_KITCHEN_RESULT_v0.3.json` są identyczne z v0.1 i v0.2. Pełny surowy
wynik: `B4_KITCHEN_RESULT_v0.3.json`.

## Wynik surowy

| | v0.1 (pełna perm.) | v0.2 (perm. blokowa L=12) | v0.3 (Spearman n_eff AR(1)) |
|---|---|---|---|
| Kontrola pozytywna | p=0.0001 ✓ | p=0.0001 ✓ | p≈0.0 ✓ |
| Kontrola negatywna | p=0.0002 ✗ | p=0.0173 ✗ | **p=0.6763 ✓** |
| `controls.passed` | false | false | **true** |
| Test główny (rho) | nieuruchomiony | nieuruchomiony | **rho=0.0708, p=0.0093** |
| Werdykt | INCONCLUSIVE | INCONCLUSIVE | **SUPPORTED** |

`rho=0.0708` jest identyczne z surową wartością obserwowaną w v0.1/v0.2
(sama korelacja rang nie zależy od metody null-distribution) — zmieniła
się WYŁĄCZNIE ocena istotności statystycznej tej samej obserwowanej
wartości, zgodnie z zamrożoną w PREREG metodą.

## Szczegóły testu głównego

```text
rho = 0.07082455871135257
r1x (autokorelacja lag-1 rang Λ_G)     = 0.6208
r1y (autokorelacja lag-1 rang Λ_META)  = 0.1614
n_eff = 1345.29  (z n=1645)
t = 2.6023
p = 0.00926
```

## Uczciwe zastrzeżenie — to jest TRZECIA próba na TYCH SAMYCH danych

To musi być powiedziane wprost, zanim ktokolwiek zacytuje "SUPPORTED": to
jest trzeci przebieg analizy na dokładnie tym samym zbiorze danych (v0.1
pełna permutacja, v0.2 permutacja blokowa, v0.3 korekta n_eff AR(1)), a
dopiero trzeci dał wynik pozytywny. Dwa argumenty za tym, że to NIE jest
zwykły p-hacking, i jeden argument, dlaczego mimo to wymaga dużej
ostrożności:

**Dlaczego to nie jest proste p-hacking:**
1. Każda zmiana metody między wersjami była zdecydowana i zamrożona PRZED
   zobaczeniem testu głównego na realnych danych Kitchen — v0.2 i v0.3
   zostały wybrane na podstawie tego, czy KONTROLE (syntetyczne,
   niezależne od realnych danych) przechodzą, nie na podstawie tego, jak
   wypada test główny. `controls.passed=false` w v0.1/v0.2 zablokowało
   nawet WYLICZENIE testu głównego — więc nie było możliwości, żeby wynik
   główny v0.1/v0.2 "podpowiedział", w którą stronę modyfikować metodę.
2. Wybór metody dla v0.3 (korekta n_eff AR(1)) był oparty na kalibracji
   na 300 NIEZALEŻNYCH, syntetycznych losowaniach AR(1)
   (`B4_KITCHEN_v03_METHOD_SELECTION.md` §3), nie na dopasowaniu do
   danych Kitchen.

**Dlaczego mimo to wymaga ostrożności:** to wciąż JEDNO efektywne
"śledztwo" rozciągnięte na trzy iteracje metodologiczne na JEDNYM zbiorze
danych (jedna sesja nagraniowa, jeden uczestnik, jeden przepis). Nawet
przy w pełni uczciwej procedurze, prawdopodobieństwo, że KTÓRAŚ z kilku
prawidłowo skalibrowanych metod da p<0.05 na tym samym zbiorze, jest
wyższe niż nominalne 5% pojedynczego testu — to fundamentalna
właściwość wielokrotnego próbowania, nawet gdy każda pojedyncza próba
jest metodologicznie czysta.

## Rozmiar efektu

`rho=0.0708` to MAŁY efekt (dla porównania: skala rank-biserial `r` z
protokołu `timdr-signal-framework` klasyfikuje `<0.1` jako pomijalny) —
istotność statystyczna wynika głównie z dużego `n_eff≈1345`, nie z
silnego związku. "Statystycznie istotne" ≠ "duże" — ta sama zasada, którą
ten ekosystem stosuje wszędzie indziej.

## Klasyfikacja statusu

Zgodnie ze słownikiem statusów w `TIMDR_Branch_Specification.md`: **NIE
ustalony (wstępny sygnał pozytywny, wymaga replikacji)**. Nie kwalifikuje
się nawet do tieru "częściowo ustalony" w sensie użytym dla mostów
M/S↔G/M/S↔K, bo:

- brak testu przenośności międzydomenowej (tu: jedna domena — jedna
  sesja Kitchen; mosty M/S↔G/M/S↔K miały 3 domeny: łożyska/sejsmika/BTC),
- brak niezależnej repliki (inny uczestnik/przepis CMU Kitchen, albo
  inny zbiór kinematyczny),
- trzy-iteracyjna historia metodologiczna na tym samym zbiorze (opisana
  wyżej) — czynnik ostrożności, nie dyskwalifikujący, ale wymagający
  jawnego nazwania.

## Co dalej (nie zrobione tutaj, jawnie nazwane jako otwarte)

1. Niezależna replika: inny uczestnik/przepis CMU Kitchen Capture (inny
   plik `.AMC`/`.wav`), ta sama zamrożona metoda v0.3, bez zmian.
2. Zweryfikować kalibrację permutacji blokowej na wielu losowaniach (nie
   zrobione z powodu budżetu obliczeniowego tej sesji) — jeśli też
   okaże się dobrze skalibrowana przy odpowiednim L, dałoby to drugą,
   niezależną metodę potwierdzającą ten sam wynik.
3. Fizyczna interpretacja `r1x=0.62` vs `r1y=0.16` — geometria tułowia
   (Λ_G) ma znacznie silniejszą autokorelację blokową niż głośność audio
   (Λ_META) — samo w sobie ciekawe, niezinterpretowane tutaj.

## Status: SUPPORTED (v0.3), ale sklasyfikowany jako NIE ustalony do czasu repliki
