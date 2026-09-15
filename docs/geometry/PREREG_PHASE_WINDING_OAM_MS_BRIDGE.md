# Pre-rejestracja: winding fazy (Hilbert, inspirowane OAM fotonu) jako most M/S↔K/topologia

> Status: PRE-REJESTRACJA, zamrożona PRZED uruchomieniem. Data:
> 2026-09-15. Piąty kandydat, JAKOŚCIOWO INNY od poprzednich czterech
> (`RESULT_TREFOIL_MS_BRIDGE.md` 0/10, `RESULT_WINDING_CROSSING_MS_
> BRIDGE.md` 0/20, `RESULT_PERSISTENT_HOMOLOGY_MS_BRIDGE.md` 1/10
> niestabilne — wszystkie odrzucone z tego samego powodu: mierzyły
> lokalną nieregularność/entropię trajektorii embeddingu, a szum ma jej
> więcej niż struktura).

## 0. Skąd to się bierze i dlaczego to inna kategoria

Propozycja użytkownika: orbitalny moment pędu (OAM) fotonu, mody
Laguerre'a-Gaussa `E(r,φ,z)=A(r,z)·e^{iℓφ}·e^{ikz}` — faza pola rośnie
o `2πℓ` na pełny obrót, `ℓ` to topologiczny ładunek, niezmiennik
`h=(1/2π)∮∇φ·dl`. To jest precyzyjna, twarda fizyka (nie metafora typu
„dwoisty czas" odrzucona poprzednim razem) — konkretne równanie, dające
się operacjonalizować.

**Kluczowa różnica jakościowa względem poprzednich czterech prób**:
torsja/winding-po-trajektorii/crossing/homologia mierzyły **lokalną
lub globalną nieregularność KSZTAŁTU trajektorii** w przestrzeni
embeddingu — a to jest z natury podatne na entropię szumu (diagnoza z
`RESULT_TOPOLOGICAL_BRIDGE_MS_SCOPE.md`). Winding fazy `e^{iℓφ}` mierzy
coś innego: **systematyczną, liniową akumulację fazy w czasie** —
prawdziwa oscylacja akumuluje fazę monotonicznie i przewidywalnie
(`Δφ≈ω·Δt` każdy krok, w tym samym kierunku), podczas gdy szum bez
struktury oscylacyjnej NIE ma takiej systematycznej tendencji — jego
błądzenie fazowe rośnie dyfuzyjnie (jak `√N`), nie liniowo (jak `N`).
To jest inna sygnatura statystyczna niż „lokalna szarpanina", więc
uzasadnione jest przetestowanie tego jako coś nowego, nie czwartej
powtórki tego samego mechanizmu.

**Uczciwe zastrzeżenie a priori**: cztery porażki z rzędu też nie są
podstawą do entuzjazmu — ale mechanizm jest realnie inny, więc
oczekiwanie jest neutralne, nie automatycznie pesymistyczne jak przy
poprzednich powtórkach tej samej rodziny metod.

## 1. Gdzie to pasuje w ekosystemie — K, nie G

W odróżnieniu od poprzednich czterech (rozszerzenia gałęzi G/geometrii),
ta konstrukcja naturalnie należy do gałęzi K (rezonans modalny,
`(f,φ,A)`) — sprawdzone bezpośrednio w kodzie: `TIMDR-Modal-Formalism/
timdr_modal/phase_sync.py::instantaneous_phase()` istnieje, ale działa
na już-zdefiniowanym obiekcie `Modality` (analityczny model f/φ/A), NIE
ekstrahuje fazy z surowego, zmierzonego sygnału liczbowego przez
transformatę Hilberta — sprawdzone grepem, `hilbert`/`analytic_signal`
nie występuje NIGDZIE w `TIMDR-Modal-Formalism`. To więc NIE jest
duplikat istniejącego kodu — jest nowym, brakującym mostem: „jak
wyciągnąć fazę z surowych danych", nie „co zrobić z fazą, gdy już ją
mamy".

## 2. Operacjonalizacja — jawnie nazwane uproszczenie względem OAM

OAM fotonu to faza pola rosnąca wokół osi propagacji w PRZESTRZENI
(kąt azymutalny wokół wiązki). Sygnał M/S to szereg 1D w CZASIE, nie
pole 2D w przestrzeni — więc to NIE jest dosłowne przeniesienie OAM,
tylko adaptacja tej samej idei matematycznej (`ℓ` = ile razy faza
owija się, podzielone przez `2π`) na oś czasu zamiast osi kąta
azymutalnego. To jest jawnie nazwane uproszczenie/reinterpretacja, nie
twierdzenie, że sygnał M/S JEST polem EM o orbitalnym momencie pędu.

Konkretnie (zamrożone):

1. Sygnał traktowany wprost jako rzeczywisty (nie normalizowany do
   amplitudy jednostkowej — faza jest niezmiennicza względem skali
   amplitudy, więc normalizacja nie jest tu potrzebna, w odróżnieniu od
   poprzednich metod opartych na embeddingu).
2. Sygnał analityczny: `a(t) = scipy.signal.hilbert(x(t))` — standardowa,
   pojedyncza, dobrze przetestowana transformata (NIE wielokrotne
   różnicowanie, NIE embedding opóźniający + rzut PCA — jeden krok).
3. Chwilowa faza: `φ(t) = angle(a(t))`, rozwinięta: `unwrap(φ(t))`.
4. Metryka (zamrożona): `winding = |unwrap(φ)[-1] - unwrap(φ)[0]| / (2π)`
   — analogicznie do `h=(1/2π)∮∇φ·dl` z propozycji, tylko całka po
   pętli przestrzennej zastąpiona sumą po osi czasu okna (telescoping,
   matematycznie to samo co suma `Δφᵢ`).

**Jawnie odnotowane znane ograniczenie transformaty Hilberta**: dla
sygnału WIELOSKŁADNIKOWEGO (nasz sygnał pozytywny to suma DWÓCH
częstotliwości) „chwilowa częstotliwość" z transformaty Hilberta nie ma
tak czystej interpretacji jak dla sygnału jednoskładnikowego — możliwe
są chwilowe wychylenia (nawet ujemna chwilowa częstotliwość) w
okresach, gdy składowe się „biją" (interferują). To jest znana,
udokumentowana własność metody (nie coś odkrytego po fakcie) — i będzie
widoczne w wyniku, jeśli wpłynie na metrykę, opisane wprost, nie
ukryte.

## 3. Reszta konstrukcji — bez zmian względem poprzednich mostów

Te same generatory (pozytywna = `sin(w1·t)+0,5·sin(w2·t+φ)+szum`,
`w1=1,0, w2=2,7`; negatywna A = czysty szum; negatywna B =
`sin(w1·t+φ)+szum`), te same rozmiary okna `{300, 64}`, ta sama siatka
szumu `{0,0; 0,1; 0,3; 0,5; 1,0}`, `n_windows=30`, `alpha=0,05`, te
same kryteria sukcesu z `pipeline.run_controls()` — dla pełnej
porównywalności z czterema poprzednimi wynikami.

**Oczekiwanie konkretne, zapisane PRZED wynikiem** (żeby uniknąć
pokusy interpretacji naciąganej po fakcie): dla negatywnej B (czysta
częstotliwość `w1`) winding powinien być bliski dokładnej wartości
`w1·N/(2π)` (deterministyczny, mała wariancja) niezależnie od szumu —
jeśli tak nie będzie, to samo w sobie jest wynik wart odnotowania. Dla
negatywnej A (czysty szum) oczekiwanie jest, że winding będzie MAŁY i
o WYSOKIEJ wariancji między oknami (błądzenie losowe, nie systematyczny
dryf) — w przeciwieństwie do poprzednich czterech metod, gdzie szum
dawał SYSTEMATYCZNIE WYŻSZE wartości metryki. Jeśli winding szumu
okaże się systematycznie wysoki (nie tylko zmienny), to obalałoby
właśnie to rozróżnienie, na którym opiera się cała hipoteza tej sekcji.

## 4. Status

Zamrożone. Następny krok: implementacja, uruchomienie na syntetyce,
uczciwy raport — łącznie z wynikiem negatywnym, bez retuningu po fakcie.
