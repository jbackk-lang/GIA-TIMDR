# Wynik — turbina wiatrowa Fraunhofer LBF: sito w osi kątowej, v0.1 (2026-09-27): H1 i H2 SUPPORTED

Pre-rejestracja: `PREREG_WIND_LBF_ORDER_SIEVE_v0.1.md` (commit c3dd014, przed nagraniami ewaluacyjnymi). Liczby:
`RESULT_WIND_LBF_ORDER_SIEVE_v0.1.json`. **Poprawka po ocenie (ujawnienie):** 3 segmenty jednego nagrania InnerRace
zawierały braki (NaN) w surowym sygnale, co uniemożliwiło policzenie AUC; wykluczono segmenty z NaN w sygnale — bez
zmian metody i progów. Segmenty ewaluacyjne: Healthy 57, OuterRace 6, InnerRace 33, RollerElement 20.

| Miara | Wartość | Werdykt |
|---|---|---|
| **H1:** AUC sita kątowego QO_BPFO, bieżnia zewnętrzna vs zdrowe | **1,00** | **SUPPORTED** (próg 0,90) |
| kontrola dnia: AUC niepasującego rzędu QO_BPFI, OR vs zdrowe | 0,58 | w zakresie — brak śladu zakłócenia dniem |
| **H2:** swoistość (OR vs wszystkie inne klasy) — sito kątowe | **1,00** | |
| H2: swoistość — sito przy stałej prędkości | 0,85 | różnica **+0,15 → SUPPORTED** (próg 0,10) |
| opisowo: sito przy stałej prędkości, OR vs zdrowe | 0,85 | |
| opisowo: mediana QO_BPFO − QO_BPFI | OR 1,72; zdrowe −0,04 | zapala się właściwy rząd |
| opisowo: bieżnia wewnętrzna (QO_BPFI) / element toczny (QO_BSF×2) vs zdrowe | 0,44 / 0,24 | nie wykryte |
| opisowo: klasyczne kurtoza / RMS, OR vs zdrowe | 0,00 / 0,00 | rozdzielają idealnie, ale **odwrotnie** — różnica dni, nie usterka |

**Co to znaczy.** Na prawdziwej turbinie pracującej na wietrze (wirnik 0,2–0,9 obr/s, prędkość zmienia się prawie
dwukrotnie w ciągu minuty) sito w osi kątowej — pole pasm nośnych, rezonans ustalający oczka, zegar z sygnału modalnego —
bezbłędnie wskazuje uszkodzenie bieżni zewnętrznej, a „zapala się” właściwy rząd (BPFO), nie niepasujący. Przy stałej
prędkości szczyt się rozmywa i sito myli uszkodzenie z innymi dniami/klasami (swoistość 0,85 wobec 1,00) — prostowanie
rury wzdłuż (oś kątowa) jest tu kluczowe. Klasyczne cechy „rozpoznają” dzień nagrania, nie usterkę.

**Granice (ważne):** jedna turbina; uszkodzenia wytrawione; OuterRace to tylko 2 nagrania ewaluacyjne (6 segmentów)
z jednego dnia; bieżnia wewnętrzna i element toczny **nie** zostały wykryte; zegar pochodzi z tachometru, bo śledzenie
prędkości z samych drgań odpadło w rozwoju (błąd 40–200%). Przewidywanie typu sygnału (krok 0) nie zostało tu sprawdzone:
wskaźnik M liczy modulacje 5–500 Hz, a częstotliwości uszkodzeń tej turbiny to 1–4 Hz.
