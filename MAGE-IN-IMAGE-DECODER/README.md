# MAGE-IN-IMAGE-DECODER (kod gałęzi, wendorowana kopia)

Moduły skopiowane z siostrzanego repo aplikacyjnego
[`MAGE-IN-IMAGE-DECODER`](https://github.com/jbackk-lang/MAGE-IN-IMAGE-DECODER)
(ogólny detektor obrazu/wideo, NIE formalny fundament TIMDR) — tylko
kod z bezpośrednim związkiem z teorią/metodą TIMDR, bez testów, skryptów
real-data, danych czy dokumentacji PREREG/RESULT (te zostają wyłącznie w
repo źródłowym):

- `meta_dynamics_v1.py` — formalizm Λ-τ-ρ przeniesiony na pole ruchu
  wideo. Zależy wyłącznie od `numpy`. Wynik w repo źródłowym: ρ NOT
  SUPPORTED, Λ częściowy, niepotwierdzony trop.
- `contour_curvature.py` — krzywizna dyskretna konturów 2D (G-branch),
  hipoteza detekcji splicingu. Zależy od `numpy` + `opencv-python`.
  Wynik: częściowo supported, niska moc (N=4).
- `vector_reference.py` — wykrywanie ruchu: optyczny przepływ
  (Farneback) + kalibracja WYŁĄCZNIE na zdrowym nagraniu referencyjnym
  (mediana/MAD, próg z walidacji chronologicznej 60/40) + ocena badanego
  wideo względem tego progu. Metoda analogiczna do referencyjnej
  normalizacji kanałów z `TIMDR-Industrial-Predict`, NIE połączenie z
  faktycznymi pomiarami łożyska. Zależy wyłącznie od `opencv-python` +
  `numpy`. Wynik w repo źródłowym (CDnet 2014, sekwencje `highway`/
  `canoe`, `RESULT_CDNET_INDEPENDENT_v0.1.md`): dodanie tego pola
  wektorowego do MOG2 podnosi makro F1 o +0.03 (0.64→0.67), kosztem
  recall na rzecz precision — umiarkowana, nie rozstrzygająca poprawa.

Żaden z tych trzech plików nie importuje niczego innego z repo
źródłowego (`i2d_core` itd.) — to jest cały kod tych gałęzi, nic więcej.
