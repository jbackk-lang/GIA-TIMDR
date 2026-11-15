# TIMDR — ukryte wymuszenie kontra pamięć (2026-11-14)

## Cel
Rozdzielić informację o stanie pamięci od nowego, ukrytego oddziaływania i sprawdzić, czy wysoka przewidywalność oznacza identyfikowalność parametrów.

## Metoda
Symulacja z[t+1]=α*z[t]+u, α~U(.82,.94), z0~U(.12,.55), u~N(0,.045) stałe w pojedynczej trajektorii. 10 000 niezależnych trajektorii, 6000 trening, 2000 walidacja (niewykorzystana do strojenia), 2000 test. Osiem obserwacji z[0:8] z szumem N(0,.012); cel z[9]+N(0,.018). Modele Ridge(alpha=.001) bez strojenia; porównano liczbę obserwacji 1,2,4,8 i kontrolę ze znanymi stanami. Parametry α i u estymowano przez OLS z kolejnych zaszumionych obserwacji. Ziarno 2026111409.

## Wyniki z uruchomienia
```
test 2000 forcing_std 0.043895783420421323 target_std 0.26152776994034693
initial_state R2 0.01918 RMSE 0.25901
initial_state_alpha R2 0.0478 RMSE 0.2552
probe_1 R2 0.01885 RMSE 0.25905
probe_2 R2 0.87268 RMSE 0.09332
probe_4 R2 0.97079 RMSE 0.0447
probe_8 R2 0.99229 RMSE 0.02296
probe_8_alpha R2 0.99272 RMSE 0.02231
probe_8_est_alpha_u R2 0.99231 RMSE 0.02294
oracle_state_alpha R2 0.99392 RMSE 0.02039
oracle_state_alpha_forcing R2 0.9944 RMSE 0.01958
alpha_est_mae 0.10381197625704794 u_est_mae 0.04351747419091388
same_first_two 0.25 0.26 alpha 0.82 forcing 0.055 next 0.2682
same_first_two 0.25 0.26 alpha 0.94 forcing 0.025 next 0.2694
do_u -0.04 z9 -0.1487209439331615
do_u 0 z9 0.0791195954572165
do_u 0.04 z9 0.30696013484759443
```

## Interpretacja
Dwa pierwsze obserwowane punkty z0=.25, z1=.26 dopuszczają wiele par (α,u), bo u=z1−αz0. Dwie przykładowe pary dają różne z2. Przy szumie oszacowanie α i u jest słabe, mimo że bezpośredni model predykcyjny na ośmiu obserwacjach osiąga R²=.99229. W tym zadaniu kolejne pomiary silnie zwiększają przewidywalność, ale nie dowodzą osobnej identyfikowalności obu parametrów. Kontrolowana zmiana u przy stałych z0=.25, α=.88 zmienia z9 od −.1487 do .3070.

## Ograniczenia
Wymuszenie jest stałe w czasie obserwacji i prognozy, co upraszcza zadanie. Model zna liniową rodzinę generatora, a prognoza dotyczy krótkiego horyzontu. To nie jest eksperyment wykrywania trójek MIN–MAX–Δt: dotyczy identyfikowalności ukrytego wymuszenia i pamięci, które będą potrzebne do interpretacji relacji trójek. Walidacja została odłożona, lecz nie służyła do wyboru hiperparametrów. Żadnych wniosków o nowej sile fizycznej.

## Następny test
Zmienny w czasie ukryty sygnał wymuszający, przełączanie u w losowej chwili i wykrywanie punktu zmiany; porównać wyjaśnienie przez pamięć z wyjaśnieniem przez zewnętrzne oddziaływanie.
