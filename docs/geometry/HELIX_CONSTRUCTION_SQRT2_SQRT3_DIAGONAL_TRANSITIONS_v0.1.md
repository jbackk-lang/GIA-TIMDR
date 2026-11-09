# Model konstrukcji helisy TIMDR: przekątne √2 i √3 jako dwa poziomy geometrii (v0.1)

**Data:** 2026-11-09  
**Status:** formalizacja hipotezy konstrukcyjnej autora; matematyczne relacje przekątnych są ścisłe, ich rola w helisie pozostaje do wykazania.

## 1. Interpretacja autora

Dwie analogiczne relacje geometryczne mają stanowić model konstrukcji helisy:

1. **Poziom płaski:** przejście od motywu trójkątnego do układu kwadratowego; przekątna kwadratu jednostkowego ma długość √2.
2. **Poziom przestrzenny:** przejście od motywu czworościennego do układu sześciennego; przekątna przestrzenna sześcianu jednostkowego ma długość √3.

Pierwiastki √2 i √3 nie są traktowane jako składniki sumy przybliżającej π. Reprezentują odpowiednio diagonalne połączenie dwóch i trzech prostopadłych kierunków. Złożenie tych dwóch poziomów ma być kandydatem na model konstrukcyjny helisy TIMDR.

## 2. Fakty matematyczne

Dla kwadratu o boku a:
[
d_2=\sqrt{a^2+a^2}=a\sqrt2.
]

Dla sześcianu o krawędzi a jego przekątna ściany wynosi a√2, a przekątna przestrzenna:
[
d_3=\sqrt{(a\sqrt2)^2+a^2}=a\sqrt3.
]

Dla a=1 otrzymujemy √2 i √3. To są dokładne twierdzenia Pitagorasa.

## 3. Ważne zastrzeżenie dotyczące nazw figur

Sama przekątna √2 należy do kwadratu, nie do trójkąta. Sama przekątna √3 należy do sześcianu, nie do czworościanu. Zatem sformułowanie „trójkąt → kwadrat” oraz „czworościan → sześcian” opisuje postulowane przejścia konstrukcyjne między motywami, a nie równość ani standardową transformację brył. Trzeba jawnie zdefiniować, jak trójkątny moduł generuje kwadratowy układ i jak moduł czworościenny generuje sześcienny układ.

Nie należy też utożsamiać przekątnej sześcianu z przekątną czworościanu. Regularny czworościan o krawędzi a ma wysokość a√(2/3), a odległość między przeciwległymi wierzchołkami nie jest przekątną sześcianu.

## 4. Kandydat na regułę konstrukcji helisy

Roboczo:
[
\text{moduł 2-kierunkowy}\xrightarrow{\text{diagonalizacja}}\sqrt2,
\qquad
\text{moduł 3-kierunkowy}\xrightarrow{\text{diagonalizacja}}\sqrt3.
]

Następnie trzeba zdefiniować operator składania:
[
\mathcal H=\mathcal C(\mathcal D_2,\mathcal D_3,\sigma,\varphi),
]
gdzie:
- \(\mathcal D_2\) i \(\mathcal D_3\) oznaczają dwa diagonalne przejścia;
- \(\sigma\) oznacza orientację/znak odbicia;
- \(\varphi\) oznacza regułę fazy lub obrotu;
- \(\mathcal C\) jest jeszcze nieznanym operatorem składania w helisę.

Nie zakładamy, że samo zestawienie długości √2 i √3 tworzy helisę. Musi istnieć jawna reguła kolejności, orientacji i sklejenia modułów, z której wynika krzywa przestrzenna.

## 5. Testy rozstrzygające

1. Zdefiniować bazowy trójkątny moduł i dokładną operację dołączenia czwartego wierzchołka / utworzenia kwadratowego układu.
2. Zdefiniować czworościenny moduł i dokładną operację osadzenia/rozszerzenia do sześciennego układu.
3. Ujednolicić skalę: wszystkie długości znormalizować do boku a=1.
4. Wyprowadzić macierze przejścia i orientację diagonalnych kierunków.
5. Złożyć oba przejścia w jedną sekwencję modułów; sprawdzić, czy powstaje niezerowy skręt, faza i oś.
6. Porównać odbicie lewo-/prawoskrętne i zachować znak orientacji.
7. Dopiero po uzyskaniu zamkniętej krzywej badać węzeł, redukcję 4→3 i punkty kardynalne.

## 6. Związek z analogią π idealne → π realizowane

Wcześniejsza analogia π idealne → π realizowane pozostaje interpretacją strukturalną. √2 i √3 są teraz kandydatami na dwa dokładne geometryczne kroki konstrukcji, które mogą opisywać przejście od idealnego układu do realizowanej przestrzennej konstrukcji. Nie twierdzimy, że √2+√3=π ani że którakolwiek z tych przekątnych sama przybliża π w sposób stanowiący operator redukcji.

## 7. Kryterium potwierdzenia

Model konstrukcji helisy otrzyma wsparcie dopiero wtedy, gdy jawna reguła składania modułów:
- generuje helikalną krzywą, a nie tylko zestaw długości;
- wyznacza wewnętrzną oś i ramę;
- daje mierzalną orientację i znak skrętu;
- jest stabilna względem zmiany skali;
- zachowuje wskazane informacje na szwach;
- wyjaśnia, w jaki sposób dwa diagonalne poziomy współdziałają.

**Wniosek:** √2 i √3 dają ścisłe, komplementarne wzorce diagonalizacji w 2D i 3D. Ich złożenie jest obiecującą hipotezą konstrukcji helisy, ale operator składania pozostaje brakującym elementem dowodu.
