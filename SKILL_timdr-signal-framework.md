# TIMDR signal framework (GIA-TIMDR core) — trzy gałęzie TIMDR (M/S, G, K), Chronoproces, protokół formalizmu

> Kopia treści Claude-skilla `timdr-signal-framework`, **zawężona do własnej teorii/formalizmu/sygnałów GIA-TIMDR (gałęzie M/S, G, K, Chronoproces Ξ, protokół formalny/statystyczny)**. Pełna, cross-repo wersja skilla (audyty, case-studies z sejsmiki, radaru, bezpieczeństwa, kosmologii, EV/battery/industrial, transplanty symboliczno-neuronowe, trigger-dispatcher itd.) istnieje osobno na koncie Claude, ale NIE jest tu duplikowana — te historie błędów z innych repo nie są częścią teorii TIMDR, formalizmu ani sygnałów, więc zostały z tej kopii usunięte. Jeśli skill na koncie zostanie zaktualizowany, ten plik trzeba ręcznie zsynchronizować.

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
(`‖n(p+Δp)−n(p)‖`, axiomatized as a formal operator with explicit
domain/codomain/continuity/stability in `Axioms_G_TIMDR_Geometry.md`,
Aksjomaty G3/G8, with its curvature link closed analytically in G9 and
implemented numerically in a sibling repo — §4 below). The full,
maintained canonical list for both words lives in
[`docs/GLOSSARY_EN_PL.md`](../GLOSSARY_EN_PL.md), consolidated further in
[`docs/theory/TIMDR_Twists.md`](../theory/TIMDR_Twists.md) — check it (or
add to it) before introducing yet another informal use of either word. The
formal, tested definition of the signal-branch operators above lives in
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
(`Axioms_G_TIMDR_Geometry.md`, autorstwa użytkownika, obecnie 10 aksjomatów
G1-G10 — patrz §4 poniżej dla G8-G9, i §6 dla G10, oba dodane po powstaniu
tej sekcji) formalizuje model-trójkąta/normalną powierzchni "skręt
powierzchniowy" (`‖n(p+Δp)−n(p)‖`) jako kolejny odrębny obiekt, jawnie NIE
sprowadzalny ani do gałęzi sygnałowej, ani modalnej, i jawnie oznaczony jako
**koncepcyjny, jeszcze nie zwalidowany empirycznie** (własny aksjomat G7,
status niezmieniony przez G8-G9 — patrz §4) — związek z krzywizną
geometryczną (operator Weingartena), pierwotnie nazwany jako kierunek
(aksjomat G4) bez implementacji, jest odtąd domknięty analitycznie (G9) i
zaimplementowany numerycznie (§4), co samo w sobie jest uczciwym,
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
   fałszywe twierdzenie o kompletności. (Aktualizacja: ta konkretna luka
   została odtąd domknięta — analitycznie w Aksjomatach G8-G9, numerycznie
   w `TIMDR-Geometry-Formalism` — patrz §4 poniżej, które demonstruje
   dokładnie ten wzorzec zamiast tylko go opisywać.)

## 4. Domknięcie gałęzi geometrycznej: formalny operator T_S (G8), dyskretny Weingarten (G9), konsolidacja skrętów/gałęzi, i pierwsza numeryczna implementacja

§3 zostawiło jedną lukę jawnie otwartą: Aksjomat G4 nazwał związek skrętu
powierzchniowego z krzywizną przez operator Weingartena, bez implementacji.
Ta sekcja domyka ją w dwóch, osobno oznaczonych krokach — najpierw
analitycznie, potem numerycznie — wzorzec wart powtórzenia za każdym razem,
gdy dokument formalny nazywa relację, której jeszcze nie domknął (czwarty
wniosek §3, tu zademonstrowany, nie tylko opisany).

**Domknięcie analityczne — Aksjomaty G8-G9.** G8 formalizuje T_S jako
właściwy operator: dziedzina `S×ℝ³⇀[0,2]`, ciągłość przy `Δp→0`, ograniczenie
Lipschitza przez `κ_max(p)=max(|κ1(p)|,|κ2(p)|)`. G9 podaje jawne `F`:
klasyczny różniczkowy operator kształtu `S_p(v)=-D_v n(p)` (konwencja znaku
do Carmo), jego dyskretną aproksymację różnicową na siatce, oraz relację
pierwszego rzędu `T_S(p)=‖Δp‖·‖S_p(Δ̂p)‖+O(‖Δp‖²)` — to jest realna
tożsamość różniczkowo-geometryczna (rozwinięcie Taylora pola normalnych), nie
nowa konstrukcja TIMDR, jawnie tak oznaczona. Kluczowe: to domyka G4b tylko
analitycznie — status G7 "koncepcyjna" i pozostałe wymogi (formalna
przestrzeń powierzchni, testy empiryczne, niezależna walidacja) zostają
otwarte; tylko wymóg (1) jest teraz częściowo spełniony.

**Konsolidacja w dwóch dokumentach-indeksach.** W miarę narastania zestawów
aksjomatów (Axioms_S 13 aksjomatów, Axioms_G 10 aksjomatów, Axioms_K 10
aksjomatów, każdy z własnymi obiektami/operatorami), kanoniczne fakty
rozproszyły się po plikach z jedynie tabelą porównawczą w głównym README.
Dwa nowe dokumenty konsolidują to bez redefiniowania czegokolwiek:
`TIMDR_Branch_Specification.md` (jedna strona na gałąź: obiekty, operatory,
aksjomaty, pliki źródłowe, jawne "czym NIE jest" per gałąź, jedna tabela
porównawcza) i `TIMDR_Twists.md` (wszystkie cztery znaczenia skrętu —
sygnałowy/topologiczny τ/powierzchniowy/blokowy — z dziedziną/
przeciwdziedziną/definicją, jedno pod drugim). Żaden dokument nie definiuje
nowej matematyki; oba są indeksami, których jedynym zadaniem jest uczynić
dyscyplinę "to samo słowo, inny obiekt" (ustanawianą wielokrotnie w tym
ekosystemie — patrz §7/§8 pełnego skilla) sprawdzalną w jednym miejscu
zamiast wymagać krzyżowego odniesienia N plików aksjomatów.

**Pierwsza numeryczna implementacja gałęzi G — `TIMDR-Geometry-Formalism`.**
Odzwierciedlając to, jak protokół §3 stał się realnym kodem jako
`TIMDR-Math-Formalism` dla gałęzi sygnałowej, dyskretny operator Weingartena
(G9) jest teraz realnym, uruchamialnym kodem w repozytorium siostrzanym:
`timdr_geometry/weingarten.py` — normalne wierzchołkowe (ważone polem),
sąsiedztwo 1-ringu, rzut na płaszczyznę styczną, dopasowanie metodą
najmniejszych kwadratów dyskretnego operatora kształtu (symetryzowane),
dekompozycja własna dla krzywizn głównych, plus oba sposoby liczenia T_S
(bezpośredni wg G3, przewidywany wg G9c) do porównania. Cztery testy
stabilności na powierzchniach ze znaną analitycznie odpowiedzią: płaszczyzna
(krzywizna ≈0 wszędzie), sfera (obie krzywizny główne ≈1/R), walec (jedna
krzywizna ≈0 wzdłuż osi, druga ≈1/r obwodowo) i rafinacja siatki (błąd maleje
przy zagęszczaniu). **Jawne, istotne zastrzeżenie**: ten kod został napisany
i matematyka prześledzona ręcznie krok po kroku, ale sandbox bash był
niedostępny przez całą sesję, w której powstał (RPC pipe closed) — testy
nigdy faktycznie nie zostały uruchomione. Udokumentowane to we własnym
README repozytorium i na górze pliku testowego, dokładnie tym samym wzorcem
uczciwości, którego użył skrypt realnej walidacji `TIMDR-Math-Formalism`,
gdy on też nie mógł zostać uruchomiony we własnej sesji (§3 powyżej) — zawsze
sprawdzaj i zachowuj to zastrzeżenie, dopóki ktoś faktycznie nie uruchomi
`pytest tests/ -v` i nie zgłosi wyniku; nie porzucaj go po cichu w
przyszłym podsumowaniu.

**Wnioski wielokrotnego użytku, rozszerzające listę z §3:**

5. Kiedy dokument formalny jawnie nazywa niedomkniętą relację (wniosek 4
   powyżej), domykaj ją w dwóch wyraźnie oddzielonych, jawnie oznaczonych
   krokach, jeśli pełne domknięcie nie jest możliwe naraz: najpierw
   wyprowadzenie analityczne/matematyczne (tanie, bez kodu, natychmiast
   sprawdzalne ręcznie), potem implementacja numeryczna (realny kod, realne
   testy) — i podaj dokładnie, które części oryginalnej listy "wciąż
   otwarte" zamyka każdy krok, zamiast ogłaszać całą lukę rozwiązaną po
   którymkolwiek z nich.
6. Gdy aksjomaty narastają w wielu równoległych plikach (jeden na gałąź),
   buduj osobny jednostronicowy indeks dla każdego powtarzającego się
   zagadnienia przekrojowego (tu: jeden dokument porównania gałęzi, jeden
   dokument rozróżnienia słów) zamiast pozostawiać porównanie wyłącznie jako
   tabelę w README, którą trzeba ręcznie synchronizować — jedynym źródłem
   prawdy dla dokumentów-indeksów są pliki aksjomatów, i powinny to jawnie
   mówić (jak oba tutaj), by przyszła edycja aksjomatu nie rozsynchronizowała
   po cichu indeksu.
7. Gdy kod nie może zostać uruchomiony w sesji, w której powstaje (brak
   sandboxa, brak powłoki), nie pomijaj pisania testów — pisz je z celowo
   szerokimi/konserwatywnymi tolerancjami, prześledź ręcznie matematykę,
   którą sprawdzają, i jawnie oznacz zastrzeżenie "nie uruchomione"
   (README, góra pliku testowego) zamiast albo pomijać testy, albo po cichu
   przedstawiać nieuruchomione liczby jako zweryfikowane.

## 5. Chronoproces Ξ=(T,x,Γ,φ): most między trzema gałęziami, i most Fouriera M/S↔K

Odpowiedź na postulat z głównego README §7.3 (`t_lokalne=f(τ_globalne)`)
i na pierwszą, błędną próbę uogólnienia "czasu" na wszystkie trzy gałęzie
naraz (błąd kategorii w G: krzywa 1D nie ma operatora kształtu; `f` w K
postulowane bez definicji). Pełny opis:
`docs/theory/TIMDR_Chronoprocess.md`.

**Konstrukcja — jedno źródło, trzy NIEZALEŻNE rzuty, zero identyfikacji
(warunek zgodności z §4 wyżej / `TIMDR_Branch_Specification.md`):**
nośnik `T` (uporządkowany zbiór chwil), `Ξ=(T,x,Γ,φ)`, gdzie
`x:T→ℝᵈ` czyta M/S, `Γ:T×I→ℝ³` czyta G, `φ:T→(f,φ,A)` czyta K.

- **M/S**: `tempo(t)=Δt`, `drift(t)=Δt-nominalne` — czysta reinstancja
  `x:T→ℝᵈ`, zero nowych aksjomatów. `TIMDR-Math-Formalism/chronosignal.py`
  — **62/63 pytest potwierdzone przez użytkownika** (1 błąd niezwiązany:
  lokalny `PermissionError` katalogu tymczasowego Windows).
- **G**: naprawa błędu obiektu — rodzina trajektorii `{γ_s}`,
  `Γ(t,s)=γ_s(t)`, `S=Γ(T×I)⊂ℝ³` jest prawdziwą powierzchnią, na której
  G3/G8/G9 działają dosłownie. Analogia (nie równoważność) do kongruencji
  geodezyjnych w OTW (Raychaudhuri) — rozkład ekspansja/ścinanie/skręt
  NIE zaimplementowany. `TIMDR-Geometry-Formalism/chronocongruence.py`
  — nieuruchomione.
- **K**: mapa synchronizacji faz `f`, formalizująca dosłownie
  `t_lokalne=f(τ_globalne)` przez dopasowanie fazy chwilowej dwóch
  modalności. AFINICZNA (nie Kuramoto-sprzężona) — bo Aksjomaty K3/K4
  modelują modalność jako oscylator o stałych parametrach; pełniejsza
  wersja wymagałaby rozszerzenia aksjomatów, jawnie NIE zrobione.
  `TIMDR-Modal-Formalism/phase_sync.py` — pierwszy kod dla K w ogóle,
  nieuruchomione.
- **Most Fouriera M/S↔K** (jedyny jawny wyjątek od "zero identyfikacji"):
  dualizm falowo-cząsteczkowy fotonu ma tę samą matematyczną strukturę co
  klasyczna zasada nieoznaczoności Gabora dla sygnałów — FFT jest
  KONKRETNĄ, znaną transformatą między `x(t)` i `(f,φ,A)`, nie
  utożsamieniem. Wyprowadzone ręcznie w tej sesji: dla impulsu
  gaussowskiego `Δt·Δf=1/(4π)` dokładnie, niezależnie od szerokości —
  granica Gabora/Heisenberga OSIĄGANA. `TIMDR-Time-Formalism/fourier_bridge.py`
  — część jednotonowa dokładna algebrą, część gaussowska z szerokimi
  (±30%) tolerancjami, nieuruchomione.

**Wnioski wielokrotnego użytku, rozszerzające listę z §3-§4:**

8. Kiedy dwie gałęzie formalizmu współdzielą tylko wspólny NOŚNIK
   (indeks/parametr), a nie wspólny obiekt, zbuduj kontener orkiestrujący
   oddzielne rzuty NA nośnik zamiast próbować zdefiniować jeden obiekt
   spinający obie gałęzie naraz — to jest formalny sposób realizacji
   "wielu niezależnych opisów tej samej sytuacji", bez łamania
   nieredukowalności.
9. Jeśli między dwiema formalnie nieredukowalnymi gałęziami istnieje
   PRAWDZIWA, ustalona matematyczna transformata (nie nowa hipoteza) —
   jak FFT między sygnałem czasowym a jego widmem — jej dodanie jako
   jawnie oznaczonego, pojedynczego wyjątku jest uczciwe i wartościowe;
   nieoznaczenie go jako wyjątku (czyli cichne rozmnożenie takich mostów)
   byłoby dokładnie tym, przed czym chroni zasada nieredukowalności.
10. Gdy analogia fizyczna (tu: dualizm fotonu) ma zostać użyta do
    uzasadnienia konstrukcji matematycznej, sprawdź, czy analogia ma
    WSPÓLNE ŹRÓDŁO matematyczne (tu: sprzężone zmienne Fouriera), a nie
    tylko powierzchowne podobieństwo słowne — jeśli tak, wyprowadź
    konkretną, sprawdzalną konsekwencję (tu: `Δt·Δf=1/(4π)` dla impulsu
    gaussowskiego) zamiast zostawić analogię jako czystą metaforę.

## 6. Aksjomat G10 (parametr obwiedni P/Q), samo-znaleziony błąd w G10e, i dokument spekulacyjny TIMDR_Gravity_Speculative.md

**Aksjomat G10.** Formalizuje inny obiekt niż G3-G9 (krzywizna
**powierzchni**): krzywiznę **krzywej**, obwiedni zaokrąglonej
`∂_R(Δ)` zbudowanej na trójkącie z G2 — rozkład na część prostą `L0(R)`
(krzywizna 0) i łukową `Lk(R)` (krzywizna `1/R`), `P=L0/L`, `Q=Lk/L=1-P`.
Z twierdzenia o sumie kątów zewnętrznych, `Lk(R)=2πR` dokładnie; `L0`
afiniczne w `R`. Udowodniono ręcznie (nierówność Jensena, reguła
ilorazu): `P(R)` jest ściśle monotoniczna na `[0,R_max(Δ))`, więc
odwracalna — daje to oba kierunki wprost postulowane przez użytkownika
("redukcja" krzywa↦(P,Q), "i odwrotnie" — zadane P↦R↦obwiednia),
udowodnione dla TEJ jednoparametrowej rodziny, nie dla dowolnej krzywej.
Pełny tekst: `Axioms_G_TIMDR_Geometry.md`, Aksjomat G10.

**Domknięcie numeryczne — `TIMDR-Geometry-Formalism/timdr_geometry/envelope.py`.**
Tym samym wzorcem co G8-G9 (wniosek 5/7): `TriangleGeometry` (boki, kąty,
`s`, pole, `r_in`, `c(Δ)`), `L0_of_R/Lk_of_R/L_of_R/P_of_R/Q_of_R`
(postać zamknięta G10c), `R_of_P` (odwrotność w postaci zamkniętej —
funkcja Möbiusa, bez solvera), `rounded_triangle_boundary` (sama
obwiednia jako polilinia odcinki+łuki, skonstruowana geometrycznie
NIEZALEŻNIE od wzorów zamkniętych) i `verify_envelope_length`
(porównanie obu). **✅ Zweryfikowane przez użytkownika: 65/65 testów
przeszło** (`tests/test_envelope.py`) — w tym poprawiona tożsamość
`R_max(Δ)=r_in(Δ)` na 5 trójkątach (dwiema niezależnymi ścieżkami,
żeby test nie był kołowy), `L0(R_max)=0`/`Q(R_max)=1` dla każdego z
nich, nierówność Jensena, ścisła monotoniczność i odwracalność `P(R)`,
oraz niezależna zgodność skonstruowanej geometrii z wzorem zamkniętym
(ten sam duch co `T_S_empirical` vs `T_S_predicted` w `weingarten.py`).

**Samo-znaleziony błąd matematyczny w G10e — i dlaczego jest to nowy,
ogólny wniosek dla protokołu z §2.** Pierwsza wersja G10e twierdziła, że
złamanie symetrii trójkąta ściśle ogranicza zasięg `Q` (`R_max(Δ)<r_in(Δ)`,
`Q_max<1` dla każdego trójkąta poza równobocznym) — "sprawdzone krok po
kroku" w chwili napisania. Błąd wyszedł na jaw dopiero przy liczeniu
KONKRETNEGO przykładu liczbowego (trójkąt 3-4-5) do
`TIMDR_Gravity_Speculative.md` (§ niżej): dla tego jawnie asymetrycznego
trójkąta wyszło `R_max=r_in=1.0` dokładnie, sprzeczne z tekstem aksjomatu.
Ręczne wyprowadzenie ogólne pokazało dlaczego: ze standardowej tożsamości
stycznej-do-okręgu-wpisanego `cot(θᵢ/2)=(s-aᵢ)/r_in` wynika
`R_max(Δ)=r_in(Δ)` **dokładnie, dla KAŻDEGO trójkąta** — `Q=1` jest więc
osiągalne zawsze, nie tylko dla trójkąta równobocznego. Poprawione w
`Axioms_G_TIMDR_Geometry.md` z jawnym dopiskiem o naprawie (nie cichym
nadpisaniem) — co POZOSTAJE prawdą: przy ustalonym obwodzie trójkąt
równoboczny ma NAJWIĘKSZY `r_in`, więc symetria wpływa na bezwzględny
promień `R`, przy którym `Q→1` następuje, nie na to, czy w ogóle następuje.

11. **Nowy wniosek wielokrotnego użytku (rozszerza §2/§3):** nawet ręczne
    wyprowadzenie "sprawdzone krok po kroku" może zawierać fałszywe
    twierdzenie OGÓLNE, jeśli nigdy nie zostało podstawione pod jeden
    konkretny przykład liczbowy. Ten błąd nie został znaleziony przy
    przeglądzie samego aksjomatu — wyszedł dopiero przy budowaniu
    NIEZWIĄZANEGO, downstream przykładu liczbowego dla innego dokumentu.
    Wniosek: policz choć jeden konkretny przypadek dla KAŻDEGO ogólnego
    twierdzenia geometrycznego/matematycznego przed opublikowaniem go w
    pliku aksjomatów — dokładnie ten sam duch co kontrolki
    pozytywna/negatywna z §2, tylko zastosowany do czystej matematyki, nie
    do statystyki.

**`TIMDR_Gravity_Speculative.md` — jak potraktowano propozycję łamiącą
zasadę nieredukowalności.** Użytkownik zaproponował rozszerzenie:
tensor czasoprzestrzeni `Ω=(P,Q)⊗(k_MS,k_G,k_K)` (jeden "parametr czasu"
per gałąź — nowe, nieistniejące wcześniej obiekty) plus masa `M` i
analogia grawitacyjna `g~M·Ω` (echo Newtonowskiego
`Φ(x)=-G∫ρ(x')/‖x-x'‖d³x'`). To wprost łączy WSZYSTKIE TRZY gałęzie
naraz przez iloczyn tensorowy — dokładnie ten typ konstrukcji, przed
którym chroni "zasada nadrzędna" `TIMDR_Branch_Specification.md`, i bez
odpowiednika mostu Fouriera (§5 wniosek 9: most Fouriera ma za sobą
KONKRETNĄ znaną tożsamość matematyczną; `Ω` nie ma żadnej). Rozwiązanie
(zapytane wprost, wybrane przez użytkownika): ANI cichy refuz, ANI ciche
wpisanie do aksjomatów — osobny, jawnie oznaczony dokument spekulacyjny
(`GIA-TIMDR/docs/theory/TIMDR_Gravity_Speculative.md`), z bannerem
statusu na górze, który NIE jest cytowany przez żaden plik `Axioms_*` ani
`TIMDR_Branch_Specification.md`.

Dokument zawiera: (a) propozycje `k_MS,k_G,k_K` zbudowane z obiektów już
istniejących w Chronoprocesie (druga różnica driftu dla M/S, `∂H/∂t`
wzdłuż kongruencji dla G, `d²f/dτ²` dla K) — z uczciwym wnioskiem, że
`k_K≡0` jest KONSEKWENCJĄ aksjomatów K3/K4 (modalność afiniczna), nie
luką; (b) jawną postać `Ω` jako macierzy `2×3`, z zaznaczeniem, że
`g~M·Ω` nie zgadza się rzędem tensora z prawdziwym polem grawitacyjnym
bez dodatkowej, nierozstrzygniętej mapy kontrakcji; (c) konkretny
przykład liczbowy (trójkąt 3-4-5, syntetyczne `k_MS=0.10,k_G=0.03`) —
patrz niżej za wnioskiem stąd; (d) listę czterech braków do przejścia od
analogii do teorii (jednostki, zasada wariacyjna/równanie pola,
odróżniająca predykcja, kontrola pozytywna/negatywna wg protokołu z §2);
(e) cztery jednozdaniowe "zamknięcia" dodane na wyraźną prośbę
użytkownika o "kuloodporność": dlaczego `Ω` nie może być drugim mostem
(brak znanej tożsamości za sobą, w przeciwieństwie do Fouriera), dlaczego
`k_K≡0` nie jest luką, dlaczego brak zależności od odległości
(`1/‖x-x'‖`) jest fundamentalny (nie kosmetyczny) dla każdej konstrukcji
grawitacji-podobnej, i mini-sekcja "dlaczego to jest tylko analogia"
(brak równania pola/jednostek/dynamiki).

12. **Nowy wniosek wielokrotnego użytku:** gdy propozycja użytkownika
    wprost łamie zasadę, którą framework sam sobie narzucił (tu: zero
    mostów poza jednym, udowodnionym wyjątkiem), właściwa reakcja to ani
    milczące podporządkowanie się, ani milczący refuz — nazwij konflikt
    wprost, zapytaj, jak go potraktować (tu: `AskUserQuestion` z trzema
    opcjami), i jeśli wybrany zostanie "osobny dokument", zbuduj go tak,
    żeby żaden plik aksjomatów go nie cytował jako uzasadnienie — samo
    istnienie dokumentu nie może po cichu osłabić zasady, przed którą
    reszta frameworku ma chronić.
13. **Nowy wniosek wielokrotnego użytku (znaleziony przy liczeniu
    przykładu z `TIMDR_Gravity_Speculative.md`):** gdy tensorujesz/łączysz
    wielkość UNORMOWANĄ (składowe sumujące się do stałej, tu `P+Q≡1`) z
    niepowiązanym wektorem, najprostsza "naiwna" kontrakcja (suma
    wszystkich wpisów) jest zwykle ZDEGENEROWANA — sprowadza się do
    funkcji WYŁĄCZNIE drugiego wektora, kasując całą informację niesioną
    przez wielkość unormowaną (tu: suma wszystkich 6 wpisów `Ω` wyszła
    `(P+Q)(k_MS+k_G+k_K)=k_MS+k_G+k_K`, niezależnie od `P,Q`). Zawsze
    sprawdź proponowaną kontrakcję na konkretnych liczbach, zanim uznasz
    ją za sensowną — to ten sam duch co wniosek 11 (podstaw liczby, nie
    ufaj samej algebrze), zastosowany tu do wyboru operacji, nie do
    twierdzenia.
