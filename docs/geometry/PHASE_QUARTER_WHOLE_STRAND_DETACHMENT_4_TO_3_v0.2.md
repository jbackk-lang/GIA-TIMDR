# Faza ćwierćobrotu i odpadnięcie całej helisy: redukcja 4→3 (v0.2)

**Data:** 2026-11-09  
**Status:** nowa interpretacja robocza, model fazowy i testy; nie jest jeszcze pełnym rozwiązaniem topologicznym ani mechanicznym.

## 1. Zasada konstrukcyjna

Wersja 0.1 została zastąpiona jako model mechanizmu redukcji. Nie wycinamy łuku helisy i nie łączymy końców mostkiem. **Odpada cała jedna zamknięta helisa.**

Początkowy węzeł ma cztery helisy/fazy rozmieszczone równomiernie wokół osi. Jedna ćwiartka pełnego obrotu fazowego wyznacza sektor przypisany każdej helisie:

\[
\Delta\phi_4=\frac{2\pi}{4}=\frac{\pi}{2}=90^\circ.
\]

Granice dopasowania są zatem fazowe i wspólne dla całego obiektu, a nie wybierane lokalnie na fragmencie jednej krzywej. Dla kuli przyjmujemy obrót fazowy jako podstawową miarę podziału.

Po odpadnięciu całej czwartej helisy trzy pozostałe muszą dopasować się do nowej kolistości:

\[
\Delta\phi_3=\frac{2\pi}{3}=120^\circ.
\]

Zmiana rozstawu fazowego wynosi:

\[
\frac{\Delta\phi_3}{\Delta\phi_4}=\frac{4}{3}.
\]

To jest warunek symetrycznego rozmieszczenia wokół osi, nie wynik optymalizacji energii. Właściwa relaksacja ma dopiero ustalić, jak zmieniają się promień, krzywizna, torsja, długość i położenie osi.

## 2. Kula jako geometria podstawowa

Przyjmujemy kulę jako bazową przestrzeń odniesienia, zgodnie z aktualną decyzją badawczą. W niej:
- faza azymutalna jest naturalnym parametrem obiegu;
- cztery sektory mają po 90°;
- po redukcji trzy sektory mają po 120°;
- granice sektorów są jednoznaczne i nie wymagają zastępowania fazy długością łuku.

Nie twierdzimy, że fizyczny obiekt TIMDR jest już kulą. Kula jest hipotezą geometrii bazowej do sprawdzenia.

## 3. Jajo jako wariant kontrolny

Dla bryły jajowatej zachowujemy ten sam opis fazowy, ale nie zakładamy, że ćwierć obrotu fazowego odpowiada ćwierci długości przebiegu po powierzchni. W kodzie zapisujemy osobno diagnostykę podziału według długości łuku.

To pozwala porównać dwie interpretacje:
1. podział fazowy — zgodny z konstrukcją kulistą;
2. podział metryczny — ćwiartki równej długości po powierzchni.

Nie rozstrzygamy z góry, która miara jest właściwa dla jajowatej geometrii.

## 4. Rozszerzanie/kurczenie i warunek odpadnięcia

Wprowadzamy parametr skali \(\lambda\):

\[
K_4(\lambda)=\lambda K_4(1).
\]

Granica dopuszczalności jest opisana przez warunek brzegowy. Dla każdej helisy można zdefiniować funkcję luzu:

\[
g_i(\lambda)=b_i-\mathcal E_i(K_4(\lambda)),
\]

gdzie \(b_i\) jest dopuszczalną granicą, a \(\mathcal E_i\) miarą zajętości/wychylenia helisy. Próg krytyczny spełnia:

\[
g_i(\lambda_{c,i})=0.
\]

Odłączenie całej helisy jest zdarzeniem topologicznym, nie samym ciągłym skalowaniem. Model musi więc określić, co dzieje się z połączeniem w chwili przekroczenia granicy.

**Istotna kontrola symetrii:** jeśli kula, cztery helisy i warunki brzegowe są idealnie symetryczne, wszystkie cztery helisy mają ten sam próg \(\lambda_c\). Samo rozszerzanie lub kurczenie nie wybierze jednej z nich. Aby jedna konkretna helisa odpadła jako pierwsza, musi istnieć fizyczna przyczyna selekcji: asymetria, zaburzenie, nierówny luz albo różny warunek brzegowy. Nie będziemy jej sztucznie dopisywać.

## 5. Ręczność

W modelu fazowym orientację zapisujemy przez znak:

\[
\sigma=\operatorname{sign}\left(\frac{d\phi}{du}\right)\in\{-1,+1\}.
\]

Przy zmianie liczby helis znak \(\sigma\) ma być zachowany. To jest kontrolowany niezmiennik orientacji obiegu w tej parametryzacji.

Nie utożsamiamy go automatycznie z podpisaną torsją Freneta. Torsja może zmieniać znak nawet wtedy, gdy azymutalny kierunek obiegu jest zachowany. Obie wielkości należy rejestrować oddzielnie.

## 6. Co implementuje v0.2

Kod: `experiments/helix_reduction/phase_locked_whole_strand_reduction.py`.

- tworzy cztery zamknięte przebiegi z fazami co 90°;
- usuwa całą wybraną helisę, bez lokalnego mostka;
- rozmieszcza trzy pozostałe fazami co 120°;
- zachowuje znak kierunku obiegu;
- liczy długości zamkniętych przebiegów;
- oblicza diagnostykę progu granicznego;
- dla jaja raportuje osobno granice ćwiartek długości łuku.

Testy: `experiments/helix_reduction/tests/test_phase_locked_whole_strand_reduction.py`.

## 7. Ograniczenia i następny krok

v0.2 jest modelem kinematycznym. Nie rozwiązuje jeszcze:
- fizycznego mechanizmu odłączenia zamkniętej składowej;
- relaksacji trzech pozostałych helis;
- geodezyjnego/energetycznego dopasowania po zmianie warunków brzegowych;
- pełnego niezmiennika węzła/ogniwa (linking number, knot type);
- położenia punktów kardynalnych wynikającego z równań, a nie z ręcznego wyboru.

Następny etap: zdefiniować energię deformacji i warunki brzegowe, dopuścić niezależne zmiany promienia/fazy każdej z trzech ocalałych helis i znaleźć minimum energii po usunięciu całej czwartej. Równolegle zbadać stabilność progu \(\lambda_c\) przy kontrolowanych, jawnych perturbacjach. Wtedy można sprawdzić, czy punkty kardynalne wynikają z samego rozwiązania.

## 8. Zasada badawcza

**Kula jest geometrią bazową; podział ćwiartkowy jest fazowy; odłącza się cała helisa; trzy pozostałe dostosowują się do nowych warunków brzegowych.** Jajo pozostaje wariantem kontrolnym, w którym porównujemy podział fazowy z podziałem długościowym, bez arbitralnego utożsamiania tych dwóch miar.
