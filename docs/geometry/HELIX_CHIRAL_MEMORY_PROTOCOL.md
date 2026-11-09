# Protokół TIMDR: chiralność a pamięć informacyjna helisy

**Status:** protokół badawczy i hipotezy zerowej. Nie dodaje aksjomatu ani nie zmienia G5.

Powiązany eksperyment syntetyczny: [Helix-Lock — helix_chiral_memory_retention.py](https://github.com/jbackk-lang/Helix-Lock/blob/experiment/chiral-memory-retention/experiments/helix_chiral_memory_retention.py).

## 1. Pytanie rozstrzygające

Czy różnica między helisą lewo- i prawoskrętną zmienia samą zdolność zachowania informacji, czy tylko sposób zapisu/odczytu fazy w lokalnym układzie Freneta?

Nie wolno utożsamiać:
- zmiany znaku torsji;
- odbicia współrzędnych fazowych;
- błędu dekodera;
- rzeczywistej utraty informacji.

## 2. Hipoteza zerowa: symetria lustrzana pamięci

Dla pary geometrii lustrzanych:
- krzywizna pozostaje niezmieniona;
- znak torsji zmienia się;
- lokalna faza helisy zmienia znak przy zachowaniu tej samej fazy kanonicznej.

Oznaczmy chiralność przez (h\in\{-1,+1\}), fazę kanoniczną przez \(\phi_c\), a lokalną fazę przez:

\[
\phi_{local}=h\phi_c.
\]

Odczyt kanoniczny wymaga:

\[
\phi_c=h\phi_{local}.
\]

Hipoteza zerowa mówi, że po tej normalizacji lustrzane pary powinny mieć taki sam błąd pamięci i taki sam wskaźnik odzyskania payloadu, jeżeli szum i dynamika również są lustrzanie sparowane.

Dla operatora pamięci zapisanego w lokalnych współrzędnych warunek kowariancji ma postać:

\[
\mathcal M_{-h}(-X)=-\mathcal M_h(X).
\]

To warunek spójności reprezentacji, nie twierdzenie o fizycznym mechanizmie pamięci.

## 3. Zmienne eksperymentalne

Eksperyment Helix-Lock krzyżuje:

| Czynnik | Poziomy |
|---|---|
| Chiralność | lewa, prawa |
| Pamięć | brak historii, ostatnie przejście, pełny cykl |
| Odczyt | nieuwzględniający orientacji, uwzględniający orientację |
| Zakłócenie fazy | 0.25, 0.5, 0.85, 1.2 rad |

Mierzone wielkości:
- błąd estymacji zapamiętanej fazy;
- końcowy błąd fazy;
- dokładność odzyskania symboli payloadu;
- różnica wyników lewej i prawej helisy dla tych samych seedów.

## 4. Kryterium interpretacji

1. Różnica lewo/prawo tylko przy odczycie nieuwzględniającym orientacji oznacza błąd konwencji współrzędnych.
2. Zgodność lewo/prawo po normalizacji wspiera hipotezę zerową dla tego modelu syntetycznego.
3. Różnica lewo/prawo po poprawnej normalizacji jest sygnałem do szukania niesymetrii modelu, błędu implementacji lub jawnego mechanizmu chiralnego. Sama w sobie nie dowodzi fizycznej zależności pamięci od skrętności.
4. Lepszy wynik pełnego cyklu niż ostatniego przejścia dotyczy estymacji historii w tym modelu; nie dowodzi automatycznie pamięci w rzeczywistym Chronoprocesie.

## 5. Czego obecnie nie określa G5

G5 używa modułu torsji w symetrycznym sprzężeniu sztywności. W tej postaci operator nie przechowuje znaku chiralności w macierzy sztywności. Nie wynika z tego jednak, że pamięć całego układu jest niezależna od chiralności — G5 nie jest jeszcze modelem pamięci informacyjnej.

Nie należy dopisywać zależności \(h\)-zależnej do równań pamięci bez:
- definicji stanu pamięci;
- określenia, co jest przechowywaną informacją;
- wskazania źródła sprzężenia lub szumu zależnego od chiralności;
- uzasadnienia wymiarowego i geometrycznego;
- eksperymentu porównawczego z kontrolą niehelikalną.

## 6. Następne kroki

1. Uruchomić i zachować raport CI eksperymentu Helix-Lock.
2. Dodać kontrolę niehelikalną z identycznym szumem i sprzężeniem.
3. Zwiększyć alfabet fazowy i długość payloadu.
4. Oddzielić utratę informacji od błędu dekodowania i od dryfu fazy.
5. Dopiero po wskazaniu uzasadnionego mechanizmu chiralnego rozszerzyć model o parametr zależny od (h\).
6. Porównać wyniki z modelem trzech pętli Chronoprocesu, nie przenosząc wniosków z zabawkowego modelu bezpośrednio do TSI.

## 7. Decyzja

Na obecnym etapie nie ma podstaw, by twierdzić, że pamięć informacyjna helisy zależy od skrętności lewo/prawo. Jest to otwarte pytanie. Pierwszym obowiązkiem jest odróżnić symetrię pamięci od symetrii samej reprezentacji fazowej.
