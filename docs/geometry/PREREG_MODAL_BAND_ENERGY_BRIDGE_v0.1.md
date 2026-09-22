# Pre-rejestracja: modal_band_energy_bridge — most M/S→K, energia obwiedni w pasmach BPFO/BPFI/BSF, test specyficzności pasmo↔uszkodzenie

> Status: PRE-REJESTRACJA, zamrożona PRZED dotknięciem jakichkolwiek
> danych (kod jeszcze nie napisany w chwili zapisania tego dokumentu).
> Data: 2026-09-22. Powrót do prostego mostu M/S→K (klasyczna analiza
> widma obwiedni — "envelope spectrum analysis", ugruntowana w
> literaturze diagnostyki łożysk), BEZ gałęzi G — świadoma rezygnacja
> z konstrukcji geometrycznych (chrono_cone/sphere/modal_geometry,
> wszystkie odrzucone lub niestabilne) na rzecz metody, która już ma
> częściowe potwierdzenie w tym repo (`chrono_membrane_bridge`,
> widmo korelacji/koncentracja spektralna — CONFIRMED).

## 0. Skąd to się bierze

Po trzech kolejnych konstrukcjach geometrycznych (cone, sphere,
modal_geometry — odpowiednio: odrzucony, odrzucony, niestabilny)
decyzja: wrócić do rzeczy, które już realnie reagują na defekt —
energia w pasmach charakterystycznych, korelacje/koncentracja widma,
proste mosty M/S→K bez G. Ta konstrukcja NIE zanurza niczego w
przestrzeni geometrycznej — energia w paśmie to skalar per okno per
pasmo, porównywany bezpośrednio testem statystycznym. Most M/S→K w
sensie katalogu ustalonego w tej sesji: `Φ(f)` (widmo DE) → filtr
pasmowy → `Φ_res(f)` → energia.

## 1. Audyt nazw PRZED użyciem

Grep na całym `GIA-TIMDR`: `band_energy`, `envelope_energy`,
`modal_band` — zero kolizji. Reużywa `bandpass_fft`/`hilbert_envelope`
z `core/chrono_modal_geometry_bridge.py` (ten sam kod, bez zmian) —
odnotowane wprost, nie zduplikowane.

## 2. Dane (te same, już zweryfikowane)

Kanał `DE`, cztery pliki 1797 RPM/0.021°: `Normal`, `IR_21` (bieżnia
wewnętrzna), `OR@6_21` (bieżnia zewnętrzna), `B_21` (kulka) — patrz
`PREREG_CHRONO_SPHERE_BRIDGE_v0.1.md` §2 dla hashy/szczegółów.
Częstotliwości charakterystyczne (zweryfikowane w
`PREREG_CHRONO_MODAL_GEOMETRY_BRIDGE_v0.1.md` §2): **BPFO=107.364 Hz,
BPFI=162.186 Hz, BSF=141.169 Hz** (1797 RPM), pasma ±15% (§3.1
tamtego dokumentu) — **bez zmian, te same granice**.

## 3. Konstrukcja (zamrożona)

### 3.1 Metryka: średnia obwiedni Hilberta w paśmie

Dla okna `T_win=1.0s` (12000 próbek), pasmo `s∈{BPFO,BPFI,BSF}`:

```
x_res,s(t) = bandpass_fft(x_DE, fs=12000, f_lo_s, f_hi_s)
A_s(t) = |hilbert(x_res,s(t))|
energy_s = mean(A_s(t))            # jedna liczba na okno na pasmo
```

Bez decymacji (niepotrzebna — nie liczymy tu żadnych pochodnych
czasowych, tylko średnią). Bez normalizacji względem energii całego
sygnału (surowa średnia obwiedni w jednostkach oryginalnego sygnału —
prostsza, mniej stopni swobody niż znormalizowany wariant; jeśli
DE między plikami ma różne globalne wzmocnienie czujnika, będzie to
widoczne w wynikach i odnotowane, nie ukryte normalizacją wybraną po
fakcie).

### 3.2 Przewidywanie specyficzności (zamrożone, zgodnie z literaturą diagnostyki łożysk)

```
IR_21   → energy_BPFI istotnie WYŻSZA niż Normal (dopasowane pasmo)
OR@6_21 → energy_BPFO istotnie WYŻSZA niż Normal (dopasowane pasmo)
B_21    → energy_BSF  istotnie WYŻSZA niż Normal (dopasowane pasmo)
```

Pasma NIEDOPASOWANE (np. `energy_BPFO` dla pliku `IR_21`) — BEZ
przewidywanego kierunku, raportowane opisowo (czy podnoszą się też,
częściowo — sidebandy/harmoniczne mogą wyciekać między pasmami, co
było już odnotowane jako ryzyko w PREREG modal_geometry §3.1), ale NIE
wchodzą do klasyfikacji SUPPORTED/NOT_SUPPORTED głównego testu
specyficzności.

## 4. Kontrole syntetyczne (zamrożone PRZED implementacją)

`fs_syn=1000 Hz` (skala syntetyczna niezależna od CWRU), pasmo testowe
`f_lo=90, f_hi=110 Hz` (analogiczna względna szerokość do realnego
przypadku), `WINDOW_SIZES=(500,1000,2000)` próbek, `N_WINDOWS=30`,
`SEED=0`, `ALPHA=0.05`.

- **(a) POZYTYWNA**: biały szum + oscylacja W PAŚMIE testowym
  (`sin(2π·100·t/fs)`, amplituda umiarkowana względem szumu tła).
  Przewidywanie: `energy` w tym paśmie istotnie WYŻSZA niż (b).
- **(b) NEGATYWNA**: czysty biały szum, bez żadnej strukturalnej
  oscylacji. Przewidywanie: `energy` niska, płaska, brak systematycznej
  różnicy między powtórzeniami.
- **(c) SPECYFICZNOŚĆ**: biały szum + oscylacja POZA pasmem testowym
  (np. `sin(2π·300·t/fs)`, daleko od `[90,110]`). Przewidywanie:
  `energy` w paśmie `[90,110]` NIE różni się istotnie od (b) — sygnał
  poza pasmem nie powinien podnosić energii w paśmie, w którym go nie
  ma (test na to, czy filtr FFT-domenowy faktycznie izoluje pasmo, nie
  przecieka).

**Test POZYTYWNY**: (a) vs (b), Mann-Whitney, oczekiwane `p<0.05`,
`|r|≥0.3`, `median(a)>median(b)`. **Test SPECYFICZNOŚCI**: (c) vs (b),
oczekiwany BRAK istotnej różnicy — jeśli (c) i (b) się różnią, to sam w
sobie ważny wynik (przeciek między pasmami), zgłoszony wprost, nie
ukryty.

## 5. Realne dane (URUCHAMIANE WYŁĄCZNIE, jeśli §4 przejdzie)

Segmentacja: nieprzecinające się okna 1.0s, `N_WINDOWS=30` losowych
segmentów na plik, `SEED=0`. Trzy pary (`Normal` vs `IR_21`, `Normal`
vs `OR@6_21`, `Normal` vs `B_21`) × trzy pasma (BPFO,BPFI,BSF) = 9
testów. Mann-Whitney jednostronny (`alternative="greater"`) DLA PAR
DOPASOWANYCH (§3.2 — mamy jawne przewidywanie kierunku, w odróżnieniu
od poprzednich konstrukcji tej sesji), dwustronny dla par
niedopasowanych (opisowe, nie klasyfikujące). Korekta Bonferroniego na
3 testy DOPASOWANE (nie 9 — niedopasowane są eksploracyjne, nie część
formalnej klasyfikacji): `α_corr=0.05/3≈0.0167`.

## 6. Klasyfikacja końcowa

**SUPPORTED (specyficzność potwierdzona)** = wszystkie trzy pary
dopasowane (IR→BPFI, OR→BPFO, B→BSF) istotne w przewidywanym kierunku
przy `α_corr`, ORAZ stabilne (ten sam kierunek) między
nieprzecinającymi się podpróbkami okien (podział pół-na-pół, sanity
check powtarzalności, nie formalny dodatkowy test). **CZĘŚCIOWO
SUPPORTED** = 1-2 z trzech par istotne w przewidywanym kierunku.
**NOT_SUPPORTED** = żadna para nie osiąga `α_corr` w przewidywanym
kierunku. Wynik zgłoszony z pełnymi liczbami dla wszystkich 9 testów
(3 dopasowane + 6 niedopasowanych, opisowo), niezależnie od tego, do
której kategorii trafia klasyfikacja główna.

## 7. Status

Zamrożone. Kolejność: (1) `core/modal_band_energy_bridge.py` —
konstrukcja + kontrole syntetyczne (§4); (2) jeśli PASSED:
`core/real_modal_band_energy_bridge.py` na czterech plikach CWRU (§5);
(3) `docs/geometry/RESULT_MODAL_BAND_ENERGY_BRIDGE_v0.1.md` z pełnym
wynikiem, łącznie z częściowym/negatywnym, bez retuningu po fakcie.
