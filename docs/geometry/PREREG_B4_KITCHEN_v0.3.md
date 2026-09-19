# B4-Kitchen v0.3 — prerejestracja metody Spearman z korektą n_eff AR(1)

**Status: PREREGISTERED, NOT YET RUN.** Zamrożone przed dotknięciem
jakiegokolwiek nowego wyniku na realnych danych Kitchen — łącznie z
negatywną kontrolą poniżej, której wynik na tych konkretnych ziarnach
NIE został sprawdzony przed zapisaniem tego dokumentu (patrz §3). Osobna
prerejestracja od `B3_KITCHEN_PREREG_v0.1.md`/`B4_KITCHEN_ADDENDUM_v0.1.md`
i od `PREREG_B4_KITCHEN_v0.2.md` — żadna z tamtych nie jest edytowana.

## 0. Kontekst — dlaczego v0.3, nie kolejna zmiana w v0.2

`RESULT_B4_KITCHEN_v0.2.json`: permutacja blokowa L=12 poprawiła kontrolę
negatywną ~86× względem v0.1 (p: 0.0002→0.0173), ale wciąż nie przeszła
progu `alpha=0.05` na zamrożonej parze ziaren `20260917`/`20260918`.
Zamiast dalej ręcznie próbować kolejnych `L` na TEJ SAMEJ parze ziaren (co
byłoby dokładnie tym rodzajem post-hoc tuningu, którego zakazuje własna
zasada anty-tuningu v0.2 §6), przeprowadzono metodologiczne badanie
WYŁĄCZNIE na danych syntetycznych — `B4_KITCHEN_v03_METHOD_SELECTION.md`.
Kluczowe ustalenie stamtąd: **żadna z 10 wypróbowanych metod (4 długości
bloku, 5 przepustowości HAC, korekta n_eff AR(1)) nie przeszła TEJ JEDNEJ
zamrożonej pary ziaren** — ale test o `alpha=0.05` z definicji odrzuca
prawdziwą hipotezę zerową w ~5% przypadków, więc pojedyncze losowanie nie
może rozstrzygnąć, czy metoda jest wadliwa, czy to był pechowy traf.
Kalibracja na 300 NIEZALEŻNYCH losowaniach AR(1) (inne ziarna, wygenerowane
regułą, nie ręcznie) pokazała, że **korekta n_eff AR(1) i korekta HAC są
obie statystycznie zgodne z poprawną kalibracją** (odsetek fałszywych
alarmów 4.33% i 5.33%, oba przedziały ufności zawierają nominalne 5%).

## 1. Dane wejściowe — DOKŁADNIE te same co v0.1/v0.2

Ten sam zbiór, triangulacja, alignment czasu, hashe co
`docs/geometry/b4_kitchen_manifest_template.json` (patrz `PREREG_B4_KITCHEN_v0.2.md`
§2 dla pełnych hashy — nie powtarzane tu). v0.3 startuje z DOKŁADNIE tych
samych 1645 par `(lambda_g, lambda_meta)`, jakie wyprodukował
`core/b4_kitchen_run_v0_2.py` (identyczne z v0.1). Zero ponownej ekstrakcji
geometrii/audio.

## 2. Metoda: Spearman z korektą efektywnej liczebności próby AR(1)

Wybrana w `B4_KITCHEN_v03_METHOD_SELECTION.md` §4 na podstawie kalibracji
na danych WYŁĄCZNIE syntetycznych (nigdy realnych Kitchen). Definicja
(frozen, identyczna z `ar1_effective_n_spearman()` w
`core/_kitchen_v03_candidate_methods_synthetic_only.py`):

```text
rx, ry = rangi(x), rangi(y)  (wyśrodkowane)
rho = spearman(x, y)
r1x = lag-1 autokorelacja rx (wyśrodkowanych rang x)
r1y = lag-1 autokorelacja ry (wyśrodkowanych rang y)
n_eff = n · (1 − r1x·r1y) / (1 + r1x·r1y)     [dolne obcięcie: n_eff ≥ 3]
t = rho · sqrt((n_eff − 2) / (1 − rho²))
p = erfc(|t| / sqrt(2))     [przybliżenie normalne rozkładu t dla dużego n_eff]
```

Żaden parametr swobodny (brak długości bloku, brak przepustowości) — jedyny
wybór to sama forma korekty (Bartlett-owska efektywna liczebność próby dla
dwóch procesów AR(1)), zamrożona przed uruchomieniem na realnych danych.

## 3. Kontrole — NOWE ziarna, wygenerowane regułą PRZED sprawdzeniem wyniku

**Ziarna `20260917`/`20260918` z v0.1/v0.2 NIE są tu ponownie używane** —
już wiadomo, że ta para daje p=0.0233 dla tej metody (§1 w
`B4_KITCHEN_v03_METHOD_SELECTION.md`), więc jej zamrożenie jako "kontrola"
nie miałoby wartości diagnostycznej. Nowe ziarna wygenerowane
MECHANICZNIE, bez ręcznego wyboru i **bez sprawdzenia, czy przechodzą,
przed zapisaniem tego dokumentu**:

```python
import hashlib
seed_x = int(hashlib.sha256(b"B4_KITCHEN_v0.3_NEG_X").hexdigest()[:8], 16) % 10_000_000
seed_y = int(hashlib.sha256(b"B4_KITCHEN_v0.3_NEG_Y").hexdigest()[:8], 16) % 10_000_000
# seed_x = 1452413
# seed_y = 9303707
```

- **(+) pozytywna**: dwa identyczne monotoniczne wektory długości 1645,
  seed `20260919` (bez zmian z v0.1/v0.2 — ta kontrola zawsze przechodzi
  niezależnie od metody, brak ryzyka cherry-pickingu).
- **(−) negatywna**: dwie niezależne serie AR(1), `phi=0.8`, długość 1645,
  **seedy `1452413`/`9303707`** (nowe, powyżej).

Werdykt główny liczy się WYŁĄCZNIE, gdy obie kontrole przejdą — identyczna
brama jak w v0.1/v0.2.

## 4. Werdykt

- **SUPPORTED** — obie kontrole przechodzą i `p_main < 0.05`.
- **NOT SUPPORTED** — obie kontrole przechodzą i `p_main >= 0.05`.
- **INCONCLUSIVE** — którakolwiek kontrola nie przechodzi.

Jeśli NOWA para ziaren negatywnej kontroli też nie przejdzie: to NIE
uruchamia kolejnej rundy "spróbuj inne ziarno" — `B4_KITCHEN_v03_METHOD_SELECTION.md`
§3 już pokazał, że metoda jest kalibrowana w agregacie (300 losowań); jedno
kolejne niefortunne losowanie byłoby zgodne z oczekiwanym ~5% odsetkiem
fałszywych alarmów, nie dowodem przeciwko metodzie. W takim wypadku wynik
zostanie zgłoszony jako INCONCLUSIVE z jawnym wyjaśnieniem tego rozróżnienia
— bez dalszych prób zmiany ziaren w ramach v0.3.

## 5. Zasada anty-tuningu

Po uruchomieniu v0.3 nie wolno zmieniać: formy korekty n_eff, ziaren
kontrolnych, progu `alpha`, definicji `Lambda`, kierunku hipotezy — na
podstawie uzyskanego wyniku. Zmiana którejkolwiek z tych rzeczy po
zobaczeniu wyniku oznacza nową prerejestrację (v0.4).

## 6. Co v0.3 NIE rozstrzyga

Tak jak v0.1/v0.2: nawet SUPPORTED nie byłoby niezależnym potwierdzeniem
poza jednym przebiegiem na jednym zbiorze danych. Permutacja blokowa
pozostaje niezweryfikowana wielokrotnie (zbyt kosztowna obliczeniowo w tej
sesji) — jeśli ktoś w przyszłości zweryfikuje jej kalibrację na wielu
losowaniach i okaże się równie dobra, mogłaby być alternatywną metodą dla
v0.4, nie zastępstwem dla v0.3 post-hoc.

## 7. Status końcowy

**Candidate B4-Kitchen v0.3 — preregistered, not run.** Sekcje 1-6 nie
mogą się zmienić po zobaczeniu wyniku testu głównego ani kontroli.
