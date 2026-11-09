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


## 9. Wynik uruchomienia CI

Workflow [42565302887](https://github.com/jbackk-lang/GIA-TIMDR/actions/runs/42565302887) zakończył sukcesem testy i obliczenia dla kuli oraz jaja. Artefakt `helix-four-to-three-phase-locked-v02`, ID `13650114967`, SHA-256 `52e8a5393cddb19a49e26c5582ab743583090beb6242ef1a8b8713b5eb5f0855`.

| Wynik | Kula | Jajo |
|---|---:|---:|
| Podział początkowy | 90° | 90° |
| Podział końcowy | 120° | 120° |
| Liczba ocalałych helis | 3 | 3 |
| Długość każdej ocalałej krzywej w modelu | 6.502990 | 6.571573 |
| Znak obiegu fazowego zachowany | tak | tak |
| Jedna helisa wybrana jako pierwsza przez symetryczny próg | nie | nie |

Wynik potwierdza spójność księgowania fazowego 90°→120° oraz zachowanie znaku kierunku obiegu w implementacji. **Nie potwierdza fizycznego mechanizmu selektywnego odpadnięcia**: w tej rodzinie krzywych wszystkie cztery przebiegi mają ten sam profil geometryczny z przesunięciem fazowym, więc próg graniczny jest zdegenerowany. Samo jednorodne rozszerzanie/kurczenie nie wskazuje jednej helisy.

### 9.1. Granica obecnego modelu topologicznego

W v0.2 cztery przebiegi są reprezentowane jako cztery zamknięte krzywe, a operacja usuwa jedną całą krzywą z listy. To formalizuje liczbę helis i podział fazowy, ale **nie koduje jeszcze połączeń/węzłów między nimi**. Nie oblicza typu węzła, liczby splątania ani tego, czy dwie granice odcięcia jednej helisy rzeczywiście pasują do wspólnych punktów węzła.

Następna wersja musi reprezentować cały obiekt jako połączony graf przestrzenny (węzły połączeń + skierowane łuki helikalne osadzone w 3D). Dwie granice odłączenia mają być wyznaczone przez ćwiartki globalnej fazy i muszą spełnić zgodność pozycji oraz stycznych po dopasowaniu. Dopiero wtedy wolno stwierdzić, że jedna helisa rzeczywiście odpada z czterowęzła, a pozostałe zamykają się w trójwęzeł.
