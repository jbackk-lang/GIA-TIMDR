# 54A.12 — Adaptacja przy zmianie optymalnego opóźnienia

32 768 bajtów, 64 segmenty po 512 bajtów, naprzemienne generatory lag 1/3/64 z 2% mutacji. Seed 5412. Decyzje przyczynowe, gzip level 9 całego strumienia reszt, round-trip zgodny.

| Metoda | Bajty | Wykryte granice | Średnie opóźnienie |
|---|---:|---:|---:|
| gzip | 3360 | — | — |
| statyczna | 5764 | — | — |
| adaptacyjna | 3910 | 63/63 | 24.29 |
| szybka | 4049 | 63/63 | 25.90 |

Wykrycie: 8 kolejnych wyborów właściwego predyktora. Trafność po granicach: adaptacyjna 95.28%, szybka 94.88%. Szybka nie poprawia kompresji ani czasu reakcji; oba predyktory gorsze niż gzip. Syntetyczny test adaptacji, nie pełna dynamika TIMDR. Brak narzutu nagłówka.

Uruchom: python 54A12_SWITCH.py
