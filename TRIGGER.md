# TRIGGER — atlas paradoksów TIMDR (UV/IR, Defekt/Emergentność)

## Metodologia

Każdy paradoks w tym repo jest traktowany jako przypadek UV/IR i rozstrzygany
wyłącznie w dwóch osiach:

- **Lokalnie (UV)** — czy paradoks wynika z niedomknięcia definicji, złej
  referencji, błędnego progu, niepełnej struktury lub lokalnej niespójności.
- **Globalnie (IR)** — czy paradoks wynika z powstania nowej struktury
  globalnej, której nie da się wyprowadzić z lokalnych faktów
  (Emergentność), albo przeciwnie: czy globalna struktura nie powstaje, mimo
  poprawnej lokalnej matematyki.

Żadne etykiety liczbowe (`/2`, `/118`) nie są używane, dopóki nie zostaną
formalnie zdefiniowane w repo. Zamiast tego wyłącznie:

- **Defekt (lokalny/UV)**
- **Emergentność (globalna/IR)**

Każdy wpis jest rozstrzygany w czterech krokach: (1) analiza lokalna (UV),
(2) analiza globalna (IR), (3) klasyfikacja TIMDR — Defekt / Emergentność /
przypadek dwuwarstwowy / prawdziwy paradoks UV/IR, (4) werdykt — jednozdaniowe
rozstrzygnięcie + element zmieniający reżim.

Źródło wpisów: udokumentowane, zweryfikowane ustalenia z `timdr-signal-framework`
(sekcje podane przy każdym wpisie) — nie hipotetyczne przykłady.

---

## 1. `ringdown_resonance()` — próg decyduje o wyniku (§7)

1. **Lokalnie (UV):** `is_oscillatory` flippuje True→False przy zmianie
   `noise_floor_factor` z 1.5 na 2.0 — definicja progu nie jest domknięta.
2. **Globalnie (IR):** brak stabilnej struktury; wynik zależy od parametru,
   nie od sygnału.
3. **Klasyfikacja TIMDR:** Defekt (UV).
4. **Werdykt:** Reżim zmienia parametr progu, nie sygnał.

## 2. Helisa Boerdijka–Coxetera → Riemann/pierwsze (§12)

1. **Lokalnie (UV):** helisa jest matematycznie poprawna (dowiedziona
   symbolicznie).
2. **Globalnie (IR):** nie powstaje żadna struktura łącząca ją z liczbami
   pierwszymi.
3. **Klasyfikacja TIMDR:** Emergentność (IR) — negatywna.
4. **Werdykt:** Lokalna geometria nie generuje globalnej struktury; brak
   elementu zmieniającego reżim.

## 3. `prime_spectrum_filter.py` — próg 0.25 vs model Craméra (§13, case 4)

1. **Lokalnie (UV):** próg 0.25 generował artefakty (24.5% fałszywych
   trafień na losowych ciągach).
2. **Globalnie (IR):** po przejściu na model Craméra/Gallaghera pojawia się
   słaba, ale realna korelacja (r=-0.0568, p≈4.4e-57).
3. **Klasyfikacja TIMDR:** dwuwarstwowy: Defekt → Emergentność.
4. **Werdykt:** Reżim zmienia wybór modelu bazowego (metryka domowej
   roboty → model teorii liczb).

## 4. `Category_Q` — słownictwo bez aksjomatów (§15)

1. **Lokalnie (UV):** są pojedyncze morfizmy między sąsiednimi obiektami,
   ale brak morfizmów tożsamościowych.
2. **Globalnie (IR):** struktura nie domyka się do pełnej kategorii.
3. **Klasyfikacja TIMDR:** Defekt (UV).
4. **Werdykt:** Reżim zmienia brakujące morfizmy tożsamościowe.

## 5. Detektor defektu v1→v4 — prawdziwy paradoks UV/IR (§21)

1. **Lokalnie (UV):** detekcja pojedynczego defektu wymaga referencji
   odpornej na zanieczyszczenie.
2. **Globalnie (IR):** śledzenie zmiany reżimu wymaga referencji, która się
   aktualizuje — sprzeczne z (1).
3. **Klasyfikacja TIMDR:** prawdziwy paradoks UV/IR.
4. **Werdykt:** Reżim zmienia gęstość defektów względem okna kalibracyjnego
   (v4 rozdziela wymagania na dwa moduły, ale przy gęstym nasyceniu
   pierwszego bloku kalibracyjnego problem globalny wraca).

## 6. Fuzja MAD-z — odwrócenie kierunku (§25)

1. **Lokalnie (UV):** z-score działa matematycznie poprawnie w każdym
   punkcie.
2. **Globalnie (IR):** brak segmentu „as-new" w oknie referencyjnym
   odwraca kierunek — najzdrowsza próbka wypada jako najbardziej anomalna.
3. **Klasyfikacja TIMDR:** Defekt (UV) → błędna Emergentność (IR).
4. **Werdykt:** Reżim zmienia obecność/brak segmentu referencyjnego „as-new"
   (naprawa: `calibrate()`/`fuse_calibrated()` z zamrożoną referencją).

---

## Podsumowanie atlasu

- 4/6 paradoksów to Defekt (UV) — lokalne niedomknięcie definicji lub
  referencji.
- 1/6 to prawdziwy paradoks UV/IR — strukturalny konflikt dwóch wymagań,
  nieusuwalny bez podziału na moduły.
- 1/6 to czysta Emergentność (IR) — negatywna (brak globalnej struktury).

Atlas jest spójny, nie wymaga nowych osi, zgodny z TIMDR-Core i gotowy do
rozszerzania o kolejne wpisy w tym samym czteroetapowym formacie.
