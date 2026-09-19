# B4-Kitchen v0.2/v0.3 — log wykonania i weryfikacja hashy (2026-09-19)

## Weryfikacja hashy źródłowych (przed jakimkolwiek uruchomieniem)

Zweryfikowane bezpośrednio (`sha256sum`) na plikach udostępnionych przez
użytkownika, PRZED uruchomieniem v0.2/v0.3, względem
`docs/geometry/b4_kitchen_manifest_template.json` (zamrożonego w v0.1):

```text
$ sha256sum S13_Brownie_Mocap.zip S13_Brownie_Audio.zip
77609d7ecf8478c68013f2c040f9d48c7b560b828ef7c27defb9cf6b4e93aa9f  S13_Brownie_Mocap.zip
27a1ad07ad05cd6c2aea951b34dd35c029e52d758aabcdc998bbda6440a8dc15  S13_Brownie_Audio.zip
```

Zgodne (case-insensitive) z manifestem:
`mocap_archive_sha256=77609D7ECF8478C68013F2C040F9D48C7B560B828EF7C27DEFB9CF6B4E93AA9F`,
`microphone_archive_sha256=27A1AD07AD05CD6C2AEA951B34DD35C029E52D758AABCDC998BBDA6440A8DC15`.
Triangulacja: `triangulation_sha256=9BCDFD51CE489063B2F18A652A31D1882FC7BE52C65100E87F866A91ECFF55E8`
(plik `kitchen_triangulation.json` nie był w ogóle dotykany w v0.2/v0.3,
więc jego hash jest niezmieniony względem v0.1 — nie przeliczany ponownie).

## Log wykonania

Środowisko: sandbox liniowy, 2 vCPU (`nproc`=2). Pojedyncze wywołanie
powłoki ma twardy limit czasu (~150-180s, niezależny od żądanego
timeoutu) — H-trace dla 82 219 klatek (Weingarten na czworościanie,
`ProcessPoolExecutor`, 2 workery) trwa ok. 10 minut łącznie, więc policzony
w resumowalnych partiach przez `core/_kitchen_h_checkpoint_runner.py`
(checkpoint `.npy`, wznawiany między wywołaniami — NIE zmienia żadnej
matematyki, czysto harnas wykonawczy).

**v0.2 (pierwsze liczenie H-trace):**

```text
wywołanie 1: 0 -> 36 000/82 219 klatek (141.4s)
wywołanie 2: 36 000 -> 62 000/82 219 klatek (140.2s)
wywołanie 3: 62 000 -> 82 219/82 219 klatek (63.7s) -- ALL DONE
finalizacja (bloki + kontrole + test główny): 18.2s
```

Wynik v0.2: `controls.passed=false` (kontrola negatywna p=0.0173),
werdykt INCONCLUSIVE, test główny nieuruchomiony. Zapisany:
`B4_KITCHEN_RESULT_v0.2.json`.

**v0.3 (H-trace policzony ponownie od zera — checkpoint z v0.2 usunięty
jako scratch po zapisaniu wyniku v0.2):**

```text
wywołanie 1: 0 -> 70 000/82 219 klatek (140.3s; sandbox mniej obciążony
              niż przy v0.2, stąd wyższy postęp na wywołanie)
wywołanie 2: 70 000 -> 82 219/82 219 klatek (26.6s) -- ALL DONE
finalizacja (bloki + kontrole nowymi ziarnami + test główny n_eff AR(1)): 10.1s
```

Wynik v0.3: `controls.passed=true` (kontrola negatywna p=0.6763),
werdykt **SUPPORTED** (rho=0.0708, p=0.0093). Zapisany:
`B4_KITCHEN_RESULT_v0.3.json`.

**Sanity check między uruchomieniami:** `h_summary`/`q_summary`/
`lambda_g_summary`/`lambda_meta_summary` w obu finalizacjach są
bit-do-bitu identyczne ze sobą i z v0.1 — potwierdza, że dwukrotne
przeliczenie H-trace (raz dla v0.2, raz od zera dla v0.3) dało
deterministycznie ten sam wynik, jak oczekiwano dla nielosowej, czysto
geometrycznej funkcji.

## Pliki wykonawcze (harnas, NIE część zamrożonej analizy)

- `core/_kitchen_h_checkpoint_runner.py` — resumowalny runner H-trace,
  jawnie oznaczony w docstringu jako harnas wykonawczy.
- `core/_kitchen_v03_candidate_methods_synthetic_only.py`,
  `core/_kitchen_v03_calibration_check_synthetic_only.py` — dobór metody
  v0.3, wyłącznie na danych syntetycznych (nigdy Kitchen).

Żaden z powyższych plików nie zmienia definicji operatora Weingartena,
triangulacji, alignmentu czasu ani żadnego zamrożonego parametru — tylko
sposób, w jaki obliczenie jest rozłożone na wiele wywołań powłoki.
