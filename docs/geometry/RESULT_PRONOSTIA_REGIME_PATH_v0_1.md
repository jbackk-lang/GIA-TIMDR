# RESULT — PRONOSTIA: droga reżimu wzdłuż życia łożyska, v0.1

Pre-rejestracja: `PREREG_PRONOSTIA_REGIME_PATH_v0_1.md` (commit 85ea96b, przed cechami 11 łożysk eval). Jedno uruchomienie.
Liczby: `RESULT_PRONOSTIA_REGIME_PATH_v0_1.json`. Po zamrożeniu: jeden plik (Bearing1_4/acc_01279) był pusty po przerwanym
pobieraniu — przywrócony z repozytorium (`git diff` bez innych różnic); metoda bez zmian.

| Hipoteza | Wynik | Werdykt |
|---|---|---|
| H1: D spada wzdłuż życia (pole → cząsteczka), ρ ≤ −0,3 | 9/11 łożysk | **SUPPORTED** |
| H2: −ρ_D > ρ_RMS (mediany) | 0,52 vs −0,64 | **SUPPORTED** (zastrzeżenie niżej) |
| H3: powrót D na końcu (≥ 1,2 × minimum) — fala | 7/11 | **SUPPORTED** |
| H4: sito z kotwicą słabsze od D (reguła wykonalności, N_cyk ≈ 15) | ρ_Q 0,14 vs 0,52 | **SUPPORTED** |

Przewidywanie bez werdyktu: remis D z kurtozą — potwierdzony (0,52 vs 0,48).

## Zastrzeżenia
- H2 porównuje trendy ze znakiem. W wartości bezwzględnej RMS ma silniejszy trend (mediana |ρ| 0,67 vs 0,52), ale
  **niespójny kierunek**: rośnie w 3 łożyskach, maleje w 6 (docieranie). D ma spójny kierunek w 9/11, kurtoza w 10/11.
  Przewaga D polega na spójności kierunku, nie na sile trendu.
- D jest miarą impulsowości obwiedni i zachowuje się jak kurtoza — nie jest od niej lepszy. Wkład TIMDR to interpretacja
  trajektorii (pole → cząsteczka → fala) i przewidywanie powrotu D na końcu, które się potwierdziło (7/11).
- Jedno łożysko (Bearing2_3) nie przechodzi przez reżim cząsteczki (ρ_D = 0,03) — kurtoza też nie rośnie.

## Wniosek
Przewidywania wynikające z budowy modelu przeszły na nieoglądanych łożyskach: degradacja przesuwa sygnał z reżimu pola
do reżimu cząsteczki, a pod koniec życia w większości łożysk z powrotem w stronę fali. Reguła wykonalności trafnie
przewidziała słabość sita z kotwicą przy krótkim oknie (0,1 s).
