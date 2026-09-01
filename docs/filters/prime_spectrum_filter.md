# Prime Spectrum Filter
### Jak działa filtr na liczby pierwsze i dlaczego łączy się z widmem kosmosu

---

## 1. Cel hipotezy

Hipoteza Prime Spectrum Filter miała sprawdzić, czy:

- cyfry rozwinięć √2 i √3,
- pobierane na pozycjach pierwszych,
- połączone operacją XOR,

tworzą nieprzypadkową strukturę widmową, mogącą mieć analogię do "widma
kosmosu" (rozumianego jako rozkład energii, częstotliwości lub sygnałów).
Założenie: √2 (struktura binarna) i √3 (struktura trójkowa) mogą
generować wzór zgodności/niezgodności, który nie jest losowy.

---

## 2. Fundament: trzy liczby i ich zakładane struktury

Filtr opierał się na trzech rozwinięciach dziesiętnych:

- √2 – struktura binarna (45°), zakładana gęstość cyfr pierwszych ≈ 36%
- √3 – struktura trójkowa (60°), zakładana gęstość cyfr pierwszych = 50%
- q = √2 + √3 – struktura mieszana, zakładana gęstość ≈ 48%

(Te wartości to pierwotne, ZAŁOŻONE liczby hipotezy — zmierzone i
obalone w §4 poniżej.)

---

## 3. Mechanizm testowany

**Warstwa 1 — pozycje pierwsze.** Filtr działał wyłącznie na cyfrach
znajdujących się na pozycjach: 2, 3, 5, 7, 11, 13, 17, 19, 23, … ("pierwsze
pozycje").

**Warstwa 2 — XOR(√2, √3).** Dla każdej pozycji pierwszej:

XOR(d₂, d₃) = 0, jeśli cyfry są równe; 1, jeśli cyfry są różne.

Hipoteza przewidywała: stabilną gęstość XOR=1, powtarzalny wzór,
odchylenie od losowości, możliwą analogię do rozkładów widmowych.

---

## 4. Wyniki audytu (WERYFIKACJA, sesja 2026-08-29)

Pełny audyt (precyzja dowolna, `mpmath`, 20 000+ cyfr) wykonany w
`prime_position_filter.md` (testy XOR, histogramy, porównania z
losowością) i `al_filter_predictions.md` (gęstości cyfr, testy
przewidywań) — liczby poniżej nie są tu powtarzane po raz trzeci w
oddzielnych obliczeniach, tylko cytowane z tamtych dwóch audytów.

**Wynik końcowy: hipoteza obalona.** Konkretnie:

- zgodność XOR na pozycjach pierwszych: **9.505%** (2262 pozycje pierwsze
  wśród 20 004 cyfr) — statystycznie nieodróżnialne od 10% oczekiwanych
  dla niezależnych, jednostajnie losowych cyfr (test dwumianowy, p=0.46);
- brak różnicy między pozycjami pierwszymi a niepierwszymi (p=0.29);
- brak różnicy między pozycjami liczb bliźniaczych a pozostałymi
  pierwszymi (p=0.65 — w dodatku w kierunku przeciwnym do hipotezy);
- gęstość cyfr pierwszych {2,3,5,7} w √2, √3 i q, zmierzona bezpośrednio:
  wszystkie trzy ~39.2–39.7%, zgodne z 40% oczekiwanymi dla niezależnych,
  jednostajnie losowych cyfr — **nie** z zakładanymi 36%/50%/48%;
- żadne "widmo" nie wyłania się jako statystycznie istotne;
- brak zdefiniowanego, mierzalnego związku z jakimkolwiek rozkładem
  kosmicznym — porównanie nigdy nie miało testu poza analogią słowną.

---

## 5. Dlaczego hipoteza była sensowna (ale błędna)

**Sensowna:**

- √2 i √3 mają silne, dobrze zbadane struktury matematyczne
  (niewymierność, ciągłe ułamki);
- liczby pierwsze mają własne, realne "widmo" (rozkład Gaussa,
  funkcja ζ Riemanna);
- połączenie dwóch niewymiernych rozwinięć z pozycjami pierwszymi
  wyglądało jak naturalny kandydat na filtr widmowy.

**Błędna:**

- cyfry rozwinięć dziesiętnych √2 i √3 są, w zmierzonym zakresie,
  statystycznie nieodróżnialne od ciągu pseudolosowego;
- pozycje pierwsze same w sobie nie wprowadzają żadnej struktury
  korelacyjnej do cyfr liczby z nimi niepowiązanej;
- XOR dwóch niezależnych, pseudolosowych ciągów nie wzmacnia żadnego
  wzoru — miesza szum z szumem;
- "widmo kosmosu" nie miało w tej hipotezie zdefiniowanego, mierzalnego
  odpowiednika — było powiązaniem czysto skojarzeniowym (ten sam problem,
  co nazwa bez spełnionej struktury formalnej, opisany szerzej w innych
  dokumentach tego repo dla przypadku terminologii kategorii).

---

*Ten dokument zachowuje oryginalną hipotezę w całości (§1-3) — wersję
sprzed audytu, jaką była — i dopisuje pełny wynik audytu (§4-5), zamiast
usuwać albo cichcem poprawiać pierwotny tekst.*
