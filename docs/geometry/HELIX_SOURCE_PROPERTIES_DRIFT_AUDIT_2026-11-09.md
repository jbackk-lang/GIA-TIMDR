# Audyt powrotu do pierwotnych właściwości helisy TIMDR (2026-11-09)

**Cel:** sprawdzić, czy ostatnia linia badań — spiralna oś wewnętrzna, wymuszanie skrętu przez kulę, próg 5→6 modułów — wynika z wcześniejszej definicji helisy TIMDR, czy jest nową hipotezą, która odsunęła badanie od właściwości źródłowych.

## 1. Punkt odniesienia — wcześniejsza definicja programu

Dokument `docs/geometry/TRIANGLE_HELIX_NODE_BOUNDARY_CONDITIONS.md` definiuje kolejność badania jako:

`trajektoria trójkąta → redukcja → struktura trójhelikalna / węzeł → oś i punkty kardynalne → sygnał`.

Dokument ten mówi wprost:
- trójkąt ma być źródłem trajektorii / stanów; trzeba ustalić, czy jest figurą, przebiegiem po krawędziach, czy cyklem stanów;
- redukcja nie jest jeszcze jednym ustalonym operatorem: możliwa jest redukcja stopni swobody, kontrakcja grafu, projekcja albo zmiana topologiczna;
- węzeł trójhelikalny należy odróżnić od klasycznego trefoila;
- oś jest elementem pierwotnym, nie pomocniczą linią wyprowadzoną z gotowej krzywej;
- punkty kardynalne nie mają jeszcze zatwierdzonej liczby ani definicji;
- trzeba rozdzielić torsję Freneta, twist pasma, writhe, linking, fazę modalną i skręt powierzchniowy;
- warunki brzegowe obejmują domknięcie pozycji, stycznej, ramy, fazy, indeksów gałęzi i reguły przejścia.

To jest właściwa kolejność i zakres. Oś/punkty kardynalne mają być odzyskane z definicji TIMDR, a nie dopowiedziane z góry.

## 2. Co katalog właściwości faktycznie definiuje

`docs/geometry/HELIX_SENSITIVITY_REPRODUCIBILITY.md` zawiera katalog miar krzywej:
- pozycja, prędkość, przyspieszenie, szarpnięcie, szybkość;
- krzywizna (kappa=|v\times a|/\|v\|^3);
- torsja Freneta–Serreta (	au_{FS}=((v\times a)\cdot j)/\|v\times a\|^2);
- kandydacka helikalność (H=\sqrt{\kappa^2+\tau_{FS}^2}), wyraźnie bez statusu niezmiennika;
- długość łuku, skręt całkowity i topologia — wciąż niezmierzone / nieustalone dla ogólnej helisy.

Katalog podkreśla, że (	au) MetaState, torsja Freneta i skręt topologiczny są odrębnymi wielkościami. Wrażliwości promienia, skoku, częstotliwości, fazy, orientacji i parametryzacji pozostają w dużej części nieprzebadane.

## 3. Co mówią aksjomaty geometrii G

`docs/theory/Axioms_G_TIMDR_Geometry.md` opisuje gałąź G jako geometrię trójkąta, powierzchni i skrętu powierzchniowego:
- G2: trójkąt równoboczny jest stanem symetrii; odejście od równoboczności jest asymetrią geometryczną i w tej gałęzi kandydatem na pierwotne źródło skrętu;
- G3: skręt powierzchniowy jest zmianą pola normalnych powierzchni, a nie torsją krzywej;
- G4: relacja skrętu powierzchniowego z operatorem kształtu / krzywizną;
- dalsze aksjomaty mają jawne ograniczenia statusu; część to wyprowadzenia, a nie zwalidowany model helisy.

Ważne: aksjomaty G nie mówią, że kulista granica sama generuje helisę lub węzeł. W tym źródle kula nie jest mechanizmem źródłowym helisy.

## 4. Co faktycznie robią obecne eksperymenty 4→3

`experiments/helix_reduction/four_to_three_surface_reduction.py`:
- z góry generuje cztery krzywe na zadanej kuli/jaju z (	heta(u)=\pi/2+0.22\sin(2u)) i (phi_j(u)=u+2\pi j/4);
- wybiera czwartą krzywą, wycina zadany łuk i łączy końce mostkiem interpolowanym w parametrach powierzchni;
- pozostałe trzy generuje ponownie z równym rozstawem 120°;
- nie wyprowadza czterech helis z trójkątnego modułu/odbicia;
- nie wyprowadza wyboru ciętej gałęzi z warunku brzegowego;
- nie dowodzi powstania węzła ani mechanizmu 5→6.

`phase_locked_whole_strand_reduction.py`:
- zakłada cztery krzywe i cztery równe sektory fazowe;
- usuwa całą wybraną krzywą na granicy;
- ponownie rozstawia trzy krzywe na 120°;
- zachowuje zadany znak azymutalnego windingu;
- w idealnej kuli wszystkie cztery progi radialne są identyczne, więc model nie wybiera samodzielnie jednej gałęzi;
- jawnie deklaruje, że nie oblicza pełnego niezmiennika splotu/węzła i nie wyprowadza prawa fizycznego odłączenia.

Są to modele kinematyczne redukcji zadanych krzywych, nie implementacja źródłowego mechanizmu TIMDR.

## 5. Ocena ostatniego kierunku

| Twierdzenie | Status po audycie |
|---|---|
| Obrót trójkątnych modułów generuje helisę | hipoteza użytkownika; brak operatora i testu w obecnym kodzie |
| Wewnętrzna oś jest spiralna | hipoteza; brak źródłowej definicji / rekonstrukcji osi |
| Kula wymusza dodatkowy skręt | nieudowodnione; brak prawa kontaktu, energii lub ograniczenia dynamicznego |
| Skręt prowadzi do węzła | hipoteza; potrzebne domknięcie i niezmiennik topologiczny |
| Piąty moduł mieści się, szósty wymusza redukcję | hipoteza; brak modelu modułu i pomiaru progu |
| Redukcja 4→3 | w kodzie istnieje tylko zadana operacja kinematyczna; nie jest wyprowadzona z trajektorii trójkąta |

**Wniosek:** ostatnia linia badań odsunęła się od właściwości źródłowych. Sfera/spiralna oś/5→6 to na razie warstwa spekulatywna, nie rdzeń formalizmu. Nie należy usuwać jej, ale należy ją oznaczyć jako hipotezę potomną i wstrzymać rozwijanie, dopóki nie odzyskamy operatora generującego helisę z trójkąta i jego odbicia.

## 6. Właściwy powrót do badań — kolejność

1. Odzyskać dokładny obiekt bazowy: trójkąt, jego trajektorię i regułę odbicia (w tym co dokładnie odbijamy: wierzchołki, moduł, orientację czy stan).
2. Zdefiniować operator obrotu kolejnych modułów i regułę ich sklejenia.
3. Z tego operatora wyprowadzić oś i gałęzie, nie zakładać ich parametryzacji.
4. Zmierzyć właściwości z katalogu: (kappa), (	au_{FS}), fazę, orientację, długość, pitch/promień jeśli mają sens dla wyprowadzonej krzywej, oraz niezależne miary twist/writhe/linking.
5. Wyznaczyć punkty kardynalne jako zdarzenia wynikające z konstrukcji; nie ustalać ich liczby z góry.
6. Dopiero potem dodać otoczenie kuliste jako kontrolowany warunek i porównać z brakiem ograniczenia.
7. Dopiero po tym badać próg liczby modułów i redukcję 4→3.
8. Klasyfikować wynik topologiczny dopiero po zbudowaniu zamkniętego obiektu i obliczeniu odpowiedniego niezmiennika.

## 7. Zasada ochrony własności

Żadna redukcja nie może bez jawnego raportu usuwać:
- orientacji obiegu;
- znaku skrętu/odbicia;
- fazy;
- kolejności punktów przejścia;
- lokalnej ramy osi;
- warunków sklejenia na szwie;
- informacji o tym, czy krzywa jest otwarta, zamknięta, czy stanowi fragment większego obiektu.

Wartości bezwzględne, sortowanie faz i ponowne równomierne rozstawienie gałęzi są transformacjami potencjalnie stratnymi; należy je raportować jako takie.

## 8. Decyzja

Na obecnym etapie **wstrzymać rozbudowę modelu „kula wymusza spiralną oś i węzeł”**. Nie uznawać go za fałszywy — po prostu nie jest jeszcze zakotwiczony w źródłowej konstrukcji. Priorytetem jest odtworzenie geometrii trójkąta/odbicia i wyprowadzenie osi oraz helisy z reguł konstrukcyjnych.

Dokument odniesienia:
- `docs/geometry/TRIANGLE_HELIX_NODE_BOUNDARY_CONDITIONS.md`
- `docs/geometry/HELIX_SENSITIVITY_REPRODUCIBILITY.md`
- `docs/theory/Axioms_G_TIMDR_Geometry.md`
