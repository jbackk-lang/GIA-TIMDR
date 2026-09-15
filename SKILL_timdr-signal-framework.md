# TIMDR signal framework (GIA-TIMDR core) — uproszczony skrót

> Uproszczona wersja skilla `timdr-signal-framework` (kopia treści z konta Claude), zawężona do własnej teorii/formalizmu/sygnałów GIA-TIMDR. Pełna, cross-repo wersja skilla (audyty, case-studies z sejsmiki, radaru, bezpieczeństwa, kosmologii, EV/battery/industrial, Quantum-Lattice, Synoptyk-v3 itd.) istnieje osobno i NIE jest tu duplikowana. Stan: 2026-09-16.

## 1. Co to w ogóle jest?

Rdzeń formalizmu TIMDR: cztery sygnały, protokół testowania (anty-numerologia), CZTERY gałęzie (M/S, G, K, i od 2026-09-10 formalnie META-DYNAMICS Λ-τ-ρ-J jako rodzina operatorów agregatowych, analogicznie do rodziny krzywizn w Geometry Formalism), Chronoproces spinający M/S/G/K bez mieszania, domknięcia geometryczne (G8-G10), operator G-Rezonans (G5), uniwersalny walidator agregatu Λ-τ-ρ-J, test prawa redukcji TRM, poprawiony GS-Matrix i pełny operator bifurkacji Θ_bif z phase diagram (2026-09-12), zakres empiryczny mostu Fouriera ustalony na realnych danych i nowa, jawnie eksploracyjna konstrukcja sprzężenia helikalnego K↔Θ_bif (2026-09-15), i most M/S↔topologia/K przetestowany na 3 realnych domenach z silnym, częściowo scharakteryzowanym sygnałem na łożyskach (2026-09-15/16, punkt 19).

## 2. Cztery sygnały TIMDR (M/S)

- **anomalia** — wartość poza normą (np. > mean+2σ).
- **defekt** — skok między kolejnymi próbkami > próg.
- **rezonans M** — ≥3 anomalii w tym samym czasie (koincydencja, NIE fizyczny oscylator).
- **skręt sygnałowy** — odwrócenie trendu, flip znaku nachylenia > próg.

„Rezonans" i „skręt"/τ mają wiele znaczeń w całym ekosystemie GIA-TIMDR —
zawsze podawaj który: rezonans ma 4 znaczenia (M sygnałowy, K modalny,
kierunkowy R(t), G-Rezonans/G5 — punkt 11; plus kanał J w META-DYNAMICS,
patrz punkt 14, który jest POKREWNY duchem ale formalnie odrębny — 5
znaczeń licząc J), skręt/τ ma **6** formalnie skonsolidowanych w
`TIMDR_Twists.md` (sygnałowy, topologiczny τ [Operators_N_TIMDR.md,
torus→Möbius→tetroida], powierzchniowy, blokowy, Frenet-Serret trójwęzła,
i **τ dynamiczny TRM** [R=k·τⁿ, `TRM_biology.md`, punkt 13] —
NIEROZSTRZYGNIĘTE, czy to rozszerzenie skrętu topologicznego czy odrębny
obiekt pod tym samym symbolem) PLUS **τ META-DYNAMICS** (transformacja,
Λ-τ-ρ-J, punkt 14) — formalnie poza zakresem "skrętu" (nigdy tak nie
nazywane w kodzie), ale współdzieli symbol τ, więc licz 7 kolizji
symbolu τ w sumie. Kanoniczna lista: `docs/GLOSSARY_EN_PL.md`,
`TIMDR_Twists.md`, `TIMDR_Branch_Specification.md`.

## 3. Protokół formalizmu (anty-numerologia)

9 zasad, najważniejsze: preregistracja definicji/progów przed danymi
(zero tuningu po fakcie) · testy na tle losowym, nie na "czy sygnał
odpala gdy wzorzec już jest" · Mann-Whitney U + rozmiar efektu r
(obowiązkowy, nie opcjonalny) · kontrolka pozytywna I negatywna przed
testem głównym · moc testu: wysokie p ≠ brak efektu, jeśli zero zdarzeń
kwalifikujących się do testu · jedno uruchomienie, korekta Bonferroniego
przy wielu oknach · wynik negatywny jest pełnoprawną odpowiedzią ·
dodatkowa wielkość funkcyjna (np. wykładnik n w prawie potęgowym)
musi wygrać z prostszym baseline'em przez kryterium informacyjne (AIC/BIC),
nie samo "dopasowuje się" — patrz punkt 13 · **deklarowane ograniczenie/sufit
wzoru operatora musi być zweryfikowane na PEŁNYM zakresie wejść, jakie
operator faktycznie zobaczy w sprzężonym systemie, nie tylko na małych
reprezentatywnych wartościach użytych w testach jednostkowych — patrz
punkt 16, błąd R_phase[S]** · **pre-rejestracja z małą próbą (np. 6-10
powtórzeń) może dać złudnie dobry wynik będący artefaktem jednego,
wygodnego przypadku (np. stałego warunku początkowego) — formalny test
z większą próbą (N≥30) i losowanymi nuisance-parametrami jest tym, co to
łapie, patrz punkt 18.**

## 4. Formalizacja gałęzi sygnałowej — TIMDR-Math-Formalism

Implementacja protokołu jako kod (`timdr_formalism/pipeline.py`),
rozmiar efektu, dyscyplina mocy. Realny test na Kraków_Centrum: p≈1, bo
ciśnienie miało 0/24 przekroczeń własnego progu 2σ (zero zdarzeń do
przetestowania), NIE potwierdzony brak rezonansu — kontrolka pozytywna
złapana czysto (p≈0.0002), więc mechanika testu działa poprawnie.

**Rozszerzenie 2026-09-10: `timdr_formalism/meta_validator.py`** —
uniwersalny, domenowo-agnostyczny walidator agregatu Λ-τ-ρ-J (formalizm
TIMDR-META-DYNAMICS), NIE importuje żadnej klasy z TIMDR-META-DYNAMICS
(działa na płaskim `MetaSeriesData`, każdy adapter buduje go trywialnie
ze swojego wyniku). Pięć obszarów: kształt/zakresy kanałów, izolacja
kanałów (Spearman między parami, wykrywa wzorzec "zdublowanego sygnału"
jak już odrzucone Ω=D+|R|), diagnostyka progów fazowych (raportuje, NIE
zmienia — sugestie percentylowe jawnie oznaczone "nie do automatycznego
zastosowania"), porównanie reżimów (Mann-Whitney + Kołmogorow-Smirnow
jako druga, niezależna metoda), stabilność klasyfikacji faz i spójność
między niezależnymi przebiegami/ziarnami (współczynnik zmienności).
Zwendorowany jako pierwszy klient do TIMDR-Quantum-Lattice (domenowy
case-study, poza zakresem tego skilla) — tam ujawnił nowe ustalenie:
podczas aktywnego kolapsu kanały Λ i τ są silnie skorelowane (Spearman
~0.9-0.96), zinterpretowane jako wspólny monotoniczny trend, NIE
duplikat liczenia (kanał J pozostaje niezależny nawet wtedy).

**Rozszerzenie 2026-09-12: GS-Matrix, Θ_bif, phase diagram** — patrz
punkt 16 dla pełnego opisu; skrótowo: poprawiony warunek zachowawczości
macierzy sprzężenia (antysymetryczna, nie hermitowska), pełny operator
bifurkacji z dwoma kanałami (tłumiący/kondensujący) i dwoma zbadanymi
reżimami pracy (miękki/twardy), 4-strefowa mapa parametrów, i realny,
znaleziony-i-naprawiony błąd przepełnienia w samym operatorze.

**Rozszerzenie 2026-09-15: zakres mostu Fouriera + sprzężenie
helikalne K↔Θ_bif** — patrz punkty 17-18 dla pełnego opisu; skrótowo:
most Fouriera przetestowany na 3 realnych domenach i zawężony do
pojedynczego, idealnego modu; nowa, jawnie eksploracyjna konstrukcja
łącząca GS-Matrix z Θ_bif, z częściowo działającym (binarnym) i
częściowo nie (ilościowym) estymatorem.

**Rozszerzenie 2026-09-15/16: most M/S↔topologia/K** — patrz punkt 19
dla pełnego opisu; skrótowo: pięć metryk skalarnych odrzuconych na
syntetyce (1/50), ale silny (łożyska 82%) i częściowo scharakteryzowany
(korelacja+homogeniczność+odróżnienie od kurtozy/entropii widmowej)
sygnał na realnych danych, niespójny/słaby na dwóch innych domenach
(sejsmika, BTC).

## 5. Cztery gałęzie TIMDR (i rozdzielenie znaczeń)

- **M/S** — sygnały czasowe (anomalia/defekt/rezonans M/skręt sygnałowy), `Axioms_S_TIMDR_Signal.md`, 13 aksjomatów.
- **K** — rezonans modalny (częstotliwość/faza między modalnościami), `Axioms_K_TIMDR.md`, 10 aksjomatów — zupełnie inny obiekt niż rezonans M.
- **G** — geometria (skręt powierzchniowy, operator kształtu/Weingarten, krzywizny obwiedni, G-Rezonans), `Axioms_G_TIMDR_Geometry.md`, 10 aksjomatów.
- **META-DYNAMICS** (dodana formalnie 2026-09-10, punkt 14) — agregatowy wektor 4D `MetaState(Λ,τ,ρ,J)` + operator ewolucji `M=dS/dt`, 0 aksjomatów (jawna luka), ale działający kod w 6 domenach + 1 uniwersalny walidator (punkt 4).

Plus starszy, nieformalny szkic kierunkowy `R(t)=mean(sign(Sᵢ'(t)))` w
głównym README (poprzednik M/S, nie osobna gałąź), TRM (`TRM_biology.md`,
punkt 13) jako PIĄTY, narracyjny/nieformalny użytkownik liter Λ/τ/ρ,
spoza tej czwórki formalnych gałęzi — TRM NIE jest tożsame z gałęzią
META-DYNAMICS mimo współdzielonych liter (patrz punkt 13, kolizja τ
NIEROZSTRZYGNIĘTA; kolizja Λ/ρ w ogóle niezbadana), oraz GS-Matrix/
SG-Coupling/Θ_bif (punkt 16) jako toy-model demonstrujący mechanikę K
antysymetryczne-vs-symetryczne i pełny operator bifurkacji — świadomie
NIE aksjomatyzowany, żyje wyłącznie jako kod+testy w
`TIMDR-Math-Formalism/tests/`, nie jest szóstą gałęzią. Sprzężenie
helikalne K↔Θ_bif (punkt 18, 2026-09-15) jest nową konstrukcją
ROZSZERZAJĄCĄ ten sam toy-model — też świadomie nieaksjomatyzowana, też
nie jest szóstą gałęzią, i pozostaje tam mimo częściowo pozytywnego
wyniku (w odróżnieniu od mostu Fouriera, który miał gotową matematykę
przed jakąkolwiek sesją). Most M/S↔topologia/K (punkt 19) tym bardziej
— pięć konkurencyjnych, świadomie nieaksjomatyzowanych konstrukcji, nie
szósta gałąź, mimo silnego wyniku na łożyskach.
Żadna gałąź nie jest rozszerzeniem innej — każda ma własny obiekt/operator,
mimo współdzielonych nazw.

## 6. Domknięcie gałęzi geometrycznej (G8-G9)

G8 formalizuje T_S jako właściwy operator (dziedzina/ciągłość/Lipschitz).
G9 podaje jawne F: dyskretny operator Weingartena,
`T_S(p) ≈ ‖Δp‖·‖S_p(Δ̂p)‖ + O(‖Δp‖²)`. Implementacja:
`TIMDR-Geometry-Formalism/timdr_geometry/weingarten.py` (4 testy stabilności
na płaszczyźnie/sferze/walcu/rafinacji siatki) — napisane i sprawdzone
ręcznie, ale nieuruchomione w sesji, w której powstały (brak sandboxa).

## 7. Chronoproces Ξ=(T,x,Γ,φ)

Most między trzema gałęziami BEZ ich mieszania — jeden nośnik `T`, trzy
niezależne rzuty: M/S czyta `x:T→ℝᵈ` (tempo/drift), G czyta
`Γ:T×I→ℝ³` (rodzina trajektorii → powierzchnia), K czyta `φ:T→(f,φ,A)`
(synchronizacja faz, afiniczna nie Kuramoto). Most Fouriera M/S↔K
(`Δt·Δf=1/(4π)` dla impulsu gaussowskiego) to JEDYNY dopuszczony
wyjątek od zasady zero-identyfikacji między gałęziami — bo ma za sobą
konkretną, znaną transformatę matematyczną (FFT), nie nową hipotezę.
**Zakres tego mostu jawnie ograniczony 2026-09-15 (punkt 17)**: ważny
tylko dla pojedynczego, idealnego modu gaussowskiego — na realnych
zdarzeniach M/S (sejsmika, łożyska, finanse) `Δt·Δf` NIE ma wąskiej,
stabilnej struktury.

## 8. Aksjomat G10 (parametr obwiedni P/Q)

Krzywizna krzywej (nie powierzchni) na obwiedni zaokrąglonego trójkąta:
`P=L0/L` (część prosta), `Q=Lk/L=1-P` (część łukowa), `Lk(R)=2πR`
dokładnie. `P(R)` ściśle monotoniczne → odwracalne (oba kierunki
krzywa↔(P,Q)). Implementacja + 65/65 testów: `timdr_geometry/envelope.py`.
Błąd znaleziony i naprawiony: pierwsza wersja twierdziła `Q_max<1` poza
trójkątem równobocznym — w rzeczywistości `R_max(Δ)=r_in(Δ)` dokładnie
DLA KAŻDEGO trójkąta (tożsamość styczna-do-okręgu-wpisanego), `Q→1`
zawsze osiągalne. (Uwaga: to jest OBWIEDNIA TRÓJKĄTA z Geometry-Formalism
— nie mylić z parametrem obwiedni `Q(R)=1-L0/L(R)` z toy-modelu
SG-Coupling w punkcie 16, który jest innym, niepowiązanym użyciem
litery Q i wzoru o podobnym kształcie w zupełnie innym repo/kontekście.)

## 9. Dokument spekulacyjny (grawitacja)

Propozycja tensoru `Ω=(P,Q)⊗(k_MS,k_G,k_K)` + `g~M·Ω` łamie zasadę
nieredukowalności gałęzi (łączy wszystkie 3 naraz, bez odpowiednika
mostu Fouriera) → osobny, jawnie oznaczony `TIMDR_Gravity_Speculative.md`,
NIE cytowany przez żaden plik `Axioms_*`. Zawiera 4 braki do przejścia
od analogii do teorii i uczciwe zastrzeżenie "dlaczego to tylko analogia".

## 10. Domknięcie pętli samokorekty (Axioms_S, Axioms_K)

Jednorazowa walidacja w dokumencie ≠ reużywalna kalibracja w kodzie.
`TIMDR-Math-Formalism/calibration.py::calibrate_resonance_K()` — sprawdza
moc PRZED rekomendacją, zwraca `insufficient_power` zamiast zmyślać.
`TIMDR-Modal-Formalism/phase_sync.py` dostał pierwszy w gałęzi K kontakt
z realnymi danymi (sejsmika Ridgecrest 2019, CI.CLC/CI.RIO).

## 11. Trójwęzeł helikalny i Aksjomat G5 (G-Rezonans)

Piąte znaczenie skrętu: torsja Freneta-Serreta trójwęzła (odróżniona od
skrętu topologicznego τ mimo wspólnego symbolu). Czwarte znaczenie
rezonansu: pierścień N≥3 tłumionych oscylatorów sprzężonych węzłami
krzywej 3D, warunek stabilności jako predykat algebraiczny (dodatnia
określoność M/K/Γ ⟹ brak bieguna na osi rzeczywistej —
`core/geometric_resonance_operator.py::is_stable()`). Uogólniony z
prototypu N=3 (tylko 1 z 6 funkcji zakładała N=3) i zweryfikowany
niezależnie teorią macierzy cyrkulantowych (N=3,4,5,6,8). Wsteczna
zgodność z prototypem: bit-w-bit (`np.array_equal`). 23 testy.

Po drodze: uczciwy wynik negatywny (próba na realnych danych pogodowych
zawiodła — luka czasowa, szum, maskowanie progu) i
znaleziony-i-naprawiony błąd (rezonans jako JEDYNY selektor pierwiastka
dawał ~46% trafień zamiast ~100% przy użyciu spójności-τ jako selektora
— rezonans to diagnostyka na już wybranym kandydacie, nie selektor).

Status: numerycznie przetestowany (mocniejszy niż G8-G10), ale zero
walidacji na realnej, zmierzonej krzywej 3D — "ogólność" = "kod nie
zakłada N=3", NIE "sprawdzone na innej realnej figurze".

## 12. Domknięcie audytu `core/operators.py`

`tests/test_operators_wiring.py` (audyt 2026-08-31) był kompletną
specyfikacją 8 brakujących funkcji/stałych — dokończone wg specyfikacji
zakodowanej w testach (próg ΔS bez składnika średniej, dynamiczny sufit
rezonansu jako mnożnik teoretycznego maksimum zamiast martwej stałej
`1e9`, ~2 000 000× za dużej). W zakresie skilla (własna warstwa
operatorów GIA-TIMDR). Pełny zestaw testów repo: 118/118.

## 13. TRM (Model Topologicznej Redukcji) — nowy, częściowo sformalizowany wątek, prawo redukcji ODRZUCONE dwukrotnie

`TRM_biology.md` (już istniejący w repo, status własny: "model
strukturalny"/"hipoteza, nie klasyczna biologia", NIEfalsyfikowany
empirycznie) używa liter Λ/τ/ρ narracyjnie (τ = "poziom złożoności/
energia utrzymania", operacyjnie mass×metabolizm w przykładzie K-Pg) —
odrębny od M/S/G/K, użytkownik tych symboli w ekosystemie. **Od
2026-09-10 (punkt 14) formalna gałąź META-DYNAMICS TEŻ używa Λ/τ/ρ/J —
DWA różne, niezależne zestawy definicji pod tymi samymi czterema
literami. τ TRM vs τ META-DYNAMICS: różne domeny (skalarny proces
redukcji vs tempo zmiany defektu w agregacie), związek niezbadany, NIE
zakładaj żadnej odpowiedzi. Λ TRM vs Λ META-DYNAMICS i ρ TRM vs ρ
META-DYNAMICS: kolizja w ogóle jeszcze nie zbadana, nawet nie
NIEROZSTRZYGNIĘTA formalnie — po prostu nikt jeszcze nie zadał tego
pytania.**
2026-09-10: użytkownik dostarczył 9 równań formalizujących wcześniej
czysto jakościowe twierdzenia TRM_biology.md ("wysokie τ → niestabilne"),
rdzeń: prawo redukcji `R(τ)=k·τⁿ`, `dI/dt=-R(τ)`, autonomicznie
(podstawiając τ=aI) `dI/dt=-C·Iⁿ`, z rozwiązaniem analitycznym dla n≠1
(zweryfikowanym algebraicznie — poprawne), plus dyskretna drabina
`τᵢ₊₁=λτᵢ→φ` i stan końcowy φ opisany jako "czysta rotacja".

**Kolizja terminologiczna, NIEROZSTRZYGNIĘTA na żądanie użytkownika**:
τ_krit w równaniach TRM i "skręt τ rośnie aż do wartości krytycznej"
w `Operators_N_TIMDR.md` (torus→Möbius→tetroida) używają uderzająco
podobnego języka, ale TRM's τ jest ciągłą wielkością skalarną z własną
dynamiką (fala, ODE), nie geometryczną deformacją powierzchni — czy to
rozwinięcie tego samego obiektu czy inny obiekt pod tym samym symbolem,
NIE ustalone. **Nie zakładaj żadnej z tych odpowiedzi bez ponownego
zapytania — to jest jawnie otwarte, nie domyślnie "to samo".**

**Test empiryczny rdzenia matematycznego (nie całego TRM_biology.md)**:
zamiast biologii/paleontologii (dane K-Pg niepobrane w tej sesji), rdzeń
`R=k·τⁿ` przetestowany na DWÓCH niezależnych, realnych/quasi-realnych
krzywych zaniku, metodą porównania AIC (model A: rozpad wykładniczy
n=1 na sztywno, 3 parametry; model B: TRM n-tego rzędu, n dopasowywane,
4 parametry; próg decyzyjny ΔAIC=2 ustalony przed dopasowaniem):

1. **TIMDR-Quantum-Lattice** (Λ(t) = circular_dispersion podczas
   kolapsu siatki, 10 ziaren uśrednione): n zbiegło do ~1.01 (praktycznie
   sam wykładniczy), ΔAIC=+7.96 na niekorzyść TRM — ODRZUCONY.
2. **NASA battery B0047** (realny fade pojemności Li-ion, 69/73 cykli,
   `TIMDR-EV-Predict/data/real_battery/`): pierwsza próba nonlinear
   curve_fit utknęła w zdegenerowanym optimum (błąd METODY optymalizacji,
   nie modelu) — naprawione siatką po n + dokładnym rozwiązaniem
   liniowym wewnątrz (transformacja w=(I-Ifloor)^(1-n) jest liniowa w t).
   Po naprawie: n=2.8 (zbieżne, nie zdegenerowane), ΔAIC=+38.02 na
   niekorzyść TRM względem prostego rozpadu wykładniczego — ODRZUCONY,
   jeszcze wyraźniej niż w (1).

**Uczciwy wniosek**: 0/2 na razie — dodatkowy wykładnik n nie zarabia
na swój koszt (dodatkowy parametr) na żadnej z dwóch niezależnych,
prawdziwych krzywych zaniku przetestowanych dotąd. To NIE obala TRM_biology.md
w całości (biologia/paleontologia pozostaje nieprzetestowana), tylko
konkretnie: rdzeń matematyczny "R=k·τⁿ jako coś więcej niż zwykły
rozpad" — na razie brak dowodu. Zgodnie z protokołem (punkt 3): wynik
negatywny zaraportowany wprost, bez naginania interpretacji.

## 14. Rodziny sygnałów — formalizacja gałęzi META-DYNAMICS (Λ-τ-ρ-J)

2026-09-10, na propozycję użytkownika: przestać traktować Λ/τ/ρ/J jako
"po prostu cztery metryki" i formalnie uznać je za CZWARTĄ gałąź TIMDR
(obok M/S, G, K) — rodzinę operatorów agregatowych, jeden kształt
obiektu matematyczny (`MetaState∈ℝ⁴` + operator ewolucji `M=dS/dt`)
instancjonowany w sześciu niezależnych domenach, dokładnie tym samym
wzorcem, w jakim `TIMDR-Geometry-Formalism` potraktował krzywiznę jako
rodzinę (Weingarten/powierzchnia, obwiednia P/Q, torsja trójwęzła,
Chronoproces/trajektoria, K-modalna) zamiast jednej wielkości. To NIE
był nowy pomysł matematyczny — kod istniał od dawna (sześć
`meta_adapter.py`, `meta_validator.py`), tylko nigdzie nie był formalnie
opisany obok M/S/G/K w `TIMDR_Branch_Specification.md`.

**Co dokładnie zrobiono:**
1. Dodano pełną sekcję "Gałąź META-DYNAMICS" do
   `TIMDR_Branch_Specification.md` (obiekty, operatory, status
   empiryczny, pliki źródłowe, "czym NIE jest") + kolumnę w tabeli
   porównawczej — wzorem M/S/G/K.
2. Rozszerzono `TIMDR_Twists.md` o τ TRM (6. znaczenie skrętu, wcześniej
   brakujące mimo że skill już to sygnalizował) i notatkę o τ
   META-DYNAMICS (poza zakresem słowa "skręt", ale kolizyjny symbol).
3. Rozszerzono `GLOSSARY_EN_PL.md` o pełną sekcję "Λ-τ-ρ-J /
   META-DYNAMICS" (definicje Λ/τ/ρ/J, dwujęzyczne, z jawnym
   rozgraniczeniem od wszystkich innych znaczeń tych symboli).
4. Zaktualizowano główny `README.md` GIA-TIMDR (nagłówek "Cztery
   gałęzie", nowa sekcja 4, wiersz w tabeli kanonicznej).

**Jawna, uzasadniona decyzja klasyfikacyjna (odpowiedź na część
propozycji użytkownika, NIE przyjęta bez zmian):** użytkownik
zaproponował, żeby `TIMDR-Quantum-Lattice` "stało się pełnoprawną
gałęzią" zamiast "dziwnym dodatkiem". Odrzucone jako osobna gałąź —
Quantum-Lattice (i pozostałe 5 domen) dzielą JEDEN kształt obiektu
matematycznego (`MetaState`+`MetaOperatorM`) i jeden protokół walidacji
(`meta_validator.py`); różnią się TYLKO mapowaniem fizycznych wielkości
domeny na Λ/τ/ρ/J — to dokładnie definicja INSTANCJI gałęzi, nie nowej
gałęzi (analogicznie do tego, jak Krakow_Centrum jest instancją M/S, nie
osobną gałęzią). Nowa gałąź byłaby uzasadniona tylko przy INNYM
kształcie obiektu matematycznego, nie przy nowej domenie tego samego
kształtu. Osobno odnotowany (NIE zaklasyfikowany, otwarty punkt):
zespolony parametr porządku `Z(t)=mean(exp(i·faza))` (Kuramoto),
używany zarówno w Quantum-Lattice jak i w `Synoptyk-v3` (spójność
kierunku wiatru) — pokrewny duchem gałęzi K, ale formalnie ani część
META-DYNAMICS, ani jeszcze własny aksjomat K.

**Uczciwa luka pozostawiona otwarta:** gałąź META-DYNAMICS ma ZERO
spisanych aksjomatów (w odróżnieniu od M/S=13, G=10, K=10) — działający
kod w 6 domenach plus 1 uniwersalny walidator, ale brak formalnego
zestawu aksjomatów analogicznego do `Axioms_S/G/K_TIMDR.md`. Nazwane
wprost jako luka, nie ukryte — wzorem tego, jak Aksjomat G7 nazwał brak
implementacji numerycznej G, zanim `TIMDR-Geometry-Formalism` ją
dostarczył.

**Runda 2, ten sam dzień: rodzina Λ (i częściowo τ) rozszerzona na G i
K.** Użytkownik zapytał "a gdyby" Λ/τ/ρ/J było rodziną CZTERECH PYTAŃ
(dyspersja/tempo/gęstość/sprzężenie) realizowaną OSOBNO w każdej
gałęzi — audyt przed obietnicą pokazał, że z 16 komórek (4×4) tylko
~6-7 miało już realny kod, reszta była czystą analogią słowną (m.in.
sprawdzone grepem: `Axioms_K_TIMDR.md` i `Axioms_G_TIMDR_Geometry.md`
nie miały ŻADNEGO operatora dyspersji). Wybrano zbudowanie dwóch
brakujących: `Λ_G` (dyspersja krzywizny średniej,
`timdr_geometry/weingarten.py::mean_curvature_dispersion`, 6/6 testów)
i `Λ_K`/`τ_K` (dyspersja fazowa i jej tempo,
`timdr_modal/phase_sync.py::modal_phase_dispersion`/`modal_phase_tempo`,
8/8 testów, w tym kontrola ANALITYCZNA τ_K≡0 dla równych częstości).
Ważna różnica: próba dla G ODRZUCIŁA pierwszy pomysł (parametr porządku
kierunków głównych krzywizny) bo kierunki żyją w różnych lokalnych
bazach stycznych (wymagałoby transportu równoległego) — zamiast tego
użyto skalara H(p). Dla K formuła Λ_K jest DOSŁOWNIE tym samym obiektem
co `circular_dispersion`, bo modalności dzielą jeden globalny okrąg
fazowy — nie trzeba było niczego odrzucać. Pełne szczegóły:
`TIMDR_Branch_Specification.md`, sekcje "Gałąź G"/"Gałąź K"/"Runda 2".
Pozostałe komórki (ρ/J w G/K, cała kolumna TRM) jawnie NIEZBUDOWANE.

## 15. Meta-zasady TIMDR (wnioski ogólne, wielokrotnego użytku)

- Audytuj istniejące znaczenia słowa PRZED napisaniem nowych aksjomatów pod tą samą nazwą.
- Protokół testowania musi być kodem z API, nie tylko prozą.
- Wysokie p jest wartościowym wynikiem negatywnym TYLKO gdy test miał moc (sprawdź, że kontrolne grupy zawierały kwalifikujące się zdarzenia).
- Luka formalna nazwana w dokumencie = poprawny stan, nie błąd — domykaj w dwóch krokach (analityczny → numeryczny), jawnie oznaczonych.
- Podstaw KONKRETNY przykład liczbowy pod każde ogólne twierdzenie matematyczne przed publikacją — ręczne "sprawdzone krok po kroku" nie wystarcza.
- Gdy propozycja łamie zasadę frameworku (np. nieredukowalność gałęzi), nazwij konflikt i zapytaj — nie milcz, nie zgadzaj się automatycznie.
- "Poprawne na syntetykach" i "użyteczne na realnych danych" to DWA różne twierdzenia — rozdzielaj zawsze, nawet gdy pierwsze wypada dobrze.
- Warunek stabilności formalizuj jako predykat algebraiczny, gdy matematyka pozwala — silniejszy i bardziej przenośny niż próg empiryczny.
- Przed uogólnieniem prototypu sprawdź, ile kodu faktycznie zakładało szczególny przypadek — i zweryfikuj ogólność NIEZALEŻNĄ teorią, nie kolejnymi testami tego samego typu.
- Selektor ("który kandydat prawdziwy") ≠ diagnostyka ("czy wybrany kandydat podejrzany") — pomylenie ich wychodzi dopiero na teście z wyrocznią.
- Jednorazowa walidacja w dokumencie ≠ reużywalna kalibracja w kodzie — dyscyplina mocy/uczciwości musi przetrwać to przejście.
- Dodatkowy parametr funkcyjny (np. wykładnik potęgowy) musi wygrać z prostszym baseline'em przez kryterium informacyjne (AIC/BIC), ustalone PRZED dopasowaniem — "da się dopasować" nie znaczy "lepszy model" (punkt 13, 0/2 na razie).
- Gdy optymalizacja nieliniowa daje zdegenerowany wynik (utknięcie na brzegu bounds), podejrzewaj METODĘ (zły init/parametryzacja) przed odrzuceniem modelu — ale nie zmieniaj progu decyzyjnego po zobaczeniu poprawionego wyniku (punkt 13, battery test).
- Gdy dwie diagnostyki na tych samych danych dają różne odpowiedzi (np. duża spójność kierunkowa I duża wirowość jednocześnie), to dowód że mierzą naprawdę różne rzeczy, nie że jedna jest zepsuta — sprawdź to explicite kontrolą przed zaufaniem nowej metryce.
- "Rodzina operatorów w jednej domenie" (np. sześć meta_adapter.py) ≠ "sześć gałęzi" — nowa gałąź wymaga INNEGO kształtu obiektu matematycznego, nie tylko nowej domeny tego samego kształtu; sprawdzaj to rozróżnienie explicite, zanim zaakceptujesz propozycję "X powinno być osobną gałęzią" (punkt 14).
- Gdy kod działa od dawna w wielu domenach, ale nigdy nie został formalnie zestawiony obok istniejących sformalizowanych struktur (tu: Λ-τ-ρ-J vs M/S/G/K), samo zestawienie w jednym dokumencie-indeksie jest realną, wartościową pracą — nawet bez nowej matematyki — bo ujawnia kolizje symboli (τ), których nikt wcześniej nie zauważył, bo nie stały obok siebie (punkt 14).
- Przed budową operatora "analogicznego" w nowej domenie (np. dyspersja krzywizny wzorem dyspersji fazowej), sprawdź czy domena ma WSPÓLNY globalny układ odniesienia dla wielkości, którą chcesz uśredniać — jeśli nie (różne lokalne bazy styczne per punkt na siatce 3D), nie wymuszaj tej samej formuły; poszukaj innej, koordynatowo-niezależnej wielkości zamiast robić błąd "podobne słowo, inny obiekt" (punkt 14, runda 2 — Λ_G vs Λ_K).
- Warunek "macierz X jest zachowawcza/stabilna" dla `dV/dt=KV` to `K` ANTYSYMETRYCZNE (`K^T=-K`, generuje obrót/normę stałą), NIE hermitowskie/symetryczne (`K=K†` daje rzeczywiste wartości własne → wzrost/zanik wykładniczy, czyli dokładna PRZECIWNOŚĆ zachowawczości) — łatwa pomyłka, bo "hermitowskie" brzmi jak słowo-klucz do zachowawczości z mechaniki kwantowej, gdzie kontekst (ewolucja unitarna `e^{-iHt}`, nie rzeczywiste `e^{Kt}`) jest inny; zawsze weryfikuj empirycznie kontrolą +/- (antysymetryczne trzyma normę, symetryczne rośnie/zanika), nie tylko nazwą własności macierzy (punkt 16).
- Gdy próg/kalibracja jest za czuła na naturalną amplitudę tła (fałszywe wyzwolenia przed prawdziwym zdarzeniem), NIE zgaduj nowej "lepszej" stałej — kalibruj próg z rozkładu SAMEGO TŁA (symulacja/dane bez wstrzykniętego efektu) z jawnym marginesem, i sprawdź to jako osobny test regresyjny, nie tylko przez konstrukcję funkcji (punkt 16).
- Deklarowany sufit/ograniczenie wzoru operatora (np. "|wyjście|≤MAX zawsze") musi być zweryfikowane przy wejściach ze SKALI, jaką operator faktycznie zobaczy w pełnym, sprzężonym systemie — nie tylko przy małych, ręcznie dobranych wartościach testowych. Formuła `współczynnik * S` (surowa wartość) NIE jest ograniczona przez `MAX`, nawet jeśli współczynnik sam jest ograniczony — jeśli intencją jest "kanał nasyca się do stałej skali niezależnie od wielkości wejścia", użyj znormalizowanego KIERUNKU (`sign(S)` albo `S/|S|`), nie surowej wartości. Ten dokładny błąd (`R_phase[S]=-S` zamiast `-sign(S)`) dawał niestabilną pętlę dodatniego sprzężenia i przepełnienie (inf) w realnym, sprzężonym scenariuszu (α=2.0, silna anomalia), mimo że 13 wcześniejszych testów jednostkowych (wszystkie na S rzędu 0.5-2.0) przechodziło bez zarzutu — jednostkowe testy na małej, wygodnej skali NIE gwarantują poprawności przy skali, jaką zobaczy pełny system (punkt 16).
- Systematyczne przeszukanie siatki parametrów ("phase diagram"/mapa reżimów) jest skutecznym sposobem na znalezienie błędów, których nie złapią pojedyncze, ręcznie dobrane testy jednostkowe — bo eksploruje kombinacje dalekie od tego, co człowiek pomyślałby przetestować z ręki (punkt 16).
- Pozornie jedna "granica między dwoma strefami" może kryć DWA różne mechanizmy o różnych zmiennych sterujących (tu: "próg nieosiągalny" zależy TYLKO od parametru systemu, a "próg nieosiągnięty" zależy też od siły konkretnego wejścia) — sprawdź explicite, czy obie strefy są funkcją tych samych zmiennych, zanim potraktujesz je jako jedną oś/jedną granicę (punkt 16, strefa martwa vs cicha).
- **Zanim zaczniesz szukać danego zjawiska w realnych danych z wielu domen, sprawdź, czy jego niezmienniczość skalowa (np. Δt·Δf niezależne od jednostki czasu `dt`) rzeczywiście zachodzi w Twojej implementacji — zweryfikuj to WPROST (to samo okno, kilka różnych `dt`, sprawdzić identyczny wynik), zamiast zakładać z matematyki wysokiego poziomu; jeśli się zgadza, różnice między domenami NIE są artefaktem jednostek, tylko realną treścią (punkt 17).**
- **"Poprawne na jednej, wąskiej domenie" NIE uogólnia się automatycznie — test na WIELU niezależnie wybranych realnych domenach (nie tylko tej, która akurat była pod ręką) jest tym, co odróżnia "most matematyczny ma treść" od "most matematyczny ma treść na TEJ jednej próbce danych"; wybieraj domeny PRZED zobaczeniem ich wyników, nie po (punkt 17, 3 domeny: sejsmika/łożyska/finanse).**
- **Filtr kształtu (odsiewanie kandydatów niepasujących do założonego wzorca) może ZAWĘZIĆ rozrzut wyniku bez go ELIMINOWAĆ — to wynik POŚREDNI, nie "test przeszedł po poprawce"; zgłoś oba stany (przed/po filtrze) i nie pozwól, żeby częściowa poprawa została odczytana jako pełny sukces (punkt 17).**
- **Gdy dokument formalny (tu: nowa konstrukcja K↔Θ_bif) łączy dwa wcześniej niepołączone obiekty kodu, sprawdź NAJPIERW, czy istniejący kod jawnie i świadomie zostawił je rozłączone (grep za komentarzem uzasadniającym decyzję) — jeśli tak, nowe połączenie jest NOWĄ KONSTRUKCJĄ wymagającą własnego banera "to nie jest wyprowadzenie", nie odkryciem ukrytej struktury (punkt 18).**
- **Estymator parametrów układu dynamicznego z JEDNEJ obserwacji skalarnej przez lokalne różnicowanie (lub DMD/log-propagator) jest z natury wzmacniaczem szumu — jeśli reżim ma DWIE różne rzeczywiste stałe czasowe, trajektoria embeddingu opóźniającego kolabuje asymptotycznie na 1D (dominujący mod przytłacza drugi), więc macierz regresji jest niemal osobliwa NIEZALEŻNIE od poziomu szumu (sprawdzaj `cond()` regresji jako wskaźnik, nie tylko końcowy wynik) — dopasowanie ZNANEGO KSZTAŁTU rozwiązania do CAŁEGO okna (nieliniowe najmniejsze kwadraty, nie różnicowanie próbka-po-próbce) jest dużo odporniejsze, bo używa globalnej struktury zamiast lokalnych różnic (punkt 18).**
- **Formalny test z większą próbą (N=30) i losowanymi warunkami początkowymi/nuisance-parametrami może ujawnić, że wstępna eksploracja z małą próbą (6-10 powtórzeń) i JEDNYM stałym warunkiem początkowym była częściowo artefaktem tego wygodnego przypadku — nie zakładaj, że mała, obiecująca eksploracja uogólnia się bez formalnego, większego powtórzenia z losowanymi nuisance-parametrami PRZED zapisaniem wyniku jako "działa" (punkt 18).**
- **Wynik estymatora/testu może być ASYMETRYCZNY między dwoma powiązanymi wielkościami (tu: `Im(λ)` solidnie odzyskiwane, `Re(λ)` nie) — nie uśredniaj/zaokrąglaj tego do jednego zdania "działa"/"nie działa"; zawęź zakres stosowalności do TEJ CZĘŚCI, która faktycznie przeszła test (tu: binarna klasyfikacja obecności rotacji, nie wartość liczbowa) — wzorem tego, jak most Fouriera został zawężony do pojedynczego modu zamiast odrzucony w całości (punkt 18).**
- **Region pozytywny testu (kontrola pozytywna vs tło) musi być JEDNORODNY w czasie/strukturze — region mieszający różne stany (np. impuls + zanikanie, albo losowo domieszkowany innym reżimem) systematycznie osłabia/zaburza rozmiar efektu; to jest generyczna własność testu Manna-Whitneya (rozcieńczenie próby), nie odkrycie specyficzne dla geometrii — traktuj jako REGUŁĘ PROTOKOŁU (obok reguł punktu 3), zweryfikowaną w kontrolowany sposób (ta sama domena, sztucznie regulowany stopień zanieczyszczenia) zanim uznasz ją za przyczynową, nie tylko skorelowaną z dwoma przykładami (punkt 19).**
- **Dwie metryki o PODOBNEJ mocy klasyfikacyjnej (podobny odsetek `passed` w tej samej siatce testów) NIE muszą mierzyć tego samego zjawiska — sprawdź korelację (Spearmana) WPROST na tych samych próbkach przed uznaniem jednej za "przemalowaną" wersję drugiej lub za dowód, że nowa metryka nie wnosi nic ponad znaną klasyczną cechę; podobna moc + brak korelacji = dwa niezależne źródła sygnału o tym samym zjawisku, nie redundancja (punkt 19).**
- **Nazwa/promocja nowego obiektu matematycznego lub aksjomatu na podstawie n=2 przykładów (dwie domeny, jedna zadziałała, jedna gorzej) jest przedwczesna — zanim sformalizujesz, odizoluj podejrzewaną zmienną przyczynową W JEDNEJ domenie (kontrolowany eksperyment), i sprawdź hipotezę na TRZECIEJ, NIEZALEŻNIE wybranej domenie zamiast poprzestać na dwóch (punkt 19, BTC obaliło nadmierne uogólnienie "jednorodność wystarczy" z n=2).**

## 16. GS-Matrix poprawiony i pełny operator bifurkacji Θ_bif z phase diagram (2026-09-12)

Toy-model `SG-Coupling`/`GS-Matrix` w `TIMDR-Math-Formalism` (kod+testy
wyłącznie w `tests/`, świadomie NIE aksjomatyzowany, NIE jest szóstą
gałęzią — patrz punkt 5) demonstrujący dynamikę `dV/dt=KV` i prosty
model progowej bifurkacji sygnału.

**Poprawka GS-Matrix (błąd matematyczny w propozycji użytkownika):**
propozycja twierdziła, że `K=K†` (hermitowskie/symetryczne dla macierzy
rzeczywistej) jest warunkiem "zachowawczości" (`dV/dt=KV` trzyma normę
`V(t)`) — odwrotnie: rzeczywiste symetryczne `K` ma rzeczywiste wartości
własne, więc daje wykładniczy wzrost/zanik (dokładna PRZECIWNOŚĆ
zachowawczości); to `K` ANTYSYMETRYCZNE (`K^T=-K`) generuje obrót
(macierz wykładnicza jest ortogonalna) i trzyma normę. Poprawione w
`timdr_formalism/gs_matrix.py` (`decompose_K`/`is_conservative`/
`simulate_linear_system`, ręcznie napisany RK4 bez scipy), 15/15 testów
z kontrolą pozytywną (czysto antysymetryczne K, 4 siły sprzężenia) i
negatywną (symetryczne K, wzrost i zanik).

**Kalibracja Q_crit** (SG-Coupling, próg cutoff): hardkodowane `0.35`
było za czułe na naturalną amplitudę tła (4 fałszywe wyzwolenia przed
oknem anomalii) — naprawione `calibrate_q_crit()`: próg = margines
(1.3x) nad maksimum Q z symulacji SAMEGO tła (bez wstrzykniętej
anomalii), nie zgadnięta nowa stała.

**Pełny operator bifurkacji Θ_bif** (`timdr_formalism/theta_bifurcation.py`):
dwa kanały — `S_down` (tłumiący/pamięć starego trendu,
`beta*S*exp(-lambda_down*dt)`) i `S_up` (kondensujący/nowy trend,
`(1-beta)*R_phase[S]*S_up_max*tanh(lambda_up*dt)`). Dwa jawnie
udokumentowane odstępstwa od niedoprecyzowanej propozycji: (1) wzór na
`beta(t)=clip(1-(Q-Q_crit)/(1-Q_crit),0,1)` (nie był podany), (2)
`tanh`-nasycenie zamiast czystego `exp(+lambda*dt)`, który rósłby bez
ograniczeń. Znaleziona (nie założona) właściwość modelu: nawet lekkie
przekroczenie progu zostawia trwałe, niezerowe plateau (nie zanika do
zera) — kompromis poprawki nasycenia, udokumentowany wprost.

**Dwa reżimy pracy, oba empirycznie zweryfikowane:** miękki (parametry
domyślne, beta_min~0.98 — kanał kondensujący ledwo się aktywuje) i
twardy (alpha i anomalia podniesione o rząd(y) wielkości, beta_min~0.29
— kondensacja dominuje, udział |S_up| rośnie z <0.5% do >15-24%).
Naiwne podniesienie JEDNEJ dźwigni (samo alpha LUB sama anomalia) NIE
wystarczało — operator ma wbudowaną pętlę ujemnego sprzężenia
ograniczającą samą siebie (Q>Q_crit natychmiast tłumi S, obniżając Q w
następnym kroku), trzeba było podnieść obie dźwignie naraz i o rząd(y)
wielkości.

**Phase diagram (4 strefy, nie 3):** mapa (alpha, siła anomalii) na
martwą/cichą/miękką/twardą. Martwa: kalibrowany `Q_crit(alpha)>1.0` —
matematycznie nieosiągalny próg (`Q(R)<1` zawsze), cutoff nigdy się nie
wyzwoli dla tego alpha NIEZALEŻNIE od anomalii — granica zależy
WYŁĄCZNIE od alpha (bisekcja, próg ok. alpha 13-14 dla domyślnych
parametrów repo). Cicha: próg osiągalny, ale DANA anomalia za słaba.
Miękka/twarda: granica na `beta_min=0.5` (matematyczny punkt równowagi
wag kanałów, nie liczba dobrana pod wynik).

**Znaleziony i naprawiony realny błąd przepełnienia:** przy
przeszukiwaniu siatki, `alpha=2.0, anomaly_bump=130.0` dawało
przepełnienie (inf), nie "strefę twardą". Przyczyna: `R_phase[S]=-S`
(surowa wartość sygnału) zamiast znormalizowanego kierunku `-sign(S)` —
deklarowany sufit `S_up_max` NIE był faktycznym ograniczeniem, gdy `S`
samo było już duże (niestabilna pętla dodatniego sprzężenia, ~10x na
krok, skończony wybuch do inf w kilkadziesiąt kroków) — dokładnie ten
sam objaw, któremu wcześniejsza poprawka `tanh` miała zapobiegać, tylko
przez inny mechanizm. Naprawione: `R_phase[S]=-sign(S)` (długość ≤1) —
sufit jest teraz prawdziwy niezależnie od wielkości `S`. Wszystkie 25
wcześniej istniejących testów przeszły bez zmian po naprawie (używały
tylko małych wartości S=0.5-2.0, nigdy nie przechodziły przez pełną
sprzężoną pętlę w skali, w której błąd się ujawniał) — dokładnie
dlatego testy jednostkowe tego nie złapały, a systematyczne
przeszukanie siatki (phase diagram) tak. Zweryfikowane ponownym
przeszukaniem szerszego zakresu (alpha do 13.5, bump do 500, 165
kombinacji) bez ani jednego przepełnienia — obserwacja w przeszukanym
zakresie, NIE dowód zupełności naprawy dla każdego możliwego parametru.

Kod: `TIMDR-Math-Formalism/timdr_formalism/{gs_matrix,theta_bifurcation}.py`,
`tests/test_{gs_matrix,theta_bifurcation,sg_coupling_full_operator,
sg_coupling_full_operator_hard_mode,sg_coupling_phase_diagram}.py`,
`docs/SG_COUPLING_PHASE_DIAGRAM.md` (+ SVG). 158/158 testów całego
repo przechodzi (1 skipped, niezwiązany) po scaleniu z równoległą pracą
nad `meta_validator.py` (punkt 4).

## 17. Zakres mostu Fouriera M/S↔K ustalony na realnych danych (2026-09-15)

Most Fouriera (`Δt·Δf=1/(4π)`, punkt 7) jest dokładny matematycznie dla
pojedynczego, idealnego impulsu gaussowskiego (10/10 pytest). Pytanie:
czy ma podobną treść na realnych zdarzeniach M/S wyciętych progiem
`anomalia_flags()`?

**Pre-rejestracja** (`TIMDR-Time-Formalism/docs/PREREG_MS_K_EVENTS.md`):
definicja zdarzenia (klastrowanie sąsiadujących flag anomalii — poprawka
odkryta na kontroli pozytywnej: pojedynczy szeroki impuls przekracza
próg na WIELU sąsiednich próbkach, nie jednej), metryka `ratio=(Δt·Δf)/(1/4π)`
i `log(ratio)`, kontrola pozytywna PRZED realnymi danymi.

**Kontrola pozytywna** (20 seedów, syntetyczny impuls w szumie): rozkład
WĄSKI, `ratio: mediana=1.326 std=0.041` — mechanizm pomiaru działa
poprawnie.

**Wynik na 3 realnych domenach** (wybranych PRZED zobaczeniem wyników —
jedyne lokalnie dostępne, wystarczająco długie/gęste realne szeregi
M/S): sejsmika (Ridgecrest 2019, stacje CLC/RIO, `fs=100Hz`), łożyska
CWRU (wibracje, `fs=12kHz`, normalne+3 typy uszkodzeń), BTC/USD
godzinowy. WSZĘDZIE rozkład ROZJECHANY, nie wąski: sejsmika CLC
`std=1.26`, RIO `std=2.08`; łożyska normal `std=2.37`, ball_fault
`std=5.04` (mediana `ratio=49.7`, prawie 50× granicę Gabora); BTC — 0
zaakceptowanych zdarzeń (brak izolowanych klastrów).

**Zweryfikowane niezależnie**: `ratio` jest DOKŁADNIE niezmiennicze
względem wyboru stałej czasowej `dt` (`Δt∝dt`, `Δf∝1/dt`, iloczyn się
kasuje — potwierdzone numerycznie na tym samym oknie z 4 różnymi `dt`,
identyczny wynik do 6 miejsc po przecinku) — rozrzut między domenami
NIE jest artefaktem jednostek.

**Filtr kształtu** (liczba przejść przez zero okna, kalibrowana na
kontroli pozytywnej PRZED realnymi danymi, progi 2/4): łożyska i BTC —
ZERO okien przechodzi nawet luźny próg (strukturalnie nieimpulsowy
kształt). Sejsmika po filtrze: rozkład ZAWĘŻA się (`std` spada z
~1.3-2.1 do ~1.6-1.9), ale NIE odtwarza wąskości kontroli pozytywnej —
wynik POŚREDNI, nie czyste tak/nie.

**Wniosek i zawężenie zakresu**: most Fouriera ma potwierdzoną treść
TYLKO dla syntetycznych impulsów gaussowskich. Zapisany osobno
(`TIMDR-Time-Formalism/docs/RESULT_FOURIER_BRIDGE_SCOPE.md`) i dopisany
EXPLICITE jako ograniczenie w `Axioms_K_TIMDR.md` i
`Axioms_S_TIMDR_Signal.md` (GIA-TIMDR) — most obowiązuje na poziomie
pojedynczego modu (definicja + testy syntetyczne), NIE jako operator
diagnostyczny nad dowolnymi realnymi zdarzeniami M/S. Katalog naturalnie
izolowanych transjentów (nie okien wyznaczonych progiem 2σ) pozostaje
jawnie odłożonym future work ("opcja 1B"), bez presji wykonania.

## 18. Sprzężenie helikalne K↔Θ_bif — nowa konstrukcja, estymator częściowo zweryfikowany (2026-09-15)

Propozycja użytkownika: wyprowadzić warunki sprzęgania helis z K
(punkt 16), Θ_bif (`λ_down`,`λ_up`,`S_down`,`S_up`,`N(t)`) i α
(z osobnej, test-owej pętli SG-Coupling `G=R0+α·S²`).

**Kluczowe ustalenie PRZED jakąkolwiek konstrukcją**: `K` (z
`gs_matrix.py`) i `Θ_bif` są DZISIAJ w kodzie DWOMA ROZŁĄCZONYMI
obiektami — sprawdzone bezpośrednio w istniejącym docstringu
(`theta_bifurcation.py`, "UWAGA O POMINIĘTYM det(K)"): Jakobian pętli
G↔S ma kolumnę `G_old` tożsamościowo zerową, `G` jest jednokierunkowym
odczytem z `S`. Więc żadne "wyprowadzenie" nie jest ekstrakcją
istniejącej struktury — jest NOWĄ konstrukcją, jawnie oznaczoną (DRAFT,
nie ustalony wynik) w `TIMDR-Math-Formalism/docs/theory/
GS_Matrix_Helical_Coupling_DRAFT.md`.

**Konstrukcja** (§1-4 draftu): `S_down`/`S_up` utożsamione z bazą
własną `K_sym` (`μ_down=-λ_down`, `μ_up=+λ_up`), nowy parametr
sprzężenia rotacyjnego `ω₀` (koncepcyjnie zastępuje `α`, strukturalnie
inny — tempo, nie współczynnik kwadratowy). Wynik (zweryfikowany
numerycznie na wartościach własnych `K`, nie tylko odręcznie):
`Re(λ)=(λ_up-λ_down)/2` (niezależne od `ω₀`), próg spirali
`ω₀_crit=(λ_down+λ_up)/2`, powyżej progu `Im(λ)=sqrt(ω₀²-ω₀_crit²)`.
Dzisiejszy Θ_bif (zero rotacji) odpowiada specjalnemu przypadkowi
`ω₀≤ω₀_crit`. Przewidywanie: `N(t)=S_down·S_up` powinno oscylować z
częstością `2ω` na obwiedni `exp(2Re(λ)t)` — zweryfikowane regresją,
R²=1.000000.

**Estymator, kontrola pozytywna — pierwszy bloker**: naiwny DMD/
różnicowy estymator `Re(λ)/Im(λ)` z pojedynczego `x(t)` zawiódł
KATASTROFALNIE przy szumie (nawet 1% amplitudy → błędy 700-3000%,
fałszywe artefakty aliasingu w `Im(λ)`). Zdiagnozowana przyczyna
STRUKTURALNA, nie implementacyjna: dla reżimu z dwoma różnymi
wartościami rzeczywistymi trajektoria embeddingu opóźniającego kolabuje
asymptotycznie na jedną linię (dominujący mod przytłacza drugi) →
macierz regresji niemal osobliwa niezależnie od poziomu szumu.

**Poprawka podsunięta wprost przez użytkownika**: "jeśli mamy kształt,
estymatorem są warunki brzegowe" — dopasowanie ZNANEGO kształtu
rozwiązania (`exp(Kt)V0`) do CAŁEGO okna metodą nieliniowych najmniejszych
kwadratów, zamiast różnicowania próbka-po-próbce. Zweryfikowane: błąd
spadł z 700-3000% do kilkunastu procent na tym samym teście.

**Formalna pre-rejestracja z większą próbą** (`PREREG_HELICAL_SHAPE_ESTIMATOR.md`,
N=30 powtórzeń, warunki początkowe losowane niezależnie — NIE stałe jak
we wstępnej eksploracji) ujawniła wynik ASYMETRYCZNY i GORSZY niż
eksploracja: **kryterium A (dokładność `Re(λ)`) NIE PRZESZŁO** — błąd
30% już przy szumie 2%, 99.6% przy szumie 10%; **kryterium B (binarna
klasyfikacja "czy jest rotacja") PRZESZŁO** — czułość/swoistość 90-100%
w całym testowanym zakresie szumu. Częściowy sukces, nie zaokrąglony w
górę.

**Zawężenie zakresu (wzorem punktu 17) i zastosowanie do realnych
danych**: estymator NIE nadaje się do ilościowych `Re(λ)` na realnych
danych, nadaje się jako BINARNY detektor obecności rotacji. Zastosowany
do tych samych okien co punkt 17: sejsmika CLC 0%, RIO 7.4% z rotacją;
łożyska normal 50%, ball_fault 100%, outer_race 100%. Kierunek
fizycznie sensowny, ale JAWNIE oznaczone jako opisowa obserwacja na
małej próbie (N=1-27/domenę), NIE test istotności.

**Status**: konstrukcja pozostaje częścią GS-Matrix (eksploracyjny,
NIEaksjomatyzowany toy-model, punkt 5) — NIE dopisana do `Axioms_*`.
Streszczenie: `TIMDR-Math-Formalism/docs/theory/
RESULT_HELICAL_COUPLING_SCOPE.md`.

## 19. Most M/S↔topologia/K: seria syntetyczna odrzucona (1/50), ale REALNE dane dają silny, częściowo scharakteryzowany sygnał (2026-09-15/16)

Pięć kandydatów na skalarną metrykę topologiczną (torsja Freneta-Serreta,
winding/crossing number po embeddingu opóźniającym, homologia
perzystentna β₁, winding fazy Hilberta inspirowany OAM fotonu),
przetestowanych na SYNTETYCZNYM sygnale (2 częstotliwości + szum) przez
`pipeline.run_controls()` — **1/50 komórek siatki, ta jedna odrzucona
jako niewiarygodna** (`GIA-TIMDR/docs/geometry/RESULT_TOPOLOGICAL_
BRIDGE_MS_SCOPE.md`). Cztery z pięciu dzieliły wspólny mechanizm
(embedding opóźniający: szum ma większą lokalną/globalną złożoność
geometryczną niż sygnał periodyczny), piąty (winding fazy) zawiódł z
odrębnego powodu (dominująca częstotliwość maskuje słabszą składową).
Krótko, bo to ślepa uliczka bez dalszego potencjału w tej postaci —
pełne szczegóły w RESULT-ach, nie tutaj.

**Zwrot: te same 5 metryk na TRZECH realnych domenach dało jakościowo
inny, dużo bardziej informacyjny obraz** (`GIA-TIMDR/docs/geometry/
RESULT_REAL_{BEARING,SEISMIC,BTC}_NOISE_ROBUSTNESS.md` +
`AUDIT_G_COMPLEXITY_HYPOTHESIS.md`) — realny „pozytyw"/„negatyw"
zamiast syntetycznych generatorów, ten sam syntetyczny szum addytywny
dołożony NA WIERZCH:

- **Łożyska CWRU (normal vs 3 typy defektu)**: **123/150 (82%)**.
  `winding_number`/`crossing_number`/`phase_winding`: 30/30, duży
  efekt (r≥0,8) utrzymany nawet przy szumie o mocy sygnału (σ=1,0).
  `torsion`: kierunek ODWRÓCONY względem pozostałych + fałszywy alarm
  specyficzności — ten sam wzorzec niskiej wiarygodności torsji co w
  serii syntetycznej, powtórzony na realnych danych.
- **Trzy tanie kontrole PO wyniku, PRZED nazwaniem czegokolwiek nowym
  obiektem** (`AUDIT_G_COMPLEXITY_HYPOTHESIS.md`, odpowiedź na
  propozycję „G-complexity"/nowy aksjomat): (1) korelacja Spearmana
  między `winding`/`crossing`/`phase_winding` na 96 realnych
  segmentach: ρ=0,83–0,93 — **to jeden, wspólny sygnał**, nie trzy
  przypadkowe zbieżności; (2) test homogeniczności regionu
  pozytywnego W IZOLACJI (ta sama domena, sztucznie zanieczyszczony
  region pozytywny, `mix_frac=0→0,75`) — monotoniczna degradacja
  `r: 1,0→0,2`, **potwierdzone empirycznie w kontrolowany sposób**,
  ale mechanizm to generyczne rozcieńczenie próby w teście
  Manna-Whitneya (statystyka, nie geometria) — reguła protokołu, NIE
  aksjomat gałęzi G; (3) dwie klasyczne cechy (kurtoza, entropia
  widmowa) na tej samej siatce: podobna moc klasyfikacyjna (22/30,
  27/30 vs 30/30) ale PRAKTYCZNIE BRAK korelacji z naszą trójką
  (|ρ|<0,25 we wszystkich 6 porównaniach) — **podobna moc ≠ ten sam
  obiekt**, nasza trójka mierzy coś realnie innego niż oba klasyczne
  kandydaty.
- **Sejsmika Ridgecrest (koda vs tło, 2 stacje)**: 47/100 (47%) —
  kierunek NIESPÓJNY między stacjami (ten sam mainshock!), efekt
  KRUCHY (znika σ≥0,3-0,5). Zdiagnozowane: region pozytywny (300s
  kody) jest wewnętrznie NIEJEDNORODNY (nieliczne okna silnego
  wstrząsu + wiele cichnących okien) — w odróżnieniu od jednorodnego
  regionu defektu łożyska.
- **BTC/USD (reżim zmienności, bloki 24h wg mediany std)**: 6/50
  (12%) — mimo region pozytywny ŚWIADOMIE zaprojektowany jako
  jednorodny (okna nigdy nie przecinają granicy bloku, lekcja z
  sejsmiki wprost zastosowana). **Jednorodność okazała się KONIECZNA,
  ale NIE WYSTARCZAJĄCA** — hipoteza „jednorodność gwarantuje sukces"
  została tu przetestowana i w dużej mierze obalona na nowej domenie.

**Status**: cała seria (syntetyczna i realna) pozostaje eksploracyjna,
NIE promowana do `Axioms_G_TIMDR_Geometry.md`. Nazwa „G-complexity"
dla `winding`/`crossing`/`phase_winding` — PRZEDWCZESNA (tylko 2 z 6
zaproponowanych alternatyw faktycznie przetestowane jako kontrola
korelacji). Otwarte, nieodłożone: envelope spectrum/autokorelacja jako
kolejne klasyczne baseline'y; powtórzenie kontroli korelacji na
sejsmice/BTC.
