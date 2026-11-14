# TIMDR — identyczne trójki, różne relacje, różna przyszłość (2026-11-14)

Eksperyment rzeczywiście wykonany lokalnie, seed 202611140821. N=5000, trening 3200, test 1200. Każdy proces zawiera 4 identyczne trójki (-1,+1,0.05 s), odstępy będące permutacją [9,16,25] próbek. Przyszłość wynika z pobudzania tłumionego oscylatora q[t+1]=2r cos(ω)q[t]-r²q[t-1]+u[t], r=.975, ω=.31. Cel: stan za 12 próbek z szumem .03; pomocnicze dwa pomiary stanu z szumem .12. Regresja Ridge(alpha=.1).

| Cechy | R² | RMSE |
|---|---:|---:|
| Same trójki | -.000049 | .228986 |
| Trójki + posortowane odstępy | -.000049 | .228986 |
| Trójki + uporządkowane odstępy | .238611 | .199803 |
| Dwa pomiary stanu | .577251 | .148881 |
| Pomiary + trójki + relacje | **.744342** | **.115779** |
| Pomiary + przemieszane relacje | .577006 | .148924 |
| Oracle: prawdziwa dynamika i czasy | .983681 | — |

Wszystkie 6 permutacji wystąpiło. Kontrola przemieszania relacji znosi korzyść. **Nie wykonano jeszcze automatycznej filtracji trójek**: sprawdzono informacyjną wartość relacji, a nie działający operator filtrujący. Trójki są zadanymi identycznymi zdarzeniami, nie wykrytymi z sygnału. Jeden generator i seed, bez CI. Wynik nie dowodzi uniwersalnej ontologii trójek ani uniwersalnej kompresji. Kod i stdout są lokalnymi artefaktami rozmowy.