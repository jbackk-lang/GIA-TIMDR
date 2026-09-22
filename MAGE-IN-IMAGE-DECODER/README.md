# MAGE-IN-IMAGE-DECODER (kod gałęzi, wendorowana kopia)

Dwa moduły skopiowane z siostrzanego repo aplikacyjnego
[`MAGE-IN-IMAGE-DECODER`](https://github.com/jbackk-lang/MAGE-IN-IMAGE-DECODER)
(ogólny detektor obrazu/wideo, NIE formalny fundament TIMDR) — jedyne
dwie rzeczy stamtąd mające bezpośredni związek z teorią TIMDR:

- `meta_dynamics_v1.py` — formalizm Λ-τ-ρ przeniesiony na pole ruchu
  wideo. Zależy wyłącznie od `numpy`.
- `contour_curvature.py` — krzywizna dyskretna konturów 2D (G-branch),
  hipoteza detekcji splicingu. Zależy od `numpy` + `opencv-python`.

Żaden z nich nie importuje niczego innego z repo źródłowego (`i2d_core`
itd.) — to jest cały kod gałęzi, nic więcej.

Testy, skrypty real-data, dane (UCSD Ped2, CASIA2) i wyniki
(PREREG/RESULT: ρ NOT SUPPORTED, Λ częściowy trop; CONTOUR_CURVATURE
częściowo supported przy N=4) zostają w repo źródłowym — nie duplikujemy
ich tutaj.
