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
