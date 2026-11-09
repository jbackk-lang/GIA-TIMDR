# Dowód kąta skrętu: czworościan → konfiguracja sześcienna (problem otwarty v0.1)

**Data:** 2026-11-09  
**Status:** fakty geometrii klasycznej wyprowadzone; interpretacja jako skręt helisy TIMDR nierozstrzygnięta.  
**Cel:** rozstrzygnąć dowodami, czy kąt 90° jest docelowym obrotem modułu/ramy, czy tylko kątem dwuściennym sześcianu.

## 1. Dane geometryczne pewne

Dla regularnego czworościanu o boku (a), przyjmijmy dwa sąsiednie trójkątne ściany. Kąt dwuścienny wewnętrzny (alpha_T) spełnia:
[
\cos\alpha_T=\frac13,qquad
\alpha_T=\arccos(1/3)\approx70.5287793655^\circ.
]
Kąt między zewnętrznymi normalnymi do tych ścian jest kątem dopełniającym do (180^\circ):
[
\beta_T=180^\circ-\alpha_T=\arccos(-1/3)
\approx109.4712206345^\circ.
]
Dla sześcianu kąt dwuścienny wewnętrzny wynosi:
[
\alpha_C=90^\circ.
]
Zatem:
[
\alpha_C-\alpha_T\approx19.4712206345^\circ,
\qquad
\alpha_C-\beta_T\approx-19.4712206345^\circ.
]
Wartość bezwzględna różnicy jest taka sama, lecz znak zależy od tego, czy porównujemy kąty wewnętrzne, czy kierunki normalnych. Nie wolno pominąć tej konwencji orientacji.

## 2. Czego te fakty NIE dowodzą

Kąt dwuścienny jest własnością pary ścian bryły. Nie jest automatycznie:
- obrotem modułu trójkątnego wzdłuż osi helisy;
- kątem skrętu ramy normalnej;
- torsją Freneta krzywej;
- fazą helisy;
- całkowitym skrętem pasma;
- kątem kardynalnym TIMDR.

Z samego faktu, że czworościan ma kąt dwuścienny 70.53°, a sześcian 90°, nie wynika, że helisa wykonuje obrót o 19.47° ani że 90° jest jej progiem. Potrzebny jest operator przenoszący orientację jednego modułu na następny.

## 3. Kandydacki model przenoszenia orientacji

Niech moduł (n) ma zorientowaną ramę (F_n\in SO(3)). Reguła przejścia między modułami jest obrotem:
[
F_{n+1}=F_n R_n,qquad R_n\in SO(3).
]
Jeśli przejście wynika ze sklejenia dwóch płaszczyzn trójkątnych wzdłuż wspólnej krawędzi, (R_n) musi być wyprowadzony z:
1. wektora wspólnej krawędzi;
2. normalnych obu modułów;
3. konwencji orientacji i strony odbicia;
4. ewentualnego dodatkowego obrotu wokół wspólnej krawędzi.

Sam kąt między normalnymi określa tylko część obrotu. Nie ustala całej macierzy (R_n), dopóki nie określimy osi i znaku obrotu.

Dla ciągu modułów holonomia po zamkniętym cyklu wynosi:
[
R_{\rm loop}=R_0R_1\cdots R_{m-1}.
]
Warunek domknięcia ramy wymaga (R_{\rm loop}=I), ewentualnie jawnej permutacji/identyfikacji modułów na szwie. Właśnie ta wielkość może być kandydatem na mierzalny „skręt całkowity” modułowej helisy. Nie należy zastępować jej sumą kątów bez sprawdzenia nieprzemienności obrotów 3D.

## 4. Hipotezy do rozstrzygnięcia

- **H1 — kąt wewnętrzny:** źródłem jest przejście od (alpha_T=70.5288°) do (90°); przyrost to (+19.4712°).
- **H2 — normalne zewnętrzne:** źródłem jest przejście od (eta_T=109.4712°) do (90°); zmiana to (-19.4712°).
- **H3 — obrót modułu:** 90° jest niezależnym kątem obrotu modułu, a kąty brył są jedynie ograniczeniami geometrycznymi.
- **H4 — holonomia:** 90° jest kątem resztkowego obrotu ramy po cyklu; wynika z iloczynu macierzy przejść, nie z pojedynczego kąta dwuściennego.
- **H5 — próg kardynalny:** zdarzenia kardynalne pojawiają się przy zmianie kąta przekraczającej 90°. Ta hipoteza wymaga niezależnej definicji kąta lokalnego i testu, czy próg jest ostry/stabilny.

Żadnej z H1–H5 nie uznajemy obecnie za potwierdzoną.

## 5. Minimalny program dowodowy

### P1 — ustalić prymityw geometryczny
Zidentyfikować, co w TIMDR ma kąt: ściana/moduł, krawędź wspólna, normalna, lokalna rama osi czy wektor styczny. Ustalić orientację i znak.

### P2 — wyprowadzić macierz przejścia
Zbudować współrzędne bazowego trójkąta i jego odbicia. Wyznaczyć (R_n) dokładnie, nie dopasowywać numerycznie kąta do 90°.

### P3 — porównać bryły odniesienia
Obliczyć kąty dwuścienne i macierze przejścia dla konfiguracji czworościennej oraz sześciennej przy tej samej konwencji orientacji. Sprawdzić, czy 90° jest kątem pojedynczego przejścia, czy tylko kątem między ścianami.

### P4 — zbadać ciąg modułów
Policzyć (R_{\rm loop}), jego kąt osiowy i znak. Porównać wynik dla odbicia lewego/prawego, odwrócenia kolejności i różnych sklejeń.

### P5 — sprawdzić punkty kardynalne
Jeśli lokalny kąt (	heta(s)) jest zdefiniowany, badać zdarzenia (	heta(s)=90°) oraz przekroczenia (	heta(s)>90°). Punkt kardynalny musi być stabilny względem próbkowania, parametryzacji i małych perturbacji; samo arbitralne przecięcie progu nie wystarcza.

### P6 — dowód/falsyfikacja
- Jeśli wynik 90° wynika dokładnie z iloczynu przejść i nie zależy od parametryzacji, jest kandydatem na niezmiennik konstrukcji.
- Jeśli zmienia się przy zmianie triangulacji, odbicia lub sklejenia, nie jest uniwersalną własnością helisy.
- Jeśli 90° występuje tylko dlatego, że wpisano kąt sześcianu jako wejście, eksperyment jest kołowy i nie stanowi dowodu.
- Jeśli brak jednoznacznego operatora moduł→moduł, twierdzenie pozostaje niedookreślone.

## 6. Punkty kardynalne „powyżej 90°”

Zapisujemy jako przypomnianą hipotezę autora: punkty kardynalne mogą odpowiadać zdarzeniom, w których kąt skrętu przekracza 90°. Nie utożsamiamy tego jeszcze z kątem dwuściennym sześcianu. Do dowodu trzeba zdefiniować ciągłą funkcję kąta (	heta(s)), orientację znaku oraz regułę wykrywania przejścia przez próg. Sprawdzić osobno (90°), (>90°) i kąt obrócony modulo (360°).

## 7. Decyzja badawcza

Wstrzymać używanie „720°” i „faza 1–0–1” jako ustalonych cech tej konstrukcji. Nie wpisywać 19.4712° jako kąta skrętu helisy, dopóki P1–P4 nie wyprowadzą operatora przejścia. Zachować 70.5288°, 90° i 109.4712° jako klasyczne punkty odniesienia z jawną konwencją.

**Wniosek:** klasyczna geometria dostarcza dokładnych kątów odniesienia, ale nie rozstrzyga sama mechanizmu TIMDR. Rozstrzygnięcie wymaga wyprowadzenia zorientowanej macierzy przejścia modułów i holonomii ich cyklu.
