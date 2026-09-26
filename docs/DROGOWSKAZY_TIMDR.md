# Drogowskazy TIMDR — jak zbudować program analizujący sygnał

TIMDR jest modelem do **budowania** programów analizy sygnałów: daje pojęcia, które podpowiadają konstrukcję,
i protokół, który mówi, czy konstrukcja naprawdę działa. Nie jest gotowym detektorem — operatory TIMDR użyte wprost
jako cechy nie dawały przewagi (tabela w README). Program zbudowany według drogowskazów dał najlepszy wynik na
najtrudniejszych danych (niżej).

## Drogowskazy

| Krok | Pytanie | Pojęcie TIMDR | Znany odpowiednik (do porównania) |
|---|---|---|---|
| 0. Typ sygnału (hipoteza) | Czy sygnał sam jest widmem (wyraźne linie — **modalny**), czy informacja siedzi w widmie pola (modulacje pasm nośnych — **polowy**)? Modalny → pracuj na liniach (K, śledzenie, samonaprawa); polowy → buduj pole i sito; mieszany (np. turbina) → modalne ustawia zegar, polowe niesie uszkodzenie. Wskaźnik: `core/signal_character.py` | membrana / modalność | płaskość widma, analiza obwiedni |
| 1. Pole | W jakiej przestrzeni sygnał ma strukturę? Czas × pasmo? Czas × kanał? | membrana = pole | spektrogram, bank filtrów |
| 2. Rezonans | Gdzie w polu coś powtarza się okresowo lub zgadza się między częściami pola? | rezonans (K: częstotliwość, faza) | widmo obwiedni, korelacja widmowa |
| 3. Sito | Co przepuścić, co odrzucić? | sito, którego oczka ustala rezonans | wybór pasma (kurtogram) |
| 4. Samokorekta | Czy sito ma się dopasować do hipotezy? Czy model ma się sam przestroić do sygnału ([samonaprawa modelu modalnego](theory/TIMDR_Modal_Self_Repair.md))? | samokorekta; osobne oczka dla każdej hipotezy; most K ↔ Chronoproces | filtr dopasowany, śledzenie rzędów, PLL |
| 5. Geometria | Czy kształt pola (grzbiet, krzywizna, rozciągłość) coś dodaje? Zwiń pole w rurę: promień = obwiednia, kąt = faza, skręt = częstotliwość ([rura analityczna](theory/TIMDR_Analytic_Tube.md)) | gałąź G, Chronoproces | sygnał analityczny (Gabor), cechy kształtu |
| 6. Test | Czy to działa na danych, których nie widziałeś? | protokół: rozwój → zamrożenie → jeden test | walidacja krzyżowa, holdout |

Zasady protokołu (z doświadczenia 2026-09): punkt odniesienia musi być **mocny** (dla łożysk: widmo obwiedni i kurtogram,
nie same statystyki); test na **innych jednostkach** niż uczenie (inne łożyska, maszyny); sprawdź **ślady akwizycji**
(np. inne przesunięcie DC w części plików SEU); przy **suficie** baseline'u wynik jest nierozstrzygnięty; kryteria i reguła
sufitu zapisane **przed** danymi; rozwój wolno robić na części danych, ocenę — raz, na części nieotwieranej.

## Krok 0 — status hipotezy

Wskaźnik (`core/signal_character.py`): L = udział mocy w wąskich liniach widma, M = siła modulacji pasm nośnych;
modalny gdy L ≥ 0,5, polowy gdy L < 0,5 i M ≥ 8 (progi wstępne, ustalone 2026-09-27 przed testem turbiny).
Sprawdzenie wsteczne (po fakcie, nie dowód): drgania Paderborn → polowy (L 0,03–0,26), prądy silnika Paderborn → modalny
(L = 1,0), CWRU zdrowe → modalny (L 0,75), CWRU z uszkodzeniem bieżni → polowy (L 0,23; uszkodzenie zmienia charakter
sygnału). Budynek LANL: L = 0,02 — wbrew wcześniejszemu opisowi „modalny” szerokie rezonanse konstrukcji wskaźnik
widzi jako niemodalne, a próbkowanie 322 Hz nie pozwala policzyć M → nieokreślony. Przewidywanie zapisane przed danymi:
drgania łożyskowe turbiny Fraunhofer LBF — mieszane (linie wirnika + modulacje pasm przy uszkodzeniu).

## Krok 0 rozszerzony — mapa dualności (hipoteza, 2026-09-27)

Analogia z przejściem fotonu przez szczelinę (J. Kielich), oparta na tej samej matematyce Fouriera (Δt·Δf ≥ 1/4π,
most Fouriera M/S↔K) — **nie** twierdzenie o fizyce kwantowej. Trzy osie w `core/signal_character.py`:
**falowość** L (moc w wąskich liniach), **cząsteczkowość** P (udział energii obwiedni powyżej 1 kHz w najsilniejszych 5%
chwil; szum ≈ 0,20, ton ≈ 0,05; próg 0,3), **rytm** M (modulacja pasm nośnych; próg 8).

| Etykieta | Warunek | Znaczenie |
|---|---|---|
| falowy | L ≥ 0,5, P < 0,3 | linie widma, faza — pracuj na liniach (K) |
| cząsteczkowy | P ≥ 0,3, M < 8 | pojedyncze, nieregularne uderzenia |
| pakiet falowy | P ≥ 0,3, M ≥ 8, L < 0,5 | cząstki w rytmie — tu sito ma działać najlepiej |
| mieszany (fala + pakiet) | P ≥ 0,3, M ≥ 8, L ≥ 0,5 | linie + rytmiczne uderzenia (np. turbina) |
| polowy (modulowany szum) / szumowy | P < 0,3 | modulacje bez wyraźnych cząstek / brak struktury |

Właściwość sprawdzona testem: **ściśle okresowy** ciąg uderzeń ma widmo z samych linii, więc jest jednocześnie falą
i pakietem; poślizg 1% (jak w łożysku) rozmywa linie i zostaje czysty pakiet falowy.

Sprawdzenie wsteczne (po fakcie): CWRU zdrowe → **falowy** (P 0,15); bieżnia wewnętrzna → mieszany (P 0,41);
zewnętrzna → **pakiet falowy** (P 0,69); kulka → pakiet falowy (P 0,35) — uszkodzenie zamienia falę w pakiet cząstek.
Paderborn drgania (zdrowe i naturalnie uszkodzone) → polowy, P 0,26–0,29 tuż pod progiem — uszkodzenia naturalne nie dają
wyraźnych cząstek, co zgadza się z trudnością tego zbioru. Paderborn prądy → mieszany, ale cząsteczkowość prądu to
najpewniej przełączanie falownika (PWM) powyżej 1 kHz, nie łożysko — uwaga na źródła cząstek niezwiązane z usterką.
Przewidywanie przed danymi dla turbiny Fraunhofer LBF: drgania łożyskowe **mieszane (fala + pakiet)** przy uszkodzeniu,
**falowe lub polowe** przy stanie zdrowym.

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
