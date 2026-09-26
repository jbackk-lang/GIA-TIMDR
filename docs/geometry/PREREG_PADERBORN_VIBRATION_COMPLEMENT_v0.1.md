# PREREG — czy topologia TIMDR uzupełnia klasyczne cechy w obrębie warunku pracy? Drgania Paderborn, v0.1

Zamrożone PRZED obliczeniem cech (2026-09-26). Kod: `core/real_paderborn_vibration_complement.py`.

## 0. Skąd hipoteza

SEU gearset v0.2 (`RESULT_SEU_GEARSET_CONFIRM_v0.2.md`): w obrębie warunku pracy klasyczne + TIMDR 0,86 / 0,80 wobec
klasycznych 0,70 / 0,66 — obserwacja opisowa, poza kryterium. Tu to twierdzenie jest kryterium głównym, na innej maszynie.

## 1. Dane

Paderborn, `K001` (zdrowe), `KA01` (EDM bieżnia zewnętrzna), `KI01` (EDM bieżnia wewnętrzna), kanał `vibration_1`
(64 kHz). Tylko pomiary `train` i `calibration` zamrożonego podziału `TIMDR-AI-Core/prereg/PADERBORN_MS_REPLICATION_v0.1.json`
(SHA-256 `f72623c68918b48c896c31824ac0c984565dd22b3a0dc7af399aba4228a96cf9`); `holdout` nie jest otwierany.
**Ujawnienie:** kanał drgań tych pomiarów był już czytany w AI-Core (activation probe v0.7: model bezbłędny na calibration)
— ryzyko sufitu klasycznych cech; obsługuje je reguła sufitu (§3). Jedno łożysko na klasę.

## 2. Metoda

Decymacja ×4 (`scipy.signal.decimate`, FIR, zero-phase) → 16 kHz. 8 kolejnych okien po 512 próbek od początku zapisu
(32 ms każde), centrowanych. Jeden kanał, więc bez membrany.
- **B (4):** std, kurtoza nadwyżkowa, crest factor, entropia widmowa (te same funkcje co SEU v0.1).
- **T (3):** `winding_metric_fn`, `crossing_metric_fn`, `phase_winding_fn` (bez zmian).
- **BT (7).**
Każdy warunek pracy (N15_M07_F10, N09_M07_F10, N15_M01_F10, N15_M07_F04) standaryzowany własną średnią/std (bez etykiet).
LDA z kurczeniem 0,1, równe priory. Miara: macro-F1 (3 klasy, losowo ≈ 0,33).

## 3. Kryterium główne — w obrębie warunku

Dla każdego warunku: uczenie na oknach pomiarów `train` tego warunku, test na oknach pomiarów `calibration` tego warunku
(rozłączne pliki pomiarowe). g_c = F1(BT) − F1(B).
**SUPPORTED:** średni g ≥ 0,05 i g > 0 w ≥ 3 z 4 warunków. **NOT SUPPORTED:** średni g ≤ 0. Inaczej **MIESZANY**.
**Sufit:** F1(B) ≥ 0,97 w ≥ 3 warunkach → **INCONCLUSIVE (sufit)**.
Opisowo: F1(T) i przeniesienie na nowy warunek (leave-one-condition-out na train+calibration).

## 4. Kontrole

Negatywna: permutacja etykiet uczących (seed 20260926), BT, wszystkie warunki: średni F1 ≤ 0,45.
Pozytywna: syntetyczne okna 512 — szum vs szum z impulsami co 64 próbki (seed 20260926), 100/klasę, uczenie na połowie,
BT: F1 ≥ 0,9. Niezaliczona → INCONCLUSIVE.

## 5. Zasady

Jedno uruchomienie, wynik trafia do README GIA-TIMDR niezależnie od werdyktu.
