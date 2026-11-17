# 51B.25 — kontrola skali operacyjnego GIAFilter

## Zakres

Przeczytano `filters/_vendor_senscore_gia_filter.py` z repozytorium. Uruchomiono lokalną rekonstrukcję logiki `GIAFilter.apply`, `_robust_axis` i `_pca_axis` (bezpośredni import oryginalnego modułu nie był wykonany). Wynik nie jest testem informacyjnym ani walidacją na danych rzeczywistych.

12 konfiguracji: 10 trafień na osi x (0..9), 1 odstający punkt w (5,y,0), y=1,3,10,50; `max_residual`=0.2,1,5. Dla `max_residual=5` odstający punkt jest zachowany dla wszystkich badanych y, w tym y=50. Dla `max_residual=1` jest odrzucany przy y=3,10,50. Dla `max_residual=0.2` jest odrzucany dla wszystkich y.

| max_residual | y | zachowane prawdziwe | zachowany odstający |
|---:|---:|---:|---|
| 0.2 | 1,3,10,50 | 10/10 | nie |
| 1.0 | 1 | 10/10 | tak |
| 1.0 | 3,10,50 | 10/10 | nie |
| 5.0 | 1,3,10,50 | 10/10 | tak |

**Interpretacja:** maksymalna reszta musi być kalibrowana względem skali i geometrii danych. Domyślna wartość 5 nie zapewnia uniwersalnego odrzucania odstających punktów. To obserwacja o selekcji przestrzennej, nie o `Delta`, `n_epsilon` ani przewadze predykcyjnej.

## Stan serii 51B

51B.18: kontrprzykład utraty informacji przez selekcję geometryczną. 51B.19: dokładny selektor predykcyjny jest optimum w porównywanej klasie. 51B.20–22: syntetyczny prior może pomagać albo szkodzić, zależnie od zgodności z procesem. 51B.23–24: integracja z referencyjną geometrią i kalibracją syntetyczną nie wykazuje uniwersalnej przewagi. 51B.25: operacyjna logika GIAFilter ma istotną zależność od skali.

**Wniosek końcowy:** nie ma dowodu przewagi predykcyjnej operacyjnego GIAFilter przy jednakowym budżecie reprezentacji i niezależnym teście. Dalszy test powinien użyć rzeczywistych danych i oryginalnego modułu, a nie mnożyć syntetyczne warianty.
