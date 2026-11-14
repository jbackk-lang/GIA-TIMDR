# TIMDR-INFO-GEOMETRY v0.1 — metodologia

**Data:** 2026-11-14. **Status:** projekt prerejestracji; brak wyników.

## Cel
Zbadać, czy geometryczne cechy trajektorii sygnału zwiększają skuteczność (a) detekcji zmiany reżimu, (b) przewidywania przyszłego stanu i (c) rozróżniania struktur czasowych przy zbliżonym rozkładzie amplitud.

## Reprezentacja
Dla szeregu `x[t]` i opóźnienia `d` rekonstruujemy stan `X[t] = (x[t], x[t-d], ..., x[t-(m-1)d])`. W pilocie: `m=3`; `d` dobieramy wyłącznie na zbiorze treningowym. Pochodne i krzywiznę liczymy na wygładzonej trajektorii, z jawną kontrolą wpływu wygładzania i częstotliwości próbkowania. Dla trzech wymiarów krzywizna: `kappa = ||X' × X''|| / ||X'||^3`, tylko gdy `||X'||` przekracza wcześniej ustalony próg stabilności. Skręt: `torsion = det(X', X'', X''') / ||X' × X''||^2`, tylko dla nieosobliwych punktów. Osobliwości raportujemy jako brak wartości, nie jako dowód zdarzenia.

## Hipotezy do zamrożenia przed testem
- **H1:** geometryczne cechy poprawiają detekcję zmian reżimu względem dopasowanego modelu klasycznego przy tej samej procedurze walidacji.
- **H2:** poprawiają prognozę następnego stanu lub zdarzenia na danych spoza uczenia.
- **H3:** rozróżniają sekwencje o podobnych rozkładach amplitud, lecz odmiennych zależnościach czasowych.
- **H0 / kontrola negatywna:** na odpowiednio skonstruowanych danych losowych nie pojawia się stabilna, powtarzalna przewaga.

## Dane i kontrole
1. Syntetyczne: biały i skorelowany szum, proces AR, oscylator, skoki reżimu, impulsy, mieszanki sygnału i szumu. Ustalić generatory, parametry i ziarna przed testem.
2. Kontrole: tasowanie czasu (zachowuje histogram, niszczy kolejność), surrogaty zachowujące widmo, zmiana próbkowania, poziomu szumu i amplitudy.
3. Dopiero po pilocie: osobne zbiory z sejsmiki, EKG/EEG lub radaru, jeśli dostępne z legalną licencją i właściwymi etykietami.
4. Podziały chronologiczne lub grupowe bez przecieku okien z tej samej sesji do treningu i testu.

## Porównania
- Proste: energia, RMS, wariancja, różnice i autokorelacja.
- Czasowo-częstotliwościowe: cechy widmowe / STFT.
- Informacyjne: entropia próbkowa lub permutacyjna oraz zysk predykcyjny.
- Modele: ten sam klasyfikator/regresor z cechami bazowymi oraz z dodatkiem geometrii; kontrola liczby cech i budżetu strojenia.
- Ablacja: bez krzywizny, bez skrętu, bez cech TIMDR.

## Metryki
Detekcja: precision/recall, F1, fałszywe alarmy na jednostkę czasu i opóźnienie detekcji. Predykcja: MAE/RMSE lub log-loss, zależnie od zadania. Dodatkowo: przedziały ufności przez bootstrap po niezależnych sesjach, testy odporności na parametry i koszty obliczeniowe.

## Kryterium interpretacji
`SUPPORTED` tylko po uprzednim zamrożeniu kryterium sukcesu i dodatnim wyniku na odłożonym teście; `NOT SUPPORTED` przy niespełnieniu kryterium; `INCONCLUSIVE` przy niewystarczającej mocy lub jakości danych. Dokładny próg sukcesu, główny zbiór i metryka **nie są jeszcze zamrożone**. Żadna przewaga w detekcji nie dowodzi istnienia elementarnej cząstki informacji.

## Następny krok
Ustalić główną metrykę i minimalny efekt, przygotować generatory i zamrożony podział danych; następnie uruchomić test z raportem również dla wyników negatywnych.
