# B3-A1 v0.2 — Aneks prerejestracyjny: CymruFluency
## Korekta warstwy synchronizacji przed B4

**Status:** AMENDED / FROZEN BEFORE B4.

### 1. Powód korekty

Źródło publikacyjne podaje, że dane 3D i audio były rejestrowane synchronicznie,
3D przy 48 fps, a audio przy 16 kHz. Jednocześnie publiczne metadane datasetu
podają `num_frames = 190...396`, podczas gdy długości plików audio wynoszą
około 0.76–4 s. Te zakresy nie uzasadniają założenia, że pierwsza klatka
meshu odpowiada dokładnie próbce audio w chwili t=0 ani że oba strumienie
mają identyczny czas trwania. citeturn174949search8turn491693search1

W konsekwencji poprzednia wersja aneksu, która wpisywała z góry
[t_i,t_{i+1}) = [i/48,(i+1)/48), była zbyt mocnym założeniem.

### 2. Co pozostaje zamrożone

Bez zmian pozostają:

\[
\Lambda_G
=
\frac{\sigma(H)}
{\sigma(H)+|\bar H|+\varepsilon_G}
\]

\[
\Lambda_{\mathrm{META,disp}}
=
\frac{\sigma(Q)}
{\sigma(Q)+|\mu(Q)|+\varepsilon_M}
\]

oraz:

- `window_size = 50`;
- partycja rozłączna;
- redukcja \(H(t_i,s_j)\rightarrow H_i\) przez średnią po valid vertices;
- `invalid`, nigdy zero;
- hipoteza \(H_1:\rho_s>0\);
- kontrola (+), kontrola (-);
- 10 000 permutacji, seed 0;
- klaster = `(speaker_id, phrase_id)`.

### 3. Zasada synchronizacji obowiązująca w B4

B4 może wykorzystać CymruFluency tylko wtedy, gdy dla konkretnej sekwencji
istnieje **źródłowo uzasadniona mapa czasu audio ↔ czasu 3D**.

Akceptowane są wyłącznie:

1. jawne timestampy/indeksy czasowe obecne w danych;
2. jawna dokumentacja datasetu lub kod autorów określający przesunięcie
   i sposób synchronizacji;
3. równoważny artefakt pochodzący bezpośrednio z procesu akwizycji, który
   zachowuje jednoznaczne przypisanie czasu.

Nie wolno:

- optymalizować offsetu tak, aby zwiększyć korelację;
- wykonać cross-correlation audio↔geometria i wybrać najlepsze przesunięcie;
- dopasowywać początku/końca po obejrzeniu wyniku;
- rozciągać/skraczać osi czasu zależnie od sekwencji;
- użyć DTW;
- zmieniać offsetu osobno dla różnych fraz lub mówców po wyniku.

### 4. Konsekwencja dla RMSE

`Q_i` może być zdefiniowane jako RMSE audio w interwale czasu przypisanym
do klatki 3D **dopiero po uzyskaniu źródłowo uzasadnionej mapy czasu**.

Samo stwierdzenie „audio i 3D są synchronized” jest wystarczające do uznania,
że jest to ten sam eksperyment multimodalny, ale nie wystarcza do odtworzenia
dokładnego indeksu próbki audio dla każdego `frame_id` bez dodatkowej
informacji. citeturn174949search8

### 5. Kryterium kwalifikacji sekwencji

Sekwencja `speaker_id, phrase_id` jest **VALID FOR B4** tylko wtedy, gdy:

- dostępne są wszystkie wymagane klatki 3D dla analizowanego odcinka;
- istnieje jednoznaczna mapa czasu 3D → audio;
- mapowanie nie wymaga strojenia pod wynik;
- można zbudować \(H_i\) oraz \(Q_i\) na tych samych chwilach;
- po zastosowaniu `window_size=50` istnieją wymagane valid blocks.

W przeciwnym przypadku sekwencja ma status **INVALID**, a nie jest
„naprawiana”.

### 6. Kontrola integralności

Manifest B4 musi zawierać dodatkowo:

```text
sequence_id:
speaker_id:
phrase_id:
num_3d_frames:
audio_sample_rate:
audio_num_samples:
audio_duration_s:
three_d_fps:
time_mapping_source:
time_mapping_artifact:
offset_s:
```

`offset_s` może być wpisany tylko wtedy, gdy pochodzi ze źródła/procesu
akwizycji. Jeżeli brak jest takiego artefaktu → `offset_s = UNKNOWN` i sekwencja
nie kwalifikuje się do testu głównego.

### 7. Stan po korekcie

CymruFluency pozostaje kandydatem danych do B4, ale **nie jest jeszcze
manifestem B4**.

B3-A1 v0.2 nie dopuszcza żadnej post-hoc synchronizacji. To celowa blokada
metodologiczna: lepiej zatrzymać B4 niż wprowadzić ukryty parametr dopasowania.

### 8. Źródła

- CymruFluency — Hugging Face, główne metadane i struktura 327 sekwencji.
- CymruFluency — repozytorium 3D mesh.
- CymruFluency — repozytorium audio.
- Bali et al., *CymruFluency - A fusion technique and a 4D Welsh dataset
  for Welsh fluency analysis*, opis akwizycji: 48 fps, zsynchronizowane 3D
  + audio, audio 16 kHz. citeturn491693search0turn398274search2turn174949search8
