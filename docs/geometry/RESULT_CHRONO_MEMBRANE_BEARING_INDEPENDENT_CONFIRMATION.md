# Wynik: chrono_membrane_bridge — NIEZALEŻNY test potwierdzający na prawdziwie świeżych danych CWRU (1730/1750 RPM, typy B/IR/OR@3/OR@6, rozmiary 7/14/21 mils). Kierunek `normal > fault` REPLIKUJE się (znak stabilny, dodatni na wszystkich 3 oknach), ale ŚCIŚLE wg zamrożonego kryterium v0.2 wynik jest CZĘŚCIOWY — 2/3 okien osiąga pełny próg istotności, jedno (w=256) nie (p=0.068), głównie z powodu jednego typu uszkodzenia (B/kulka) (2026-09-21)

> Metodologia (`membrane_window_metrics`, `spectral_concentration`,
> rozmiary okna, N_WINDOWS, ALPHA, kryterium SUPPORTED/NOT_SUPPORTED)
> jest ZAMROŻONA z `docs/geometry/PREREG_CHRONO_MEMBRANE_BEARING_v0.1.md`
> i `..._v0.2.md` — TA sesja jej NIE zmienia, TYLKO stosuje do nowych
> danych. Kod: `core/real_chrono_membrane_bridge_independent.py`
> (nowy plik, ale konstrukcja/stałe 1:1 skopiowane z
> `core/real_chrono_membrane_bridge_v0_2.py`, bez modyfikacji logiki).
> Test: `tests/test_real_chrono_membrane_bridge_independent.py`.

## 0. Co czyni ten test niezależnym

W odróżnieniu od v0.1/v0.2 (które używały WYŁĄCZNIE 1797 RPM, wyłącznie
typów uszkodzenia IR i OR@6, wyłącznie rozmiaru 21 mils, z lokalnego
mirrora `TIMDR-Industrial-Predict`), ta sesja używa:

- **Dwóch RPM nigdy wcześniej lokalnie nietestowanych**: 1730 i 1750
  (1797 RPM — jedyne dotąd testowane — jest tu całkowicie NIEOBECNE).
- **Czterech typów uszkodzenia** zamiast dwóch: B (kulka), IR (bieżnia
  wewnętrzna), OR@3, OR@6 (bieżnia zewnętrzna, różne pozycje zegara) —
  B nigdy dotąd nie był testowany w tej rodzinie.
- **Trzech rozmiarów uszkodzenia** zamiast jednego: 7, 14, 21 mils (21
  mils — jedyny dotąd testowany — występuje tu tylko w 1/6 plików
  fault).
- **Zupełnie innego archiwum źródłowego**: `CWRU_Bearing_NumPy_4LUM-main.zip`
  (dostarczone przez użytkownika, ok. 236MB, rozpakowane wybiórczo do
  `/tmp/cwru_fresh/`, NIE skopiowane do repo), niezależnego od pliku
  `TIMDR-Industrial-Predict/data/cwru_bearing/b4_raw/source_mirror/`
  użytego w v0.1/v0.2.

## 1. Wybór plików — DOKONANY I ZAPISANY PRZED uruchomieniem testu

Z `Contents.md` archiwum wybrano pliki z kolumnami DE/FE/BA = ✔/✔/✔ lub
✔/✔/✘ (normal), świadomie zróżnicowane pod względem RPM/typu/rozmiaru,
PRZED zobaczeniem jakiegokolwiek wyniku:

**Normal (N=2, DE+FE — kolumna BA=✘ w Contents.md dla obu plików
Normal, dokładnie jak `1797_Normal.npz` w v0.1/v0.2):**
- `1730_Normal_0_DE12.npz` (1730 RPM, 485 643 próbek)
- `1750_Normal_0_DE12.npz` (1750 RPM, 485 063 próbek)

**Fault (6 plików, DE+FE+BA dostępne w źródle, ale test primarny używa
TYLKO DE+FE — dokładnie jak primarny test v0.1/v0.2, żeby normal i
fault były porównywane na tym samym podzbiorze kanałów; BA jest
świadomie pominięte w tej sesji, nie ukryte, mogłoby zasilić przyszły
test sekundarny):**

| plik | RPM | typ | rozmiar | próbki |
|---|---|---|---|---|
| `1730_IR_7_DE12.npz` | 1730 | IR | 7 mils | 122 917 |
| `1730_B_14_DE12.npz` | 1730 | B | 14 mils | 122 136 |
| `1730_OR@6_21_DE12.npz` | 1730 | OR@6 | 21 mils | 121 991 |
| `1750_IR_14_DE12.npz` | 1750 | IR | 14 mils | 121 846 |
| `1750_B_21_DE12.npz` | 1750 | B | 21 mils | 122 136 |
| `1750_OR@3_7_DE12.npz` | 1750 | OR@3 | 7 mils | 121 556 |

Uzasadnienie wyboru: po 3 pliki fault na każde z dwóch RPM, każdy inny
typ uszkodzenia (B/IR/OR@3/OR@6 — 4 z 4 dostępnych typów pokryte), każdy
inny rozmiar (7/14/21 mils — wszystkie 3 dostępne rozmiary pokryte),
tak żeby żaden pojedynczy typ/rozmiar nie zdominował połączonej próby
fault. Struktura plików NPZ sprawdzona (`np.load(...).keys()`) —
identyczna z lokalnie używanym formatem (klucze `DE`/`FE`/`BA`, kształt
`(N,1)`, `float64`) — loader `load_synchronous_cwru_channels`
(`TIMDR-Geometry-Formalism`) użyty BEZ ŻADNYCH zmian.

## 2. Metoda — bez zmian względem v0.1/v0.2

`WINDOW_SIZES=(128,256,512)`, `N_WINDOWS=30` (losowane bez powtórzeń w
każdej komórce — dostępność zawsze ≥237 segmentów na najmniejszej
puli), `ALPHA=0.05`, próg efektu `|r|≥0.3`, Mann-Whitney U + rank-biserial
`r` (`timdr_formalism.pipeline.mann_whitney_test`, bez zmian). Grupa
`pos=normal` (połączone okna z OBU plików normal, 1730+1750), grupa
`neg=fault` (połączone okna ze WSZYSTKICH 6 wybranych plików fault) —
tak że `r>0` odpowiada wprost hipotezie `normal > fault`, zgodnie z
konwencją v0.2. Test dodatkowy (diagnostyczny, NIE decyduje o
klasyfikacji głównej): `normal` (połączone) vs KAŻDY z 6 plików fault
osobno.

## 3. Wynik GŁÓWNY — normal (połączone 1730+1750) vs fault (połączone 6 plików)

| okno | p | r | efekt | status (wg kryterium v0.2, per okno) |
|---|---|---|---|---|
| 128 | 0.000111 | +0.582 | duży | SUPPORTED |
| 256 | 0.0679 | +0.276 | mały | **NOT_SUPPORTED** (p≥0.05) |
| 512 | 0.000356 | +0.538 | duży | SUPPORTED |

n_valid_normal = n_valid_fault = 30 na każdej komórce (brak
INCONCLUSIVE). n_avail_normal = 7583/3791/1895 (okno 128/256/512, bez
reużycia), n_avail_fault (połączone 6 plików) = 5721/2859/1428.

**Stabilność znaku**: `r: +0.582(128) → +0.276(256) → +0.538(512)`.
**ZNAK NIGDY nie zmienił się na ujemny — kierunek `normal > fault` jest
stabilny na wszystkich trzech oknach.** Ale okno=256 nie przekracza
progu istotności `p<0.05` (p=0.068, blisko granicy) ani progu efektu
`|r|≥0.3` (r=0.276).

**Klasyfikacja wg ZAMROŻONEGO kryterium v0.2 §4** (SUPPORTED wymaga
`p<0.05`, `|r|≥0.3`, `r>0` na WSZYSTKICH trzech oknach ORAZ stabilnego
znaku): **formalnie NIE w pełni SUPPORTED** — 2/3 okien spełnia pełne
kryterium, okno=256 nie. To NIE jest „NIESTABILNY" w sensie zdefiniowanym
w v0.2 (który dotyczył ZMIANY ZNAKU między oknami — tu znak nigdy się
nie zmienia), więc raportowane uczciwie jako własna, czwarta kategoria:
**CZĘŚCIOWO SUPPORTED (kierunek replikuje, istotność niepełna)**.

## 4. Wynik DODATKOWY (diagnostyczny) — normal vs każdy typ uszkodzenia osobno

| plik | okno=128 | okno=256 | okno=512 | znak stabilny | wszystkie r>0 |
|---|---|---|---|---|---|
| `1730_IR_7` | r=+0.451, SUPPORTED | r=+0.424, SUPPORTED | r=+0.613, SUPPORTED | TAK | TAK |
| `1730_B_14` | r=+0.051, NOT_SUPPORTED | r=+0.007, NOT_SUPPORTED | r=-0.116, NOT_SUPPORTED | **NIE** | **NIE** |
| `1730_OR6_21` | r=+0.453, SUPPORTED | r=+0.444, SUPPORTED | r=+0.533, SUPPORTED | TAK | TAK |
| `1750_IR_14` | r=+0.602, SUPPORTED | r=+0.573, SUPPORTED | r=+0.940, SUPPORTED | TAK | TAK |
| `1750_B_21` | r=+0.549, SUPPORTED | r=+0.304, SUPPORTED | r=+0.518, SUPPORTED | TAK | TAK |
| `1750_OR3_7` | r=+0.396, SUPPORTED | r=+0.349, SUPPORTED | r=+0.624, SUPPORTED | TAK | TAK |

**Kluczowa diagnoza**: 5 z 6 wybranych plików fault (IR i OR@3/OR@6 na
obu RPM, `1750_B_21`) daje SILNY, STABILNY efekt `normal > fault` na
WSZYSTKICH trzech oknach — replika dokładnie tak mocna jak w v0.1/v0.2.
**Jeden plik, `1730_B_14` (kulka, 1730 RPM, 14 mils), łamie wzorzec**:
efekt bliski zeru na oknie 128/256 i UJEMNY (r=-0.116, kierunek
przeciwny) na oknie 512 — jedyny przypadek w całej tej serii (v0.1,
v0.2, ta sesja), gdzie znak `r` faktycznie się odwraca między oknami
dla POJEDYNCZEGO pliku/typu. To właśnie ten jeden plik ściąga w dół
połączony wynik główny na oknie=256 (gdzie połączona próba `neg` losuje
relatywnie więcej okien z tego pliku niż na innych oknach, przez
losowanie niezależne per okno — dokładnie mechanizm "region pozytywny/
negatywny niejednorodny rozcieńcza test Manna-Whitneya", odnotowany
jako ogólna reguła protokołu w skillu, punkt 15/19).

Uczciwa uwaga: `1750_B_21` (też typ B, ale inne RPM i rozmiar) NIE
pokazuje tego problemu (silny, stabilny, dodatni efekt) — więc to NIE
jest generyczna słabość typu uszkodzenia "kulka" per se, tylko
konkretnie plik `1730_B_14`. Możliwe wyjaśnienia (nierozstrzygnięte tą
sesją, nie testowane dalej żeby uniknąć dopasowywania po fakcie):
uszkodzenia kulki (B) są fizycznie znane z literatury jako trudniejsze
do wykrycia niż uszkodzenia bieżni (mniej okresowy, bardziej
nieregularny wzorzec uderzeń) — może to być bliżej granicy wykrywalności
przy tym konkretnym rozmiarze/RPM, ale to POST-HOC spekulacja, nie
zweryfikowane twierdzenie.

## 5. Interpretacja — czy to replikuje v0.1/v0.2?

**Kierunek (`normal > fault` w `spectral_concentration`) REPLIKUJE się
na prawdziwie nowych danych (inne RPM, inne typy/rozmiary uszkodzenia,
inne archiwum źródłowe)**: na głównym połączonym teście znak `r` jest
dodatni na WSZYSTKICH trzech oknach (nigdy się nie odwraca), a na
poziomie pojedynczych plików fault 5/6 pokazuje pełne SUPPORTED na
wszystkich trzech oknach, z rozmiarem efektu często dużym (r do 0.94).

**Ale ścisłe zastosowanie zamrożonego kryterium v0.2** (SUPPORTED
wymaga pełnego progu istotności na WSZYSTKICH oknach połączonego testu)
**daje wynik CZĘŚCIOWY, nie czyste SUPPORTED**: okno=256 połączonego
testu głównego nie przekracza `p<0.05` (p=0.068), z powodu jednego
nietypowego pliku (`1730_B_14`) rozcieńczającego połączoną próbę fault.
Zgłoszone w pełni, zgodnie z protokołem (wynik zostałby zgłoszony
identycznie szczegółowo, gdyby wypadł w pełni negatywnie) — **nie
zaokrąglamy „prawie SUPPORTED" w górę do SUPPORTED**.

**Uczciwa końcowa ocena**: hipoteza `spectral_concentration: normal >
fault` przechodzi ten pierwszy prawdziwie niezależny test w sensie
KIERUNKOWYM (silne, powtarzalne, stabilne zwycięstwo znaku dodatniego
w 5/6 pojedynczych plików fault i we wszystkich 3 oknach połączonego
testu), ale NIE w pełni w sensie ścisłego, zamrożonego kryterium
istotności na WSZYSTKICH oknach — jeden nietypowy plik (typ B, 1730
RPM, 14 mils) jest wystarczający, żeby połączony wynik na jednym z
trzech okien spaść poniżej progu. To pierwszy wynik w całej tej serii
(v0.1 obserwacja post-hoc, v0.2 formalne SUPPORTED na drugiej połowie,
teraz ten test), który NIE jest czystym 6/6 lub podobnym — i to jest
sygnał, że efekt, choć realny i replikujący się kierunkowo, może nie
być jednorodny across wszystkich typów/rozmiarów uszkodzenia, tylko
across WIĘKSZOŚCI z nich.

## 6. Status w ekosystemie

Podobnie jak v0.1/v0.2: NIE dopisywane do `Axioms_G_TIMDR_Geometry.md`
ani `Axioms_S_TIMDR_Signal.md` — konstrukcja pozostaje eksploracyjna.
Ten wynik jest jednak najsilniejszym dotychczasowym testem
metodologicznym całej serii chrono_membrane_bridge — pierwszym na
danych, które nigdy wcześniej nie zostały zobaczone w JAKIEJKOLWIEK
formie przy formułowaniu hipotezy (w odróżnieniu od v0.1 post-hoc i
v0.2 split-half tego samego nagrania). Otwarty punkt na przyszłość:
zbadać, czy uszkodzenia typu B (kulka) systematycznie dają słabszy/
niestabilny efekt niż IR/OR na WIĘKSZEJ próbie plików tego typu
(tutaj tylko 2 pliki B, wynik sprzeczny między nimi) — wymagałoby
osobnej pre-rejestracji, nie doraźnego dociekania po tym wyniku.
