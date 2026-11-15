# TIMDR / Chronoproces — checkpoint 51B.6–51B.9
Data: 2026-11-14. Zapis roboczy z rozmowy; nie jest recenzowaną publikacją.

## Definicje
Niech X będzie zbiorem dopuszczalnych historii, ~H równoważnością identycznych rozkładów wszystkich przyszłych obserwowanych ciągów, a R rodziną relacji na X (relacje na zdarzeniach wymagają jawnego przeniesienia na historie). ~Phi to najgrubsza równoważność zawarta w ~H, przez którą faktoryzują relacje R i która jest stabilna przy dopuszczalnych przedłużeniach historii. Dla skończonego X uzyskujemy ją przez iteracyjne uszczegóławianie podziału ~H ∩ ≡R aż do punktu stałego, z uwzględnieniem zgodności dziedzin przejść. Iloraz jest minimalny pod względem liczby stanów w tej ściśle określonej kategorii reprezentacji.

Naturalne surjekcje: X -> S_Phi -> S_H, gdzie S_Phi=X/~Phi i S_H=X/~H. Nie należy pisać dosłownego zawierania zbiorów klas S_H ⊆ S_Phi ⊆ X.

Dla skończonych, niepustych ilorazów: eta=|S_Phi|/|S_H| >=1.

## 51B.6: statyczna zgodność nie wystarcza
Cztery stany a,b,c,d, przejścia a -e-> c i b -e-> d, c,d końcowe. Wszystkie a,b mają przyszłość „e, koniec”, c,d mają pustą przyszłość, więc S_H={{a,b},{c,d}}. Relacja binarna R(c,c)=1, wszędzie indziej 0. Początkowy podział zgodny z relacjami i prognozami: {{a,b},{c},{d}}. Ponieważ następcy a,b należą do różnych klas, stabilizacja rozdziela a,b: S_Phi ma 4 stany, eta=2.

## 51B.7: brak uniwersalnego ograniczenia dla relacji binarnych
X_n={a_1,...,a_n,c_1,...,c_n}; a_i -e-> c_i, c_i końcowe; R(c_i,c_i)=1 dla każdego i, R=0 na pozostałych parach. R rozróżnia c_i poprzez ustalenie drugiego argumentu c_i; stabilizacja rozróżnia a_i. |S_H|=2, |S_Phi|=2n, eta=n -> infinity. Nie istnieje stała C niezależna od procesu, dla której |S_Phi|<=C|S_H| w tej klasie.

## 51B.8: naturalne relacje — status ostrożny
W rozmowie zgłoszono eksperymenty dotyczące zawierania/hierarchii, porządku czasowego i równości trójek (MIN,MAX,Delta t), wraz z twierdzeniem o eta=n. Aby uznać je za w pełni zweryfikowane, trzeba sprawdzić konkretne definicje relacji, przypisanie atrybutów do historii/zdarzeń i kod źródłowy. Nie przenosić automatycznie dowodu dla sztucznego R na wszystkie geometryczne interpretacje. Ogólna intuicja: sam typ relacji bez ograniczeń strukturalnych nie musi ograniczać eta.

## 51B.9: warunki wystarczające
(A) Jeżeli wszystkie wymagane relacje faktoryzują przez S_H, to ~H jest już dopuszczalną kongruencją i eta=1. Przy ustalonej definicji jest to także konieczne dla eta=1.

(B) Sama liczba statycznych profili relacyjnych nie ogranicza eta: różnice mogą ujawniać się po kolejnych przejściach. Liczba klas pełnych profili relacyjno-dynamicznych w obrębie każdej klasy prognostycznej <=K daje eta<=K, ale jest bliska definicji.

(C) Konstruktywny warunek: istnieje dodatkowa zmienna geometryczna q∈Q, |Q|=K, taka że reprezentacja (s,q), s∈S_H, dokładnie odtwarza wymagane relacje i ma jednoznaczną aktualizację po każdym zdarzeniu. Wtedy |S_Phi|<=K|S_H| i eta<=K. Należy jawnie określić relacje między parami (s,q) i obsługę dopuszczalności przejść.

Samo stwierdzenie R=F(T,H) nie gwarantuje małego eta, jeśli F wykorzystuje szczegóły historii niewidoczne w S_H.

## Punkt wznowienia: 51B.10
Zbudować dla naturalnej relacji TIMDR (najpierw zawieranie/hierarchia) skończony automat dodatkowej pamięci geometrycznej Q. Sformułować niezależne warunki ograniczające |Q|, wykazać poprawność aktualizacji, policzyć eta i odróżnić dowód od testów syntetycznych.

## Granice twierdzeń
Wyniki dotyczą określonego alfabetu obserwacji, relacji na X i modelu dopuszczalnych przejść. Jeżeli geometria zostanie włączona do obserwowanych przyszłości, zmieni się ~H. Podobieństwo do kongruencji automatowych i minimalizacji systemów przejść należy jawnie wskazywać; nie deklarować nowości bez porównania z literaturą.
