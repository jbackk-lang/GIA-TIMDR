# AUDYT ISTNIEJĄCEGO FORMALIZMU DLA HELISY TIMDR

Data: 2026-11-09
Zakres: TIMDR-Math-Formalism, TIMDR-Geometry-Formalism, TIMDR-Time-Formalism, TIMDR-Modal-Formalism i powiązane dokumenty GIA-TIMDR.

## 1. Werdykt

Nie zaczynamy od zera. Istnieją już: (1) geometria powierzchni i operator kształtu Weingartena G8-G9; (2) miara zmiany orientacji pola normalnych T_S; (3) kongruencja Γ(t,s), która tworzy rzeczywistą powierzchnię z rodziny trajektorii; (4) redukcja/rozwinięcie obwiedni trójkąta przez P,Q; (5) formalizm sygnałowy i abstrakcyjny GS-Matrix dV/dt=KV; (6) fazy modalne i synchronizacja; (7) Chronoproces Ξ=(T,x,Γ,φ), który orkiestruje gałęzie bez utożsamiania ich obiektów.

Nie znaleziono jednak wyprowadzonego i empirycznie zwalidowanego operatora mapującego sygnał/pole na zmianę geometrii helisy i zwrotną odpowiedź. To pozostaje główną luką.

## 2. Geometry Formalism: co jest gotowe

### G8-G9: krzywizna powierzchni

timdr_geometry/weingarten.py reprezentuje powierzchnię jako trójkątną siatkę S⊂R³, liczy normalne wierzchołkowe, estymuje dyskretny operator kształtu S_p:T_pS→T_pS metodą najmniejszych kwadratów, a jego wartości własne dają krzywizny główne κ1,κ2. Liczone są H=(κ1+κ2)/2 i K=κ1κ2.

T_S_empirical=||n(q)-n(p)||; T_S_predicted=||Δp||·||S_p(Δp_hat)||. Implementacja jest testowana na płaszczyźnie, sferze i walcu oraz na zbieżności siatki. Testy geometrii deklarowane są jako 83/83 PASS łącznie z envelope i chronocongruence. To walidacja implementacji na syntetycznych powierzchniach o znanej odpowiedzi, nie pomiar rzeczywistej helisy.

### Luka krytyczna: znak skrętu

T_S jest normą różnicy normalnych. Jest nieujemny i usuwa kierunek zmiany. Samodzielnie nie koduje chiralności lewo/prawo, torsji krzywej osi ani holonomii po obiegu. S_p jest operatorem kształtu powierzchni, nie automatycznie torsją osi helisy. To ograniczenie definicji obserwabli, nie błąd kodu.

### Γ(t,s): sposób utworzenia powierzchni

chronocongruence.py tworzy siatkę z rodziny trajektorii Γ(t,s). Pojedyncza oś jest krzywą 1D i nie ma operatora kształtu powierzchni. Rodzina trajektorii tworząca powierzchnię 2D pozwala zastosować normalne i Weingartena. To może być baza opisu powierzchni otaczającej tunel helisy, jeśli jawnie zdefiniujemy parametryzację i warunki okresowości.

### G10: redukcja obwiedni trójkąta

envelope.py definiuje rodzinę zaokrąglonych obwiedni ∂_R(Δ): L0(R) jest długością części prostych, Lk(R)=2πR długością łuków, P=L0/L, Q=Lk/L=1-P. P(R) jest ściśle monotoniczne i odwracalne w obrębie tej jednej rodziny przy ustalonym trójkącie; Rmax=r_in dla każdego trójkąta.

To ścisły wynik dla konkretnej jednoparametrowej rodziny obwiedni. Nie dowodzi ogólnego twierdzenia, że dowolny czworościan redukuje się do trójwęzła albo dowolna helisa do struktury trójdzielnej.

## 3. Math Formalism: GS-Matrix nie jest geometrią przestrzenną

gs_matrix.py definiuje abstrakcyjny układ dV/dt=KV, V=[G,S]^T. Dokument GS_Matrix_Helical_Coupling_DRAFT.md proponuje nowe sprzężenie z Θ_bif.

Ustalenia źródłowe: K i Θ_bif były wcześniej rozłączne; ω₀ jest nowym parametrem, nie wyprowadzonym z istniejącej geometrii; próg ω₀crit=(λ_down+λ_up)/2 i Im(λ)=sqrt(ω₀²-ω₀crit²) są dokładne dla przyjętej macierzy 2×2; przewidywanie oscylacji N(t)=S_down·S_up z częstością 2ω jest sprawdzone algebraicznie i numerycznie w tym modelu.

Identyfikacja S_down/S_up z bazą własną K_sym jest decyzją konstrukcyjną. Model liniowy pomija β(Q) i nasycenie tanh prawdziwego S_up. Estymator Re(λ) nie przeszedł kryterium dokładności; binarna klasyfikacja rotacji przeszła testy syntetyczne, a wyniki na realnych danych są opisowe i małopróbkowe.

Najważniejsze rozróżnienie: spirala w tym dokumencie jest trajektorią w przestrzeni stanów (G,S), a nie dowodem przestrzennej helisy 3D. Te obiekty mogą być powiązane, ale nie są automatycznie tym samym.

## 4. Time Formalism: brak mostu G↔M/S

Chronoproces Ξ=(T,x,Γ,φ) orkiestruje x (M/S), Γ (G) i φ (K). README jawnie stwierdza, że nie dodaje nowej matematyki ani nie przekazuje automatycznie wyników między gałęziami. Most Fouriera M/S↔K ma podstawę w klasycznej analizie Fouriera. Analogicznego mostu G↔M/S jeszcze nie ma.

To wyjaśnia, dlaczego nie można po prostu wpiąć historii fazowej MAGE do G-Rezonansu: interfejs nie został formalnie zdefiniowany.

## 5. Modal Formalism: faza to nie pamięć mechaniczna

phase_sync.py definiuje fazę chwilową modalności, interferencję, rezonans pary, lokalny czas oraz Λ_K(t)=1-|mean(exp(iθ_i(t)))| i τ_K=|Λ_K(t+dt)-Λ_K(t)|/dt. Są to obserwable na wspólnym okręgu fazowym, nie miara chiralności przestrzennej ani odpowiedzi mechanicznej helisy.

K-GRID-FREQ ma status SUPPORTED w zawężonym protokole replikacji; K-MARS-DAS v0.1/v0.2 ma status NOT SUPPORTED. Nie wolno uogólniać pojedynczego sukcesu na całą gałąź K.

## 6. Co można zestawić już teraz

Na poziomie architektury danych można zestawić: MAGE/Synoptyk (sygnał i historia/pole), M/S (stan sygnałowy), K (faza modalna), G (Γ, normalne, S_p, κ1,κ2,H,K,T_S), Chronoprocess (wspólny nośnik T). To mapa obserwabli, nie sprzężony model fizyczny.

## 7. Dokładne braki dla helisy TIMDR

A. Geometria osi i tunelu: brak kompletnej parametryzacji helisy TIMDR obejmującej oś, tunel, przekrój i warunki brzegowe.

B. Miara skrętu ze znakiem: trzeba rozdzielić krzywiznę osi, torsję krzywej osi, skręt powierzchni i holonomię transportu ramy. To różne obiekty.

C. Zachowanie historii geometrycznej: formalizmy fazowe opisują fazę modalną, a MAGE przyrosty fazowe. Brak operatora mapującego historię na stan pamięci powierzchni i odróżniającego pamięć od zależności od bieżącego stanu.

D. Kanał sygnał→geometria→odpowiedź: brak mapowania sygnału/pola na geometryczne stopnie swobody (np. parametry Γ, krzywizny, skręt, stan osi/tunelu) oraz niezależnego pomiaru odpowiedzi.

## 8. Najbardziej ekonomiczny następny krok

Nie pisać nowego formalizmu od razu. Przygotować kartę obiektu geometrycznego helisy TIMDR: typ obiektu (oś jako krzywa, powierzchnia boczna, objętość/tunel), parametryzacja osi i powierzchni, ramy i konwencja orientacji, warunki brzegowe/okresowość, obserwable już dostępne (κ1,κ2,H,K,T_S), obserwable brakujące (krzywizna osi, torsja osi, znak skrętu, holonomia), oraz dane/siatka, na których można je zmierzyć.

Dopiero po zatwierdzeniu karty porównać istniejące operatory z wymaganymi obserwablami. Jeśli operator nie obejmuje zjawiska, dopiero wtedy dopisać brak, wraz z testem analitycznym i niezależnym testem numerycznym.

## 9. Konkluzja

Trzeba pilnować rozróżnień: krzywizna powierzchni ≠ torsja osi helisy; norma zmiany normalnych ≠ chiralność ze znakiem; spirala w przestrzeni stanów (G,S) ≠ przestrzenna helisa; redukcja obwiedni trójkąta (P,Q) ≠ ogólna redukcja węzła/helisy; faza modalna ≠ pamięć mechaniczna powierzchni.

To są konkretne luki do rozstrzygnięcia przed wiarygodnym modelem odpowiedzi helisy na informację.

## 10. Uzupełnienie po odczytaniu oryginalnych dokumentów GIA: tunel osi i torsja trójwęzła

Audyt uzupełniono o dwa istniejące dokumenty, które są bezpośrednio bliższe aktualnemu pytaniu niż ogólne G8-G10:

### 10.1 AXIS_TUNNEL_BOUNDARY_CONDITIONS_TWIST_RANGE_REDUCTION_v0.1.md

To już istniejący program formalizacji tunelu osi. Definiuje oś A(s), otoczenie rurowe o promieniu r(s), lokalne współrzędne z ramą poprzeczną, warunki poprzeczne i osiowe, sklejenia pozycji/stycznej/ramy/fazy/indeksu gałęzi/orientacji, warunki regularności oraz zorientowany kąt θ(s) i tempo ω(s)=dθ/ds. Redukcja jest zdefiniowana jako utrata dopuszczalności min_j g_j(X)=0, a nie arbitralny próg liczby modułów. Próg 90° jest wyraźnie hipotezą testową. To dokładnie właściwy punkt startowy; status dokumentu pozostaje programem formalizacji, nie zwalidowanym modelem fizycznym.

### 10.2 ROTATION_INNER_SPIRAL_SPHERICAL_CONFINEMENT_TO_KNOT_v0.1.md

Ten dokument rozdziela moduł M_n, wewnętrzną oś A(s) i gałęzie H_i(s). Opisuje obrót modułów, odbicie m_n∈{−1,+1}, ramę, ograniczenie kulą, torsję osi, holonomię, twist gałęzi i writhe. Jawnie stwierdza, że kula sama nie tworzy skrętu i że zamknięcie geometryczne nie dowodzi węzła; potrzebne są warunki domknięcia, brak samoprzecięć i niezmiennik topologiczny. To hipoteza do falsyfikacji, nie gotowy model.

### 10.3 Istniejąca torsja Freneta-Serreta trójwęzła

`core/trefoil_frenet_torsion.py` liczy krzywiznę i podpisaną torsję osi z κ=||v×a||/||v||³ oraz τ=det(v,a,j)/||v×a||², z bramkowaniem przy małej krzywiźnie. `docs/geometry/TIMDR_Trefoil_FrenetTorsion.md` raportuje 4/4 testy na syntetycznym trefoilu: negatywna kontrola bez fałszywych alarmów, dodatnia lokalna deformacja wykrywana; rezonans 2-z-3 kanałów zwęża 31 rozproszonych punktów torsji do 4. To nie jest walidacja fizycznej helisy TIMDR, ale istniejący kod do podpisanej torsji osi jest ważnym punktem startowym.

### 10.4 Krytyczna utrata znaku w G-Rezonans

W `core/geometric_resonance_operator.py` sprzężenie segmentowe jest budowane jako `kc[i]=kc_scale*abs(tau[i])`. Komentarz kodu jawnie stwierdza, że znak torsji nie zmienia siły sprzężenia w tym modelu, tylko kierunek geometryczny, którego macierz nie reprezentuje. Zatem obecny G-Rezonans może reagować na wielkość torsji, ale nie rozróżnia jej znaku/chiralności przez ten kanał. Nie należy po cichu zmieniać `abs`; to wymaga odrębnej decyzji modelowej i testu symetrii lustrzanej.

### 10.5 Wniosek skorygowany

Główna luka nie brzmi już „brak geometrii osi/tunelu” — istnieje jej jawna specyfikacja koncepcyjna. Luka brzmi: brak implementacji i walidacji tej specyfikacji oraz brak integracji jej podpisanych wielkości (θ, ω, τ osi, holonomia, twist gałęzi) z mechanicznym G-Rezonansem. Najbardziej ekonomiczny następny krok to audyt zgodności tych trzech artefaktów: tunel/warunki brzegowe, Frenet torsion i G-Rezonans, a następnie minimalny test, który sprawdza czy zmiana znaku torsji zmienia odpowiedź. Nie tworzyć jeszcze nowego operatora.
