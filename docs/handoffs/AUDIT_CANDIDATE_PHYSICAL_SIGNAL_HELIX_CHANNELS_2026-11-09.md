# AUDYT KANDYDATÓW NA KANAŁ SPRZĘŻENIA INFORMACJA/SYGNAŁ → HELISA

**Data:** 2026-11-09  
**Zakres:** istniejące repozytorium GIA-TIMDR; analiza dokumentacji i kodu.  
**Cel:** wskazać, co w ekosystemie już opisuje transfer/sprzężenie, a co jest tylko analogią, klasyfikatorem lub postulatem teoretycznym.

## 1. Wynik najważniejszy

W repozytorium znaleziono więcej istniejących elementów niż w pierwszym audycie ścieżki G:

1. `TIMDR-Math-Formalism/timdr_formalism/gs_matrix.py` — jawny, wykonywalny model sprzężenia między stanem geometrii G i sygnału S:
   `dV/dt = K V,; V=[G,S]^T`.
   Macierz jest rozkładana na część antysymetryczną (obrót/zachowawcze mieszanie stanów) i symetryczną (wzrost/zanik). To najbliższy istniejący, ogólny operator G↔S.
2. `TIMDR-Math-Formalism/timdr_formalism/signal_meta_bridge.py` — istniejący pipeline sygnał → SG-Coupling → Θ_bif → klasa I/II/III → MetaState → faza systemu. Łączy sygnał i dynamikę stanu META, ale nie geometrię helisy G jako mechaniczny obiekt.
3. `core/modal_band_energy_bridge.py` i wynik v0.2 — istniejący most M/S→K, który z obwiedni sygnału mierzy energię w pasmach modalnych; na danych CWRU wykazał różnicę fault/normal w trzech dopasowanych parach. Jest to diagnostyczna cecha energii sygnału, nie dowód przepływu energii do helisy.
4. `Model_T_Field_Theory.md` i `Model_U_Information_Theory.md` — wcześniejsze szkice pola informacyjnego, modalności, rezonansu i przepływu informacji. To kandydat na język formalny, ale nie zdefiniowane, skalibrowane prawo oddziaływania z helisą.
5. `HELIX_SIGNAL_RESPONSE_COUPLING_v0.1.md` — wcześniejsza specyfikacja pytania badawczego, która trafnie odróżnia reakcję, pamięć, adaptację, samonaprawę i odzyskanie informacji.

**Korekta do poprzedniego wniosku:** nie jest prawdą, że w całym GIA-TIMDR nie ma żadnego operatora G↔S. Jest istniejąca GS-Matrix. Brakuje natomiast wykazanego mapowania tej abstrakcyjnej macierzy na mierzalny kanał fizyczny, stopnie swobody konkretnej helisy i jednostki eksperymentalne. Pierwszy audyt nie uwzględnił tego pliku wystarczająco mocno.

## 2. Kandydaci — status i ograniczenia

### A. GS-Matrix — najsilniejszy kandydat obliczeniowy

Plik: `TIMDR-Math-Formalism/timdr_formalism/gs_matrix.py`.

Model:
[
\dot V=KV,\qquad V=(G,S)^T,
]
[
K=K_{anti}+K_{sym},\quad
K_{anti}=\frac{K-K^T}{2},\quad
K_{sym}=\frac{K+K^T}{2}.
]

Kod słusznie poprawia wcześniejszy błąd: dla rzeczywistego układu liniowego część antysymetryczna generuje obroty zachowujące normę, natomiast część symetryczna może wzmacniać lub tłumić stan. To użyteczny rozdział sprzężenia zachowawczego i strat/wzmocnienia.

Czego nadal brakuje:
- definicji składowych G i S jako konkretnych, wymiernych obserwabli helisy i sygnału;
- jednostek i kalibracji współczynników K;
- przestrzennego operatora rozmieszczenia sprzężenia wzdłuż węzłów/strands helisy;
- relacji GS-Matrix z macierzami M/K/Γ operatora mechanicznego G-Rezonans;
- walidacji na pomiarze helisy.

Wniosek: GS-Matrix jest pierwszym miejscem do ponownego wykorzystania. Nie należy jednak uznawać jej parametrów za stałe fizyczne ani wprost wstawiać do G-Rezonansu bez wyprowadzenia.

### B. SG-Coupling + Θ_bif + META — kanał stanu sygnału

Pliki:
- `TIMDR-Math-Formalism/timdr_formalism/signal_meta_bridge.py`
- `TIMDR-Math-Formalism/docs/SG_COUPLING_PHASE_DIAGRAM.md`

Pipeline już łączy cechy sygnału z ewolucją MetaState. Wielkości Λ, τ, ρ, J agregują dyspersję obwiedni, tempo zmiany β, frakcję klasy III i nakładanie kanałów N.

Ograniczenie: to stan/klasyfikacja pipeline'u sygnałowego. Nie ma w nim jawnego mechanicznego sprzężenia z położeniami, przemieszczeniami lub naprężeniami helisy. Progi faz są opisane jako heurystyczne/nieskalibrowane.

Wniosek: może dostarczyć reprezentacji wejścia/stanu sygnałowego do eksperymentu, ale nie jest fizycznym kanałem helisy.

### C. Modal Band Energy — obserwabla sygnałowa, nie transfer energii

Pliki:
- `core/modal_band_energy_bridge.py`
- `docs/geometry/RESULT_MODAL_BAND_ENERGY_BRIDGE_v0.2.md`
- `docs/geometry/PREREG_MODAL_BAND_ENERGY_BRIDGE_v0.2.md`

Pipeline: pasmo rezonansu → filtracja → obwiednia Hilberta → widmo obwiedni → pik przy częstotliwości charakterystycznej. Wynik CWRU jest formalnie wspierający dla trzech par dopasowanych; dokument uczciwie zaznacza, że pełna specyficzność nie była formalnie przetestowana i wynik kulki jest mniej selektywny.

Ograniczenie: wielkość nazywana energią jest w implementacji średnią amplitudą obwiedni w paśmie, a nie pomiarem energii mechanicznej przekazanej do helisy. Nie wolno utożsamiać korelacji cechy sygnału z przepływem energii.

Wniosek: dobry kanał pomiarowy/obserwabla wejścia, nie prawo sprzężenia.

### D. Model T — pole informacyjne i modalne

Plik: `docs/theory/Model_T_Field_Theory.md`.

Szkic wprowadza pola I, M, R, E oraz Lagrangian z potencjałem interferencyjnym i członem rezonansowym. Jednak zapisy są niekompletne jako model fizyczny: nie podano jednostek pól, wymiarów stałych, symetrii, warunków brzegowych ani jawnej zależności R od I i M pozwalającej policzyć wymagane pochodne. Równania Eulera–Lagrange’a są zapisane formalnie, ale nie stanowią jeszcze jednoznacznie zdefiniowanego, skalibrowanego prawa dla helisy.

Wniosek: zachować jako hipotezę/ramę wariacyjną. Nie wybierać z niej współczynnika sprzężenia bez uzupełnienia definicji i wymiarów.

### E. Model U — przepływ informacji

Plik: `docs/theory/Model_U_Information_Theory.md`.

Zawiera gradient, dyfuzję, równanie ciągłości i mapowanie informacji na modalności. Zapis entropii `-I ln I` wymaga jawnej normalizacji/dodatniości I; wielkości informacyjne i fizyczne nie mają tu jeszcze wspólnego układu jednostek. Model nie definiuje mechanicznej siły, momentu, naprężenia ani innego kanału działającego na helisę.

Wniosek: opisuje potencjalny przepływ/transformację informacji, nie fizyczne wymuszenie helisy.

## 3. Najbardziej prawdopodobna architektura dalszej integracji

Nie tworzyć nowej teorii od zera. Zachować rozdział ról:

[
\text{sygnał surowy}
\rightarrow \text{M/S + modal-band observables}
\rightarrow \text{stan sygnału (SG/META)}
\rightarrow \boxed{\text{GS-Matrix: kandydat G\leftrightarrow S}}
\rightarrow \text{mechaniczny G-Rezonans}
\rightarrow \text{obserwowalna odpowiedź}.
]

Ramka GS-Matrix jest na razie abstrakcyjnym interfejsem, a nie potwierdzonym fizycznym łącznikiem. Mechaniczny kanał musi zostać zidentyfikowany z danych lub konkretnej konstrukcji: np. wymuszenie przemieszczeniowe, siła, moment, naprężenie, ciśnienie albo pole elektromagnetyczne — zależnie od tego, czym rzeczywiście jest badana helisa i jaki sygnał do niej dociera. Nie wybieramy żadnego z tych kanałów bez podstaw w dokumentacji/eksperymencie.

## 4. Co jest teraz potrzebne z ekosystemu 70 repozytoriów

Wcześniej wskazano, że lokalne kody znajdują się w `C:\Users\jback\Downloads\a`, w tym repozytoria poza GIA-TIMDR. Tych plików nie można odczytać bezpośrednio z lokalnego dysku w tej sesji. Należy udostępnić archiwum/katalog z repozytoriami lub wypchnąć wskazane repozytoria na GitHub.

Priorytetowe wyszukiwanie w całym ekosystemie:
- TSI oraz repozytoria opisujące helisę jako fizyczny obiekt;
- implementacje GS/G-S coupling i sprzężeń między gałęziami;
- modele energii, siły, momentu, naprężeń, pól lub przepływu;
- wcześniejsze testy na rzeczywistych sygnałach/urządzeniach, w których jednocześnie rejestrowano wejście i odpowiedź struktury.

Szukane terminy: `TSI`, `GS coupling`, `G-S`, `helix response`, `signal transfer`, `energy transfer`, `force`, `torque`, `stress`, `field coupling`, `transduction`, `input-output`.

## 5. Decyzja robocza

1. Zachować minimalny test G-Rezonans jako demonstrację zależności odpowiedzi od stanu.
2. Nie uznawać go za fizyczne sprzężenie informacji.
3. Ponownie użyć GS-Matrix jako istniejącego kandydata interfejsu G↔S, ale dopiero po identyfikacji obserwabli i jednostek.
4. Użyć SG/META i modal-band energy do opisu wejścia, nie jako dowodu oddziaływania na helisę.
5. Przeszukać pozostałe repozytoria, zwłaszcza TSI, zanim powstanie nowy operator lub nowa hipoteza fizyczna.

**Konkluzja:** najbliższy istniejący kandydat na kanał formalnego sprzężenia to GS-Matrix; najbliższy kanał obserwacji sygnału to modal-band energy; Model T/U dostarczają hipotez pola i przepływu informacji. Żaden z nich samodzielnie nie ustala jeszcze fizycznego mechanizmu sygnał→helisa. Dalszy krok to audyt TSI i pozostałych repozytoriów, a nie dopisywanie nowej fizyki.
