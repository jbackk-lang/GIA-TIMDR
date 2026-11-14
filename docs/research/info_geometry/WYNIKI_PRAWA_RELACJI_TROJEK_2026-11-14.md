# TIMDR: prawo relacji trzech lokalnych trójek — 2026-11-14

## Cel
Sprawdzić, czy relacje pomiędzy zdarzeniami zawierają informację nieobecną w samych lokalnych trójkach (MIN, MAX, podpisane Δt). Nie zwiększać wymiarowości jednostki zdarzenia.

## Konstrukcja i metoda
Sygnał 256 próbek. Trzy podobne lokalne zdarzenia: ujemny impuls Gaussa (amplituda -1.6), po siedmiu próbkach dodatni (+1.6); szerokość 1.5; szum Gaussa σ=.055. Klasa 0: odstępy między początkami zdarzeń [24,48], klasa 1: [48,24]. Początek losowany niezależnie od klasy w [24,104]. Przekształcenie zegara: f(t)=(t/255)^p, p=exp(U(-.55,.55)), ściśle rosnące. W wariancie trudnym dwa dodatkowe impulsy losowego znaku i amplitudy 0.35..0.85.

Detektor nie zna położeń zdarzeń: po trzypróbkowym wygładzeniu wyszukuje lokalne minima poniżej -.8, a następnie lokalne maksima powyżej +.8 w oknie 4..11 próbek. Bierze pierwsze trzy wykryte zdarzenia. Każde ma dokładnie trzy współrzędne: (MIN, MAX, podpisane Δt obserwowanego zegara). Relacja trzech trójek jest wyrażona przez znormalizowane dwa odstępy między początkami zdarzeń; do klasyfikacji podaje się obie części sumujące się do jedności. To **krawędzie relacyjne**, nie nowe współrzędne zdarzenia.

Porównanie: globalna trójka; trzy lokalne trójki (9 cech); bezwzględne odstępy między zdarzeniami (2); znormalizowane relacje (2); trójki+relacje (11). Modele: StandardScaler + LogisticRegression. Trening 3000 przykładów; testy po 1500: zwykły, nieliniowy zegar, nieliniowy zegar z dwoma dodatkowymi impulsami, kontrola negatywna z losową etykietą niezależną od sygnału. Ziarna 301..305. Kod uruchomiony lokalnie jako `triplet_relation_laws.py`.

## Faktyczne wyniki
```
SET ordinary detected 1.0 mean_candidates 3.0
SET clock_warp detected 1.0 mean_candidates 3.0
SET clock_warp_distractors detected 0.9727 mean_candidates 2.994
SET negative_control detected 1.0 mean_candidates 3.0
RESULT global ordinary 0.4813
RESULT global clock_warp 0.5107
RESULT global clock_warp_distractors 0.506
RESULT global negative_control 0.5067
RESULT triplets ordinary 0.498
RESULT triplets clock_warp 0.5127
RESULT triplets clock_warp_distractors 0.516
RESULT triplets negative_control 0.4887
RESULT gap_absolute ordinary 1.0
RESULT gap_absolute clock_warp 1.0
RESULT gap_absolute clock_warp_distractors 0.986
RESULT gap_absolute negative_control 0.4827
RESULT relations ordinary 1.0
RESULT relations clock_warp 1.0
RESULT relations clock_warp_distractors 0.9867
RESULT relations negative_control 0.4827
RESULT triplets+relations ordinary 1.0
RESULT triplets+relations clock_warp 1.0
RESULT triplets+relations clock_warp_distractors 0.986
RESULT triplets+relations negative_control 0.4827
```

## Interpretacja i granice
Lokalne trójki same nie opisują przerw pomiędzy zdarzeniami, dlatego nie odróżniają obu klas. Znormalizowana relacja R=(t2-t1)/(t3-t1) pozwala odróżnić kolejność krótszego i dłuższego odstępu. W badanym zakresie monotonicznych nieliniowych zmian zegara różnica była odporna empirycznie. **Nie jest to ogólna niezmienniczość na dowolny monotoniczny warp**: takie przekształcenie może odwrócić relację wielkości odstępów. W szczególności R jest dokładnie niezmiennicze na dodatnie afiniczne zmiany czasu, ale nie na ogólną nieliniową zmianę czasu.

Przyszła etykieta jest w tym eksperymencie po prostu klasą generatora, a nie pomiarem niezależnie wygenerowanej przyszłości. Nie wolno nazywać wyniku dowodem fizycznej predykcji. Dodatkowe impulsy są słabsze od właściwych, co ułatwia detekcję. Wartość 98.7% dotyczy wyłącznie tej rodziny syntetycznych przebiegów.

## Następne badanie
Sprawdzić odporność relacji przy silniejszym warp, losowych brakach danych i fałszywych zdarzeniach o amplitudzie równej właściwym. Wprowadzić rozróżnienie między niezmiennikami porządku (zachowane przez każdy rosnący warp) i niezmiennikami proporcji czasu (zachowane tylko przez transformacje afiniczne). Następnie poszukać niezależnych danych rzeczywistych.
