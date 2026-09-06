# TIMDR signal framework (GIA-TIMDR core) — uproszczony skrót

> Uproszczona wersja skilla `timdr-signal-framework` (kopia treści z konta Claude), zawężona do własnej teorii/formalizmu/sygnałów GIA-TIMDR. Pełna, szczegółowa wersja (z dokładnymi liczbami, nazwami plików/funkcji, pełnymi uzasadnieniami każdego wniosku) zachowana w `SKILL_timdr-signal-framework_PELNA.md` w tym samym katalogu — sięgnij po nią, gdy potrzebujesz konkretów, nie tylko orientacji. Pełna, cross-repo wersja skilla (audyty, case-studies z sejsmiki, radaru, bezpieczeństwa, kosmologii, EV/battery/industrial itd.) istnieje osobno i NIE jest tu duplikowana. Stan: 2026-09-06.

## 1. Co to w ogóle jest?

Rdzeń formalizmu TIMDR: cztery sygnały, protokół testowania (anty-numerologia), trzy gałęzie (M/S, G, K), Chronoproces spinający je bez mieszania, domknięcia geometryczne (G8-G10), operator G-Rezonans (G5) i jeden jawnie oznaczony dokument spekulacyjny.

## 2. Cztery sygnały TIMDR (M/S)

- **anomalia** — wartość poza normą (np. > mean+2σ).
- **defekt** — skok między kolejnymi próbkami > próg.
- **rezonans M** — ≥3 anomalii w tym samym czasie (koincydencja, NIE fizyczny oscylator).
- **skręt sygnałowy** — odwrócenie trendu, flip znaku nachylenia > próg.

„Rezonans" i „skręt" mają wiele znaczeń w całym ekosystemie GIA-TIMDR —
zawsze podawaj który: rezonans ma 4 znaczenia (M sygnałowy, K modalny,
kierunkowy R(t), G-Rezonans/G5 — punkt 11), skręt ma 5 (sygnałowy,
topologiczny τ, powierzchniowy, blokowy, Frenet-Serret trójwęzła —
punkt 11). Kanoniczna lista: `docs/GLOSSARY_EN_PL.md`, `TIMDR_Twists.md`.

## 3. Protokół formalizmu (anty-numerologia)

9 zasad, najważniejsze: preregistracja definicji/progów przed danymi
(zero tuningu po fakcie) · testy na tle losowym, nie na "czy sygnał
odpala gdy wzorzec już jest" · Mann-Whitney U + rozmiar efektu r
(obowiązkowy, nie opcjonalny) · kontrolka pozytywna I negatywna przed
testem głównym · moc testu: wysokie p ≠ brak efektu, jeśli zero zdarzeń
kwalifikujących się do testu · jedno uruchomienie, korekta Bonferroniego
przy wielu oknach · wynik negatywny jest pełnoprawną odpowiedzią.

## 4. Formalizacja gałęzi sygnałowej — TIMDR-Math-Formalism

Implementacja protokołu jako kod (`timdr_formalism/pipeline.py`),
rozmiar efektu, dyscyplina mocy. Realny test na Kraków_Centrum: p≈1, bo
ciśnienie miało 0/24 przekroczeń własnego progu 2σ (zero zdarzeń do
przetestowania), NIE potwierdzony brak rezonansu — kontrolka pozytywna
złapana czysto (p≈0.0002), więc mechanika testu działa poprawnie.

## 5. Trzy gałęzie TIMDR (i rozdzielenie znaczeń)

- **M/S** — sygnały czasowe (anomalia/defekt/rezonans M/skręt sygnałowy), `Axioms_S_TIMDR_Signal.md`, 13 aksjomatów.
- **K** — rezonans modalny (częstotliwość/faza między modalnościami), `Axioms_K_TIMDR.md`, 10 aksjomatów — zupełnie inny obiekt niż rezonans M.
- **G** — geometria (skręt powierzchniowy, operator kształtu/Weingarten, krzywizny obwiedni, G-Rezonans), `Axioms_G_TIMDR_Geometry.md`, 10 aksjomatów.

Plus starszy, nieformalny szkic kierunkowy `R(t)=mean(sign(Sᵢ'(t)))` w
głównym README. Żadna gałąź nie jest rozszerzeniem innej — każda ma
własny obiekt/operator, mimo współdzielonych nazw.

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

## 8. Aksjomat G10 (parametr obwiedni P/Q)

Krzywizna krzywej (nie powierzchni) na obwiedni zaokrąglonego trójkąta:
`P=L0/L` (część prosta), `Q=Lk/L=1-P` (część łukowa), `Lk(R)=2πR`
dokładnie. `P(R)` ściśle monotoniczne → odwracalne (oba kierunki
krzywa↔(P,Q)). Implementacja + 65/65 testów: `timdr_geometry/envelope.py`.
Błąd znaleziony i naprawiony: pierwsza wersja twierdziła `Q_max<1` poza
trójkątem równobocznym — w rzeczywistości `R_max(Δ)=r_in(Δ)` dokładnie
DLA KAŻDEGO trójkąta (tożsamość styczna-do-okręgu-wpisanego), `Q→1`
zawsze osiągalne.

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
krzywej 3D, warunek stabilności jako predykat algebraiczny
(dodatnia określoność M/K/Γ ⟹ brak bieguna na osi rzeczywistej —
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

## 13. Meta-zasady TIMDR (wnioski ogólne, wielokrotnego użytku)

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
