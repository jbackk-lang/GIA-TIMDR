# TIMDR: relacje, homometria i test przyczynowy — 2026-11-14

## Konstrukcja
Dwa zbiory lokalnych zdarzeń A={0,1,4,10,12,17} i B={0,1,8,11,13,17} są homometryczne: mają taki sam multizbiór odległości parami. Dlatego dla impulsów o wspólnej amplitudzie i tle stałym mają dokładnie takie samo widmo mocy FFT. W obu klasach globalna trójka (MIN,MAX,t_MAX−t_MIN) jest taka sama dla każdej **sparowanej** realizacji o identycznym przesunięciu i amplitudzie. Odstępy kolejnych zdarzeń wynoszą A=[1,3,6,2,5], B=[1,7,3,2,4].

Przebieg długości 96, losowe położenie początku 10..64, losowy poziom dolny U(-1.5,-.5), górny U(.5,1.5). 3000 trening, 1500 test obserwacyjny i 1500 test interwencyjny; ziarno 405. W trybie obserwacyjnym pamięć M jest równa klasie relacji H. W trybie interwencyjnym M jest losowane niezależnie od H. Przyszły sygnał Y=0.8(2M−1)+N(0,.45). Klasyfikacja znaku Y, StandardScaler+LogisticRegression.

## Faktyczne pomiary
```
global_triple observational 0.4947
global_triple intervention 0.5073
power observational 0.5167
power intervention 0.4713
ordered_gaps observational 0.9647
ordered_gaps intervention 0.49
full_signal observational 0.5553
full_signal intervention 0.5033
actual_memory observational 0.9647
actual_memory intervention 0.9653
observational history_memory_agreement 1.0 mean_future_M1 0.7962 mean_future_M0 -0.7731
intervention history_memory_agreement 0.502 mean_future_M1 0.8095 mean_future_M0 -0.7893
exact_pair_power_difference 2.842170943040401e-14
exact_pair_triplets [-1.0,1.0,10] [-1.0,1.0,10]
gaps [1,3,6,2,5] [1,7,3,2,4]
paired_effect_memory_follows_relation 1.6
paired_effect_memory_held_fixed 0.0
```

## Eksperyment kontrfaktyczny
Dla identycznego szumu przyszłości porównano zamianę wzorca A→B w dwóch mechanizmach. Gdy pamięć jest ustawiana przez relację M:=H, średni skutek zmiany relacji na przyszły sygnał wynosi 1.6. Gdy pamięć jest utrzymana na M=0, skutek wynosi dokładnie 0. To odróżnia zmianę informacji w reprezentacji od zmiany stanu, przez który może ona działać.

## Ograniczenia
**Mechanizm przyczynowy jest zaprojektowany przez eksperymentatora**, a nie odkryty w przyrodzie. Nie wykazano, że abstrakcyjna informacja jest autonomiczną siłą; przyczynowy wpływ wynika z fizycznie interpretowalnego stanu pamięci M w równaniu generatora. W danych nie ma szumu obserwacji przeszłego przebiegu, braku próbek ani nieznanego zegara. Pełny sygnał zawiera wystarczającą informację do rozróżnienia klas, lecz liniowa regresja bez niezmienniczości przesunięcia słabo generalizuje — 55.5% nie oznacza braku informacji. Losowe amplitudy i przesunięcia są niezależne od klasy, więc globalne trójki i widma są informacyjnie nierozróżnialne w rozkładzie, ale **nie każda niesparowana próbka** ma identyczne wartości tych cech. Wypisany w skrypcie parametr max_global_triplet_pair_difference porównuje niesparowane średnie i nie jest testem homometrii.

## Interpretacja dla TIMDR
Zachowujemy lokalne trójki MIN–MAX–CZAS. Relacje pomiędzy zdarzeniami mogą kodować stan pamięci i dzięki temu przewidywać przyszły sygnał. O przyczynowości decyduje jednak mechanizm przenoszenia relacji do stanu dynamicznego, nie sama obecność informacji w opisie.

## Następny krok
Wprowadzić rzeczywisty układ z pamięcią (np. filtr z histerezą albo obwód RC z przełączanym stanem) i przeprowadzić randomizowaną interwencję na historii przy kontroli aktualnego stanu i energii, bez programowania odpowiedzi bezpośrednio z etykiety.
