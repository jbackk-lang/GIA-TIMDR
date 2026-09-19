# B3-Kitchen v0.1 — prerejestracja wejścia do B4-Kitchen

## Status

**FROZEN BEFORE B4 / GEOMETRY AND TIME GATES OPEN.** Surowe archiwa,
mapa czasu oraz triangulacja są zamrożone, a źródłowa numeracja AMC
rozstrzyga uprzednią różnicę jednego rekordu.

## 1. Kandydat danych

Jedynym pierwszym kandydatem jest sesja **CMU Kitchen Capture, Subject 13,
Brownie**. Publiczny katalog sesji wskazuje dla niej równocześnie `mocap.zip`
i `Mic.zip`.

```text
dataset_id: CMU_KITCHEN_S13_BROWNIE_v0.1
geometry_source: mocap.zip / marker trajectories
meta_Q_source: Mic.zip / one declared microphone channel
time_source: source metadata in the downloaded session
geometry_time_mapping_source: mocapTime-sync.txt + recording-synch.log
window_size: 50
```

Zmiana na innego uczestnika, przepis albo mikrofon wymaga nowej wersji B3,
przed uruchomieniem B4.

## 2. Triangulacja Γ(T,s)

Mocap dostarcza szkieletu, nie zeskanowanego meshu ciała. Prerejestrowana
powierzchnia jest dlatego celowo ograniczona do **zamkniętego czworościanu
tułowia** zapisanego w `kitchen_triangulation.json`. Jego cztery wierzchołki
to `pelvis`, `lclavicle`, `rclavicle` oraz `LowerNeck`; wszystkie są jawnymi
kolumnami `brownie_1.V.global` i elementami hierarchii `participant.ASF`.

Artefakt jest wypełniony przed B4 wyłącznie na podstawie nazw stawów i
hierarchii ASF — nie z korelacji z audio ani z wyniku B4. Ma następującą
wiążącą topologię:

```json
{
  "vertices": ["pelvis", "lclavicle", "rclavicle", "LowerNeck"],
  "faces": [[0, 2, 1], [0, 1, 3], [0, 3, 2], [1, 2, 3]],
  "topology_source": "participant.ASF hierarchy",
  "created_before_b4": true
}
```

To nie jest twierdzenie o rzeczywistej powierzchni skóry: wynik B4 dotyczy
wyłącznie tak zdefiniowanej powierzchni kinematycznej. Klatka jest ważna tylko
przy 12 skończonych współrzędnych i `abs(V_tetrahedron) > 1e-10 m^3`.
Braki lub degeneracja unieważniają klatkę; nie są interpolowane ani zerowane.

## 3. Alignment czasu

Źródłowy artefakt synchronizacji jest obecny w pobranych archiwach:

```text
recording-synch.log: audio start = 12_01_45_2056940
mocapTime-sync.txt: frame 1 = 12_02_01_2318490; frame 82220 = 12_13_26_3874417
```

Stały, źródłowo obliczalny offset pierwszej klatki względem początku audio
wynosi `16.0261550 s`. To nie jest parametr dopasowany do wyniku.

### Reguła indeksu wierszy

`brownie_1.AMC` jest źródłowym plikiem ruchu z jawną numeracją **0–82220**:
ma więc 82 221 klatek. `brownie_1.V.global` ma dokładnie 82 221 rekordów
współrzędnych, natomiast `mocapTime-sync.txt` zaczyna numerację od
`Frame:1` i kończy na `Frame:82220`. Reguła parowania, zamrożona przed B4,
brzmi zatem:

```text
V.global record 0  = AMC frame 0  → wykluczony: brak timestampu
V.global record i  = AMC frame i  → paired with mocapTime-sync Frame:i, i=1..82220
```

Klatka `0` nie ma zerowych współrzędnych, lecz jest jawnie nazwana przez
AMC i nie występuje w źródłowej liście timestampów; jej wykluczenie nie
jest parametrem ani doborem po wyniku. Klatka `82220` ma geometrię i czas,
ale jest wykluczona z B4, ponieważ dla definicji `Q_i` brakuje `T_(i+1)`.

Wybrany przed B4 kanał `Q` to `AudioTrack.wav`; mono, 44 100 Hz, 16-bit.
Dla klatki `i`, o timestampie `T_i` z `mocapTime-sync.txt`, używamy:

```text
start_i = ceil((T_i - T_audio_start) * 44100)
end_i   = ceil((T_(i+1) - T_audio_start) * 44100)
Q_i     = RMSE(AudioTrack.wav[start_i:end_i])
```

Ostatnia klatka nie ma źródłowego `T_(i+1)` i jest wykluczona, nie
ekstrapolowana. Tak powstały `Q_i` ma dokładnie tę samą źródłową oś czasu co
`H_i`.

Zakazane są: cross-correlation, DTW, dobór offsetu, osobne offsety per
mikrofon i rozciąganie czasu po obejrzeniu wyniku.

Po utworzeniu triangulacji, dla każdej ważnej klatki geometrii `t_i`:

```text
H_i = mean(H(t_i, s_j) po valid vertices)
Q_i = RMSE wybranego kanału mikrofonu w źródłowo przypisanym przedziale t_i
```

Oba szeregi mają następnie identyczną oś `t_i` i są dzielone na rozłączne
bloki po 50. Ostatni niepełny blok jest raportowany, a nie łączony z innym.

## 4. Manifest i stop condition

Manifest `b4_kitchen_manifest_template.json` zawiera hashe archiwów, mapę
czasu i hash triangulacji. `n_valid_blocks` pozostaje polem do wypełnienia
przez pierwszy, deterministyczny przebieg — nie parametrem do wyboru.

## 5. Co nie jest hipotezą B4

Triangulowany szkielet/markery tworzą prerejestrowaną **powierzchnię
kinematyczną**. Wynik B4-Kitchen może mówić o tej zdefiniowanej geometrii,
nie o bezpośrednio zeskanowanej powierzchni ciała.
