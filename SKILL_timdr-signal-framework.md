# TIMDR signal framework (GIA-TIMDR core) — sygnałowa gałąź TIMDR: definicje, protokół, formalizacja

> Kopia treści Claude-skilla `timdr-signal-framework`, **zawężona do teorii TIMDR-M (gałąź sygnałowa) i jej protokołu formalnego/statystycznego**. Pełna, cross-repo wersja skilla (audyty, case-studies z sejsmiki, radaru, bezpieczeństwa, kosmologii, EV/battery/industrial, transplanty symboliczno-neuronowe, trigger-dispatcher itd.) istnieje osobno na koncie Claude, ale NIE jest tu duplikowana — te historie błędów z innych repo nie są częścią teorii TIMDR, formalizmu ani sygnałów, więc zostały z tej kopii usunięte. Jeśli skill na koncie zostanie zaktualizowany, ten plik trzeba ręcznie zsynchronizować.

## 1. Cztery sygnały TIMDR (anomalia, defekt, rezonans M, skręt) — i dlaczego "rezonans"/"skręt" wymagają kwalifikatora

- **anomalia** — a single reading falls outside a statistically "normal" range
  for that parameter (e.g. `value > mean + 2*std` or outside `[p10, p90]`-derived
  bounds).
- **defekt** — a sudden jump between consecutive readings of the same parameter,
  bigger than a threshold derived from the recent spread of that parameter
  (e.g. `0.3 * (p90 - p10)`).
- **rezonans (M)** — several parameters flag `anomalia` at the same timestamp
  simultaneously (e.g. ≥3) — a stronger, more trustworthy signal than any single
  anomaly. **This is a coincidence counter, not a physical oscillator.**
- **skręt (sygnałowy)** — a trend reversal: the sign of the local slope flips
  between two consecutive windows, and the magnitude of the flip exceeds a
  threshold (e.g. `1.5 * std`).

These four generalize to any multi-parameter time series.

**Both "rezonans" and "skręt" are overloaded across the wider TIMDR ecosystem —
treat the bare word as ambiguous, always name which one.** Within GIA-TIMDR
alone, "rezonans" already has at least two distinct, formally separate
meanings: **rezonans sygnałowy (M)** (the coincidence counter above,
axiomatized in `Axioms_S_TIMDR_Signal.md`) and **rezonans modalny**
(frequency/phase alignment between wave-like modalities, an unrelated
mathematical object axiomatized in `Axioms_K_TIMDR.md`) — plus a third,
earlier, less-formalized **rezonans kierunkowy** sketch
(`R(t)=mean(sign(Sᵢ'(t)))`) in the main README. "Skręt" similarly has several
meanings: **skręt sygnałowy** (trend-reversal, this section), **skręt
topologiczny (τ)** (surface deformation torus→Möbius→tetroida,
`Operators_N_TIMDR.md`), and **skręt powierzchniowy**
(`‖n(p+Δp)−n(p)‖`, axiomatized in `Axioms_G_TIMDR_Geometry.md`). The full,
maintained canonical list for both words lives in
[`docs/GLOSSARY_EN_PL.md`](../GLOSSARY_EN_PL.md) — check it (or add to it)
before introducing yet another informal use of either word. The formal,
tested definition of the signal-branch operators above lives in
`TIMDR-Math-Formalism` (`docs/theory/Axioms_S_TIMDR_Signal.md`) — §3 below
covers what that adds (effect size, test power, a real empirical validation
of the rezonans-M independence baseline).

## 2. Protokół numerologii/formalizmu: jak testować, czy wzorzec sygnałowy jest realny

Cel: odróżnić realny wzorzec statystyczny (np. częstość koincydencji rezonansu
M, częstotliwość skrętu) od artefaktu niedotestowanego dopasowywania wzorców.
Ten protokół jest zaimplementowany jako gotowy, testowalny kod w
`TIMDR-Math-Formalism` (`timdr_formalism/pipeline.py`) — patrz §3.

1. **Zdefiniuj dokładny obiekt/wzorzec, metrykę i model null PRZED** dotknięciem
   realnych danych lub zobaczeniem wyniku. Zamroź parametry (progi, rozmiary
   okien) na syntetycznym sanity-checku najpierw — zmiana definicji po
   zobaczeniu realnego wyniku to pułapka data-snoopingu.
2. Porównuj docelowe okno z **realnie losowymi/tłowymi oknami**, nie z "czy
   sygnał odpala się, gdy wzorzec już jest obecny" — to detekcja, nie
   prawdziwy test koincydencji/niezależności.
3. Użyj prawdziwego testu istotności (**Mann-Whitney U** dla porównań
   dwupróbkowych), nie samego porównania percentylowego względem jednego
   rozkładu tła.
4. Każdemu testowi istotności towarzyszy **rozmiar efektu** (rank-biserial
   `r = 2U/(n_test·n_background) − 1`, `r∈[-1,1]`) — wymagany obok p, nie
   opcjonalny. Etykiety wielkości: `<0.1` pomijalny, `0.1–0.3` mały,
   `0.3–0.5` średni, `≥0.5` duży.
5. Uruchom syntetyczny self-test z **oboma** kontrolkami — pozytywną
   (wstrzyknij efekt, potwierdź że pipeline go wykrywa — p powinno być małe)
   i negatywną (niezależne próbki tła bez wstrzykniętego efektu — p powinno
   być duże) — i uzależnij uruchomienie na realnych danych od przejścia
   obu.
6. Zgłoś rzeczywisty wynik, łącznie z "brak efektu", bez narracyjnego
   łagodzenia — wynik negatywny jest kompletną, ważną odpowiedzią. Uruchom
   raz; jeśli przeszukiwanie wielu kandydatów/okien jest nieuniknione,
   skoryguj liczbę porównań (Bonferroni).
7. Zanim uznasz "brak struktury" na podstawie wyniku negatywnego, sprawdź,
   czy dziedzina ma już ugruntowany, dedykowany model statystyczny zamiast
   metryki zbudowanej naprędce — porażka domowej metryki jest dowodem
   przeciwko *tej metryce*, nie automatycznie przeciwko badanemu zjawisku.
8. **Sprawdź, czy test miał moc statystyczną do wykrycia efektu**, zanim
   odczytasz wysokie p jako potwierdzenie "braku efektu". Retrospektywnej/
   post-hoc "obserwowanej mocy" NIE wolno liczyć — to deterministyczna
   funkcja p, nie dająca nowej informacji. Moc trzeba sprawdzać prospektywnie
   (np. symulacją Monte Carlo ze znanym wstrzykniętym efektem, albo
   potwierdzeniem, że porównywane grupy faktycznie zawierają wystarczająco
   dużo kwalifikujących się/anomalnych zdarzeń — patrz realny wynik
   Krakow_Centrum w §3, gdzie p≈1 oznaczało zero kwalifikujących się
   zdarzeń, a nie potwierdzony brak rezonansu).
9. Pojedynczy pozornie pozytywny wynik nie jest dowodem — to wstępny trop
   wymagający replikacji na niezależnym zbiorze danych/oknie, zanim zostanie
   uznany za ustalony.

**Operator okna (formalizacja z Axioms_S/PROTOCOL.md)** — istotne dla
formalizmu sygnałowego: klasyczne okno przesuwne `W_k(x)(t)=(x(t-k),...,x(t+k))`
vs. faktyczna implementacja, partycja `P_k(x)` na rozłączne/nienachodzące na
siebie bloki — celowo nienachodzące, bo Mann-Whitney U wymaga niezależnych
obserwacji.

## 3. Formalizacja gałęzi sygnałowej: TIMDR-Math-Formalism, trzy gałęzie TIMDR, realna (uczciwie niejednoznaczna) walidacja rezonansu

Zadanie inne niż zwykłe audyty: nie znalezienie błędu w istniejącym kodzie,
tylko zbudowanie brakującej warstwy formalnej/testującej dla pytania
numerologia-vs-realna-matematyka (§2) — jako instalowalny kod, a potem
natychmiastowe uczciwe użycie go na realnym zbiorze danych, łącznie z
sytuacją, gdy wynik był szczerym "nie da się rozstrzygnąć", a nie czystym
tak/nie.

**Co powstało — `TIMDR-Math-Formalism`, realne repo, nie propozycja.**
Sześciokrokowy protokół (preregistracja z odciskiem SHA-256 łapiącym
post-hoc tuning, kontrolki pozytywna+negatywna bramkujące test główny,
Mann-Whitney U, uczciwe raportowanie wyniku negatywnego, korekta Bonferroniego
dla wielu porównań) — to protokół z §2, dostarczony jako `pip install`-owalny
kod (`timdr_formalism/pipeline.py`) plus dashboard Tkinter do uruchamiania go
bez pisania Pythona, zamiast procedury odtwarzanej ręcznie za każdym razem.
Dwa dodatki ponad wcześniejszą wersję protokołu: **rozmiar efektu**
(`rank_biserial_effect_size`, `r=2U/(n1·n2)-1`, wymagany obok każdego
p-value, nie opcjonalny — koduje "istotne ≠ duże" jako kod, nie tylko
prozę) oraz jawna **dyscyplina mocy testu** (§2 punkt 8): wysokie p-value
jest ważnym wynikiem negatywnym tylko wtedy, gdy test miał moc do wykrycia
efektu, a retrospektywnej/post-hoc "obserwowanej mocy" nie wolno liczyć —
moc trzeba sprawdzać prospektywnie, np. potwierdzając, że grupy kontrolne
faktycznie zawierają kwalifikujące się zdarzenia.

**Rozgraniczenie trzech gałęzi tego, co formalnie znaczy "TIMDR".**
Budowa aksjomatów gałęzi sygnałowej (`Axioms_S_TIMDR_Signal.md`) ujawniła,
że GIA-TIMDR miało już *inny*, wcześniej istniejący, w pełni rozwinięty
zestaw aksjomatów (`Axioms_K_TIMDR.md`, 10 aksjomatów) dla "rezonansu
modalnego" — wyrównania częstotliwości/fazy między modalnościami falowymi —
zupełnie inny obiekt matematyczny niż progowa koincydencja "rezonansu
sygnałowego" z tej sekcji, mimo wspólnej nazwy. Trzecia, geometryczna gałąź
(`Axioms_G_TIMDR_Geometry.md`, autorstwa użytkownika, 7 aksjomatów)
formalizuje model-trójkąta/normalną powierzchni "skręt powierzchniowy"
(`‖n(p+Δp)−n(p)‖`) jako kolejny odrębny obiekt, jawnie NIE sprowadzalny ani
do gałęzi sygnałowej, ani modalnej, i jawnie oznaczony jako
**koncepcyjny, jeszcze nie zwalidowany empirycznie** (własny aksjomat G7) —
związek z krzywizną geometryczną (operator Weingartena) jest nazwany jako
kierunek (aksjomat G4) bez implementacji, co samo w sobie jest uczciwym,
poprawnym sposobem zapisania otwartej luki formalizacyjnej wewnątrz zestawu
aksjomatów, zamiast milczącego przemilczenia. Wszystkie trzy gałęzie, plus
czwarty, jeszcze wcześniejszy nieformalny szkic wbudowany w główny README
GIA-TIMDR (kierunkowa koherencja `R(t)=mean(sign(Sᵢ'(t)))`, odrębna od
pozostałych trzech), są teraz nazwane i skrzyżowo odniesione w jednym
miejscu (`GIA-TIMDR/docs/GLOSSARY_EN_PL.md`).

**Realny test empiryczny — i dlaczego "p≈1" było błędnym wnioskiem.**
Zastosowano dostarczony pipeline do prawdziwego, prerejestrowanego testu
bazowej niezależności rezonansu sygnałowego (teoretyczne oszacowanie
`P(Binom(n,0.0455)≥K)`, ≈0.09% dla udokumentowanego systemu n=5/K=3)
względem 24 realnych dni danych pogodowych Krakow_Centrum
(temperatura/ciśnienie/wiatr — jedyne 3 z 5 udokumentowanych parametrów z
pełnym realnym pokryciem w dostępnym pliku). Uruchomiono zarówno test
oparty na permutacji częstości koincydencji, JAK I sanity-check kontrolki
pozytywnej. Wynik: ciśnienie przekroczyło swój własny próg 2σ ZERO razy w
24-dniowym oknie, więc częstość koincydencji wyniosła 0/24 zarówno dla K=2,
jak i K=3, dając p=1.0 dla realnych danych — ale kontrolka pozytywna
(sztucznie wymuszona koincydencja 3 dni w tej samej realnej serii) została
wykryta czysto przy p≈0.0002, co dowodzi, że mechanika testu działa.
**Poprawnym odczytem jest "to okno miało zero kwalifikujących się zdarzeń
do testowania koincydencji na nich", a nie "potwierdzony brak rezonansu
ponad przypadek"** — czysta, realna instancja dokładnie dyscypliny
sprawdzania mocy z §2 punkt 8. Pełne liczby i metoda:
`TIMDR-Math-Formalism/docs/REAL_DATA_VALIDATION.md`.

**Wnioski wielokrotnego użytku dla każdego przyszłego przejścia
formalizacyjnego w tym ekosystemie:**

1. Formalizując termin, który ekosystem już używa nieformalnie w wielu
   miejscach, audytuj istniejące formalne/nieformalne użycia TEGO SAMEGO
   słowa pod INNĄ definicją matematyczną przed napisaniem nowych aksjomatów
   — pierwsze zdanie nowego zestawu aksjomatów powinno jawnie mówić, czym
   *nie* jest, nie tylko czym jest.
2. Dostarcz protokół testowania numerologii jako instalowalny, przetestowany
   kod z udokumentowanym API, nie jako procedurę odtwarzaną ręcznie za
   każdym razem — dodatki rozmiaru efektu i mocy testu to dokładnie ten
   rodzaj luki, który ujawnia się dopiero, gdy protokół faktycznie jest
   wielokrotnie uruchamiany na realnych danych, nie z ponownego czytania
   prozy protokołu.
3. Realny przebieg na realnych danych jest więcej wart niż teoretyczne
   oszacowanie bazowe, ale tylko jeśli sprawdzona jest jego własna moc —
   uczciwie niejednoznaczny realny wynik (ta sekcja) jest cenniejszy do
   zapisania niż albo pewna-ale-niesprawdzona liczba teoretyczna, albo
   realny wynik, którego zastrzeżenie zerowej mocy nie zostało sprawdzone
   i zostaje zgłoszony jako czysty wynik negatywny.
4. Kiedy aksjomat jawnie nazywa relację, której jeszcze nie sformalizował
   (tu: związek skrętu powierzchniowego z operatorem Weingartena,
   aksjomat G4), to jest poprawny sposób zapisania rzeczywistej otwartej
   luki wewnątrz dokumentu formalnego — lepszy niż milczenie i lepszy niż
   fałszywe twierdzenie o kompletności.
