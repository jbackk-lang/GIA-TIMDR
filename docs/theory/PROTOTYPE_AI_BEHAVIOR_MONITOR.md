# Prototyp: monitor zachowania AI na bazie formalizmu M/S (rezonans-K)

> Odpowiedź na pytanie użytkownika: "czy możemy i ma to sens stworzyć
> zabezpieczenie AI przed szkodliwym działaniem?" — na wyraźną prośbę
> jako koncepcja/prototyp, BEZ konkretnego monitorowanego systemu i BEZ
> realnych danych na tym etapie. Kod: `core/ai_behavior_monitor.py`.
> Data: 2026-09-16.

## Czym to jest, a czym nie jest

To NIE jest "bezpieczeństwo AI" w sensie głębokiego alignmentu — nie
zapobiega temu, żeby dostatecznie zdolny/złośliwy system zaprojektował
działanie, które nie zaburza śledzonych statystyk. To jest generyczny
statystyczny detektor dryfu/koincydencji anomalii na wybranych przez
użytkownika sygnałach proxy — czujnik dymu, nie zrozumienie ognia.
Złapie nagłą, skoordynowaną zmianę w wielu śledzonych kanałach naraz;
NIE złapie pojedynczego, dobrze zamaskowanego szkodliwego działania,
które nie porusza żadnej z wybranych metryk powierzchniowych.

## Zero nowej matematyki — całkowite reużycie

Cała mechanika (`anomalia_flags`, `defekt_flags`, `skret_flags` z
`chronosignal.py`; `compute_anomaly_flags`, `calibrate_resonance_K`,
test permutacyjny + kontrola mocy z `calibration.py`) jest reużyta
1:1 z `TIMDR-Math-Formalism`, bez modyfikacji. Nowość w tym module to
wyłącznie: (a) pięć kanałów-proxy dla "zachowania AI" (propozycja
startowa, nie ustalona definicja — patrz `CHANNEL_DESCRIPTIONS`),
(b) syntetyczny generator normalny/atak do demonstracji mechaniki.

## Wynik samo-testu syntetycznego (K=3 z 5 kanałów)

**Kontrola negatywna** (normalna praca, 5 niezależnych szumów): 0/200
zdarzeń koincydencji przy K=3 → `insufficient_power`, system POPRAWNIE
odmawia rekomendacji zamiast fałszywie twierdzić "brak zagrożenia" —
ten sam wzorzec uczciwości co realny wynik Kraków_Centrum
(`REAL_DATA_VALIDATION.md`).

**Kontrola pozytywna** (wstrzyknięta skoordynowana eskalacja w oknie
[150,170): wzrost `risk_action_rate`, spadek `refusal_rate`, wzrost
`latency_ratio` i `repetition_score`, celowo BEZ ruszania
`output_entropy` — test odporności na częściowe pominięcie kanału):
20/200 zdarzeń przy K=3, p=0,0002, moc potwierdzona kontrolą
pozytywną — złapane czysto.

**Uczciwy niuans**: automatyczna kalibracja (po korekcie
Bonferroniego za przetestowanych kandydatów K) zarekomendowała K=5 z
5 — wymóg jednomyślności WSZYSTKICH kanałów naraz. Na tym konkretnym,
syntetycznym przykładzie to działa (bo wstrzyknięty atak poruszał 4/5
kanałów, a real_event_count liczony był dla K=3, nie K=5), ale
jednomyślność jako rekomendacja jest w praktyce KRUCHA — atak, który
świadomie pomija choć jeden z pięciu kanałów (co robi ten konkretny
test dla `output_entropy`), przy K=5 zostałby przeoczony. Nie jest to
ukryte — jest to dokładnie ten sam kompromis czułość/swoistość, którego
mechanizm sam uczciwie ujawnia, gdy się go uruchomi i przeczyta wynik,
a nie tylko `passed`/`nie passed`.

## Warunki przed użyciem na realnym systemie

1. Realna definicja każdego kanału dla KONKRETNEGO systemu (skąd
   dokładnie liczony jest `risk_action_rate`, jaka kategoryzacja
   ryzyka, itd.) — obecne pięć kanałów to propozycja startowa.
2. Realne dane kontroli pozytywnej (znane epizody szkodliwe/ataki) i
   negatywnej (normalna praca) — bez tego `calibrate_resonance_K`
   prawidłowo odmówi rekomendacji progu, dokładnie jak w kontroli
   negatywnej powyżej.
3. Jawna akceptacja, że to warstwa UZUPEŁNIAJĄCA (wykrywanie dryfu/
   koincydencji statystycznej), nie ZASTĘPUJĄCA dedykowanych narzędzi
   AI safety (klasyfikatory treści, probing aktywacji, circuit
   breakers, red-teaming), które rozumieją semantykę, nie tylko
   statystykę powierzchniową.

## Status

Koncepcyjny prototyp, mechanika zweryfikowana na syntetyce (poprawne
zachowanie w obu kontrolach). Zero walidacji na realnych danych
zachowania AI — nie dlatego, że to pominięto, tylko dlatego, że
użytkownik jawnie potwierdził brak konkretnego monitorowanego systemu
na tym etapie. Nie promowane do żadnej gałęzi aksjomatów — to
zastosowanie istniejącej matematyki M/S do nowej domeny, nie nowa
matematyka.
