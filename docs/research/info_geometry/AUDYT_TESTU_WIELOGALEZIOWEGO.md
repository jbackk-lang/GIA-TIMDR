# Audyt testu wielogałęziowego przed interpretacją

**2026-11-14. Status: audyt kodu, nie wynik eksperymentalny.**

## Ustalenia
1. `multibranch_receiver_test.py` porównuje cztery reprezentacje, lecz nie zawiera **modelu pojedynczego odbiornika**. Nie wolno z niego wyciągać wniosku, że dwa odbiorniki są lepsze od jednego.
2. Wariant ALL ma więcej cech niż M/S, dlatego poprawa może wynikać z wymiaru reprezentacji, nie z mostów TIMDR.
3. K_PROXY (energia pierwszych różnic) i M/S (autokorelacja) mogą być silnie zależne matematycznie dla procesu stacjonarnego: energia różnic jest związana z wariancją i kowariancją opóźnienia 1. Nie traktować ich jako niezależnych źródeł dowodu.
4. G_PROXY jest kątem zwrotu krzywej 2D, a nie formalnym operatorem G. Nie nazywać go walidacją gałęzi geometrycznej.
5. Zmiana SOURCE i COMMON_CHANNEL jest rozróżnialna w konkretnej symulacji dzięki wybranym parametrom, ale ogólnie może być nieidentyfikowalna z samych obserwacji.
6. Kod nie posiada klasy UNKNOWN, testu na nieznanych parametrach toru ani oceny niepewności. Nie wolno ogłaszać rozstrzygnięcia ontologicznej kategorii informacji.
7. Warianty dla jednego ziarna dzielą innowacje generatora i szum czujników; jest to użyteczne jako porównanie sparowane, ale sesje należy grupować po ziarnie w podziale train/test.

## Warunki następnego etapu
- Baseline: odbiornik A tylko; odbiornik B tylko; oba odbiorniki bez cech mostowych.
- Ablacja: M/S; M/S+K; M/S+G; ALL; kontrola z losowymi dodatkowymi cechami.
- Osobna kalibracja progu UNKNOWN; test na niewidzianych filtrach, obcięciach i szumach.
- Raport osobno SOURCE↔COMMON_CHANNEL, SOURCE↔RECEIVER_A/B, z przedziałami ufności po sesjach.
- Dla pełnych mostów: jawne odwzorowania i operator zgodny ze specyfikacją TIMDR, nie tylko konkatenacja.
- Przed uruchomieniem testu potwierdzającego zamrozić kod, ziarna, metryki i reguły decyzji.

## Rejestr
Na tym etapie **nie uruchomiono** programu ani nie uzyskano liczbowych wyników. Ten audyt ogranicza dopuszczalne interpretacje przyszłego wyniku.
