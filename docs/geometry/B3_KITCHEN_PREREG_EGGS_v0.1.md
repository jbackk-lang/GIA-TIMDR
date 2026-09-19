# B3-Kitchen Eggs v0.1 — prerejestracja wejścia do repliki B4-Kitchen

## Status

**FROZEN BEFORE B4 / GEOMETRY AND TIME GATES OPEN.** Napisane po policzeniu
wyłącznie deterministycznych, nie-statystycznych wielkości (hashe, liczba
klatek, offset czasu) i PRZED jakimkolwiek uruchomieniem operatora
Weingartena czy testu statystycznego na danych Eggs. Ten dokument jest
odpowiedzią na jawnie nazwane w `RESULT_B4_KITCHEN_v0.3.md` "co dalej":
replika na innym przepisie tego samego uczestnika (CMU Kitchen Capture nie
udostępnia przekonwertowanego mocapu AMC/ASF dla żadnego innego uczestnika
niż Subject 13 — patrz uzasadnienie w §0).

## 0. Dlaczego "ten sam uczestnik, inny przepis", nie "inny uczestnik"

Pełna tabela pobrań `kitchen.cs.cmu.edu/main.php` (39 uczestników) ma
skonwertowany `mocap.zip` (AMC/ASF, wymagany przez zamrożony pipeline z
`kitchen_triangulation.json`) **wyłącznie dla Subject 13** — pozostali
uczestnicy udostępniają tylko surowe Video/Audio/IMU/RFID/eWatch, bez
przekonwertowanego mocapu. To zgodne z historią strony (aktualizacja z
2010: "Motion capture files from subject 13 have been converted to AMC
and ASF files"). Subject 13 ma gotowe `mocap.zip`+`Audio.zip` dla czterech
przepisów: Brownie (już użyty w v0.1-v0.3), Eggs, Salad, Sandwich.

**To jest replika kontrolująca zmienność PRZEPISU, nie zmienność
UCZESTNIKA.** Musi być tak nazywana wszędzie, gdzie cytowany jest wynik —
nie zastępuje prawdziwej repliki międzyosobniczej.

## 1. Kandydat danych

```text
dataset_id: CMU_KITCHEN_S13_EGGS_v0.1
geometry_source: S13_Eggs_Mocap.zip / eggs_2.V.global (marker trajectories)
meta_Q_source: S13_Eggs_Audio.zip / AudioTrack.wav
time_source: mocapTime-sync.txt + recording-synch.log (ten sam format co Brownie)
window_size: 50   (identyczne z Brownie — parametr metody, nie danych)
```

Zweryfikowane przed dotknięciem geometrii:

- `participant.ASF` w `S13_Eggs_Mocap.zip` zawiera dokładnie te same
  nazwy stawów co w Brownie: `pelvis`, `lclavicle` (+`lclavicle_phantom`),
  `rclavicle` (+`rclavicle_phantom`), `LowerNeck` (+`LowerNeck_phantom`).
  Ten sam uczestnik (Subject 13) → ta sama hierarchia szkieletu ASF.
- Nagłówek `eggs_2.V.global` ma dokładnie te same 87 kolumn w tej samej
  kolejności co `brownie_1.V.global` (zweryfikowane bezpośrednim
  porównaniem tekstu nagłówka).
- `recording-synch.log` ma ten sam format co w Brownie: `Recording stream
  opened at:` / `Closing recording stream at:`.

## 2. Triangulacja Γ(T,s) — REUŻYTA bez zmian

Ponieważ triangulacja `kitchen_triangulation.json` jest zdefiniowana
wyłącznie przez nazwy stawów w hierarchii ASF (nie przez wartości
współrzędnych ani przez konkretny plik `.V.global`), a hierarchia ASF
Subject 13 jest identyczna w Eggs i Brownie (§1), triangulacja jest
**reużywana bez modyfikacji, bit-do-bitu** — `kitchen_triangulation.json`
NIE jest tworzony na nowo ani edytowany dla Eggs. Jedyna zmiana to
`coordinate_source`, opisana tutaj, a nie w samym artefakcie triangulacji
(który pozostaje poprawny opisem repliki Brownie — patrz jego własny
`artifact_id`).

Ta sama zasada ważności klatki: `abs(V_tetrahedron) > 1e-10 m^3`, wszystkie
12 współrzędnych skończonych. Braki/degeneracja wykluczają klatkę, bez
interpolacji.

## 3. Alignment czasu

Źródłowe znaczniki, odczytane z pobranych archiwów `S13_Eggs_Mocap.zip` /
`S13_Eggs_Audio.zip`:

```text
recording-synch.log: audio start = 12_42_22_6824940
mocapTime-sync.txt:  frame 1     = 12_42_41_6981013
                      frame 58508 = 12_50_49_2544844
```

Offset pierwszej klatki względem startu audio, tą samą formułą co Brownie
(`(h*3600+m*60+s+frac/1e7)`, różnica):

```text
first_frame_offset_s = 19.0156073 s
```

### Reguła indeksu wierszy (identyczna z Brownie)

`eggs_2.AMC` ma jawną numerację **0–58508** (58509 klatek).
`eggs_2.V.global` ma dokładnie 58509 rekordów współrzędnych (58510 linii
= 1 nagłówek + 58509 danych). `mocapTime-sync.txt` zaczyna się od
`Frame:1`, kończy na `Frame:58508`.

```text
V.global record 0  = AMC frame 0  → wykluczony: brak timestampu
V.global record i  = AMC frame i  → paired with mocapTime-sync Frame:i, i=1..58508
```

Klatka `58508` ma geometrię i czas, ale jest wykluczona z B4: `Q_i`
wymaga `T_(i+1)`, którego źródło nie dostarcza. Stąd:

```text
n_geometry_frames (valid H_i/Q_i indices) = 58507   (i = 1..58507)
```

Wybrany kanał audio: `AudioTrack.wav` (mono, ta sama nazwa co w Brownie —
zweryfikowana obecność w archiwum, format nie sprawdzany bit-do-bitu tutaj,
tylko przy uruchomieniu).

```text
start_i = ceil((T_i - T_audio_start) * 44100)
end_i   = ceil((T_(i+1) - T_audio_start) * 44100)
Q_i     = RMSE(AudioTrack.wav[start_i:end_i])
```

Zakazane, identycznie jak w Brownie: cross-correlation, DTW, dobór offsetu,
rozciąganie czasu po zobaczeniu wyniku.

## 4. Bloki i stop condition

```text
window_size = 50
n_total_blocks = ceil(58507 / 50) = 1171   (1170 pełnych + 1 blok po 7 klatek)
```

`n_valid_blocks` (po odrzuceniu bloków z niewalidnymi klatkami geometrii)
jest polem do wypełnienia przez pierwszy deterministyczny przebieg — nie
jest wybierane ani dopasowywane.

## 5. Metoda statystyczna — BEZ zmian, w pełni odziedziczona z v0.3

Ta replika NIE otwiera nowej prerejestracji metody. Używa dosłownie
`ar1_effective_n_spearman()` zamrożonej w
`core/_kitchen_v03_candidate_methods_synthetic_only.py` i opisanej w
`PREREG_B4_KITCHEN_v0.3.md` §2 — żaden parametr (forma korekty n_eff,
próg alfa=0.05, kierunek hipotezy) nie jest tu zmieniany.

Kontrole muszą być regenerowane przy nowej długości `n` (liczba bloków
Eggs różni się od 1645 dla Brownie) — używając TEJ SAMEJ reguły
generowania ziaren co v0.3 (hash etykiety, mechanicznie, bez ręcznego
wyboru), z nowymi etykietami tekstowymi tak, by nie kolidowały z
istniejącymi ziarnami Brownie:

```python
import hashlib
seed_x = int(hashlib.sha256(b"B4_KITCHEN_EGGS_NEG_X").hexdigest()[:8], 16) % 10_000_000
seed_y = int(hashlib.sha256(b"B4_KITCHEN_EGGS_NEG_Y").hexdigest()[:8], 16) % 10_000_000
```

Te ziarna są generowane TERAZ, w tym dokumencie, PRZED policzeniem
jakiejkolwiek geometrii czy audio z Eggs — więc PRZED zobaczeniem wyniku
głównego czy kontroli negatywnej na tych ziarnach.

- **(+) pozytywna**: dwa identyczne monotoniczne wektory długości
  `n_total_blocks` (1171 albo `n_valid_blocks` po ustaleniu), seed
  `20260919` (bez zmian — kontrola zawsze przechodzi niezależnie od
  metody).
- **(−) negatywna**: dwie niezależne serie AR(1), `phi=0.8`, długość
  `n_valid_blocks`, ziarna wyliczone powyżej.

## 6. Werdykt i zasada anty-tuningu

Identyczne z v0.3: SUPPORTED / NOT SUPPORTED / INCONCLUSIVE wg tej samej
bramki (obie kontrole muszą przejść, żeby test główny się liczył). Po
uruchomieniu nie wolno zmieniać niczego z powyższego na podstawie wyniku.
Jeśli kontrola negatywna nie przejdzie na tych ziarnach — wynik to
INCONCLUSIVE, bez próby kolejnych ziaren w ramach tej repliki.

## 7. Co ta replika rozstrzyga, a czego nie

Nawet SUPPORTED tutaj byłoby potwierdzeniem przenośności na inny PRZEPIS
tego samego uczestnika — nie na innego uczestnika. Prawdziwa replika
międzyosobnicza pozostaje otwarta (wymagałaby konwersji surowego Vicon
innego uczestnika do AMC/ASF, poza zakresem tego dokumentu).

## 8. Status końcowy

**B3-Kitchen-Eggs v0.1 — preregistered, not run.** Sekcje 1-6 nie mogą się
zmienić po zobaczeniu wyniku testu głównego ani kontroli.
