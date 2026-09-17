# Widmo Laplasjanu na wstędze Möbiusa — siódme znaczenie "skrętu", rygorystycznie policzone i zweryfikowane dwiema niezależnymi metodami

**Status:** matematyka wyprowadzona analitycznie i potwierdzona numerycznie
(dwie niezależne metody, zgodne w granicach błędu dyskretyzacji — patrz
§3). Odrębne od pozostałych sześciu znaczeń "skrętu" w tym ekosystemie —
patrz `TIMDR_Twists.md` punkt 7 dla formalnej specyfikacji domeny/
przeciwdziedziny i tabeli rozdzielenia. Pełny, źródłowy dokument (z
pełnym wyprowadzeniem, tabelami i dowodami): [`Spectral_Analysis_of_the_
Mobius_Laplacian_v2.pdf`](./Spectral_Analysis_of_the_Mobius_Laplacian_v2.pdf)
(Jacek Kielich, wersja 2 — poprawiona po niezależnym przeglądzie, patrz
"Note on this revision" na początku PDF). Opublikowane na Zenodo:
[10.5281/zenodo.22812269](https://doi.org/10.5281/zenodo.22812269).

## 0. Skąd to się wzięło

Dokument powstał POZA tym repozytorium, jako samodzielna notatka
matematyczna ("Spectral Analysis of the Möbius Laplacian"), oceniona
przez niezależny przegląd i poprawiona w dwóch rundach (v1 → v2: usunięty
niezdefiniowany operator skrętu, dodane jawne założenie o parzystości,
jawnie wybrany warunek brzegowy Dirichleta z dowodem, wycięta
nieuzasadniona sekcja "paraleli" do problemów milenijnych, dodana pełna
weryfikacja numeryczna). Na prośbę użytkownika dołączona teraz do
`GIA-TIMDR` i skatalogowana zgodnie z dyscypliną tego repo — w
szczególności rozgraniczona od WCZEŚNIEJ istniejących, dużo mniej
rygorystycznych użyć słów "Möbius"/"Laplasjan" w tym samym repo (§1).

## 1. Ważne rozgraniczenie PRZED jakąkolwiek matematyką

Ten dokument NIE jest kontynuacją ani formalizacją żadnego z trzech
wcześniej istniejących, luźnych użyć "Möbiusa" w tym repo:

- **`docs/geometry/tourosomobius.md`** ("Potrójny Tourosomobius") —
  jawnie opisany w `TIMDR_Twists.md` jako "wyłącznie notacja pojęciowa:
  brak dziedziny/przeciwdziedziny, brak dowodu, brak kodu, brak testów".
  Warunek borromejski, "skręt Λ Möbiusa jako obrót o 180°", projekcja
  tetraoidalna — żadne z tych pojęć nie występuje w tym dokumencie i
  żadne nie zostało tu ani użyte, ani potwierdzone.
- **`docs/geometry/diffraction_mobius.md`** ("Diffraction as a Double
  Möbius") — zawiera zdanie "The Laplacian of twist reveals where
  interference becomes stable" bez żadnej definicji, dziedziny ani
  dowodu. Ten dokument liczy INNY, konkretny obiekt (Laplasjan na
  wstędze Möbiusa z ustalonym warunkiem brzegowym) i nie potwierdza ani
  nie zaprzecza niczemu w `diffraction_mobius.md` — te dwa teksty są
  matematycznie niepowiązane poza wspólnym słownictwem.
- **`docs/GLOSSARY_EN_PL.md`**, wpis "Möbius Band": *"Odwrócenie fazy,
  zmiana modalności"* — luźna, niesformalizowana sugestia w kierunku
  modalności (gałąź K). Wynik §3-4 tego dokumentu jest w tym samym
  ogólnym kierunku (skręt zmienia dopuszczalne częstotliwości modalne),
  ale jest węższy i innego rodzaju niż "odwrócenie fazy" — patrz §4 dla
  precyzyjnego, ostrożnie sformułowanego związku.

Ten dokument nie jest też instancją żadnego z sześciu WCZEŚNIEJ
skatalogowanych znaczeń "skrętu" (`TIMDR_Twists.md`, punkty 1-6) — jest
siódmym, formalnie odrębnym znaczeniem: **skręt jako warunek
identyfikacji brzegowej definiujący dziedzinę operatora różniczkowego**
(patrz tabela T2 w `TIMDR_Twists.md` po aktualizacji).

## 2. Model geometryczny i wynik (streszczenie)

Wstęga Möbiusa jako iloraz płaskiego cylindra \(S^1\times[-1,1]\) przez
wolne działanie \(\mathbb{Z}/2\), \(\psi(s,t)=(s+\pi,-t)\). Laplasjan
POZOSTAJE klasyczny (\(\Delta u = u_{ss}+u_{tt}\)) — skręt wchodzi
WYŁĄCZNIE przez dziedzinę operatora (funkcje spełniające
\(u(s+\pi,-t)=u(s,t)\)), nie przez modyfikację samego operatora. Przy
warunku Dirichleta na wolnych brzegach \(t=\pm1\), pełne widmo:

\[
\lambda_{k,n} = k^2 + (n\pi/2)^2, \quad (k \text{ parzyste}, n
\text{ nieparzyste}) \text{ lub } (k \text{ nieparzyste}, n
\text{ parzyste}), \quad k\in\mathbb{Z},\, n\geq1.
\]

Stan podstawowy: \(\lambda_1 = \pi^2/4 \approx 2.4674\) — LICZBOWO
identyczny jak dla zwykłego cylindra z tym samym warunkiem brzegowym.
Szczelina widmowa jest więc dziedziczona z warunku Dirichleta, NIE
tworzona przez sam skręt (pełne uzasadnienie, w tym uwaga o przypadku
Neumanna, w którym szczelina znika — PDF §5).

**Co skręt faktycznie, mierzalnie robi:** wybiera podzbiór par \((k,n)\)
— mniej więcej połowę pełnego zbioru \(\mathbb{Z}\times\mathbb{N}\)
dostępnego na cylindrze — usuwając systematycznie te tryby, dla których
parzystość \(k\) i parzystość \(n\) się NIE zgadzają z regułą powyżej.
Zweryfikowane wprost na przykładzie kontrolnym: para \((k,n)=(0,2)\)
istnieje w widmie cylindra, ale jest nieobecna w widmie Möbiusa (PDF §6).

## 3. Weryfikacja (dwie niezależne metody)

1. **Rozdzielenie zmiennych** (forma zamknięta) — wzór powyżej,
   bezpośrednio z klasycznego zagadnienia Sturma-Liouville'a na
   \([-1,1]\).
2. **Niezależna dyskretyzacja 2D** — siatka różnic skończonych 50×40 na
   pełnym cylindrze (schemat pięciopunktowy), operator skrętu \(\Psi\)
   zbudowany jako jawna macierz permutacji (sprawdzone
   \(\Psi^2=I\)), widmo Möbiusa uzyskane przez rzut na podprzestrzeń
   \(+1\) \(\Psi\) i diagonalizację — metoda NIE zakłada rozdzielenia
   zmiennych.

Obie metody zgodne w granicach oczekiwanego błędu dyskretyzacji
\(O(h^2)\) (0.05%–1.8% dla pierwszych 6 wartości własnych, błąd rośnie
z numerem modu — zgodnie z oczekiwaniem, nie jest sygnałem
niezgodności). Pełna tabela: PDF §6, Table 1.

## 4. Kandydujący (NIE ustalony) most do gałęzi K

Wartości własne \(\lambda_{k,n}\) operatora \(-\Delta\) są w standardowej
interpretacji (równanie falowe \(\partial_\tau^2 u=\Delta u\))
częstotliwościami własnymi \(\omega_{k,n}=\sqrt{\lambda_{k,n}}\) — a
częstotliwość jest dokładnie tym, czym `Axioms_K_TIMDR.md` Aksjomat 3
definiuje modalność \((f_i,\phi_i,A_i)\). To daje KONKRETNY, policzalny
(nie słowny) kandydat na most G→K: reguła doboru
\((k\text{ parzyste}\leftrightarrow n\text{ nieparzyste})\) z §2 jest
formalnie regułą selekcji topologicznej na dopuszczalny zbiór
częstotliwości modalnych na powierzchni z tym skrętem.

**To NIE jest ustalony most.** Zgodnie z dyscypliną już zastosowaną dla
mostu Fouriera M/S↔K (`Axioms_K_TIMDR.md`, "Zakres mostu Fouriera
M/S↔K") — jedynego dotąd wyjątku od zasady zerowej identyfikacji między
gałęziami TIMDR — ten kandydat NIE jest tu ogłaszany jako działający
operator międzygałęziowy. Brakuje: (a) definicji, co w tym kontekście
znaczyłoby "interferencja"/"rezonans" (Aksjomaty K4-K5) dla dyskretnego,
nieskończonego zbioru modów \(\{\omega_{k,n}\}\) zamiast skończonej listy
modalności \((f_i,\phi_i,A_i)\); (b) jakiejkolwiek walidacji empirycznej
lub choćby syntetycznej poza samym istnieniem reguły selekcji; (c)
sprawdzenia, czy reguła uogólnia się poza płaski, dokładnie rozwiązywalny
przypadek Möbiusa/cylindra. Traktuj to jako nazwaną, otwartą lukę —
dokładnie tak, jak `Axioms_G_TIMDR_Geometry.md` Aksjomat G4 nazwał
związek skrętu powierzchniowego z krzywizną PRZED jego domknięciem w
G8-G9 — nie jako wynik.

## 5. Ograniczenia, jawnie

- Wynik dotyczy WYŁĄCZNIE płaskiej metryki (\(ds^2+dt^2\)) i warunku
  Dirichleta — inne metryki lub warunek Neumanna dają inny wynik
  (patrz PDF §5, uwaga).
- Weryfikacja numeryczna jest jakości dyskretyzacji skończonej (siatka
  50×40); nie jest to dowód formalny zbieżności, tylko zgodność
  liczbowa w oczekiwanym zakresie błędu.
- §4 powyżej jest świadomie NIEROZSTRZYGNIĘTY kandydat, nie wynik —
  traktuj każde przyszłe odwołanie do "mostu G↔K" jako wymagające
  osobnej, jawnej walidacji, tak jak most Fouriera M/S↔K.

## Powiązane

[`TIMDR_Twists.md`](./TIMDR_Twists.md) (punkt 7 — formalna
specyfikacja domeny/przeciwdziedziny tego znaczenia "skrętu"),
[`Axioms_G_TIMDR_Geometry.md`](./Axioms_G_TIMDR_Geometry.md) (dopisek
cross-referencyjny, nie nowy aksjomat), [`Axioms_K_TIMDR.md`](./Axioms_K_TIMDR.md)
(dopisek o kandydującym moście, ten sam wzorzec co most Fouriera M/S↔K),
[`Spectral_Analysis_of_the_Mobius_Laplacian_v2.pdf`](./Spectral_Analysis_of_the_Mobius_Laplacian_v2.pdf)
(pełny dokument źródłowy), [DOI 10.5281/zenodo.22812269](https://doi.org/10.5281/zenodo.22812269)
(wersjonowany zapis na Zenodo), [`tourosomobius.md`](./tourosomobius.md) i
[`diffraction_mobius.md`](./diffraction_mobius.md) (wcześniejsze, dużo
mniej rygorystyczne użycia "Möbiusa" w tym repo — patrz §1, ten dokument
ich NIE formalizuje ani nie potwierdza).
