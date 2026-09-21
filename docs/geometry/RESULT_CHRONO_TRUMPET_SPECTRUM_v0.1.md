# Wynik: chrono_trumpet_spectrum — widmo zwinięte w trąbkę, dyskretna krzywizna Weingartena. EKSPLORACYJNE, wzorzec ZNAKU KRZYWIZNY MIESZANY między kanałami i plikami — BRAK spójnej struktury, jawnie NIE potwierdzone (2026-09-21)

> Kontynuacja `PREREG_CHRONO_TRUMPET_SPECTRUM_v0.1.md` (zamrożonej PRZED
> uruchomieniem). Kod: `core/chrono_trumpet_spectrum.py`. Operator
> Weingartena (`TIMDR-Geometry-Formalism/timdr_geometry/weingarten.py`)
> użyty BEZ ZMIAN. Nic w kodzie nie zostało zmienione po zobaczeniu
> wyników poniżej.

> **PRZYPOMNIENIE ZASTRZEŻENIA Z PREREG §5 (dotyczy CAŁEGO tego
> dokumentu)**: to jest zadanie DIAGNOSTYCZNE/EKSPLORACYJNE, NIE twardy
> test z formalnym wnioskiem SUPPORTED/NOT_SUPPORTED. Przy `N∈{2,3}`
> punktów na obwodzie każdy pojedynczy wynik `p<0.05` poniżej NIE jest
> promowany do statusu potwierdzonego odkrycia — zgłoszony w pełni z
> liczbami, ale czytany jako obserwacja wstępna wymagająca znacznie
> większego `N` (więcej jednoczesnych kanałów, niedostępnych lokalnie)
> do prawdziwej weryfikacji.

## 0. Konstrukcja (rekapitulacja)

`window_size=256` (zamrożone, PREREG §4.3), wszystkie kolejne,
nieprzecinające się okna całego pliku. Dla każdego okna: widmo macierzy
korelacji `λ_1≥...≥λ_N` (funkcje z `chrono_membrane_bridge.py`, bez
zmian), promień `r_i(t)=λ_i(t)/Σλ(t)` (znormalizowany), kąt
`θ_i=2π(i-1)/N` (stały), wysokość `z(t)=t` [s]. Siatka trójkątna
zbudowana wzorem `make_cylinder_mesh` (`i` zawinięte, `t` otwarte).
Krzywizna Gaussa `K=κ_1·κ_2` na wewnętrznych wierzchołkach
(`weingarten.discrete_shape_operator`), test serii Walda-Wolfowitza na
sekwencji `sign(K(i,·))` dla każdego indeksu widma `i` osobno.

## 1. Degeneracja siatki (PREREG §3.4 — sprawdzone empirycznie, nie tylko przewidziane)

| plik | N | T (okien) | wierzchołki wewnętrzne | ważne (nie-degenerate) | ułamek ważnych |
|---|---|---|---|---|---|
| Normal | 2 | 952 | 1900 | 1494 | 78.6% |
| IR_21 | 3 | 477 | 1425 | 1425 | **100.0%** |
| OR6_21 | 3 | 478 | 1428 | 1428 | **100.0%** |

Zgodnie z przewidywaniem PREREG §3.4: `N=2` daje WYRAŹNIE gorszą
degenerację (21.4% wierzchołków odrzuconych przez
`discrete_shape_operator` jako zdegenerowane — rząd macierzy stycznej
<2 przy tylko jednym punkcie kątowym w 1-ringu) niż `N=3` (0% odrzuceń
— trójkątny obwód daje wystarczającą liczbę niezależnych kierunków
stycznych). To jest bezpośrednie potwierdzenie zastrzeżenia zapisanego
PRZED uruchomieniem: struktura geometryczna przy `N=2` jest realnie
osłabiona, nie tylko teoretycznie.

## 2. Wynik testu serii per indeks widma `i`, per plik

### Normal (N=2)

| i | n1 (+) | n2 (−) | n | n_zero | n_nan(degen.) | R | E[R] | z | p |
|---|---|---|---|---|---|---|---|---|---|
| 0 | 320 | 458 | 778 | 0 | 174 | 431 | 377.76 | +3.944 | **8.01e-05** |
| 1 | 293 | 423 | 716 | 0 | 236 | 393 | 347.20 | +3.543 | **3.96e-04** |

Oba indeksy widma (`λ_1` największa, `λ_2` najmniejsza) pokazują
**więcej serii niż losowo oczekiwane** (`z>0`, `p<0.05`) — sekwencja
znaku krzywizny Gaussa jest BARDZIEJ naprzemienna wzdłuż czasu niż
losowa kolejność tych samych `n1`/`n2`. Kierunek SPÓJNY między obu
indeksami widma tego samego pliku.

### IR_21 (N=3)

| i | n1 (+) | n2 (−) | n | n_zero | n_nan | R | E[R] | z | p |
|---|---|---|---|---|---|---|---|---|---|
| 0 | 365 | 110 | 475 | 0 | 2 | 141 | 170.05 | **−3.753** | **1.75e-04** |
| 1 | 305 | 170 | 475 | 0 | 2 | 223 | 219.32 | +0.368 | 0.7127 |
| 2 | 416 | 59 | 475 | 0 | 2 | 116 | 104.34 | +2.468 | **0.0136** |

`i=0` (λ_1, dominująca wartość własna): ZNAK PRZECIWNY — mniej serii
niż losowo (`z<0`), czyli krzywizna Gaussa jest bardziej "sklejona"
(dłuższe odcinki jednego znaku) niż losowa kolejność. `i=1`: brak
odchylenia od losowości (`p=0.71`). `i=2` (najmniejsza wartość własna):
więcej serii niż losowo (`z>0`, jak w pliku Normal). **Trzy różne
indeksy widma TEGO SAMEGO pliku dają TRZY różne odpowiedzi** (sklejanie
/ brak struktury / naprzemienność) — brak jednego spójnego wzorca
nawet wewnątrz jednego nagrania.

### OR6_21 (N=3)

| i | n1 (+) | n2 (−) | n | n_zero | n_nan | R | E[R] | z | p |
|---|---|---|---|---|---|---|---|---|---|
| 0 | 395 | 81 | 476 | 0 | 2 | 134 | 135.43 | −0.233 | 0.8156 |
| 1 | 392 | 84 | 476 | 0 | 2 | 151 | 139.35 | +1.841 | 0.0656 |
| 2 | 420 | 56 | 476 | 0 | 2 | 109 | 99.82 | +2.034 | **0.0419** |

`i=0`: brak odchylenia. `i=1`: na granicy (`p=0.066`, NIE przechodzi
`α=0.05`). `i=2`: marginalnie istotne (`p=0.042`), w tym samym kierunku
(naprzemienność) co `i=2` w IR_21 i oba indeksy w Normal.

## 3. Synteza — czy istnieje spójny wzorzec "siatki pól"?

**Krótko: NIE, nie w sensie jednorodnym.** Obserwacje faktyczne:

- **Normal (N=2)**: obie kolumny istotnie NAPRZEMIENNE (`p<0.001` na
  obu), spójny kierunek.
- **IR_21 (N=3)**: JEDNA kolumna istotnie SKLEJONA (`i=0`, przeciwny
  kierunek), JEDNA bez efektu (`i=1`), JEDNA istotnie naprzemienna
  (`i=2`) — trzy różne odpowiedzi w jednym pliku.
- **OR6_21 (N=3)**: dwie kolumny bez jednoznacznego efektu (`i=0`
  zupełnie płasko, `i=1` graniczne), jedna marginalnie naprzemienna
  (`i=2`).
- **Najniższy indeks widma (`i` odpowiadający NAJMNIEJSZEJ wartości
  własnej, `i=N-1`) jest jedynym, który pokazuje SPÓJNY kierunek
  (naprzemienność, `z>0`) na WSZYSTKICH TRZECH plikach** — to jedyna
  regularność widoczna w tych danych, ale przy zaledwie trzech
  niezależnych plikach i braku pre-rejestrowanego uzasadnienia
  fizycznego DLACZEGO akurat najmniejsza wartość własna miałaby to
  robić (nie było to przewidziane przed uruchomieniem — obserwacja
  POST-HOC), jest to dokładnie ten rodzaj wzorca, przed którego
  przedwczesnym uznaniem ostrzega PREREG §5.
- **Dominująca wartość własna (`i=0`, `λ_1`) zachowuje się NIESPÓJNIE**:
  naprzemienna w Normal, sklejona w IR_21, płaska w OR6_21 — trzy
  różne reżimy w trzech plikach na TEJ SAMEJ kolumnie widma.

## 4. Wniosek (jawnie EKSPLORACYJNY, nie klasyfikacja SUPPORTED/NOT_SUPPORTED)

Krzywizna Gaussa na powierzchni "trąbki" NIE jest losowym szumem
znaku wszędzie — 5 z 8 przetestowanych kolumn (`i`) daje `p<0.05` lub
blisko tego progu, co samo w sobie pokazuje, że konstrukcja NIE jest
zdegenerowana (siatka niesie jakąś strukturę, nie jest płaska/losowa).
**Ale kierunek i siła tej struktury są NIESPÓJNE między indeksami
widma i między plikami** — nie ma jednego, powtarzalnego wzorca
"regularnej siatki pól" w sensie, w jakim był operacjonalizowany
(jednolita naprzemienność wzdłuż czasu, ten sam znak efektu wszędzie).
Zgodnie z PREREG §5, **ten wynik NIE jest promowany do statusu
potwierdzonego odkrycia** — jest zgłoszony w pełni jako obserwacja
wstępna. Jedyna cząstkowa regularność (najmniejsza wartość własna
konsekwentnie naprzemienna na 3/3 plikach) jest odnotowana jako
KANDYDAT do przyszłego, OSOBNO pre-rejestrowanego testu z konkretnym
przewidywaniem kierunku sformułowanym PRZED nowymi danymi — nie jako
wynik tej sesji.

**Dodatkowa, metodologicznie ważna obserwacja**: sama degeneracja
siatki (§1) różni się drastycznie między `N=2` (21% odrzuceń) i `N=3`
(0% odrzuceń) — potwierdza to explicite zastrzeżenie PREREG §3.4/§5,
że przy tak małej liczbie punktów na obwodzie interpretacja krzywizny
jest z natury słabo uzasadniona, zwłaszcza dla `N=2`. Test na
znacznie większym `N` (więcej jednoczesnych kanałów, niedostępnych
lokalnie w tym repo — patrz `B4_BEARING_DATA_FREEZE.md`) pozostaje
warunkiem koniecznym prawdziwej weryfikacji tej idei.

## 5. Status w ekosystemie

Eksploracyjne, NIE dopisywane do `Axioms_G_TIMDR_Geometry.md`. Nie
zmienia statusu domknięcia G8-G9 (`weingarten.py` samo w sobie
pozostaje zweryfikowane analitycznie na płaszczyźnie/sferze/walcu —
punkt 6 skilla) — ta sesja jest NOWYM zastosowaniem istniejącego,
niezmienionego operatora do nowego, syntetycznie skonstruowanego
obiektu (widmo-jako-powierzchnia), nie zmianą samego operatora ani
nowym twierdzeniem geometrycznym.
