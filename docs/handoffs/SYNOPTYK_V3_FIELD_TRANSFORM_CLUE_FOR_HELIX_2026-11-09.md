# SYNOPTYK-v3 JAKO WZORZEC TRANSFORMACJI SYGNAŁU DO POLA DLA SPRZĘŻENIA GS–G

**Data:** 2026-11-09  
**Źródło:** `jbackk-lang/Synoptyk-v3`  
**Cel:** ocenić, czy warstwa pola z Synoptyk-v3 podpowiada brakujący etap pomiędzy sygnałem S/GS-Matrix a mechanicznym G-Rezonansem.

## 1. Odpowiedź w skrócie

**Tak — Synoptyk-v3 dostarcza ważnego wzorca architektonicznego: nie podawać surowego sygnału bezpośrednio do operatora mechanicznego, lecz najpierw przekształcić go do reprezentacji pola, a następnie wyznaczyć jego strukturę i cechy.**

Nie należy jednak przenosić meteorologicznej implementacji 1:1. Synoptyk-v3 przekształca rozproszone pomiary pogodowe w przestrzenne pola fizyczne na siatce. Nie jest uniwersalnym transformatorem dowolnej informacji ani modelem odpowiedzi helisy.

## 2. Co konkretnie robi Synoptyk-v3

Pliki źródłowe:
- `membrane/interpolate.py`: rozproszone pomiary → regularna siatka pól skalarnych i wektorowego pola wiatru. Kierunek wiatru jest najpierw rozkładany na składowe kartezjańskie u/v, interpolowane osobno, a potem może być odtworzony.
- `membrane/spectrum.py`: 2D FFT i radialny rozkład mocy; gradienty pól; wirowość `dv/dx-du/dy`; koherencja kierunku.
- `membrane/defects.py`: lokalne anomalie przez próg mediana + k·MAD.
- `membrane/resonance.py`: współwystępowanie anomalii w kilku kanałach w tej samej komórce.
- `membrane/analyze.py`: scala te operacje w jeden pipeline.
- `membrane/meta_adapter.py`: mapuje cechy pola na `MetaState(Λ,τ,ρ,J)`; kod jawnie zaznacza, że jest to jedno z możliwych mapowań, a progi nie są uniwersalnymi stałymi fizycznymi.

To ważne: Synoptyk-v3 rozdziela **reprezentację pola** od **operatorów analizy pola** i od **adaptera do stanu META**.

## 3. Co z tego wynika dla helisy TIMDR

Potencjalna architektura:

`surowy sygnał/informacja`
→ `transformacja do pola (reprezentacja przestrzenna lub modalna)`
→ `cechy pola: gradient / rotacja / widmo / defekty / koherencja`
→ `stan sygnałowy S lub MetaState`
→ `GS-Matrix (kandydat na sprzężenie G↔S)`
→ `G-Rezonans (mechaniczna dynamika i odpowiedź)`
→ `pomiar odpowiedzi / sprzężenie zwrotne`.

To jest hipoteza architektury, nie zatwierdzony łańcuch równań. W szczególności trzeba ustalić, czy pole dla helisy powinno być:
- polem skalarnym (np. amplituda/energia/odchylenie),
- polem wektorowym (kierunek/przepływ/orientacja),
- polem fazowym/modalnym,
- czy wielokanałowym polem stanu.

Nie zakładać, że wszystkie te reprezentacje są potrzebne. Najpierw ustalić, jaką informację ma zachować sygnał i jaki stopień swobody helisy ma na nią odpowiedzieć.

## 4. Najważniejsza wskazówka z Synoptyk-v3

W module interpolacji kierunek wiatru nie jest interpolowany bezpośrednio jako kąt, ponieważ 350° i 10° leżą blisko siebie, mimo że średnia arytmetyczna kątów daje błędne 180°. Najpierw zamienia się kierunek na składowe u/v, wykonuje transformację, a dopiero potem odtwarza reprezentację kierunkową.

To daje ogólną zasadę dla helisy: **nie wolno transformować sygnału w reprezentacji, która gubi jego cykliczność, fazę lub orientację.** Dla sygnału helikalnego należy sprawdzić, czy reprezentacja zespolona/fazorowa albo para składowych jest bezpieczniejsza niż surowy kąt lub wartość bezwzględna. Zachować znak fazy i chiralność.

Druga wskazówka: Synoptyk-v3 liczy gradient, wirowość i widmo dopiero po utworzeniu pola. Dla helisy może to być właściwy porządek: najpierw zdefiniować pole wejściowe, potem badać jego strukturę, a dopiero potem mapować je na sprzężenie G.

## 5. Ograniczenia i pułapki

- Pole Synoptyk-v3 jest polem pogodowym w przestrzeni geograficznej, a nie polem oddziaływania na helisę.
- 2D FFT i gradienty nie tworzą same z siebie kanału fizycznego; są analizatorami reprezentacji.
- Defekt i rezonans Synoptyka są diagnostycznymi heurystykami; „rezonans” jest koincydencją kanałów, nie fizycznym oscylatorem.
- `MetaState` jest znormalizowanym opisem cech; nie należy interpretować Λ/τ/ρ/J jako siły, energii lub naprężenia bez wyprowadzenia jednostek.
- Interpolacja do siatki może wygładzić/zmienić sygnał. Dla helisy trzeba wykazać, które cechy są zachowane, a które tracone.
- Samo pole nie daje odpowiedzi helisy; potrzebny jest jawny operator mapujący pole na stopnie swobody G i sprzężenie zwrotne z G do kolejnego stanu pola/sygnału.

## 6. Odpowiedź na pytanie o GS-Matrix i G-Rezonans

Można je architektonicznie połączyć, ale Synoptyk-v3 sugeruje, że między nimi może być potrzebny **adapter pola**:

1. Synoptykowy wzorzec transformacji tworzy reprezentację pola z wejścia.
2. Adapter wydobywa z pola zachowujące informację cechy/stany.
3. GS-Matrix opisuje abstrakcyjne sprzężenie stanu sygnałowego i geometrycznego.
4. G-Rezonans wylicza mechaniczną odpowiedź konkretnego modelu geometrii.

Nie należy bezpośrednio utożsamiać `MetaState` z wektorem G/S ani podstawiać `Λ,τ,ρ,J` do macierzy mechanicznej. Najpierw potrzebne jest jawne mapowanie zmiennych i zgodność wymiarowa. Jeśli GS-Matrix ma stanowić część mechaniki, jej współczynniki muszą zostać wyprowadzone z modelu lub skalibrowane, a nie dobrane intuicyjnie.

## 7. Najmniejszy następny krok

Zamiast pisać nowy operator, zrobić **mapę reprezentacji** dla jednego sygnału testowego:
- oryginalny przebieg z fazą i orientacją;
- jego transformacja do pola;
- cechy pola po transformacji;
- rekonstrukcja sygnału z pola (jaki błąd i co utracono);
- wskazanie, które składowe pola mogłyby zasilać stan S w GS-Matrix;
- wskazanie, które mierzalne stopnie swobody G mogłyby być odpowiedzią.

Na tym etapie nie uruchamiać jeszcze mechanicznego sprzężenia ani nie deklarować fizycznej interpretacji. Najpierw sprawdzić, czy reprezentacja pola zachowuje dokładnie tę informację, na którą helisa ma odpowiedzieć.

## 8. Konkluzja

Synoptyk-v3 podpowiada brakującą **warstwę reprezentacji/transformacji sygnału do pola**. Nie dostarcza gotowego prawa oddziaływania na helisę, ale pokazuje sprawdzony w kodzie wzorzec: dane → pole → cechy pola → adapter stanu. To może być brakujący etap pomiędzy sygnałem S/GS-Matrix a mechanicznym G-Rezonansem. Najważniejsze pytanie przed integracją: jakie własności informacji muszą przetrwać transformację do pola, aby odpowiedź helisy mogła być jednoznacznie zbadana?
