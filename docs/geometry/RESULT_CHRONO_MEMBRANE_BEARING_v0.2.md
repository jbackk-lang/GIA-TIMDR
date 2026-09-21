# Wynik: chrono_membrane_bridge v0.2 — odwrócony kierunek (normal > fault w `spectral_concentration`), test na czasowo odosobnionej drugiej połowie. SUPPORTED na 6/6 komórkach DRUGIEJ (rozstrzygającej) połowy, znak stabilny (2026-09-21)

> Kontynuacja `PREREG_CHRONO_MEMBRANE_BEARING_v0.2.md` (zamrożonej PRZED
> uruchomieniem). Kod: `core/real_chrono_membrane_bridge_v0_2.py`.
> Konstrukcja (`core/chrono_membrane_bridge.py`) BEZ ZMIAN względem
> v0.1. Nic w tym pliku nie zostało zmienione po zobaczeniu wyniku na
> drugiej (testowej) połowie.

## 0. Przypomnienie ograniczenia uczciwości (PREREG §1)

To NIE jest test na świeżych danych — te same trzy pliki NPZ co w
v0.1. Zastosowany częściowy środek zaradczy: podział czasowy każdego
nagrania na dwie nienachodzące się połowy. Pierwsza połowa =
kalibracja (nie-rozstrzygająca z definicji, bo kierunek już wiadomy z
v0.1, który użył całych plików). **Druga połowa = jedyny wynik, który
się tu liczy** — nigdy wcześniej nie była osobno wydzielona i
przetestowana jako samodzielny zbiór.

## 1. Pierwsza połowa (KALIBRACJA — nie-rozstrzygająca, raportowana dla przejrzystości)

| fault | okno | p | r | status |
|---|---|---|---|---|
| IR_21 | 128 | 6.53e-08 | +0.813 | SUPPORTED |
| IR_21 | 256 | 9.83e-08 | +0.802 | SUPPORTED |
| IR_21 | 512 | 5.49e-11 | +0.987 | SUPPORTED |
| OR6_21 | 128 | 1.70e-09 | +0.907 | SUPPORTED |
| OR6_21 | 256 | 4.50e-11 | +0.991 | SUPPORTED |
| OR6_21 | 512 | 3.02e-11 | +1.000 | SUPPORTED |

Znak `r` dodatni i stabilny na obu typach uszkodzenia, wszystkich trzech
oknach — zgodnie z oczekiwaniem (§0): to jest DOKŁADNIE wynik v0.1
odczytany na podzbiorze tych samych danych, nie nowa informacja.

## 2. Druga połowa (TEST — jedyna część rozstrzygająca, PREREG §4)

| fault | okno | p | r | efekt | status |
|---|---|---|---|---|---|
| IR_21 | 128 | 0.00205 | +0.464 | średni | **SUPPORTED** |
| IR_21 | 256 | 7.38e-10 | +0.927 | duży | **SUPPORTED** |
| IR_21 | 512 | 3.34e-11 | +0.998 | duży | **SUPPORTED** |
| OR6_21 | 128 | 3.57e-06 | +0.698 | duży | **SUPPORTED** |
| OR6_21 | 256 | 4.50e-11 | +0.991 | duży | **SUPPORTED** |
| OR6_21 | 512 | 3.02e-11 | +1.000 | duży | **SUPPORTED** |

n_valid_normal = n_valid_fault = 30 na każdej komórce (brak
INCONCLUSIVE). Dostępność segmentów na drugiej połowie (bez reużycia w
żadnej komórce): normal 952/476/238 (okno 128/256/512), IR 477/238/119,
OR6 478/239/119.

**Stabilność znaku (PREREG §3.4/§4, GŁÓWNE pytanie metodologiczne)**:
`IR_21: r=+0.464(128)→+0.927(256)→+0.998(512)`. `OR6_21:
r=+0.698(128)→+0.991(256)→+1.000(512)`. **ZNAK STABILNY (dodatni) na
WSZYSTKICH trzech rozmiarach okna, dla OBU typów defektu.**

**Klasyfikacja (PREREG §4)**: `p<0.05`, `|r|≥0.3`, `r>0` na WSZYSTKICH
6 komórkach drugiej połowy, znak stabilny → **SUPPORTED dla obu typów
uszkodzenia**, WEDŁUG kryterium tej sesji.

## 3. Interpretacja — co ten wynik faktycznie znaczy, a czego NIE znaczy

Kierunek `normal > fault` w `spectral_concentration` (odwrócony
względem v0.1) utrzymuje się na fragmencie danych, który nie był
wcześniej osobno raportowany jako samodzielny test — to jest
WYRAŹNIE silniejszy standard niż zwykłe przemalowanie kierunku na tym
samym zbiorze, i wynik przechodzi ten test w pełni (6/6, duży efekt
na 5/6 komórek, znak idealnie stabilny).

**Ale to formalnie NIE jest niezależne odkrycie** (PREREG §0/§2 wprost):
kierunek został ustalony post-hoc z v0.1, który widział CAŁE pliki
(w tym drugą połowę, tylko nie jako osobny test). Test na drugiej
połowie zmniejsza, ale nie eliminuje, ryzyko cyrkularności — obie
połowy pochodzą z TEGO SAMEGO nagrania fizycznego (to samo łożysko,
ten sam przebieg), więc każdy wspólny dryf/artefakt akwizycji obecny w
całym pliku (np. stan łożyska niezmieniający się istotnie w skali
nagrania, co jest fizycznie prawdopodobne dla krótkich, kilkusekundowych
przebiegów CWRU) byłby obecny w obu połowach jednocześnie i nie zostałby
złapany przez ten podział. Prawdziwa niezależna replikacja wymagałaby
NOWEGO nagrania (inne łożysko/dzień/RPM/obciążenie), niedostępnego
lokalnie — odnotowane wprost, zgodnie z PREREG §1.

## 4. Wniosek

Na DRUGIEJ, uprzednio nietkniętej połowie każdego z trzech plików CWRU:
odwrócony kierunek (`normal > fault` w `spectral_concentration`)
**SUPPORTED dla obu typów uszkodzenia (IR_21, OR6_21), 6/6 komórek,
znak stabilny na wszystkich trzech rozmiarach okna** — zgłoszone w
pełni, zgodnie z protokołem (wynik byłby zgłoszony identycznie
szczegółowo, gdyby wyszedł przeciwnie). Status metodologiczny: **silny
wynik na uczciwie odizolowanym podzbiorze danych, ale NIE pełnoprawna
niezależna replikacja** (§3) — właściwa interpretacja to "kierunek z
v0.1 przetrwał najsurowszy test możliwy przy obecnie dostępnych
danych", nie "nowe, niezależne potwierdzenie efektu fizycznego".
Prawdziwa niezależna replikacja (nowe nagranie) pozostaje otwartym
punktem, tak jak w v0.1 §7.

## 5. Status w ekosystemie

Podobnie jak v0.1: NIE dopisywane do `Axioms_G_TIMDR_Geometry.md` ani
`Axioms_S_TIMDR_Signal.md` — konstrukcja eksploracyjna z jawnie
ograniczonym standardem replikacji (§3), udokumentowana w pełni tutaj.
