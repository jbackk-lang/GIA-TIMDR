# Plan interpretacji pilota G/H/R

**2026-11-14. Status:** przed wykonaniem. Skrypt: [pilot_ghr.py](pilot_ghr.py).

## Pytanie
Czy różne manipulacje w generatorze (G), kanale (H) i odbiorniku (R) prowadzą do podobnych zmian cech geometrycznych obserwacji? Czy pojedyncza obserwacja pozwala przypisać przyczynę?

## Uruchomienie
```bash
python -m pip install numpy
python docs/research/info_geometry/pilot_ghr.py > pilot_ghr_output.csv
```

Program tworzy siedem wierszy BASE, G, H, R, GH, GR, ALL. Ma stałe ziarno losowe, ale **jeden przebieg nie daje oszacowania niepewności ani zdolności klasyfikacji**.

## Jak czytać wyniki
- Porównać każdy wariant z BASE; nie zakładać, że większa krzywizna oznacza więcej informacji.
- Jeśli H lub R zmienia krzywiznę bez zmiany źródła, jest to bezpośredni przykład niejednoznaczności interpretacji.
- Jeśli G i H lub G i R dają podobne wartości cech, same te cechy mogą nie rozstrzygać pochodzenia zmiany.
- Różne wartości cech nie dowodzą identyfikowalności w ogólnym przypadku.

## Ograniczenia pilota
Wariant G korzysta z tego samego ziarna innowacji, ale zmienia parametr AR. Kanał jest filtrem liniowym, odbiornik obcinaczem amplitudy; to uproszczenia. Skrypt nie implementuje testu statystycznego, nie używa wielu niezależnych sesji i nie bada fizycznej natury informacji. Skręt geometryczny nie jest w nim jeszcze liczony. Kolejny etap: replikacje wielosesyjne, modele klasyfikujące G/H/R i pomiar referencyjny przed odbiornikiem.

## Rejestr wyników
**Nie wykonano tutaj pomiaru.** Po uruchomieniu należy zapisać wyjście CSV, wersję Python/NumPy, commit oraz interpretację, również gdy wyniki są negatywne.
