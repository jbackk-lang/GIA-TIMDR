# Stan projektu TIMDR

_Stan na: 2026-09-30_

Dokument żywy: zamiast kolejnych datowanych podsumowań jest jeden stan bieżący. Część **automatyczna** (bilans i lista testów) odświeża się jednym poleceniem — `python scripts/stan_projektu.py` albo dwuklik na `aktualizuj_stan.bat` — z tabeli wyników w [README](README.md). Część **ręczna** (poniżej, do linii z bilansem) zmienia się tylko wtedy, gdy zmienia się obraz całości. Poprzednie podsumowanie: [archiwum, 23.09.2026](docs/archiwum/PODSUMOWANIE_PROJEKTU_2026-09-23.md).

## Aktualizacja: astronomia

Dodano dwa prototypy i kopie wybranych źródeł: [orbity, krzywe blasku i zdjęcia](docs/astronomy/ASTRONOMIA_2026-09-30.md). Wyniki małoetykietowe z innych dziedzin nie przenoszą się automatycznie na astronomię: OGLE i tani pilot ATLAS nie potwierdziły przewagi obecnej adaptacji sita nad lasem losowym. Fotometria zdjęć ma testy syntetyczne; śledzenie orbit nie ma niezależnej walidacji na rzeczywistych pomiarach pozycji. Ta aktualizacja nie zmienia historycznych tabel automatycznych poniżej.

## Czym TIMDR jest dziś

**TIMDR to model do budowania programów analizujących sygnały**: rama opisu (gałęzie M/S, G, K, META-DYNAMICS i wspólny czas Chronoprocesu), drogowskazy konstrukcji i protokół badania — a nie gotowy detektor. Pojedyncze operatory użyte wprost jako cechy nie dały przewagi nad metodami klasycznymi; przewagę dają **konstrukcje z drogowskazów**, zbudowane przed danymi i sprawdzone raz na części zamkniętej.

Mapa formalna bez zmian: [specyfikacja gałęzi](docs/theory/TIMDR_Branch_Specification.md), [Chronoproces](docs/theory/TIMDR_Chronoprocess.md), [aksjomaty META](docs/theory/Axioms_META_TIMDR.md), [reguła kalibracji i zamrożenia](docs/theory/TIMDR_CALIBRATION_FREEZE_RULE.md), [parametry przejść](docs/theory/TIMDR_Parametry_Przejsc.md).

## Czego nauczyły testy (zasady, które się powtarzają)

1. **Pierwszy trybik to zegar.** O powodzeniu łańcucha decyduje wybór osi czasu: turbina w osi kątowej 1,00 wobec 0,85 w czasie; radar z oknem za wolnym na łopaty — słabo wszystko dalej; budżet — decyzja w chwili wpływu, zobowiązania według ich kalendarza.
2. **Zasada odniesienia.** Sygnał nakłada się na wzorzec z tego samego ośrodka, znosi to, co wspólne, i czyta resztę (stereoskopia połówek radaru, stosunki częstotliwości jako termometr ze stali, CPI każdej kategorii w budżecie). **Wzorzec ma znosić zakłócenie, a nie wielkość, o którą pyta decyzja** — dzielenie salda przez dochód wycięło sygnał wypłacalności.
3. **Reguła wykonalności** — liczona przed testem, także na części testowej: rytm musi mieścić się w oknie (≥ 10 cykli), a stosunki częstotliwości działają tylko przy równym skalowaniu (znaki ρ(f_k, T) zgodne).
4. **Gałąź sama — minus, most — plus.** Ułożone w kolejności wyniki układają się naprzemiennie: operatory jednej gałęzi wprost przegrywają z klasyką, mosty (pole + sito, kotwica K + kształt, K → META) wygrywają.
5. **TIMDR przed uczeniem maszynowym.** Struktura TIMDR wykonuje pracę: sieć na polu TIMDR uogólnia od 4 przykładów na klasę, na spektrogramie potrzebuje 8× więcej, na surowym przebiegu 40×; sieć nie dodaje nic ponad samą strukturę.

## Najmocniejsze wyniki (szczegóły w tabeli niżej)

- **Łożyska Paderborn, uszkodzenia naturalne, łożyska spoza uczenia** — sito rezonansowe lepsze od cech klasycznych i kurtogramu w trzech kolejnych testach (łącznie +0,08, 12/15 foldów).
- **Turbina wiatrowa w terenie** — sito w osi kątowej: bieżnia zewnętrzna AUC 1,00 przy swoistości 1,00.
- **Mosty (KW51, Hell Bridge)** — kotwica modalna i stosunki częstotliwości znoszą temperaturę lepiej niż termometr, gdy skalowanie jest równe.
- **Radar mmWave (surowe I/Q)** — lustro i cień potwierdzone 3/3, gdy reguła wykonalności jest spełniona.
- **PRONOSTIA** — parametr reżimu D przechodzi pole → cząsteczka → fala w drodze łożyska do zniszczenia (9/11 i 7/11).
- **Zarządca budżetu (symulacja)** — MUZ wyprowadza na prostą 60,8% zadłużonych gospodarstw wobec 55,5% najlepszego standardu i 0,3% typowej aplikacji bankowej. Symulacja jest autorska: pokazuje mechanizm, nie częstość takich gospodarstw.

Wyniki negatywne są równie ważne: radar Open Radar (widma z za długim oknem), budynek LANL jako pole, antyrezonanse (zera FRF nie przenoszą się między pozycjami wzbudzenia), LUMO (nierówne skalowanie), budżet na danych bankowych PKDD'99 (klasyka nominalna 0,94 wobec 0,87–0,91).

## Zastosowania

| Projekt | Stan |
|---|---|
| [TIMeDR-MUZ](https://github.com/jbackk-lang/TIMeDR-MUZ) | Lokalny zarządca budżetu: czyta wyciągi PDF/CSV/MT940 i wklejony tekst bez wpisywania, sam rozpoznaje opłaty stałe i stan długu, wydaje przydział do wypłaty i sprawy z kartą rozmowy i pismem. Niczego nie wykonuje sam. |
| [TIMDR-Industrial-Predict](https://github.com/jbackk-lang/TIMDR-Industrial-Predict) | Sito rezonansowe dla łożysk (program z testów Paderborn). |
| [TIMDR-fusion-tools](https://github.com/jbackk-lang/TIMDR-fusion-tools) | Tokamak TCABR: 19/19 nowych strzałów przez czas zaniku prądu; transfer na MAST niezweryfikowany etykietami. |
| [synoptyk-v2.0](https://github.com/jbackk-lang/synoptyk-v2.0), [SYNOPTYK-ARCTIC](https://github.com/jbackk-lang/SYNOPTYK-ARCTIC), [Synoptyk-v3](https://github.com/jbackk-lang/Synoptyk-v3) | Korekta prognoz i pomiar bias/MAE; bez przewagi wykazanej nad numerycznym modelem pogody. |
| pozostałe | [katalog ekosystemu](https://github.com/jbackk-lang/jbackk-lang.github.io/blob/main/KATEGORIE.md) — status każdego projektu w jego README. |

## Otwarte zadania

- Zegar z samego sygnału (śledzenie prędkości turbiny z drgań odpadło w rozwoju).
- Bieżnia wewnętrzna i element toczny w turbinie — niewykryte.
- Radar: dane surowe dłuższe niż rytm kroku (Part 1 w toku), mapa podmiotów przed testem niezależnym od osoby.
- Fale prowadzone (Utah) — czeka na dane.
- MUZ: reguły spraw poza podwyżkami (kilka umów tego samego rodzaju, koszt długu, opłata za konto, płatności odroczone) — do pre-rejestrowanego testu.

## Jak aktualizować

1. Po teście: wiersz w tabeli wyników README (protokół i tak go wymaga).
2. `python scripts/stan_projektu.py` (albo `aktualizuj_stan.bat`) — odświeża bilans i listę poniżej.
3. Tylko gdy zmienia się obraz całości — poprawić część ręczną powyżej.

<!-- AUTO:START -->

_Część automatyczna — odświeżona 2026-09-28 skryptem `scripts/stan_projektu.py` z tabeli wyników w README._

**Bilans pre-rejestrowanych testów: 31** — ✅ potwierdzone 13 · 🟡 mieszane 5 · ❌ niepotwierdzone 13 · ⚪ nierozstrzygnięte 0.

Werdykt w kolumnie to pierwsza hipoteza główna testu; szczegóły (hipotezy poboczne, ograniczenia) — w pliku wyniku.

| Data | Test | Werdykt | Wynik |
|---|---|---|---|
| 2026-09-28 | [Paderborn — TIMDR jako warstwa porządkująca przed siecią z uwagą (krzywe uczenia, łożyska rozłączne)](docs/geometry/RESULT_PADERBORN_LEARNING_CURVES_v0.1.md) | ✅ tak | H1–H3 SUPPORTED — 8× mniej przykładów niż spektrogram, 40× niż surowy; sieć nic nie dodaje ponad strukturę TIMDR |
| 2026-09-28 | [MUZ P1 — budżet: zegar od wypłaty + odniesienie do własnego dochodu (PKDD'99, kredyty; prognoza z historii przed kredytem)](docs/geometry/RESULT_MUZ_P1_BERKA_v0.1.md) | ❌ nie | NOT SUPPORTED (H1 −0,06, CI < 0; zegar H2 −0,01; odniesienie H3 −0,04) — odniesienie wycięło sygnał: przy wypłacalności poziom kwot jest celem, nie zakłóceniem |
| 2026-09-28 | [MUZ P2 — budżet: wzorzec = rata (to, o co pyta decyzja), dołek salda przed wypłatą](docs/geometry/RESULT_MUZ_P2_BERKA_v0.1.md) | ❌ nie | H1 NOT SUPPORTED (C+R −0,001), H2 MIXED (+0,04 rata vs dochód), H3 zegar od wypłaty NOT (−0,03), H4 remis — wzorzec poprawiony, przewagi brak, sufit ≈ 0,94 |
| 2026-09-28 | [MUZ-SIM — zarządca budżetu w zamkniętej pętli: wyprowadzenie zadłużonego gospodarstwa „na prostą” (symulacja 36 mies.: przesuwane wypłaty, inflacja per kategoria, rozliczenia, awarie, przerwy w pracy)](docs/geometry/RESULT_MUZ_SIM_v0.1.md) | ✅ tak | H1 SUPPORTED (+5,2 pkt vs koperty), zegar +3,7 i odniesienie +4,3 SUPPORTED, reżim zdarzeń MIXED; kontrola S0 i przewidziana porażka S2 zgodne; symulacja… |
| 2026-09-27 | [Łożyska Paderborn — trzecie potwierdzenie (pomiary 16–20) + łącznie 15 foldów](docs/geometry/RESULT_PADERBORN_RESONANCE_SIEVE_CONFIRM_v0.3.md) | ✅ tak | łącznie: vs klasyczne SUPPORTED (+0,08, 12/15), vs obwiednia MIESZANY (+0,04, 10/15), vs kurtogram SUPPORTED |
| 2026-09-27 | [Turbina wiatrowa Fraunhofer LBF (w terenie, zmienna prędkość)](docs/geometry/RESULT_WIND_LBF_ORDER_SIEVE_v0.1.md) | ✅ tak | SUPPORTED (H1, H2); bieżnia wewnętrzna i element toczny niewykryte; śledzenie prędkości z drgań odpadło |
| 2026-09-27 | [Radar 77 GHz, Open Radar (mikro-Doppler: człowiek/rower/dron/pojazd)](docs/geometry/RESULT_OPEN_RADAR_MICRODOPPLER_v0.1.md) | ❌ nie | NOT SUPPORTED (H1); sito samo działa (H2), ale słabiej; kinematyka 0,96 = ślad akwizycji |
| 2026-09-27 | [Radar Open Radar — jako rura (zwinięte pole, I/Q w czasie wolnym)](docs/geometry/RESULT_OPEN_RADAR_TUBE_v0.2.md) | ❌ nie | NOT SUPPORTED (H1); sam TIMDR MIXED (−0,05, CI do +0,01); „dron = cząsteczki” odwrotnie — szybka rura drona to szum |
| 2026-09-27 | [Radar Open Radar — lustro i cień (połówki ±d wokół linii ciała, stereoskopia; całe ślady)](docs/geometry/RESULT_OPEN_RADAR_MIRROR_v0.3.md) | ❌ nie | NOT SUPPORTED (H1 −0,05); rower MIXED (+0,01, vs CVD całego śladu +0,28); stereoskopia z dev nie powtórzyła się (osoby w eval 2,5× krótsze — rytm kroku w 24%… |
| 2026-09-27 | [Radar mmWave 77 GHz (surowe I/Q, chód 16 s) — lustro i cień na danych spełniających regułę wykonalności](docs/geometry/RESULT_MMWAVE_MIRROR_v0.4.md) | ✅ tak | H3 SUPPORTED 3/3 (cień i przeciwfaza przy nieruchomej ręce, rozprzężenie przy machaniu), H4 SUPPORTED, H1 MIXED (+0,11, CI od 0), H2 sufit |
| 2026-09-27 | [Budynek LANL — jako pole (kanały × pasma) + sito cząsteczkowości](docs/geometry/RESULT_LANL_FIELD_SIEVE_v0.2.md) | ❌ nie | NOT SUPPORTED (H1–H3); wykrywa rzadkie uderzenia (szczelina 0,15–0,13 mm), gubi częste — obserwacja: częste uderzenia zlewają się w falę |
| 2026-09-27 | [Budynek LANL — kotwica modalna K → linie w reżimie fali](docs/geometry/RESULT_LANL_MODAL_ANCHOR_v0.3.md) | ✅ tak | SUPPORTED (H1 odwrócenie ciężkości z −0,57; H2); D względem ciężkości NOT SUPPORTED |
| 2026-09-27 | [Łożyska PRONOSTIA do zniszczenia (11 nieoglądanych)](docs/geometry/RESULT_PRONOSTIA_REGIME_PATH_v0_1.md) | ✅ tak | SUPPORTED (H1–H4); reguła wykonalności trafnie przewidziała słabe sito przy oknie 0,1 s |
| 2026-09-27 | [Most Hell Bridge Test Arena (stalowa kratownica, 8 stanów uszkodzeń)](docs/geometry/RESULT_HBTA_MODAL_ANCHOR_v0.1.md) | ❌ nie | NOT SUPPORTED (H1, H2); ranking uszkodzeń zgodny z publikacją (H3); stężeń nie widzi |
| 2026-09-27 | [Most HBTA — most K↔G: kształt modu z fazą + krzywizna](docs/geometry/RESULT_HBTA_MODAL_CURVATURE_v0.2.md) | ❌ nie | NOT SUPPORTED (H1, H2); faza domyka lukę do AR, krzywizna nie dodaje; pionowe > stężenia (H3) |
| 2026-09-27 | [Most HBTA — lokalne uszkodzenie = przerwanie ciągłości (K → G → M/S)](docs/geometry/RESULT_HBTA_DISCONTINUITY_v0.3.md) | ❌ nie | H1 NOT SUPPORTED (remis), H2 SUPPORTED; stężenia niewidoczne dla czujników pionowych |
| 2026-09-27 | [Hell Bridge — antyrezonanse (zera FRF, gałąź K od strony zer) na nowych danych sweep](docs/geometry/RESULT_HBTA_ANTIRESONANCE_v0.4.md) | ❌ nie | NOT SUPPORTED (H1–H3); zera lokalne także na temperaturę i pozycję wzbudzenia — nie przenoszą się między pozycjami |
| 2026-09-27 | [Hell Bridge — kierunek (sweep poprzeczny, czujniki AG y) + stosunki częstotliwości (odniesienie z samej stali)](docs/geometry/RESULT_HBTA_LATERAL_RATIOS_v0.5.md) | ✅ tak | H2 SUPPORTED (null mniejszy 4/4, wbrew przewidywaniu z rozwoju); H1 kierunek MIXED; H1b SUPPORTED — stosunki działają, gdy zmiana między dniami jest równym… |
| 2026-09-27 | [KW51 — stosunki częstotliwości jako odniesienie z samej stali (bez termometru), 15 miesięcy co godzinę](docs/geometry/RESULT_KW51_RATIOS_v0.2.md) | ✅ tak | H1 SUPPORTED, H1b SUPPORTED; wykrycie wzmocnienia sufit (wszystkie 100%, 0 fałszywych) — MIXED |
| 2026-09-27 | [LUMO (wieża kratowa, CC-BY) — stosunki w porach roku (−4…40 °C) + usunięte stężenia (poziom i pojedynczy pręt)](docs/geometry/RESULT_LUMO_RATIOS_v0.1.md) | ❌ nie | NOT SUPPORTED (H1, H2) — przewidziane: mody idą z temperaturą w różne strony, więc nie ma równego skalowania |
| 2026-09-27 | [Most kolejowy KW51 (Leuven), przed i po wzmocnieniu](docs/geometry/RESULT_KW51_MODAL_ANCHOR_v0.1.md) | ✅ tak | SUPPORTED (H1–H4); widzi zmianę globalnej sztywności |
| 2026-09-27 | [Połączenie śrubowe ORION-AE (luzowanie 60 → 5 cNm)](docs/geometry/RESULT_ORION_BOLT_v0.1.md) | ✅ tak | SUPPORTED (H1, H3; H2 formalnie) |
| 2026-09-26 | [Przekładnia SEU](docs/geometry/RESULT_SEU_MULTICHANNEL_DIAGNOSTIC_v0.1.md) | 🟡 mieszany | remis; razem 0,95 / 0,81 — mieszane, po fakcie |
| 2026-09-26 | [Przekładnia SEU, koła zębate (świeże dane)](docs/geometry/RESULT_SEU_GEARSET_CONFIRM_v0.2.md) | 🟡 mieszany | MIESZANY: zysk mały przy zmianie warunków, duży w obrębie warunku |
| 2026-09-26 | [Łożyska Paderborn, drgania](docs/geometry/RESULT_PADERBORN_VIBRATION_COMPLEMENT_v0.1.md) | ✅ tak | SUPPORTED: zysk +0,09 (95% CI +0,05…+0,13), 4/4 warunki |
| 2026-09-26 | [Łożyska CWRU, test na niewidzianych łożyskach](docs/geometry/RESULT_CWRU_CROSS_BEARING_ENVELOPE_v0.1.md) | 🟡 mieszany | MIESZANY: zysk tylko tam, gdzie baseline poniżej sufitu |
| 2026-09-26 | [Łożyska Paderborn, uszkodzenia naturalne, niewidziane łożyska (15 łożysk)](docs/geometry/RESULT_PADERBORN_REAL_DAMAGE_v0.1.md) | 🟡 mieszany | A MIESZANY (brak efektu), pole/rezonans/sito NOT SUPPORTED |
| 2026-09-26 | [Łożyska Paderborn, uszkodzenia naturalne — sito samokorygujące](docs/geometry/RESULT_PADERBORN_RESONANCE_SIEVE_v0.1.md) | ✅ tak | SUPPORTED (H1 +0,12, 4/5; H2 +0,075, 3/5) |
| 2026-09-26 | [Łożyska Paderborn — replikacja sita (pomiary 11–15) + kurtogram](docs/geometry/RESULT_PADERBORN_RESONANCE_SIEVE_REPLICATION_v0.2.md) | 🟡 mieszany | replikacja częściowa: vs klasyczne SUPPORTED, vs kurtogram SUPPORTED, vs obwiednia MIESZANY |
| 2026-09-26 | [Budynek LANL (rama 3-kondygnacyjna)](docs/geometry/RESULT_LANL_3STORY_v0.1.md) | ❌ nie | brak wartości |
| 2026-09-26 | [Silnik Paderborn](docs/geometry/RESULT_PADERBORN_CURRENT_ORBIT_v0.1.md) | ❌ nie | brak wartości |

<!-- AUTO:END -->
