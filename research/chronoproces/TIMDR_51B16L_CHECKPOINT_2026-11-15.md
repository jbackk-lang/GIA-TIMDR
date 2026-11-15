# TIMDR 51B.16l — Zwięzłe certyfikaty niewykonalności bez enumeracji wszystkich regulatorów

Checkpoint 2026-11-15.

## Zakres
Skończone gry częściowej obserwacji, dokładne przejścia, skończone A, Y, X, pamięć M={0,...,k-1}. Semantyka: obserwacja y, wybór alpha(m,y), aktualizacja eta(m,y), przejście fizyczne, nowa obserwacja. Diagnoza bieżącej etykiety; zadanie kończy się przy singletonie etykiety. Nie obejmuje bezpieczeństwa po zakończeniu diagnozy.

## 16l.1 Symboliczne tablice
Zmienne U_(m,y) in A, V_(m,y) in M reprezentują całą rodzinę (|A|k)^(k|Y|) deterministycznych tablic dla ustalonego m0. Nie mylić wykładniczej złożoności z nierozstrzygalnością: dla ustalonego skończonego modelu i k problem jest rozstrzygalny.

## 16l.2 Produkt i warunki
Węzły z=(m,B,y), B niepuste dokładne przekonanie zgodne z bieżącą obserwacją. Dla ustalonych U,V i każdego y' z Psi_a(B,y') niepustym krawędź do (V_(m,y),Psi_a(B,y'),y'). Regulator działa wyłącznie na m,y. Porażka = osiągalny niebezpieczny następnik przed diagnozą lub osiągalny cykl nierozstrzygniętych węzłów; w skończonym dokładnym grafie lasso reprezentuje możliwą nieskończoną historię obserwacji.

## 16l.3 Kodowanie SAT
Zmienna R_z oznacza włączenie węzła do nadaproksymacji osiągalności. R dla wszystkich początkowych obserwacji; dla każdego R_z i nonGoal(z), wybrana akcja musi mieć Post_a(B) subset K, wszystkie możliwe krawędzie muszą prowadzić do R_z', a ranga naturalna r_z' < r_z. Rangi ograniczone przez |Z|. Formuła Phi_k jest SAT wtedy i tylko wtedy, gdy istnieje poprawny k-memory regulator dla zadanej semantyki zakończenia po diagnozie. Kierunek completeness: osiągalny nonterminal graph dobrego regulatora jest acykliczny, zatem ma topologiczne rangi. Kodowanie należy zaimplementować wiernie; formalny opis nie jest jeszcze przetestowanym encoderem.

## 16l.4 Niezależny dowód UNSAT
Cert-=(canonical model,k,Phi_k,encoding provenance,Pi). Zalecany zaufany deterministyczny encoder z modelu do CNF i niezależny LRAT proof checker. Sama odpowiedź UNSAT solvera nie wystarcza. Przy wiernym encoderze i poprawnym checkerze LRAT zaakceptowany Pi dowodzi braku k-memory regulatora. UNKNOWN/UNVERIFIED przy braku świadectwa lub wyczerpaniu zasobów. Nie twierdzić, że każdy UNSAT ma krótki certyfikat.

## 16l.5 Strukturalny przykład
X={p,q}, etykiety odmienne, obie akcje identity, obserwacja stale R, K=X. B={p,q} invariant, żadna strategia z dowolną pamięcią nie wymusza diagnozy. Jeden certyfikat epistemiczny wyklucza wszystkie k; korzystniejszy niż oddzielne UNSAT.

## 16l.6 Ograniczenia
Nie ma jeszcze działającego encodera CNF ani checkera LRAT w tej fazie. Możliwa wykładnicza liczba przekonań <=2^|X|-1, duże dowody UNSAT, kosztowna weryfikacja. Nadprzybliżona kwantyzacja ciągła nie pozwala na negatywny transfer bez realizowalności. Brak origin tags i gwarancji postdiagnostycznej.

## Następny etap
51B.16m — Implementacja deterministycznego encodera CNF, niezależny checker LRAT i testy różnicowe z enumeracyjnym 51B.16k.
