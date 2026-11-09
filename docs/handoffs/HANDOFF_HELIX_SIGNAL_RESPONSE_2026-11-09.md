# HANDOFF — HELIX/TIMDR: sygnał → helisa → odpowiedź

**Data:** 2026-11-09  
**Repozytorium nadrzędne:** GIA-TIMDR  
**Status:** punkt wznowienia pracy po resecie. Ten dokument ma zachować kierunek i zapobiec ponownemu rozproszeniu badań.

## 1. Cel nadrzędny — nie zmieniać

Badamy **wpływ informacji/sygnału na helisę TIMDR i odpowiedź helisy**.

Pytanie główne:
**Co sygnał robi z helisą, jak helisa na niego odpowiada i czy odpowiedź zależy od wcześniejszej historii sygnałów?**

Schemat:
`sygnał wejściowy → mechanizm oddziaływania w helisie → odpowiedź → wpływ odpowiedzi na kolejny sygnał`.

Nie wracać do katalogowania samych właściwości helisy jako głównego celu. Użytkownik wskazuje, że pamięć, samonaprawa i inne właściwości helisy były już przedmiotem wcześniejszych badań. Traktować je jako istniejący kontekst badawczy, ale przy używaniu ich jako przesłanek w konkretnym modelu odszukać odpowiednie źródła i nie dopisywać niezweryfikowanych szczegółów.

## 2. Najważniejsza korekta metodologiczna

Analiza mechanizmu miała pomóc zrozumieć sprzężenie sygnału z helisą. Nie wolno mnożyć niewiadomych ani rozwijać pobocznych eksperymentów bez wskazania, jak rozwiązują główne pytanie.

**Następny krok to nie nowa teoria i nie kolejny sweep parametrów. Najpierw prześledzić istniejący kod GIA-TIMDR i odtworzyć drogę sygnału od wejścia do odpowiedzi helisy.**

Dla każdego istniejącego elementu ustalić:
1. co jest wejściem i w jakiej reprezentacji;
2. gdzie i jak sygnał oddziałuje ze strukturą;
3. jaki stan helisy może się zmienić;
4. jakie wyjście/odpowiedź jest obliczane lub mierzone;
5. czy wynik zależy od historii;
6. co jest zaimplementowane, co jest hipotezą, a czego w kodzie brak.

Najpierw audyt istniejących modułów i przepływu danych. Dopiero potem wskazać **jedną** najważniejszą lukę i zaprojektować minimalny test.

## 3. Istniejące punkty zaczepienia — nie utożsamiać ich

- **G / G-Rezonans:** `core/geometric_resonance_operator.py`, model mechanicznej odpowiedzi układu w rodzaju `M x'' + Γ x' + Kx = F(t)`. To pobudzenie i odpowiedź mechaniczna; nie jest samo w sobie pełnym modelem informacji. W dotychczasowym audycie odnotowano użycie `|τ|`, które może usuwać znak chiralności ze sprzężenia.
- **K:** modalności `(f, φ, A)` i synchronizacja. Nie zakładać, że samo K zmienia geometrię helisy.
- **M/S:** analiza/klasyfikacja sygnału czasowego. Jej „rezonans” nie jest automatycznie tym samym co rezonans mechaniczny G ani fazowy K.
- **T:** szkic pola informacyjnego/modalnego/rezonansowego; nie uznawać za zwalidowane prawo sprzężenia bez jawnego równania i testu.
- **Helix-Lock:** eksperyment chiralności wskazywał, że znak orientacji/torsji może być tracony przez użycie wartości bezwzględnej. Zachować znak i fazę w analizie.

Nie scalać G/K/M/T w jeden operator bez matematycznego mostu.

## 4. Minimalny model pojęciowy

`u(t)` — wejściowy sygnał/informacja.  
`z(t)` — stan helisy przed i po pobudzeniu.  
`y(t)` — obserwowalna odpowiedź.

`z(t+1) = F(z(t), u(t))`  
`y(t) = G(z(t), u(t))`

To na razie schemat identyfikacji, nie gotowe prawo fizyczne. Nie wymyślać postaci F i G bez podstawy w istniejącym kodzie lub danych.

Rozróżniać:
- reakcję: wyjście zmienia się po pobudzeniu;
- pamięć: identyczny sygnał testowy daje różną odpowiedź zależnie od historii/stanu;
- adaptację: zmieniają się parametry odpowiedzi po serii pobudzeń;
- samonaprawę: układ wraca do niezależnie określonego stanu odniesienia po zakłóceniu;
- odzyskanie informacji: odtwarzany jest payload/stan informacyjny, nie tylko energia lub częstotliwość.

## 5. Minimalny test rozstrzygający — dopiero po audycie ścieżki

Porównać odpowiedź na **identyczny sygnał testowy** dla:
- stanu odniesienia/świeżego;
- stanu po wcześniejszym, kontrolowanym pobudzeniu.

Utrzymać identyczne warunki i mierzyć z góry wybrany kanał odpowiedzi. Dodać kontrolę bez sprzężenia. Jeśli odpowiedź zależy od historii, wykazać efekt wejście–wyjście zależny od stanu. Jeśli nie — nie zakładać pamięci w tym kanale.

Nie rozszerzać od razu na wszystkie amplitudy, częstotliwości, topologie i geometrie. Najpierw jeden poprawnie zdefiniowany tor sygnału.

## 6. Co zostaje na drugim planie

- HC-01: matematyczna helisa kołowa i jej analityczne parametry — punkt odniesienia, nie główny cel.
- HC-01-TUBE: geometria tunelu — cecha struktury, którą można wykorzystać jako zmienną objaśniającą odpowiedź.
- Redukcja 4→3, próg 90°, √2/√3, punkty kardynalne i interpretacje TRM — hipotezy wtórne. Nie prowadzić teraz osobnego programu ich rozstrzygania.
- Nie mnożyć rodzin helis i sweepów, dopóki audyt ścieżki sygnału nie pokaże, że są konieczne.

## 7. Zasada prowadzenia pracy po wznowieniu

Każdy krok ma odpowiedzieć: **jak to przybliża nas do zrozumienia wpływu sygnału na helisę i jej odpowiedzi?**

Raportować krótko:
- co znaleziono w istniejącym kodzie;
- co jest rzeczywiście wykonywane;
- czego nie ma;
- jedna luka o największym znaczeniu;
- następny minimalny test.

Nie twierdzić, że uruchomiono eksperyment, jeśli jedynie zapisano protokół lub kod. Oddzielać zapis w repo, testy CI, wykonanie eksperymentu i interpretację wyniku.

## 8. Dokumenty źródłowe w GIA-TIMDR

- `docs/geometry/HELIX_SIGNAL_RESPONSE_COUPLING_v0.1.md` — synteza sprzężenia sygnał–helisa–odpowiedź.
- `docs/theory/HELIX_TIMDR_RESEARCH_PROGRAM.md` — nadrzędny program badań, szczególnie sekcje 36–37.
- `docs/geometry/HELIX_CHARACTERIZATION_PROTOCOL_HC01_v0.1.md` — charakterystyka geometryczna HC-01, materiał pomocniczy.
- `docs/geometry/RESULT_HC01_CIRCULAR_HELIX_PILOT_2026-11-09.md` — wyniki pilotażowe HC-01/TUBE, materiał pomocniczy.

**Jednozdaniowe wznowienie:** Otwórz ten handoff, przejrzyj istniejące moduły G/K/M/T oraz kod Helix-Lock i zrekonstruuj rzeczywisty przepływ sygnału przez helisę aż do jej odpowiedzi; nie rozpoczynaj nowych pobocznych badań przed tym audytem.


## 9. Wynik audytu istniejącego przepływu (2026-11-09)

Audyt zapisany w `docs/handoffs/AUDIT_SIGNAL_TO_HELIX_RESPONSE_PATH_2026-11-09.md`. Ustalono: graf zdarzeń może generować sygnał M/S; K wyznacza modalności (f,φ,A) i afiniczną synchronizację; `chrono_modal_geometry_bridge.py` mapuje trzy obwiednie na trajektorię Γ i mierzy jej κ/τ; G buduje mechaniczny pierścień i oblicza odpowiedź harmoniczną ustaloną; `modal_self_repair.py` dopasowuje skalar częstotliwości s. Są to osobne komponenty/projekcje, nie zamknięty sprzężony tor.

**Kluczowy wynik:** brakuje wykonywalnego przejścia: sygnał wejściowy → jawne oddziaływanie z fizycznym/abstrakcyjnym stanem helisy → aktualizacja stanu → obserwowalna odpowiedź → wpływ odpowiedzi na kolejne wejście. G nie przyjmuje obecnie przebiegu sygnału w czasie ani historii; jego odpowiedź jest ustalona w dziedzinie częstotliwości. Most chrono-modal mierzy geometrię trajektorii obwiedni, ale nie aktualizuje stanu G. K nie dostraja dynamicznie geometrii. `abs(tau)` w G usuwa znak chiralności.

**Następny krok:** nie robić kolejnego sweepu. Wybrać jeden istniejący sygnał i jeden kanał wymuszenia, określić jednostki/normalizację i jawnie oznaczyć mapowanie sygnału na wymuszenie jako hipotezę modelową. Następnie zbudować minimalny test integracyjny z identycznym sygnałem testowym dla stanu odniesienia i stanu po historii pobudzenia. Bez uzasadnienia jednostek wynik pozostaje abstrakcyjnym testem wejście–wyjście, nie fizycznym dowodem.


## 10. Minimalny test integracyjny wykonany

Dodano `experiments/helix_signal_response/minimal_coupling_probe.py` i testy. CI run `42572283596` zakończył się PASS (3/3 testy); skrypt wykonał porównanie odpowiedzi na identyczny sygnał dla stanu zerowego i stanu po wcześniejszym impulsie. RMS odpowiedzi: 0.0311099 vs 0.0838454; RMS różnicy: 0.0748333; max różnicy: 0.1739572. Wynik dowodzi zależności od stanu w abstrakcyjnym liniowym modelu pierścienia G. **Nie** dowodzi fizycznego sprzężenia informacji z rzeczywistą helisą: wejście znormalizowane do siły przez arbitralny gain, bez kalibracji jednostek. Raport: `docs/handoffs/RESULT_MINIMAL_SIGNAL_HELIX_RESPONSE_PROBE_2026-11-09.md`.

Następny i jedyny priorytet: ustalić na podstawie wcześniejszych badań i repozytoriów, jaki jest rzeczywisty fizyczny/operacyjny kanał oddziaływania informacji na helisę. Nie rozszerzać modelu ani nie mnożyć sweepów, dopóki kanał nie zostanie uzasadniony.


## 11. Audyt wcześniejszych kandydatów sprzężenia G↔S

W kolejnym przeglądzie znaleziono istniejący operator, który trzeba uwzględnić: `TIMDR-Math-Formalism/timdr_formalism/gs_matrix.py`, z dynamiką `dV/dt=KV`, `V=[G,S]^T` i rozkładem K na część antysymetryczną (zachowawcze mieszanie stanów) oraz symetryczną (wzrost/zanik). To korekta wcześniejszego stwierdzenia, że w całym repo nie ma żadnego operatora G↔S. GS-Matrix jest abstrakcyjnym kandydatem obliczeniowym, ale nie ma jeszcze kalibracji jednostek ani mapowania składowych na mierzalne stopnie swobody helisy.

Dodatkowo `signal_meta_bridge.py` łączy sygnał → SG-Coupling → Θ_bif → klasy I/II/III → MetaState → faza, ale nie sprzęga mechanicznie z helisą. `modal_band_energy_bridge.py` daje obserwable pasmowe sygnału, nie pomiar energii przekazanej do helisy. Modele T/U pozostają szkicami pola/przepływu informacji, bez kompletnego, wymiarowo określonego prawa oddziaływania.

Pełny audyt kandydatów: `docs/handoffs/AUDIT_CANDIDATE_PHYSICAL_SIGNAL_HELIX_CHANNELS_2026-11-09.md`. Kolejny priorytet: audyt pozostałych repozytoriów, zwłaszcza TSI, ponieważ lokalny katalog `C:\Users\jback\Downloads\a` nie jest dostępny bezpośrednio w sesji; potrzebne jest udostępnienie archiwum lub repozytoriów na GitHub.


## 12. Synoptyk-v3 — trop warstwy pola jako transformatora sygnału

Użytkownik wskazał Synoptyk-v3. Audyt repo `jbackk-lang/Synoptyk-v3` potwierdził, że pipeline `membrane/interpolate.py` przekształca rozproszone wejścia w regularne pola skalarne/wektorowe; `spectrum.py` wyznacza FFT, gradienty, wirowość i koherencję; `defects.py` i `resonance.py` wydobywają lokalne anomalie i koincydencje; `meta_adapter.py` mapuje cechy do `MetaState(Λ,τ,ρ,J)`. Ważna lekcja: najpierw transformacja wejścia do pola, potem analiza struktury pola, dopiero potem adapter stanu.

Dla helisy może to być brakująca warstwa między surowym sygnałem a GS-Matrix/G-Rezonansem. To wzorzec architektoniczny, nie gotowy fizyczny operator: pole pogodowe Synoptyka nie jest polem oddziaływania helisy; jego heurystyczny rezonans nie jest oscylatorem fizycznym; MetaState nie jest siłą/energią. Szczególnie cenna jest praktyka zachowania orientacji: wiatr jest rozkładany na u/v przed interpolacją, by nie zgubić cykliczności kierunku. Analogicznie helikalna reprezentacja nie może gubić fazy ani znaku chiralności.

Dokument analizy: `docs/handoffs/SYNOPTYK_V3_FIELD_TRANSFORM_CLUE_FOR_HELIX_2026-11-09.md`. Następny minimalny krok: dla jednego sygnału sprawdzić transformację sygnał→pole→cechy pola→rekonstrukcja, mierząc co zostało zachowane/utracone; dopiero potem mapować wybrane cechy na stan S w GS-Matrix i odpowiedź G. Nie pisać nowego operatora ani nie zakładać fizycznego sprzężenia przed tym testem.


## 13. Test zachowania fazy/chiralności w transformacji do pola (2026-11-09)

Wykonano test syntetyczny wzorowany na interpolacji Synoptyk-v3 (griddata cubic, 9×9→81×81). Dla pola `φ=±atan2(y,x)` interpolacja pary `cosφ,sinφ` i rekonstrukcja `atan2` zachowały winding +1/−1; interpolacja samego zawiniętego kąta jako skalara dała winding ≈0 dla obu znaków. MAE fazy 0.826°, p95 3.846°. CI run `42584118204`: 3/3 PASS. Raport: `docs/handoffs/RESULT_PHASE_FIELD_CHIRALITY_PRESERVATION_2026-11-09.md`; kod: `experiments/phase_field_preservation/`.

Dodatkowa obserwacja: radialne widmo mocy i moduł gradientu nie zachowują orientacji/chiralności (lustrzane pola dają identyczne te cechy); wirowość ze znakiem oraz winding mogą ją zachować. Dla helisy trzeba przechowywać parę kwadraturową, amplitudę/normę, znak winding i miejsca zaniku normy; nie redukować do samego kąta, modułu lub radialnego widma.

Wynik potwierdza wybór reprezentacji w syntetycznym teście, nie fizyczne sprzężenie sygnału z helisą. Następny krok: test odporności pary kwadraturowej i znaku winding na szum oraz rozdzielczość próbkowania, zanim pole zostanie mapowane na S w GS-Matrix.


Rozszerzono test pola o sweep odporności: 5 rozdzielczości (5×5 do 17×17), 5 poziomów szumu (0–0.35), oba znaki chiralności, łącznie 50 przypadków. CI `42584276273`: 4/4 PASS; wszystkie 50 zachowały winding ±1. Lokalna faza degraduje się mimo zachowanego winding: najgorszy przypadek MAE 18.86°, p95 56.59° (5×5, szum 0.35). Przy 9×9 i szumie 0.1 MAE ok. 4.1–4.5°. Raport rozszerzony: `docs/handoffs/RESULT_PHASE_FIELD_CHIRALITY_PRESERVATION_2026-11-09.md`. Interpretacja: znak topologiczny jest odporniejszy niż lokalna rekonstrukcja fazy; wymaga to dalszej walidacji na nieregularnych próbkach, wielu seedach i bardziej złożonych polach.


## 14. Test historii fazowej na rzeczywistych sekwencjach MAGE

Dodano `experiments/mage_temporal_phase_history/test_phase_history.py` i workflow `.github/workflows/mage-temporal-phase-history.yml`, który pobiera publiczne repo MAGE jako źródło danych i uruchamia analizę trzech sekwencji UCSD Ped2. CI run `42585600447` zakończył się PASS.

Dla Test001 (180 klatek), Test002 (180) i Test003 (150) obliczono zespolone FFT klatek, a historię opisano przez fazę początkową + uporządkowane `Δφ_t=arg(F_{t+1} conj(F_t))`. MAE rekonstrukcji uporządkowanej: 2.50–3.26e-6 rad; po przetasowaniu przyrostów: 1.380–1.393 rad. Odwrócenie czasu spełniło oczekiwaną relację znaku/kolejności z błędem max 4.77e-7 rad. To potwierdza, że uporządkowana reprezentacja zachowuje historię fazową sekwencji; nie dowodzi autonomicznej pamięci pola ani helisy (rekonstrukcja jest konsekwencją definicji przyrostów).

Opisowa średnia aktywność fazowa normal/anomalia: Test001 0.454/0.475 rad; Test002 0.435/0.579; Test003 0.479/0.518, ale tylko 3 przejścia normalne w Test003. Nie wykonano inferencji statystycznej ani korekty ruchu kamery; wskaźnik nie rozróżnia stabilnie anomalii. Raport: `docs/handoffs/RESULT_MAGE_REAL_SEQUENCE_PHASE_HISTORY_2026-11-09.md`.

Następny priorytet: korekta globalnego ruchu, lokalna koherencja fazowa i baseline'y (różnica obrazu/przepływ optyczny/amplituda widma) na większej liczbie klipów. Nie podłączać jeszcze do G-Rezonansu; dopiero po walidacji reprezentacji pola określić mapowanie do S/GS-Matrix.


## 15. Biologiczny trop: DNA → rozwój → helikalna morfologia (2026-11-09)

Użytkownik wskazał muszle ślimaków jako przykład informacji dziedzicznej, która steruje powstawaniem struktury spiralnej. Przegląd literatury potwierdza mocną, ale pośrednią ścieżkę przyczynową: DNA/produkty matczyne → ekspresja i białka → cytoszkielet/orientacja podziałów → chiralność zarodka i asymetria ciała → asymetryczny wzrost płaszcza + mechanika → przyrostowa geometria muszli. Dla *Lymnaea stagnalis* gen matczyny Lsdia1 (formin) został eksperymentalnie powiązany z kierunkiem dextral/sinistral (Abe & Kuroda 2019, PMID 31088796). Badania PNAS 2019 wykazują asymetrie proliferacji/organizacji komórek na brzegu płaszcza; model PNAS 2021 wskazuje również na rolę mechanicznego skrętu ciała. Źródła i pełna synteza w `docs/handoffs/RESULT_DNA_TO_HELICAL_MORPHOGENESIS_REVIEW_2026-11-09.md`.

Wniosek precyzyjny: DNA nie musi kodować gotowej geometrii muszli; koduje/reguluje procesy, które iteracyjnie wytwarzają geometrię. Nie utożsamiać helisy molekularnej DNA z makroskopowym skrętem muszli. Kierunek chiralności, logarytmiczna geometria zwoju i szczegóły ornamentacji są odrębnymi cechami wymagającymi odrębnych mechanizmów.

Audyt repo: TIMDR-DNA jest analizatorem depth-of-coverage/CNV, nie modelem morfogenezy DNA; Helix-Lock jest narzędziem kryptograficznym, nie biologicznym modelem helisy. GIA-TIMDR nie ma jeszcze łańcucha DNA→rozwój→morfologia. Nie przedstawiać tego jako istniejącego kodu ani potwierdzonej fizyki TIMDR.

Następny minimalny test koncepcyjny: rozdzielić (1) parametr dziedzicznej chiralności, (2) lokalną regułę przyrostu brzegu muszli, (3) mechaniczne sprzężenie ciała i muszli oraz (4) obserwowaną geometrię zwoju. Najpierw testować, czy zmiana chiralności i parametrów wzrostu daje właściwy znak skrętu i klasy kształtów; później dodawać mechanikę. Biologia jest wzorcem architektury informacja→stan pośredni→reguły wzrostu→geometria, nie dowodem, że obecny G-Rezonans/GS-Matrix jest tym samym mechanizmem.


## 16. Korekta epistemiczna: geometria jako źródło formalizacji matematycznej (2026-11-09)

Użytkownik doprecyzował, że geometria nie jest poboczną wizualizacją ani czymś, od czego należy odchodzić ku informacji. **Geometria jest konieczna, ponieważ to z relacji geometrycznych wyprowadzamy formalizm matematyczny i liczby opisujące układ.** Osie, kąty, proporcje, odległości, skręt, orientacja/chiralność, punkty przejścia i warunki brzegowe są pierwotnymi relacjami strukturalnymi; liczby, funkcje, macierze i operatory są ich formalnym zapisem lub miarą.

Zachować więc obie strony bez odwracania ich ról:
- geometria helisy: struktura i relacje, które trzeba opisać;
- matematyka: język ilościowego wyprowadzenia tych relacji;
- operator: formalny model oddziaływania sygnału z geometrią/stanem;
- odpowiedź: wynik, który można porównać z obserwacją.

Schemat roboczy: `geometria → formalizacja matematyczna → operator oddziaływania → odpowiedź helisy`. Sygnał/informacja jest wejściem do tego układu, nie substytutem geometrii. Trop biologiczny DNA→rozwój→muszla jest przydatny jako przykład tego, jak informacja może wpływać na powstawanie i zmianę geometrii; nie uzasadnia redukowania helisy do samej informacji ani pomijania jej osi, tunelu, skrętu, chiralności i warunków brzegowych.

**Reguła metodologiczna:** nie proponować operatora oderwanego od geometrii. Najpierw wskazać relację geometryczną, następnie jej matematyczną reprezentację, potem sposób oddziaływania sygnału i mierzalną odpowiedź. Nie oznacza to, że wszystkie wielkości muszą być wyprowadzone wyłącznie z geometrii euklidesowej; oznacza, że ich znaczenie w modelu musi być zakotwiczone w jawnej strukturze i relacjach.


## 17. Geometria-first: pierwsze ścisłe relacje i granice modelu

Użytkownik podkreślił, że geometria jest źródłem formalizacji matematycznej, a nie dodatkiem. Zapisano pierwsze warunkowe wyprowadzenia: przy stałym względnym przyroście `dr/dθ=br` otrzymujemy `r=r₀e^{bθ}` i `b=ln(q)/(2π)` z ilorazu promieni po obrocie; przy stałym przesunięciu osiowym `dz/dθ=c` otrzymujemy `z=z₀+cθ` i skok `P=2πc`. Chiralność wymaga jawnej konwencji orientacji osi i parametryzacji `ε=±1`; nie jest tym samym co b ani P.

Ważne zastrzeżenie z literatury: muszla jest zwykle modelowana jako ruch/skalowanie krzywej generującej wokół osi, nie jako pojedyncza zwykła helisa. Badanie empiryczne 25 gatunków / 176 okazów wykazało, że klasyczne założenia izometrii i wykładniczego wzrostu zawodzą dla części gatunków (Paleobiology, DOI 10.1017/pab.2021.8). Logarytmiczny model jest bazą, nie uniwersalnym prawem. Dokument: `docs/handoffs/GEOMETRY_FIRST_MATHEMATICAL_DERIVATIONS_2026-11-09.md`.

Następnie należy zdefiniować własną geometrię TIMDR (oś/tunel, krzywa generująca, skręt/chiralność, ekspansja, translacja, przekrój, warunki brzegowe) i dopiero potem wyprowadzić operator. Równania powyżej są ścisłymi konsekwencjami założeń, nie dowodem, że sygnał zmienia parametry ani że GS-Matrix/G-Rezonans są prawami fizycznymi.


## 18. Audyt czterech istniejących formalizmów — wynik 2026-11-09

Przeprowadzono przegląd `TIMDR-Math-Formalism`, `TIMDR-Geometry-Formalism`, `TIMDR-Time-Formalism` i `TIMDR-Modal-Formalism`. Nie zaczynamy od zera. G8-G9 mają dyskretny operator Weingartena, krzywizny główne i `T_S`; `Γ(t,s)` tworzy powierzchnię z rodziny trajektorii; G10 ma ścisłą redukcję/odwrócenie `(P,Q)` dla jednej rodziny zaokrąglonych obwiedni trójkąta; GS-Matrix opisuje abstrakcyjną spiralną dynamikę w przestrzeni stanów `(G,S)`; Modal formalism ma fazę/synchronizację; Chronoprocess orkiestruje M/S, G, K bez automatycznego sprzężenia.

Znaleziono kluczowe rozróżnienia/luki: (1) `T_S=||n(q)-n(p)||` jest normą i gubi znak orientacji; nie jest sam w sobie chiralnością ani torsją osi. (2) operator Weingartena opisuje krzywiznę powierzchni, nie automatycznie torsję krzywej osi. (3) spirala GS-Matrix jest w przestrzeni stanów `(G,S)`, nie dowodem przestrzennej helisy 3D. (4) G10 dotyczy jednej rodziny zaokrąglonych obwiedni trójkąta; nie dowodzi ogólnej redukcji czworościan→trójwęzeł ani dowolnej helisy. (5) brak formalnego mostu sygnał/pole→zmiana Γ/geometrii→odpowiedź; Chronoprocess nie przekazuje wyników między gałęziami. (6) faza modalna nie jest pamięcią mechaniczną.

Pełny audyt: `docs/handoffs/AUDIT_EXISTING_FORMALISMS_FOR_TIMDR_HELIX_2026-11-09.md`. Następny krok: sporządzić kartę geometrycznego obiektu helisy TIMDR (oś jako krzywa, powierzchnia boczna, tunel/przekrój, rama/orientacja, warunki brzegowe) i przypisać do niej istniejące obserwable oraz jawne braki. Nie dopisywać nowego operatora przed tym mapowaniem.


## 19. Odkrycie w głównym repo: istniejąca specyfikacja tunelu osi i podpisana torsja

Po dalszym audycie `docs/geometry/` odnaleziono dwa bezpośrednio relewantne dokumenty z 2026-11-09: `AXIS_TUNNEL_BOUNDARY_CONDITIONS_TWIST_RANGE_REDUCTION_v0.1.md` oraz `ROTATION_INNER_SPIRAL_SPHERICAL_CONFINEMENT_TO_KNOT_v0.1.md`. Pierwszy definiuje oś A(s), tunel r(s), ramę Freneta/Bishopa, warunki brzegowe/sklejenia, zorientowany kąt θ(s), tempo ω=dθ/ds i redukcję jako granicę dopuszczalności min g_j=0; próg 90° pozostaje hipotezą testową. Drugi rozdziela moduł, oś wewnętrzną i gałęzie helikalne; opisuje odbicie m_n, kuliste ograniczenie, holonomię, torsję, twist, writhe i warunki topologicznego domknięcia. Oba są specyfikacjami/hipotezami do implementacji i falsyfikacji, nie dowodem fizycznym.

Odnaleziono również `core/trefoil_frenet_torsion.py` i `TIMDR_Trefoil_FrenetTorsion.md`: podpisana torsja Freneta-Serreta osi trójwęzła τ=det(v,a,j)/||v×a||², z bramkowaniem przy małej krzywiźnie. Raport 4/4 testów syntetycznych: deformacja lokalna wykrywana, czysta krzywa bez fałszywych alarmów; koincydencja 2-z-3 zawężała rozmyte wskazania torsji. To istniejąca baza, której nie trzeba pisać ponownie.

Krytyczne: `core/geometric_resonance_operator.py` używa `kc[i]=kc_scale*abs(tau[i])`. G-Rezonans traci więc znak torsji w macierzy sprzężeń i nie może przez ten kanał rozróżnić lustrzanej chiralności. Nie zmieniać tego arbitralnie; najpierw zaprojektować kontrolę lustrzaną i określić, czy znak ma wpływać na kierunek/strukturę sprzężenia.

Wniosek: główna luka została zawężona. Mamy już specyfikację tunelu osi i kod podpisanej torsji trójwęzła; brakuje ich implementacyjnej walidacji dla właściwej helisy TIMDR oraz integracji podpisanych wielkości θ, ω, τ, holonomii i twistu gałęzi z G-Rezonansem. Pełny audyt uzupełniono w `docs/handoffs/AUDIT_EXISTING_FORMALISMS_FOR_TIMDR_HELIX_2026-11-09.md`.


## 20. HC-01: istniejący matematyczny baseline helisy i tunelu

Odnaleziono `HELIX_CHARACTERIZATION_PROTOCOL_HC01_v0.1.md`, `experiments/helix_characterization/hc01_circular_helix.py`, `hc01_tube.py` oraz raport `RESULT_HC01_CIRCULAR_HELIX_PILOT_2026-11-09.md`. Dla helisy kołowej `r(t)=(a cos t,a sin t,h t)` istnieją ścisłe wzory: κ=a/(a²+h²), τ_FS=h/(a²+h²), τ/κ=h/a, skok p=2πh, długość obrotu 2π√(a²+h²). Odbicie h→−h odwraca znak torsji i skoku, zachowując krzywiznę i długość. Bezwymiarowa torsja aτ=η/(1+η²) osiąga maksimum modułu przy |η|=1, co odpowiada 45° kąta stycznej do płaszczyzny poprzecznej. To nie jest próg 90° ani punkt kardynalny TIMDR.

HC-01-TUBE porównuje lokalny promień krzywizny z globalnym ograniczeniem przez doubly-critical self-distance; dla małego skoku globalne zbliżenie osi może ograniczać tunel wcześniej niż lokalna krzywizna. Wynik dotyczy idealnej helisy kołowej. Protokół HC-01 już przewiduje HC-02 zmienny skok, HC-03 zmienny promień, HC-04 zakrzywioną oś, HC-05 zamkniętą krzywą lokalnie helikalną i HC-06 trefoil.

Istniejące modele redukcji 4→3 (`four_to_three_surface_reduction.py`, `phase_locked_whole_strand_reduction.py`) są kinematyczne: wycinają/łączą gałąź i re-fazują pozostałe, bez pełnej relaksacji mechanicznej i bez pełnego niezmiennika węzła. Audyt sinusoidy (+,−,+) względem torsji trefoila nie potwierdził prostego przypisania znaków do trzech sektorów.

Wniosek: nie trzeba ponownie wyprowadzać podstawowej geometrii helisy kołowej. Dalsze prace powinny rozwijać już zamrożony protokół HC-01 w kierunku HC-02/HC-04 i porównać wynik z modelem tunelu/warunków brzegowych. Raport audytu: `docs/handoffs/AUDIT_EXISTING_FORMALISMS_FOR_TIMDR_HELIX_2026-11-09.md`.
