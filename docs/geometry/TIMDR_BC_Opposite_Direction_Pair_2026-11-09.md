# TIMDR — przeciwbieżne helisy BC

**Data:** 2026-11-09  
**Status:** konstrukcja i testy dokładne w arytmetyce wymiernej; CI uruchomione.

## 1. Konstrukcja

Używamy dokładnej mapy śrubowej BC z `core/boerdijk_coxeter_tetrahelix.py`:
`p' = p R + t`, z `cos(theta)=-2/3` i osiowym krokiem `-2/sqrt(5)` w jednostkowym wektorze osi.

Budujemy dwie różne orbity:
- A: iteracje mapy BC (S), start w wierzchołku (p_A=(1,1,1));
- B: iteracje mapy odwrotnej (S^{-1}), start w punkcie (p_B) po przeciwnej stronie osi, na tej samej prostopadłej do osi i na tej samej współrzędnej osiowej.

Oś ma kierunek (u=(2,1,0)), a punkt osi (a=(0,0,-2/5)). Projekcja (p_A) na oś:
[
q=a+u,rac{(p_A-a)cdot u}{ucdot u}=(6/5,3/5,-2/5).
]
Punkt drugiego startu to odbicie radialne:
[
p_B=2q-p_A=(7/5,1/5,-9/5).
]
To daje dokładny kąt fazowy (pi), bez wprowadzania niewymiernych współrzędnych.

## 2. Niezmienniki dokładne

Obie orbity leżą na tym samym walcu:
[
r_A^2=r_B^2=54/25.
]
Mają tę samą współrzędną osiową na starcie, ale przeciwne kroki osiowe:
[
Delta z_A=-2,qquad Delta z_B=+2
]
przy współrzędnej osiowej mierzonej iloczynem skalarnym z (u=(2,1,0)). Są to przeciwne kierunki osiowe; jednostkowy krok wynosi odpowiednio (mp2/sqrt5).

Wektory radialne startu są dokładnie przeciwne, więc przesunięcie fazowe wynosi (pi).

## 3. Testy skończonych odcinków

Dla każdej nici wygenerowano 65 punktów dokładnych (64 kroki):
- 0 wspólnych punktów pomiędzy próbkami obu nici;
- 0 przecięć pomiędzy 64 × 64 parami odcinków łamanych, sprawdzonych dokładnym rachunkiem wymiernym;
- promień walca zachowany dokładnie;
- przeciwne przesunięcia osiowe zachowane dokładnie.

To potwierdza, że w badanym skończonym przybliżeniu mamy dwie rozłączne, przeciwbieżne nici śrubowe na tym samym walcu, z fazą początkową (pi).

## 4. Interpretacja topologiczna — ostrożnie

To nie jest jeszcze dowód, że dwie nici tworzą węzeł lub splot. Są otwarte i nieograniczone; klasyczna liczba splątania (linking number) jest zdefiniowana dla zamkniętych krzywych. Brak przecięć w skończonej próbce nie dowodzi braku przecięć dla wszystkich indeksów ani nie daje automatycznie typu topologicznego.

Ciekawy rezultat geometryczny: jedna helisa BC i jej dokładna kopia biegnąca w przeciwną stronę, ale z fazą (pi), tworzą naturalny model dwuniciowy. Następny krok to zdefiniować jawny sposób domknięcia końców (albo okresowy warunek brzegowy), a następnie sprawdzić, czy domknięcie jest ciągłe, bez samoprzecięć, i jaki ma typ splotu.

## 5. Reprodukcja

Uruchom:
`python experiments/bc_opposite_direction_pair.py`

CI:
https://github.com/jbackk-lang/GIA-TIMDR/actions

Kod wykorzystuje dokładne `Fraction`, nie przybliżenia zmiennoprzecinkowe. Nie wnioskuje o fizycznej sile wiążącej ani o mechanizmie oddziaływania między nićmi.


## 6. Korekta interpretacji kierunku

„Przeciwny kierunek” oznacza tutaj zastosowanie odwrotnej mapy afinicznej (S^{-1}): odwracają się jednocześnie znak obrotu i znak postępu osiowego. Iloraz (d\phi/dz), a więc geometryczna chiralność helisy jako nieorientowanej krzywej, pozostaje taki sam. To są dwie fazowo przesunięte o (pi) nici o tej samej chiralności geometrycznej, parametryzowane w przeciwnych kierunkach, a nie para helis o przeciwnych chiralnościach.

Wynik CI pierwszej wersji ujawnił błędną asercję: dla fazy (pi) radialne wektory są antyrównoległe, zatem ich iloczyn wektorowy jest zerowy. Poprawiono test na:
- iloczyn skalarny radialnych wektorów = (-54/25);
- kwadrat normy ich iloczynu wektorowego = (0);
- dokładnie przeciwne wektory radialne.

Dedykowany workflow zakończył się powodzeniem:
https://github.com/jbackk-lang/GIA-TIMDR/actions/runs/42603894043

Log potwierdza: 65 punktów na każdej nici, promień² (54/25), kroki osiowe (-2,+2), 0 wspólnych punktów oraz 0 przecięć w 4096 parach odcinków.

## 7. Co ten model mówi, a czego nie mówi

W obecnej konstrukcji nici są po przeciwnych stronach tej samej osi i zachowują stały kąt fazowy (pi) na każdej wspólnej wysokości. Są to dwie rozłączne, równoległe fazowo orbity na wspólnym walcu. Nie tworzą automatycznie klasycznego splotu dwóch zamkniętych krzywych. Następny sensowny eksperyment to zmienić relację fazową i/lub chiralność jednej nici niezależnie, a następnie badać, czy można uzyskać zamknięcie bez przecięć.


## 8. Drugi eksperyment: przeciwna chiralność, nie tylko odwrotny przebieg

Rozdzielamy dwa znaczenia „przeciwnych kierunków”:

1. **Odwrotna parametryzacja**: (S^{-1}) odwraca jednocześnie znak obrotu i przesuwu osiowego. Geometryczna chiralność krzywej pozostaje taka sama. To przetestowała pierwsza para.
2. **Przeciwna chiralność**: sprzęgamy mapę (S) odbiciem lustrzanym (M) w płaszczyźnie zawierającej oś śruby. Nowa mapa (MSM) zachowuje znak przesuwu osiowego, ale odwraca znak obrotu wokół osi.

Dodano drugi dokładny eksperyment:
`experiments/bc_opposite_chirality_pair.py`.

Obie nici startują na tym samym walcu, z tym samym promieniem i z przeciwległymi fazami. W odróżnieniu od pierwszego testu, teraz mają ten sam postęp osiowy, ale przeciwną chiralność. Skrypt bada dokładnie 65 punktów każdej nici i wszystkie pary 64×64 odcinków łamanych. Wynik przecięć jest raportowany, a nie zakładany z góry.

To rozróżnienie jest ważne dla hipotezy o strukturze dwuniciowej: przeciwna parametryzacja nie jest tym samym co przeciwna chiralność. Dopiero drugi model może odpowiadać intuicji dwóch lustrzanych, przeciwskrętnych nici.

CI dla obu eksperymentów:
https://github.com/jbackk-lang/GIA-TIMDR/actions
