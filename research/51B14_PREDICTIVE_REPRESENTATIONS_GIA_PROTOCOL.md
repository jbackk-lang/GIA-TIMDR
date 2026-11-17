# 51B.14 — predykcyjnie istotne reprezentacje i protokół oceny GIA

Data: 2026-11-17. Status: **definicje i prerejestracja projektu eksperymentu**. Bez wykonanych nowych testów, bez deklaracji nowości twierdzeń klasycznych.

## 0. Teza podlegająca falsyfikacji

Minimalny stan predykcyjny S=ε(H)=P(F|H) zachowuje rozkład wybranej przyszłości F. Nie musi zachowywać historii ani pełnych reprezentacji M/S, G, K, META. Nowa hipoteza TIMDR: niektóre jawnie zdefiniowane obserwable przyszłości mogą mieć zwarte reprezentacje wyznaczalne ze stanu S, a operator GIA może je przybliżać efektywniej niż dobrane kontrole.

## 1. Definicje

H — obserwowana historia do chwili decyzji; F — przyszłość (jej horyzont, jednostka czasu i sigma-ciało ustalone przed eksperymentem); Y_b=ψ_b(F) — cel predykcyjny gałęzi b∈{MS,G,K,META}. Zakładamy standardowe przestrzenie borelowskie i istnienie regularnych rozkładów warunkowych.

**Pełna wystarczalność predykcyjna** R(H): P(F|R)=P(F|H) p.n.

**Wystarczalność dla zadania b** R_b(H): P(Y_b|R_b)=P(Y_b|H) p.n.

**Minimalny stan dla zadania** S_b(H)=P(Y_b|H). Jest funkcją S(H), ponieważ P(Y_b|H) jest obrazem P(F|H) przez ψ_b. Odwrotność nie musi zachodzić.

**Reprezentacja predykcyjnie istotna w sensie słabym**: R_b(H) osiąga przewagę predykcyjną nad bezwarunkową bazą P(Y_b), mierzoną poprawnym scoring rule na niezależnym teście. Sama niekonstantność R_b nie wystarcza.

**Reprezentacja przybliżenie wystarczająca**: jej nadwyżkowe ryzyko predykcyjne względem idealnego P(Y_b|H) jest ≤δ_b, dla wcześniej ustalonego δ_b. Zależnie od scoring rule nadwyżka może odpowiadać KL lub innej dywergencji.

**Faktoryzacja przez S**: R_b(H)=r_b(S(H)) p.n. zachodzi wtedy i tylko wtedy, gdy R_b jest stała p.n. na klasach predykcyjnie równoważnych historii (ściślej: jest mierzalna względem σ(S), z dokładnością do null sets). Faktoryzacja nie implikuje wystarczalności. Dla S_b faktoryzacja zachodzi z konstrukcji.

**Uwaga o gałęziach**: oryginalna cecha historyczna G lub K może nie faktoryzować przez S; jej predykcyjny odpowiednik może faktoryzować, jeśli zostanie zdefiniowany jako funkcja przyszłego rozkładu. Należy wskazać konkretną obserwablę Y_b; nie nazywać dowolnej funkcji S „geometrią” bez znaczenia operacyjnego.

## 2. Metryka GIA

Z=C_GIA(H) (kod/stan uzyskany z historii, bez informacji przyszłej). Idealna strata względem pełnej historii:
Δ_F(Z)=E_H[KL(P(F|H)||P(F|Z))]≥0, z wartością +∞ dopuszczalną. Δ_F=0 ⇔ P(F|H)=P(F|Z) p.n. Dla zmiennych dyskretnych przy skończonych entropiach Δ_F=I(F;H|Z)=I(F;H)-I(F;Z); **nie zakładać bezwarunkowo tych równości dla nieskończonych / ciągłych przypadków bez odpowiednich warunków**.

Dla każdego Y_b: Δ_b(Z)=E[KL(P(Y_b|H)||P(Y_b|Z))]. Jeśli Z jest funkcją H, Δ_b≥0. Praktycznie estymować różnicę out-of-sample log-loss (lub inną ściśle właściwą regułę punktacji), z niepewnością po niezależnych jednostkach. Estymator może być ujemny wskutek błędu modelowania/skończonej próby; nie jest wtedy dowodem „ujemnej utraty informacji”.

**Oddzielne osie oceny**:
- Predykcja: log-loss, Brier score (klasyfikacja), CRPS (ciągłe rozkłady), kalibracja i właściwe miary domenowe.
- Kompresja: bity po kodowaniu, liczba stanów, wymiar, pamięć robocza i koszt obliczeń (raportowane oddzielnie); liczba cech ≠ liczba bitów.
- Odporność: wariancja po seedach i jednostkach, shift domeny, missingness, szum, zmiana zegara.
- Pareto: jakość–koszt; „przewaga GIA” tylko wobec dobranych kontroli przy porównywalnym budżecie.

## 3. Eksperyment porównawczy — syntetyczny, z prawdą odniesienia

**Dane A: Markow 2 stany.** X_t∈{0,1}, P(X_{t+1}=X_t)=0.9; H=(X_0,…,X_t), F=(X_{t+1},…,X_{t+k}). Znany stan wystarczający X_t. Zestawić pełną historię, ostatni symbol, losowy wybór zdarzeń, PCA/GIA w wersji zamrożonej, klasyczny enkoder liniowy, prosty model rekurencyjny. Cel: GIA nie powinien być uznany za nowatorski, jeśli tylko odzyskuje oczywisty stan X_t.

**Dane B: HMM 2 stany ukryte.** Z_t Markow, obserwacje X_t emitowane z szumem; stan referencyjny to posterior P(Z_t|H), dla ustalonych znanych parametrów. Kontrole: filtr Bayesa (oracle), histogram ostatnich k obserwacji, PCA, GIA, RNN/GRU o porównywalnym budżecie. Mierzyć KL do rozkładu przyszłości, błąd estymacji posterioru i długość kodu. Sprawdzać, czy GIA nie odrzuca informacji ważnej dla posterioru.

**Dane C: zdarzenia i zegary.** Reżim wpływa na czasy oczekiwania; obserwacje w sekundach vs indeksie zdarzeń bez odstępów. Osobne cele: czas do następnego zdarzenia i następny znacznik. T1: odwracalne przelabelowanie zegara (kontrola zerowa); T2: utrata odstępów; T3: oś kątowa ze zmienną prędkością. Przy T1 porównywać te same sigma-ciała informacji i cele; nie interpretować zmiany parametrów numerycznych jako przyrostu informacji.

**Dane D: i.i.d. Bernoulli.** Stan referencyjny stały. Kontrola negatywna: każda pozorna przewaga reprezentacji historycznej na niezależnym teście to artefakt estymacji, wycieku lub nadmiernego dopasowania.

## 4. Operacjonalizacja M/S, G, K, META

Dla każdej gałęzi przed treningiem zdefiniować Y_b:
- MS: przyszła amplituda/tempo zdarzeń albo sygnał w określonym horyzoncie.
- G: przyszła własność trajektorii lub krzywizna zdefiniowana dla obserwowalnej rodziny trajektorii; nie udawać, że pojedynczy przebieg ma automatycznie operator kształtu.
- K: przyszła energia pasmowa, rozkład fazy lub inne jawne wielkości modalne.
- META: przyszła zmiana reżimu z określonym horyzontem i kosztem fałszywego alarmu.
Porównywać R_b i S_b; nie wymagać rekonstrukcji historycznych pełnych widm/kształtów.

## 5. Split, baseline, protokół

1. Prerejestracja generatorów, parametrów, horyzontów, progów δ_b i seedów przed wynikiem.
2. Train/validation/test na **niezależnych trajektoriach** (nie na sąsiednich oknach tej samej trajektorii); dodatkowo osobny shift test.
3. Wszelkie skalery, PCA, selekcje i strojenie wyłącznie na train/validation. Frozen reference dla GIA, jeśli formalne własności tego wymagają.
4. Identyczne obserwacje, zegary, metadane, horyzonty, dostęp do informacji i budżet tuningowy w porównywanych modelach.
5. Kontrole: oracle gdy dostępny, historia pełna, minimalny znany stan, ostatnia obserwacja, losowy wybór, PCA, GIA, prosty RNN/GRU. Raportować każdą porażkę.
6. Wyniki: średnie, przedziały ufności bootstrapem po trajektoriach, wykres Pareto strat predykcyjnych vs koszt, kalibracja; metryki informacyjne tylko z uzasadnionym estymatorem.
7. Bramka sukcesu: na co najmniej jednym prerejestrowanym niebanalnym procesie GIA ma dać niższą stratę lub niższy koszt przy równoważnej stracie od odpowiednio dopasowanej kontroli, replikowalne na niezależnych seedach i shift test. Nie wywodzić uniwersalności z jednego sukcesu.

## 6. Co uznajemy za rezultat

**Potwierdzone formalnie:** istnienie i minimalność klasycznego stanu predykcyjnego pod założeniami; faktoryzacja stanów zadaniowych S_b przez S; kontrprzykład i.i.d. dla pełnych cech historycznych.

**Otwarte:** czy istnieją użyteczne, interpretowalne predykcyjne projekcje gałęzi TIMDR; czy GIA aproksymuje S lub S_b lepiej od kontroli; czy Chronoproces pomaga poza odwracalnym przelabelowaniem.

**Bez roszczeń:** nie ogłaszać nowego twierdzenia o stanach przyczynowych ani przewagi GIA przed przeprowadzeniem eksperymentów i przeglądem literatury.
