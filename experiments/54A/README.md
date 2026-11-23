# Eksperymenty 54A — indeks

Seria 54A badała warianty predykcji, adaptacji, kodowania i kompresji danych, w tym testy przełączania reżimów, geometrii oraz kompozycji predyktorów.

## Układ katalogu

- `code/` — skrypty eksperymentalne.
- `reports/` — raporty i notatki.
- `results/` — zapisane wyniki JSON.

Wszystkie pliki zachowują oryginalne nazwy. Przeniesienie nie zmienia treści ani historycznych wyników.

## Uruchamianie

Polecenia uruchamiaj z katalogu głównego repozytorium, np.:

```bash
python experiments/54A/code/54A10_MULTISCALE.py
python experiments/54A/code/54A15_STREAM_BENCH.py --records 262144 --repeats 3
```

Skrypty są samodzielnymi eksperymentami. Nie wszystkie zapisują wyniki do katalogu serii: należy sprawdzić argument `--output` i domyślną ścieżkę w danym skrypcie przed uruchomieniem. Nie nadpisuj archiwalnych plików w `results/` wynikami nowego przebiegu.

## Kod (15)

- [`54A5_COMPARE.py`](code/54A5_COMPARE.py)
- [`54A6_DYNAMIC.py`](code/54A6_DYNAMIC.py)
- [`54A9_GEOMETRY.py`](code/54A9_GEOMETRY.py)
- [`54A10_MULTISCALE.py`](code/54A10_MULTISCALE.py)
- [`54A11_SWITCH.py`](code/54A11_SWITCH.py)
- [`54A12_SWITCH.py`](code/54A12_SWITCH.py)
- [`54A14_CODEC.py`](code/54A14_CODEC.py)
- [`54A15_STREAM_BENCH.py`](code/54A15_STREAM_BENCH.py)
- [`54A16_BENCH.py`](code/54A16_BENCH.py)
- [`54A17_STREAM.py`](code/54A17_STREAM.py)
- [`54A18_BENCH.py`](code/54A18_BENCH.py)
- [`54A19_HYBRID.py`](code/54A19_HYBRID.py)
- [`54A20_ADAPT.py`](code/54A20_ADAPT.py)
- [`54A23_COMPOSITION.py`](code/54A23_COMPOSITION.py)
- [`54A24_COMPOSITION.py`](code/54A24_COMPOSITION.py)

## Raporty i notatki (22)

- [`54A5_REPORT.md`](reports/54A5_REPORT.md)
- [`54A6_REPORT.md`](reports/54A6_REPORT.md)
- [`54A7_REPORT.md`](reports/54A7_REPORT.md)
- [`54A8_REPORT.md`](reports/54A8_REPORT.md)
- [`54A9_REPORT.md`](reports/54A9_REPORT.md)
- [`54A10_REPORT.md`](reports/54A10_REPORT.md)
- [`54A11_REPORT.md`](reports/54A11_REPORT.md)
- [`54A12_REPORT.md`](reports/54A12_REPORT.md)
- [`54A13_REPORT.md`](reports/54A13_REPORT.md)
- [`54A14_REPORT.md`](reports/54A14_REPORT.md)
- [`54A15_REPORT.md`](reports/54A15_REPORT.md)
- [`54A16_REPORT.md`](reports/54A16_REPORT.md)
- [`54A17_REPORT.md`](reports/54A17_REPORT.md)
- [`54A18_BENCH_NOTES.md`](reports/54A18_BENCH_NOTES.md)
- [`54A18_REPORT.md`](reports/54A18_REPORT.md)
- [`54A19_REPORT.md`](reports/54A19_REPORT.md)
- [`54A20_REPORT.md`](reports/54A20_REPORT.md)
- [`54A21_REPORT.md`](reports/54A21_REPORT.md)
- [`54A22_REPORT.md`](reports/54A22_REPORT.md)
- [`54A23_REPORT.md`](reports/54A23_REPORT.md)
- [`54A24_REPORT.md`](reports/54A24_REPORT.md)
- [`54A26_REPORT.md`](reports/54A26_REPORT.md)

## Wyniki (21)

- [`54A5_RESULTS.json`](results/54A5_RESULTS.json)
- [`54A6_RESULTS.json`](results/54A6_RESULTS.json)
- [`54A7_RESULTS.json`](results/54A7_RESULTS.json)
- [`54A8_RESULTS.json`](results/54A8_RESULTS.json)
- [`54A9_RESULTS.json`](results/54A9_RESULTS.json)
- [`54A10_RESULTS.json`](results/54A10_RESULTS.json)
- [`54A11_RESULTS.json`](results/54A11_RESULTS.json)
- [`54A12_RESULTS.json`](results/54A12_RESULTS.json)
- [`54A13_RESULTS.json`](results/54A13_RESULTS.json)
- [`54A14_RESULTS.json`](results/54A14_RESULTS.json)
- [`54A15_RESULTS.json`](results/54A15_RESULTS.json)
- [`54A16_RESULTS.json`](results/54A16_RESULTS.json)
- [`54A17_RESULTS.json`](results/54A17_RESULTS.json)
- [`54A18_RESULTS.json`](results/54A18_RESULTS.json)
- [`54A19_RESULTS.json`](results/54A19_RESULTS.json)
- [`54A20_RESULTS.json`](results/54A20_RESULTS.json)
- [`54A21_RESULTS_SUMMARY.json`](results/54A21_RESULTS_SUMMARY.json)
- [`54A22_RESULTS.json`](results/54A22_RESULTS.json)
- [`54A23_RESULTS.json`](results/54A23_RESULTS.json)
- [`54A24_RESULTS.json`](results/54A24_RESULTS.json)
- [`54A26_RESULTS_SUMMARY.json`](results/54A26_RESULTS_SUMMARY.json)
