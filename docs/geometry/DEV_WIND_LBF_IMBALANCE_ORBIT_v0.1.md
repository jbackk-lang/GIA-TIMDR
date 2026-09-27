# DEV — turbina LBF: niewyważenie jako zgięta rura (orbita), v0.1 — zatrzymane w rozwoju

Data: 2026-09-27. Tylko pliki rozwojowe (pierwsza trzecia każdej klasy); pliki ewaluacyjne nieotwierane dla tych kanałów.
Kod: `core/wind_lbf_orbit.py`.

**Idea (J. Kielich):** rura zgina się i skręca. Dla niewyważenia wirnika naturalną rurą jest orbita
z(t) = x + i y z dwóch poziomych kierunków drgań: siła odśrodkowa wiruje z wirnikiem, więc orbita powinna obiegać
w przód raz na obrót (winding +1). Klasyczny odpowiednik: pełne widmo i orbity z rotordynamiki.

**Sprawdzone kanały** (zegar z tachometru, oś kątowa wirnika, pik rzędu ±1 wobec tła ±0,05–0,3 rzędu):
szczyt wieży (`top_l_x/y`), gondola (`Nacl_x/y`), łożysko przednie (`brng_f_x/y`), dół wieży (`bot_f_x/y`).
Klasy: Healthy, MassImbalance (2023-11-02), InnerRace i InnerRace_MassImbalance (ten sam dzień 2023-12-11 —
naturalna kontrola dnia).

**Wynik rozwoju:** w żadnym kanale niewyważenie nie daje większego piku 1× niż stan zdrowy (np. łożysko:
Healthy 2,75 vs MassImbalance 1,83; gondola 1,14 vs 0,96), a kierunek obiegu (przód/tył) jest zrównoważony we wszystkich
klasach (D1 ≈ 0). Przy wirniku 0,2–0,9 obr/s siła odśrodkowa „średniego” niewyważenia ginie w turbulencji wiatru.

**Decyzja:** test zatrzymany przed pre-rejestracją — nie ma sygnału, który rura mogłaby zgiąć. Pliki eval zostają
nieotwarte (dla tych kanałów). Do sprawdzenia zgięć rury potrzebne są dane, w których 1× jest widoczne (stanowisko
z szybszym wirnikiem, np. wirnik laboratoryjny z czujnikami zbliżeniowymi x/y).
