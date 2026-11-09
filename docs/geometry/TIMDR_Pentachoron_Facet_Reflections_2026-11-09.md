# TIMDR — odbicia faset regularnego pięciościanu 4D (pentachoronu)

**Data:** 2026-11-09  
**Status:** dokładny model wymierny, eksperyment dodany do CI.

## Dlaczego pentachoron?

Słowo „pięciościan” bywa niejednoznaczne: może oznaczać dowolną bryłę o pięciu ścianach, np. ostrosłup czworokątny. Naturalnym odpowiednikiem czworościanu w następnym wymiarze jest jednak **pentachoron**, czyli regularny 4-simpleks: ma 5 wierzchołków i 5 tetraedrycznych faset. To właśnie ten obiekt jest badany w tym eksperymencie.

## 1. Dokładna konstrukcja

Wierzchołki umieszczamy w czterowymiarowej podprzestrzeni sum-zero przestrzeni (mathbb Q^5):
[
v_i=e_i-rac15(1,1,1,1,1),quad i=1,ldots,5.
]
Wtedy:
[
v_icdot v_i=rac45,qquad v_icdot v_j=-rac15quad(i
e j).
]
Faseta przeciwległa do (v_i) leży w hiperpłaszczyźnie (v_icdot x=-1/5). Odbicie ma dokładną postać:
[
s_i(x)=x-rac52left(v_icdot x+rac15ight)v_i.
]
To afiniczna izometria czterowymiarowej podprzestrzeni; wszystkie współczynniki są wymierne.

## 2. Wynik dla par odbić

Dla dowolnych dwóch różnych faset:
[
rac{v_icdot v_j}{|v_i||v_j|}=-rac14.
]
Złożenie dwóch odbić jest obrotem w pewnej dwuwymiarowej płaszczyźnie, pozostawiającym punktowo prostopadłą dwuwymiarową podprzestrzeń 4D. Kąt obrotu spełnia:
[
cos	heta=2left(rac14ight)^2-1=-rac78.
]
Wszystkie 10 par faset daje ten sam cosinus obrotu. Ponieważ (-7/8
otin{0,pm1/2,pm1}), z twierdzenia Nivena kąt nie jest wymierną wielokrotnością (pi). Każdy taki dwufasetowy obrót ma więc nieskończony rząd.

## 3. Enumeracja słów odbić

Zredukowane słowo nie zawiera sąsiednich powtórzeń generatora (bo (s_i^2=I)). Dokładna enumeracja daje:

| Długość | Słowa zredukowane | Różne mapy afiniczne |
|---:|---:|---:|
| 1 | 5 | 5 |
| 2 | 20 | 20 |
| 3 | 80 | 80 |
| 4 | 320 | 320 |
| 5 | 1280 | 1280 |

W badanym zakresie nie ma kolizji map afinicznych. To skończony wynik obliczeniowy, nie dowód wolności całej grupy.

## 4. Porównanie z czworościanem

Dla regularnego 3-simpleksu (czworościanu) analogiczny iloczyn dwóch odbić faset ma:
[
cos	heta_3=-rac79.
]
Dla regularnego 4-simpleksu (pentachoronu):
[
cos	heta_4=-rac78.
]
Wzorzec dla regularnego (d)-simpleksu to:
[
oxed{cos	heta_d=rac{2}{d^2}-1}.
]
Dla (dge3) wartości te są wymierne i — poza szczególnymi niskowymiarowymi przypadkami — nie należą do dozwolonego zbioru Nivena, co daje nieokresowe obroty w płaszczyznach 2D.

## 5. Interpretacja i ograniczenia

Pentachoron nie tworzy „helisy w zwykłej przestrzeni 3D” wprost. Jego naturalna geometria jest czterowymiarowa. Iloczyn dwóch odbić daje obrót w płaszczyźnie 2D wewnątrz 4D, z dwuwymiarową przestrzenią punktów stałych. Jest to analog mechanizmu obrotowego z czworościanu, ale osadzony w wyższym wymiarze.

Nie wykazano jeszcze, że pentachoron tworzy odpowiednik helisy BC, węzła ani fraktala. To wymaga zdefiniowania rekurencji w 4D i sposobu projekcji do 3D. Projekcja może tworzyć pozorne przecięcia, których nie ma w 4D.

## 6. Reprodukcja

`python experiments/pentachoron_facet_reflections.py`

Kod: `experiments/pentachoron_facet_reflections.py`  
CI: `.github/workflows/pentachoron-reflections.yml`
