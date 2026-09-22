# Wynik: modal_band_energy_bridge v0.2 — POTWIERDZONY (formalnie), specyficzność częściowa (opisowo, uczciwie odnotowana)

> Pierwszy formalnie potwierdzony wynik w serii mostów tej sesji, po
> chrono_cone (odrzucony v0.1-v0.3), chrono_sphere (odrzucony v0.1-v0.2),
> chrono_modal_geometry (niestabilny v0.1) i modal_band_energy v0.1
> (błąd metodologiczny). Uruchomione: 2026-09-22.

## Kontrole syntetyczne — PASSED

Wszystkie trzy rozmiary okna (2500/5000/10000 próbek @ fs_syn=5000Hz):
sygnał impulsowy periodyczny (symulacja uderzeń defektu) daje istotnie
wyższy pik w widmie obwiedni niż szum szerokopasmowy (`p=2.4e-7–3.0e-11`,
`r=0.778–1.000`).

## Realne dane — pasmo rezonansu i wynik główny

Pasmo rezonansu wybrane z `Normal` (kurtoza nadmiarowa=0.372,
maksimum spośród 9 kandydatów 500-5000Hz): **4500-5000 Hz**.

### Pary DOPASOWANE (test formalny, α_corr=0.0167 po Bonferronim)

| para | p | r | mediana(fault) | mediana(normal) | SUPPORTED |
|---|---|---|---|---|---|
| IR_21→BPFI | 6.0e-6 | 1.000 | 0.003129 | 0.0000474 | **tak** |
| OR@6_21→BPFO | 6.0e-6 | 1.000 | 0.003343 | 0.0000597 | **tak** |
| B_21→BSF | 6.0e-6 | 1.000 | 0.0005717 | 0.0000592 | **tak** |

Stabilność (podział połówkowy): wszystkie trzy pary stabilne
(ten sam kierunek, `p<0.001` w obu połówkach).

**Formalna klasyfikacja wg zamrożonej reguły (PREREG v0.1 §6,
dziedziczonej do v0.2): SUPPORTED.**

## Zastrzeżenie uczciwe, zauważone PO wyniku, nie ukryte

Zamrożona reguła klasyfikacji testowała WYŁĄCZNIE "czy para dopasowana
różni się istotnie od Normal" — NIE testowała formalnie "czy pasmo
dopasowane różni się od pasm niedopasowanych". Nazwa etykiety w
preregu ("specyficzność potwierdzona") sugerowała więcej, niż reguła
faktycznie sprawdzała — to luka w projekcie testu, odnotowana tu
wprost, nie naprawiana retroaktywnie zmianą progu.

Patrząc opisowo na wszystkie 9 par (3 dopasowane + 6 niedopasowane,
wszystkie istotne, `r=1.000` wszędzie — sam fakt istotności nie
różnicuje):

| plik | pasmo dopasowane (krotność wzrostu) | pasma niedopasowane (krotność wzrostu) | specyficzność? |
|---|---|---|---|
| IR_21 (→BPFI) | 66× | BPFO: 8.2×, BSF: 4.3× | **wyraźna** |
| OR@6_21 (→BPFO) | 56× | BPFI: 12.7×, BSF: 10.6× | **wyraźna** |
| B_21 (→BSF) | 9.7× | BPFO: 9.1×, BPFI: 12.1× | **brak** |

IR i OR pokazują realną specyficzność opisową (pasmo dopasowane
podniesione wyraźnie mocniej niż pozostałe). B (kulka) — nie, pasmo
BSF podniesione praktycznie tyle samo co pozostałe dwa. **To jest
zgodne z ugruntowaną literaturą diagnostyki łożysk**: uszkodzenia
kulki są notorycznie trudniejsze do zdiagnozowania przez prostą
częstotliwość BSF, bo punkt kontaktu kulki z bieżniami losowo się
obraca w trakcie pracy, rozmywając periodyczną sygnaturę modulacji —
znany, udokumentowany efekt, nie artefakt tej konstrukcji.

## Status

**v0.2 POTWIERDZONY formalnie** (3/3 pary dopasowane, stabilne),
**specyficzność częściowa** (2/3 typy uszkodzenia pokazują wyraźną
przewagę pasma dopasowanego, ball fault nie) — zgłoszone w pełni
uczciwie, bez podciągania wyniku B_21 pod wzorzec IR/OR. Pierwszy
pozytywny, formalnie potwierdzony wynik w całej serii mostów z
2026-09-22 (siedem konstrukcji: chrono_cone×3, chrono_sphere×2,
chrono_modal_geometry×1, modal_band_energy×2 — ta ostatnia jako
jedyna przechodzi zarówno kontrolę, jak i dane realne w przewidywanym
kierunku).

## Co zostaje otwarte

- Formalny test specyficzności (matched vs unmatched magnitude,
  np. test parowany na krotnościach wzrostu) — nie policzony tutaj,
  naturalny następny krok, jeśli konstrukcja ma być kontynuowana.
- Czy dodanie harmonicznych BSF (2×, 3× częstotliwości) poprawiłoby
  wykrywalność uszkodzenia kulki — standardowa technika w literaturze,
  nie testowana w v0.2.
