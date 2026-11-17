# 51B.15 — informacja predykcyjna, transfer i benchmark GIA

Data: 2026-11-17. Status: dowód tożsamości teorioinformacyjnej i **projekt benchmarku**, bez uruchomienia testów. Dokument uzupełnia 51B.13 i 51B.14; nie dowodzi nowości ani skuteczności GIA.

## 1. Twierdzenie: strata predykcyjna = warunkowa informacja wzajemna

Niech H,F,Z będą zmiennymi losowymi w przestrzeniach standardowych borelowskich, a Z=C(H) będzie mierzalną deterministyczną funkcją historii. Przy regularnych rozkładach warunkowych definiujemy
Δ_pred(C)=E_{H,Z}[D_KL(P(F|H)||P(F|Z))].
Wtedy

**Δ_pred(C) = I(F;H|Z) ∈ [0,+∞].**

Dowód: z definicji warunkowej informacji wzajemnej jako średniej KL,
I(F;H|Z)=E_{H,Z}[D_KL(P(F|H,Z)||P(F|Z))].
Ponieważ Z jest funkcją H, P(F|H,Z)=P(F|H) prawie na pewno. Podstawienie daje równość, również dla wartości +∞. W szczególności Δ=0 wtedy i tylko wtedy, gdy F i H są warunkowo niezależne przy Z, czyli Z jest wystarczający predykcyjnie.

Przy skończonych odpowiednich informacjach, reguła łańcuchowa daje
I(F;H)=I(F;Z)+I(F;H|Z),
a więc Δ_pred=I(F;H)-I(F;Z).
**Nie odejmować +∞−+∞.**

Dla celu zadaniowego Y_b=ψ_b(F) analogicznie
Δ_b(C)=I(Y_b;H|Z).
Z zasady przetwarzania danych Δ_b≤Δ_pred (dla odpowiednio określonych rozkładów).

Uwaga: wzór jest klasyczną konsekwencją teorii informacji, nie nowym twierdzeniem TIMDR. Estymatory informacji wzajemnej dla ciągłych, wielowymiarowych procesów mogą być obciążone; w eksperymencie stosować również out-of-sample właściwe reguły punktacji.

## 2. Transfer: dwa różne pytania

Niech E oznacza środowisko: RPM, obciążenie, urządzenie, czujnik lub domenę. Reprezentację C i predyktor q(F|Z) trenujemy tylko w środowiskach źródłowych.

**Wystarczalność w środowisku e:** Δ_e(C)=I_e(F;H|Z). Wartość 0 oznacza brak utraty informacji w danym środowisku, ale nie zapewnia wspólnego predyktora.

**Stabilność mechanizmu predykcyjnego:** czy P_e(F|Z) pozostaje takie samo między środowiskami, na wspólnym nośniku Z? W przeciwnym razie ten sam Z może wymagać adaptacji modelu.

**Transfer bez dostrajania:** wytrenować q_source(F|Z), zamrozić C i q_source, ocenić na niewidzianym e. Raportować source i target log-loss, kalibrację, różnicę target−source, a także oracle target (wyłącznie diagnostycznie, nie jako wdrożony predyktor).

**Dekompozycja:** target cross-entropy nad idealnym P_target(F|H) można rozbić na utratę reprezentacji Δ_target(C) i niedopasowanie q_source do P_target(F|Z), gdy odpowiednie oczekiwania są skończone. Nie utożsamiać błędu transferu wyłącznie z utratą informacji przez kompresję.

**Kontrole:** shift warunków przy niezmiennym mechanizmie; shift samego mechanizmu; shift nośnika; ukryta zmienna środowiska. Podać jawnie, kiedy nie można identyfikować Δ_target z danych.

## 3. Benchmark GIA: minimalna wersja rozstrzygająca

### A. Generatory
1. Markow (znany minimalny stan = ostatni symbol): sanity check.
2. HMM z emisją zaszumioną (stan referencyjny = posterior ukrytego stanu): rzeczywista kompresja historii.
3. Proces odnowy z ukrytym reżimem i różnymi czasami oczekiwania: informacja o zegarze zdarzeń.
4. I.i.d. Bernoulli (stan stały): kontrola negatywna.
5. Proces fazowy/obrotowy z różnym RPM i szumem: kontrolowany transfer osi czasu i warunków pracy.

### B. Metody
- Oracle predictive state / Bayes filter, jeśli znany.
- Pełna historia z porównywalnym predyktorem.
- Ostatni symbol / okno długości k.
- Losowa selekcja zdarzeń (taki sam budżet reprezentacji).
- PCA / liniowa redukcja wymiaru.
- **GIA frozen-reference** zgodny z implementacją referencyjną, bez dopisywania mu nieistniejących własności.
- Prosty RNN/GRU lub inny sekwencyjny baseline z porównywalnym tuningiem.
- Ablacje: GIA bez geometrii, GIA bez informacji zegara, GIA z różną pojemnością kodu.

### C. Protokół
1. Ustalić H,F, horyzont, zegar i metadane; zamrozić generatory i progi przed pomiarami.
2. Podzielić po niezależnych trajektoriach/urządzeniach; train, validation, source test, **unseen-environment test**.
3. Zamrozić skalery, PCA, GIA, model predykcyjny i progi po walidacji; na target brak dostrajania.
4. Zrównać wejścia, dostęp do RPM, długość historii, liczbę prób strojenia i budżet obliczeń.
5. Metryki: log-loss i kalibracja, estymowana Δ_pred / Δ_b tam gdzie oracle, liczba bitów po kodowaniu, RAM, czas, stabilność i transfer gap.
6. Raportować Pareto strata–bity–koszt i osobno transfer; nie zastępować wszystkich metryk jedną arbitralną sumą.
7. Niepewność: bootstrap po niezależnych trajektoriach/maszynach; powtórzenia seedów, negatywne wyniki i awarie.
8. Bramka sukcesu: prerejestrowana przewaga Pareto GIA nad PCA/losową selekcją i co najmniej jedną mocną kontrolą sekwencyjną na HMM lub procesie zdarzeń, z replikacją na nowym środowisku. Sukces jednego generatora nie oznacza uniwersalności.

### D. Kontrprzykłady i testy falsyfikacyjne
- I.i.d.: GIA nie może zdobyć rzeczywistej przewagi predykcyjnej.
- Odwracalne przelabelowanie zegara: brak zysku informacji; możliwy zysk numeryczny.
- Różne P_e(F|Z) mimo Δ_e=0: lokalna wystarczalność bez transferu wspólnego modelu.
- Selekcja geometryczna pomija rzadki, lecz silnie predykcyjny sygnał: Δ_pred>0, mimo wysokiej geometrycznej spójności.

## 4. Granice interpretacji
- Małe empiryczne log-loss nie dowodzi małej prawdziwej informacji warunkowej bez kalibracji/odpowiedniego estymatora.
- „Kompresja” wymaga raportowania rzeczywistego kosztu kodowania, nie tylko liczby cech.
- Dodatnia Δ_e nie obala użyteczności aplikacyjnej GIA, ale obala bezstratność predykcyjną w danym środowisku.
- Transfer zależy także od mechanizmu i obserwowalności środowiska, nie tylko od reprezentacji.
- Przed roszczeniem nowości: zestawić z computational mechanics, predictive state representations, information bottleneck i domain generalization.
