# TIMDR: niezmienniki porządku i metryki czasu — 2026-11-14

## Cel
Rozdzielić relacje niezmienne na dowolne ściśle rosnące przekształcenia zegara od relacji zależnych od skali i nieliniowości zegara. Nie zmieniamy definicji lokalnej trójki MIN–MAX–CZAS; badamy relacje pomiędzy trzema zdarzeniami.

## Metoda
Klasa 0: odstępy czasu źródłowego [24,48], klasa 1: [48,24]. Początek procesu losowy U(15,65). Każdy przykład ma trzy uporządkowane zdarzenia. Trening 6000 na zegarze tożsamościowym; testy po 3000, ziarna 12 i 42. Zegary: tożsamościowy; afiniczny at+b, a>0; potęgowy 200(t/200)^p z p=exp(U(-.45,.45)) albo p=exp(U(-2.2,2.2)); skrajny potęgowy z p losowanym z {.025,.1,10,40}. Wszystkie transformacje ściśle rosnące dla t>0.

Cechy: proporcja pierwszego odstępu do sumy; dwa surowe odstępy; znak różnicy odstępów; wyłącznie porządek E1<E2<E3. Każda reprezentacja osobno: StandardScaler + LogisticRegression(max_iter=1000). Etykieta jest klasą generatora, nie niezależnym pomiarem przyszłości.

## Wyniki rzeczywistego uruchomienia
```
TEST identity fraction_gap_order_reversed_vs_source 0.0
ratio 1.0
raw_gaps 1.0
gap_order 1.0
event_order 0.5
TEST affine fraction_gap_order_reversed_vs_source 0.0
ratio 1.0
raw_gaps 1.0
gap_order 1.0
event_order 0.5
TEST mild fraction_gap_order_reversed_vs_source 0.0
ratio 1.0
raw_gaps 1.0
gap_order 1.0
event_order 0.5
TEST strong fraction_gap_order_reversed_vs_source 0.141
ratio 0.859
raw_gaps 0.859
gap_order 0.859
event_order 0.5
TEST adversarial fraction_gap_order_reversed_vs_source 0.286
ratio 0.714
raw_gaps 0.714
gap_order 0.714
event_order 0.5
NONIDENTIFIABILITY source_A [0.0,1.0,3.0] source_B [0.0,2.0,3.0] observed_both [0.0,1.0,2.0]
AFFINE_INVARIANCE_EXAMPLE 0.6666666666666666 0.6666666666666666
```

## Wniosek matematyczny
Jeśli t1<t2<t3 i f jest ściśle rosnąca, to f(t1)<f(t2)<f(t3). Jednak nierówność (t2-t1)<(t3-t2) **nie musi** przetrwać takiego f. Proporcja R=(t2-t1)/(t3-t1) jest niezmienna dla f(t)=at+b, a>0, ale nie dla ogólnego nieliniowego f. W naszym generatorze sam porządek trzech zdarzeń jest identyczny dla obu klas, dlatego osiąga 50% mimo pełnej niezmienniczości. Niezmienniczość nie implikuje informacyjnej wystarczalności.

Przykład nieidentyfikowalności: dwa różne źródłowe zestawy czasów [0,1,3] i [0,2,3] mogą zostać odwzorowane ściśle rosnącymi, odmiennymi zegarami na tę samą obserwację [0,1,2]. Bez niezależnego zegara nie da się odzyskać źródłowych proporcji.

## Ograniczenia
To eksperyment na dokładnych znacznikach czasu, bez surowego sygnału i detekcji ekstremów. Nie testuje predykcji fizycznej ani nie dowodzi pełnej teorii TIMDR. Nieliniowy zegar może być w praktyce ograniczony niezależnym odniesieniem lub modelem kalibracyjnym. Test skrajny jest celowo poza rozkładem treningowym.

## Kolejny test
Włączyć rzeczywistą detekcję trójek w szumie i porównać: porządek zdarzeń, proporcje odstępów, wspólny niezależny znacznik czasu i kalibrację zegara. Sprawdzić, które relacje pozostają predykcyjne po zmianie zegara.
