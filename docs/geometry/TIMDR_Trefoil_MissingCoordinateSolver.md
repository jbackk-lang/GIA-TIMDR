# Rozwiązywanie brakującej współrzędnej — algebra działa, praktyka nie (jeszcze)

**Status:** zaimplementowane i przetestowane (5/5 testów przechodzi,
`tests/test_trefoil_missing_coordinate_solver.py`). Realizacja
4-punktowego planu użytkownika (krzywa z brakującą współrzędną → układ
κ/τ → rezonans jako selektor → wygładzanie przed różniczkowaniem) —
**z jednym znalezionym i naprawionym błędem w projekcie potoku**, i
jednym uczciwym wynikiem negatywnym w praktycznym zastosowaniu.

## 1. Fakt matematyczny, na którym to stoi

Dla `p_t=(x,y,z)` z `x,y` ustalonymi, `v(z)=p_t−p_t1` i `a(z)=v(z)−v_prev`
są obie afiniczne w `z` (`v_prev` jest w całości historyczne). Rozwijając
`v(z)×a(z)`, wyraz kwadratowy `z²·(e_z×e_z)` znika **tożsamościowo**
(wektor iloczynowany sam ze sobą = 0) — więc `v(z)×a(z) = C0 + z·C1`,
dokładnie liniowe. Zweryfikowane numerycznie: druga różnica dyskretna
`v(z)×a(z)` po siatce `z` wychodzi rzędu `1e-15` (test 1). Skutek:
`κ(z) = |v(z)×a(z)| / |v(z)|³` jest gładka funkcja wymierna jednej
zmiennej — równanie `κ(z)=target` ma generalnie 0, 2 (czasem więcej)
rozwiązań, rozwiązywalne skanem + bisekcją.

## 2. Błąd znaleziony w pierwszej wersji potoku — i jego naprawa

Plan użytkownika: krok 2 (τ jako filtr, "redukuje liczbę dopuszczalnych
rozwiązań"), krok 3 (rezonans jako selektor między pozostałymi
kandydatami). Pierwsza implementacja pozwoliła rezonansowi wybierać
**niezależnie** od wyniku kroku 2, ignorując go.

**Test z celami oracle (idealna, dokładna wiedza o prawdziwym κ, τ)
ujawnił problem**: prawdziwe `z` jest zawsze jednym z pierwiastków
(0 przypadków, gdzie go brakuje), a `select_by_tau_consistency` **trafia
w 100% przypadków** (test 2). Ale `select_by_resonance` **jako
niezależny selektor trafia tylko w ~46%** (test 3) — bo rezonans
odpowiada na inne pytanie ("czy to wygląda jak dziki pik względem
historii"), nie "który z dwóch pierwiastków jest prawdziwy". Naprawiono:
τ-consistency **wybiera** kandydata, rezonans tylko **raportuje**, czy
wybrany kandydat jest stabilny — nie zmienia już wyboru. To dokładnie
ten sam wzorzec, co przy błędzie `RESONANCE_MAX_K`/kolejności
sygnałowej w innych repo tej sesji: dwa mechanizmy o różnym
przeznaczeniu, złożone bez jasnego pierwszeństwa, dają gorszy wynik niż
każdy osobno.

## 3. Wynik praktyczny — negatywny, zdiagnozowany

Test z celami oracle pokazuje, że **algebra i selekcja działają
bezbłędnie, gdy znamy dokładny cel**. W praktyce nigdy nie znamy
dokładnego κ/τ brakującego punktu — trzeba go oszacować (tu: mediana
κ/τ z niedawnej historii, założenie "brakujący punkt to normalna
kontynuacja"). Test 4, z takim realistycznym szacowaniem celu:

| metoda | średni błąd odzysku (jednostki z-score) |
|---|---|
| potok geometryczny, BEZ wygładzania | 1,36 |
| potok geometryczny, Z wygładzaniem (krok 4) | 1,09 (~20% lepiej) |
| **trywialny baseline** (powtórz ostatnią znaną wartość) | **0,47** |

Wygładzanie (krok 4, Savitzky-Golay bez scipy — lokalne dopasowanie
wielomianu) **realnie pomaga** (potwierdzone osobnym testem sanity —
MSE względem czystego sygnału spada), ale nie wystarcza, żeby dogonić
trywialny baseline — potok geometryczny pozostaje **ok. 2,3× gorszy**
nawet po wygładzeniu. Dodatkowo: w 40% prób równanie `κ(z)=target` nie
miało w ogóle rozwiązania w przeszukiwanym zakresie (szacowany cel był
nieosiągalny dla żadnego `z` w rozsądnym przedziale).

**Przyczyna, nie tylko obserwacja**: szacowanie celu z niedawnej
historii dziedziczy dokładnie ten sam problem, co
`TIMDR_Trefoil_RealDataValidation.md` — κ/τ liczone z krótkiego,
nie-gładkiego szeregu jest z natury niestabilne/ciężko-ogonowe, więc
"typowa niedawna wartość" jest słabym oszacowaniem tego, co powinno być
"normalne" w danym momencie. Algorytm rozwiązujący jest tak dobry, jak
cel, który mu się poda — a ten cel jest tu z natury zaszumiony.

## 4. Wniosek

Odpowiedź na pytanie "czy to się da rozwiązać" pozostaje **tak, algebra
się zgadza** — i to ładnie: liniowość `v×a` w brakującej współrzędnej
jest eleganckim, sprawdzonym faktem, a τ jako filtr między
pierwiastkami działa bezbłędnie przy dokładnym celu. Ale jako
praktyczne narzędzie do uzupełniania brakującego odczytu czujnika **nie
dorównuje najprostszej możliwej metodzie** (powtórz ostatnią wartość) —
dopóki nie rozwiąże się osobnego, głębszego problemu: jak oszacować
wiarygodny cel κ/τ na krótkim, zaszumionym szeregu, co jest dokładnie
tym samym pytaniem, które pozostało otwarte w
`TIMDR_Trefoil_RealDataValidation.md`.

## Źródła

- Kod: [`../../core/trefoil_missing_coordinate_solver.py`](../../core/trefoil_missing_coordinate_solver.py)
- Testy: [`../../tests/test_trefoil_missing_coordinate_solver.py`](../../tests/test_trefoil_missing_coordinate_solver.py)
- Poprzedni negatywny wynik (przyczyna problemu z celem): [`TIMDR_Trefoil_RealDataValidation.md`](./TIMDR_Trefoil_RealDataValidation.md)
- Matematyka bazowa (κ/τ z różnic skończonych): [`TIMDR_Trefoil_FrenetTorsion.md`](./TIMDR_Trefoil_FrenetTorsion.md)
