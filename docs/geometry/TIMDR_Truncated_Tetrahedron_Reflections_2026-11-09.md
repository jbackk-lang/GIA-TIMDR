# TIMDR — odbicia pięciościennego czworościanu ściętego

**Data:** 2026-11-09  
**Model:** regularny czworościan z jednym ściętym wierzchołkiem  
**Status:** dokładna arytmetyka wymierna; eksperyment w CI.

## 1. Bryła, o którą chodzi

To nie pentachoron 4D. Badamy zwykłą bryłę 3D powstałą przez odcięcie jednego wierzchołka regularnego czworościanu płaszczyzną równoległą do przeciwległej ściany. Powstaje pięć ścian:
- dwa trójkąty równoległe (pozostała ściana bazowa i nowa ściana cięcia);
- trzy czworokąty (ścięte dawne ściany boczne).

Wierzchołki wyjściowego czworościanu:
[
A=(1,1,1),quad B=(1,-1,-1),quad C=(-1,1,-1),quad D=(-1,-1,1).
]
Parametr (qin(0,1)) oznacza część długości krawędzi od (A), na której wykonujemy cięcie:
[
A_q^B=A+q(B-A),quad A_q^C=A+q(C-A),quad A_q^D=A+q(D-A).
]
Płaszczyzna cięcia jest:
[
x+y+z=3-4q.
]
Dla przykładu (q=1/2) nowe wierzchołki to dokładnie ((1,0,0),(0,1,0),(0,0,1)).

## 2. Pięć płaszczyzn odbicia

Numeracja generatorów w skrypcie:
- (s_0): pierwotna ściana przeciwległa do ściętego wierzchołka, (x+y+z=-1);
- (s_1): nowa ściana cięcia, (x+y+z=3-4q);
- (s_2): (x-y-z=-1);
- (s_3): (-x+y-z=-1);
- (s_4): (-x-y+z=-1).

Pierwsza ważna różnica względem zwykłego czworościanu: (s_0) i (s_1) są odbiciami względem dwóch różnych, równoległych płaszczyzn. Ich złożenie nie jest obrotem, tylko translacją.

Jej wektor (dla kolejności (s_0circ s_1)) ma długość:
[
L(q)=rac{8(1-q)}{sqrt3}.
]
Dla (q=1/2):
[
ec t=(-4/3,-4/3,-4/3),quad L=4/sqrt3.
]

Pozostałe 9 par płaszczyzn przecina się. Każda para daje obrót o kącie (	heta), dla którego:
[
cos	heta=-rac79.
]
Zatem pary generatorów dają **9 obrotów i 1 translację**. Pojawia się więc jawny mechanizm translacyjny, którego nie ma w rodzinie czterech ścian pierwotnego czworościanu.

## 3. Złożenia wielu odbić przy (q=1/2)

Wszystkie obliczenia wykonano dokładnie na ułamkach wymiernych. Słowa są zredukowane, tzn. nie mają sąsiednich powtórzeń tego samego odbicia.

| Długość słowa | Słowa | Różne mapy afiniczne | Kolizje słów |
|---:|---:|---:|---:|
| 1 | 5 | 5 | 0 |
| 2 | 20 | 20 | 0 |
| 3 | 80 | 80 | 0 |
| 4 | 320 | 320 | 0 |
| 5 | 1280 | 1280 | 0 |
| 6 | 5120 | 5102 | 18 |
| 7 | 20480 | 20372 | 108 |
| 8 | 81920 | 81242 | 678 |

Pierwsze dokładne kolizje różnych zredukowanych słów pojawiają się na długości 6. Przykładowo:
[
(0,2,0,1,2,0)quad	ext{i}quad(1,2,0,1,2,1)
]
dają tę samą mapę afiniczną dla (q=1/2). Jest to konkretna relacja w działaniu generatorów, a nie przybliżona bliskość.

Typy map dla parzystych długości (liczone po usunięciu duplikatów):
| Długość | Translacje | Obroty | Ruchy śrubowe |
|---:|---:|---:|---:|
| 2 | 2 | 18 | 0 |
| 4 | 8 | 192 | 120 |
| 6 | 50 | 1608 | 3444 |
| 8 | 266 | 12576 | 68400 |

Zatem wielokrotne odbicia generują nie tylko obroty i translacje, ale też ruchy śrubowe. Głębokość cięcia wpływa na przesuw osiowy ruchów śrubowych.

## 4. Szczególne proporcje cięcia — rezonanse zerowego skoku

Dla każdego parzystego słowa macierz obrotu jest niezależna od (q), natomiast część translacyjna zależy liniowo od (q). Można więc dokładnie obliczyć składową przesunięcia wzdłuż osi obrotu (skok śruby). Szukamy wartości (q), dla których ten skok znika. Wtedy ruch śrubowy przechodzi w czysty obrót.

W długości 6 znaleziono:
| Proporcja cięcia (q) | Liczba zredukowanych słów o zerowym skoku |
|---:|---:|
| (1/4) | 72 |
| (1/3) | 108 |
| (1/2) | 36 |

W długości 8 pojawia się już 25 różnych wymiernych proporcji rezonansowych:
[
egin{aligned}
&1/11, 1/10, 1/7, 1/6, 2/11, 1/4, 2/7, 1/3, 3/8,\
&2/5, 3/7, 7/16, 5/11, 1/2, 7/13, 6/11, 11/20,\
&4/7, 3/5, 5/8, 7/11, 9/14, 11/17, 2/3, 7/10.
end{aligned}
]
Są to wartości, dla których co najmniej jedno zredukowane słowo długości 8 ma dokładnie zerowy skok osiowy. Liczności słów dla każdej proporcji są drukowane przez skrypt.

To jest najciekawszy wynik eksperymentu: **głębokość cięcia działa jak parametr sterujący skokiem ruchów śrubowych, a określone wymierne proporcje wywołują dokładne rezonanse geometryczne**.

Uwaga: „zerowy skok” oznacza czysty obrót, a nie automatycznie zamkniętą orbitę. Kąt obrotu nadal może być niewymierną wielokrotnością pełnego obrotu.

## 5. Co to znaczy dla hipotezy TIMDR?

W zwykłym czworościanie cztery płaszczyzny odbicia nie zawierają pary równoległej. Po ścięciu jednego wierzchołka pojawia się piąta płaszczyzna i para równoległych ścian. To dodaje generator translacji. Połączenie translacji z obrotami daje ruchy śrubowe, a proporcja ścięcia steruje ich skokiem.

Możliwy dalszy kierunek:
1. znaleźć rodziny słów, których skok zeruje się dla tych samych proporcji (q);
2. sprawdzić, czy ich osie obrotu mają wspólną geometrię (przecinają się, są równoległe lub tworzą układ przestrzenny);
3. zbadać, czy kilka takich ruchów tworzy zamknięte krzywe lub sploty po dodaniu jawnego warunku domknięcia;
4. dopiero potem badać projekcje/fraktalne granice.

To jest wynik geometryczny modelu odbić. Nie dowodzi jeszcze fizycznej siły wiążącej ani mechanizmu natury.

## 6. Reprodukcja

`python experiments/truncated_tetrahedron_reflections.py`

Kod: `experiments/truncated_tetrahedron_reflections.py`  
Workflow: `.github/workflows/truncated-tetrahedron-reflections.yml`


## 7. Walidacja CI

Dedykowany workflow zakończył się powodzeniem:
https://github.com/jbackk-lang/GIA-TIMDR/actions/runs/42605654030

Uruchomienie potwierdziło:
- geometrię pięciu ścian i incydencję wierzchołków;
- 9 obrotów o cosinusie (-7/9) i jedną translację dla par ścian;
- dokładne liczności map i kolizji słów do długości 8;
- typy izometrii dla długości parzystych;
- wszystkie wymienione wymierne rezonanse zerowego skoku na długościach 6 i 8.

Wynik CI: **success**.


## 8. Czy rezonanse zerowego skoku są orbitami zamkniętymi?

Sprawdzono dokładne cosinusy kątów obrotu dla rezonansów długości 6:
| (q) | Cosinus obrotu | Liczba słów |
|---:|---:|---:|
| (1/4) | (-79/81) | 72 |
| (1/3) | (-631/729) | 72 |
| (1/3) | (-151/729) | 36 |
| (1/2) | (-79/81) | 36 |

Żadna z tych wartości nie należy do ({0,pm1/2,pm1}). Z twierdzenia Nivena wynika, że kąty nie są wymiernymi wielokrotnościami (pi). Są to więc czyste obroty nieskończonego rzędu, a nie okresowe obroty zamykające orbitę po skończonej liczbie iteracji.

To rozdziela dwa zjawiska:
- **rezonans skoku**: znika przesunięcie wzdłuż osi śruby;
- **rezonans okresowy**: kąt obrotu jest wymierną wielokrotnością pełnego obrotu.

Znaleźliśmy pierwsze, ale nie drugie. Samo wyzerowanie skoku nie wystarcza do otrzymania zamkniętej krzywej.


Pełny test po dodaniu widma kątów rezonansowych również zakończył się powodzeniem:
https://github.com/jbackk-lang/GIA-TIMDR/actions/runs/42605904137
