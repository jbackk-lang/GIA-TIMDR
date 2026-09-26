# Drogowskazy TIMDR — jak zbudować program analizujący sygnał

TIMDR jest modelem do **budowania** programów analizy sygnałów: daje pojęcia, które podpowiadają konstrukcję,
i protokół, który mówi, czy konstrukcja naprawdę działa. Nie jest gotowym detektorem — operatory TIMDR użyte wprost
jako cechy nie dawały przewagi (tabela w README). Program zbudowany według drogowskazów dał najlepszy wynik na
najtrudniejszych danych (niżej).

## Drogowskazy

| Krok | Pytanie | Pojęcie TIMDR | Znany odpowiednik (do porównania) |
|---|---|---|---|
| 1. Pole | W jakiej przestrzeni sygnał ma strukturę? Czas × pasmo? Czas × kanał? | membrana = pole | spektrogram, bank filtrów |
| 2. Rezonans | Gdzie w polu coś powtarza się okresowo lub zgadza się między częściami pola? | rezonans (K: częstotliwość, faza) | widmo obwiedni, korelacja widmowa |
| 3. Sito | Co przepuścić, co odrzucić? | sito, którego oczka ustala rezonans | wybór pasma (kurtogram) |
| 4. Samokorekta | Czy sito ma się dopasować do hipotezy? | samokorekta; osobne oczka dla każdej hipotezy | filtr dopasowany |
| 5. Geometria | Czy kształt pola (grzbiet, krzywizna, rozciągłość) coś dodaje? | gałąź G, Chronoproces | cechy kształtu |
| 6. Test | Czy to działa na danych, których nie widziałeś? | protokół: rozwój → zamrożenie → jeden test | walidacja krzyżowa, holdout |

Zasady protokołu (z doświadczenia 2026-09): punkt odniesienia musi być **mocny** (dla łożysk: widmo obwiedni i kurtogram,
nie same statystyki); test na **innych jednostkach** niż uczenie (inne łożyska, maszyny); sprawdź **ślady akwizycji**
(np. inne przesunięcie DC w części plików SEU); przy **suficie** baseline'u wynik jest nierozstrzygnięty; kryteria i reguła
sufitu zapisane **przed** danymi; rozwój wolno robić na części danych, ocenę — raz, na części nieotwieranej.

## Przykład: sito rezonansowe dla łożysk (Paderborn, uszkodzenia naturalne)

Ścieżka pokazuje, że drogowskazy prowadzą, ale nie gwarantują — liczą się także ślepe uliczki:

1. **Membrana jako macierz korelacji kanałów** — w praktyce średnia korelacja; na SEU zależna od sesji nagrania
   ([wynik](geometry/RESULT_SEU_MULTICHANNEL_DIAGNOSTIC_v0.1.md)).
2. **Topologia (winding, crossing, phase winding) jako uzupełnienie** — SUPPORTED na sztucznych uszkodzeniach jednego
   łożyska ([wynik](geometry/RESULT_PADERBORN_VIBRATION_COMPLEMENT_v0.1.md)), bez efektu na uszkodzeniach naturalnych
   ([wynik](geometry/RESULT_PADERBORN_REAL_DAMAGE_v0.1.md)).
3. **Nałożenie pól drgań i prądów jako sito** — pola prądów rozmyły informację (NOT SUPPORTED, tamże).
4. **Pole pasm nośnych + mapa rezonansu + sito, którego oczka ustawia rezonans przy częstotliwości każdej hipotezy
   uszkodzenia** — w fazie rozwoju najlepsze z 3 wariantów; w jednorazowym teście na niewidzianych łożyskach i pomiarach
   **0,68** wobec 0,56 klasycznych i 0,61 obwiedni (SUPPORTED,
   [wynik](geometry/RESULT_PADERBORN_RESONANCE_SIEVE_v0.1.md)); w replikacji 0,65, lepsze od klasycznych i od kurtogramu
   (0,55), nad samą obwiednią przewaga za mała ([wynik](geometry/RESULT_PADERBORN_RESONANCE_SIEVE_REPLICATION_v0.2.md)).
5. **Geometria grzbietu rezonansu** (krzywizna średnia, rozciągłość) — nic nie dodała; most do G w tej postaci niepotwierdzony.

Gotowy program: `bearing_resonance_sieve.py` w
[TIMDR-Industrial-Predict](https://github.com/jbackk-lang/TIMDR-Industrial-Predict/blob/main/SITO_REZONANSOWE.md)
(CLI, testy, wynik identyczny z wersją walidowaną).

## Lista kontrolna przed ogłoszeniem wyniku

- [ ] Hipoteza, cechy, klasyfikator, progi i reguła sufitu zapisane w commicie przed danymi testowymi.
- [ ] Mocny punkt odniesienia z tej samej dziedziny.
- [ ] Test na jednostkach spoza uczenia; kontrola negatywna (permutacja etykiet) i pozytywna (syntetyczna).
- [ ] Jedno uruchomienie; każda poprawka po zamrożeniu opisana w wyniku.
- [ ] Wynik (każdy) wpisany do tabeli w README; twierdzenia w README sprawdzalne przez `claim_audit`.
