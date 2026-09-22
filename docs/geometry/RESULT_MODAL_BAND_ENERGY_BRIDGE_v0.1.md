# Wynik: modal_band_energy_bridge v0.1 — ZAMKNIĘTY jako błędny wariant (metodologiczny, nie negatywny wynik)

> Kontrole syntetyczne (§4 PREREG) PRZESZŁY czysto na wszystkich trzech
> rozmiarach okna. Test na realnych danych CWRU dał statystycznie
> idealny, ale METODOLOGICZNIE BŁĘDNY wynik — zamykany tutaj jako
> pomyłka konstrukcyjna, nie jako "efekt w odwrotnym kierunku".
> Uruchomione: 2026-09-22.

## Kontrole syntetyczne — PASSED

Wszystkie trzy rozmiary okna (500,1000,2000): kontrola pozytywna
`p=3.02e-11, r=1.000`, kontrola specyficzności bez przecieku
(`p=0.45–0.67`). Mechanizm filtrowania FFT-domenowego + obwiedni
Hilberta działa poprawnie na syntetyce.

## Realne dane — wynik statystycznie idealny, ale bez specyficzności

Wszystkie 9 par (3 dopasowane + 6 niedopasowane) dały `r=-1.000`,
energia w KAŻDYM z trzech pasm (BPFO/BPFI/BSF) NIŻSZA przy uszkodzeniu
niż w Normal — identycznie dla pasma dopasowanego i niedopasowanego,
stabilnie między połówkami próby. Brak jakiejkolwiek specyficzności
pasmo↔typ uszkodzenia, wbrew przewidywaniu §3.2 PREREG.

## Diagnoza: błąd metodologiczny, nie odkrycie

Sprawdzone RMS szerokopasmowe surowego DE: `Normal=0.0738`,
`IR_21=0.525` (7×), `OR@6_21=0.583` (8×), `B_21=0.136` (1.8×) —
uszkodzenia mają WYŻSZĄ energię CAŁKOWITĄ niż Normal, zgodnie z
fizyką. Ale energia w WĄSKICH pasmach wokół niskich częstotliwości
charakterystycznych (107–162 Hz) wyszła NIŻSZA — sprzeczność
wyjaśniona: standardowa "envelope spectrum analysis" w diagnostyce
łożysk NIE filtruje bezpośrednio wokół niskiej częstotliwości
charakterystycznej. Filtruje wokół WYSOKOCZĘSTOTLIWOŚCIOWEGO rezonansu
konstrukcji (zwykle kHz, wzbudzanego przez uderzenia defektu), bierze
obwiednię TEGO pasma, i DOPIERO w WIDMIE tej obwiedni szuka piku przy
częstotliwości charakterystycznej. v0.1 pominął krok demodulacji —
filtrował bezpośrednio nisko i uśredniał wprost, więc mierzył coś
innego niż zamierzona diagnostyka: energię szerokopasmowego
uszkodzenia przypadkowo "rozcieńczoną" w wąskim, niskim paśmie, gdzie
fizycznie mało się koncentruje.

## Status

**v0.1 ZAMKNIĘTY jako błędny wariant konstrukcyjny** — nie jako
negatywny wynik teorii TIMDR, tylko jako pomyłka w implementacji
metody diagnostyki (brak kroku demodulacji rezonansu). Kod
(`core/modal_band_energy_bridge.py`, `core/real_modal_band_energy_bridge.py`)
zostaje w repozytorium jako udokumentowana historia, NIE kasowany.
Kontynuacja: `PREREG_MODAL_BAND_ENERGY_BRIDGE_v0.2.md` z pełną
demodulacją (wybór pasma rezonansu przez kurtozę, widmo obwiedni,
szukanie piku przy częstotliwości charakterystycznej).
