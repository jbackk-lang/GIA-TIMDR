# TIMDR — zmiana pamięci kontra zmiana wymuszenia (2026-11-14)

Model: z[t+1]=α_t z[t]+u_t, 64 próbki, 1200 przebiegów na klasę i poziom szumu. Bazowe α~U(.78,.93), u~U(-.05,.05), z0~U(-.5,.5); skok τ∈{28,...,45}. Zmiana α: |δα|~U(.055,.12); zmiana u: |δu|~U(.035,.09). Szum obserwacji σ=.005,.02,.05. Ziarno 20261114. Bazowe parametry estymowane OLS z pierwszych 18 próbek, skan zmian 28..45 i penalizacja 2.8σ²log(64). Próg heurystyczny, bez osobnej walidacji.

| σ | Prawda | Przewidziano α | Przewidziano u | Przewidziano brak | Trafność |
|---|---|---:|---:|---:|---:|
| .005 | α | 607 | 456 | 137 | 50.58% |
| .005 | u | 177 | 1023 | 0 | 85.25% |
| .005 | brak | 54 | 83 | 1063 | 88.58% |
| .020 | α | 500 | 374 | 326 | 41.67% |
| .020 | u | 315 | 885 | 0 | 73.75% |
| .020 | brak | 182 | 192 | 826 | 68.83% |
| .050 | α | 325 | 413 | 462 | 27.08% |
| .050 | u | 277 | 910 | 13 | 75.83% |
| .050 | brak | 349 | 268 | 583 | 48.58% |

## Identyfikowalność
Dla każdej obserwowanej trajektorii i dowolnego alternatywnego α'[t] można skonstruować u'[t]=z[t+1]−α'[t]z[t]. Bez ograniczeń na mechanizm wymuszenia nie da się odróżnić pamięci od oddziaływania. Nawet przy jednym skoku rozróżnienie może być trudne, gdy stan z jest mały i sygnał zaszumiony.

## Ograniczenia
Generator syntetyczny, jeden skok, znany zakres skanowania, różne skale interwencji, szum w regresorze OLS, brak osobnej walidacji progu. Ten podtest nie obejmuje wykrywania lokalnych trójek MIN–MAX–Δt; dotyczy identyfikowalności mechanizmu, nie potwierdzenia praw TIMDR ani nowej siły fizycznej. Pełny uruchomiony kod lokalny: `alpha_vs_forcing.py`.

## Następny krok
Losowo pobudzać układ znanym impulsem diagnostycznym i sprawdzić, czy dodatkowa informacja o odpowiedzi pomaga odróżnić zmianę α od zmiany u.