# GEOMETRY_TIME_MAPPING_FREEZE — H(t_i, s_j) -> H_i v0.1

## Status

Implementacyjnie zamknięta jest wyłącznie warstwa redukcji z jawnie
przypisanych znaczników czasu wierzchołków do jednego H_i na czas.
Nie jest to założenie o kolejności indeksów siatki i nie obejmuje
empirycznego potwierdzenia konkretnego źródła danych.

## 1. Wejście

Dane mają postać dwóch równoległych wektorów:

```text
vertex_times[j]      = rzeczywisty czas przypisany do punktu j
vertex_h_values[j]   = H(t_j, s_j) dla tego punktu
```

oraz jawnej, rosnącej osi:

```text
time_grid = [t_0, ..., t_{N-1}]
```

## 2. Redukcja

Dla każdego t_i:

```text
V_i = { j : vertex_times[j] == t_i }
H_i = mean( H_j : j in V_i, H_j finite )
```

Porównanie czasu jest dokładne (`rtol=0`, `atol=0`). Nie ma interpolacji,
nearest-neighbour, resamplingu ani wnioskowania czasu z indeksu wierzchołka.

## 3. Brak danych

Jeżeli dla t_i nie ma żadnej skończonej wartości H, funkcja rzuca
`ValueError`: czas jest **invalid, nie zero**.

## 4. Własności

- redukcja jest niezależna od kolejności wierzchołków;
- każdy H_i pochodzi wyłącznie z punktów jawnie przypisanych do t_i;
- dalsza agregacja do Lambda_G używa tej samej partycji bloków co META;
- operator Lambda_G nie wybiera ani nie modyfikuje tej osi czasu.

## 5. Implementacja

```text
`TIMDR-Geometry-Formalism/timdr_geometry/geometry_meta_alignment.py::surface_to_time_h_trace`
```

## 6. Granica zamknięcia

B2 może traktować przejście `H(t_i,s_j) -> H_i` jako CLOSED na poziomie
interfejsu, pod warunkiem że caller dostarcza rzeczywiste `vertex_times`.
To freeze nie jest twierdzeniem, że każdy konkretny dataset ma już
zweryfikowane takie przypisanie.
