# Rezonans dynamiczny trójwęzła — "co do czego", rozstrzygnięte i przetestowane

**Status:** zaimplementowane i przetestowane (6/6 testów przechodzi,
`tests/test_trefoil_resonance_model.py`). Odpowiedź na doprecyzowanie
użytkownika do `TIMDR_Trefoil_FrenetTorsion.md`: samo słowo "rezonans"
nie znaczy nic bez jasnego przypisania układu/pobudzenia/pomiaru — ten
dokument odpowiada na te trzy pytania explicite, jako **czwarte, jawnie
odrębne znaczenie** słowa "rezonans" w tym ekosystemie.

## 0. Rozgraniczenie PRZED matematyką

`docs/GLOSSARY_EN_PL.md` i `theory/Resonance_M_Operator_Empiryczny.md`
§0 dokumentują już rezonans modalny, rezonans sygnałowy (M) i rezonans
kierunkowy — trzy formalnie odrębne obiekty współdzielące nazwę. Model
w tym dokumencie jest **czwartym**: prawdziwy fizyczny/mechaniczny
rezonans (układ drgający z częstościami własnymi, wzmacniający
odpowiedź przy dopasowaniu częstości pobudzenia) — jakościowo bliższy
duchowi rezonansu modalnego (fale/częstotliwości) niż licznikowi
koincydencji rezonansu M, ale działający na zupełnie innym obiekcie
(sprzężone oscylatory geometryczne, nie modalności falowe).

**Nie mylić też z rezonansem sygnałowym z `TIMDR_Trefoil_FrenetTorsion.md`**
(koincydencja ≥K z N kanałów anomalnych krzywizny/torsji/pozycji) —
ten model dotyczy tej samej figury (trójwęzeł), ale jest zupełnie
innym obiektem matematycznym. Dwa różne "rezonanse" na jednej figurze,
świadomie nierozróżnione nazwą bez przymiotnika — stąd ten cały
rozdział.

## 1. Odpowiedzi na trzy pytania użytkownika

**Co jest układem rezonującym?** Wybrano **Wariant C**: oś helisy jako
"falowód" sprzęgający węzły, węzły jako punkty/masy sprzężenia.
Uzasadnienie wyboru: oryginalna hipoteza mówiła "oś wzdłuż figury
reprezentuje skręt" — oś coś *niesie* (sprzężenie), węzły są punktami,
w których się to zaczepia. To wprost odpowiada obrazowi falowodu z
punktami sprzężenia, nie trzem niezależnym oscylatorom (Wariant B) ani
jednemu bezpostaciowemu układowi (Wariant A) — i naturalnie łączy oś
(H1) z węzłami (H2) w jeden model, zamiast traktować je osobno.

**Co jest pobudzeniem?** Pobudzenie harmoniczne, lokalne, przyłożone
wyłącznie do węzła 1: `F(t) = F₀·cos(ωt)`, `F = [F₀, 0, 0]`. Skanowane
po częstości `ω`.

**Co jest mierzone?** Amplituda ustalonej odpowiedzi zespolonej na
każdym z trzech węzłów, `X(ω) = (K − ω²M + iωΓ)⁻¹F`, oraz wyprowadzone
z niej: położenie pików rezonansowych, ich ostrość (dobroć `Q`,
metoda połowy mocy) i stosunek amplitud sąsiadów do węzła pobudzanego.

## 2. Model

Pierścień 3 tłumionych oscylatorów harmonicznych (węzły 1-2-3-1,
sprzężone przez segmenty osi):

```
M x'' + Γ x' + K x = F(t)
```

`M = diag(m,m,m)` (masy równe), `Γ = diag(γ,γ,γ)` (tłumienie równe),
`K` zawiera sztywność własną każdego węzła na przekątnej i sprzężenie
osiowe między sąsiadującymi węzłami w pierścieniu. **Parametry
zakotwiczone w geometrii, nie dowolne stałe**: sztywność węzła `k₀ ~ κ`
(krzywizna w węźle), sprzężenie osiowe `kc₀ ~ |τ|` (torsja na osi) — z
`core/trefoil_frenet_torsion.py`, gdzie idealny trójwęzeł ma `κ=0,2062`,
`τ=0,3509` identycznie we wszystkich trzech węzłach (potwierdzona
symetria 3-krotna — patrz `TIMDR_Trefoil_FrenetTorsion.md` krok 1).

**Defekt** `D1(Δz1, Δr1, Δτ1)` na węźle 1:
- `Δr1` → zmiana lokalnej sztywności węzła 1: `k1 = k0·(1+Δr1)`.
- `Δτ1` → zmiana sprzężenia osiowego na OBU segmentach stykających się
  z węzłem 1: `kc(3,1) = kc(1,2) = kc0·(1+Δτ1)`.
- `Δz1` → **jawnie NIE reprezentowane w tym modelu**: przesunięcie
  wzdłuż osi zmienia tylko punkt równowagi układu, nie macierze
  `M/K/Γ`, więc nie wpływa na widmo rezonansowe liczone tutaj —
  uczciwe ograniczenie, nie przemilczane (patrz §5 niżej).

## 3. Wyniki

**Baza (bez defektu):** dokładnie zgodnie z teorią pierścienia o
symetrii 3-krotnej — jedna częstość własna niezdegenerowana (singlet,
`ω≈1,015`) i jedna podwójnie zdegenerowana (dublet, `ω≈2,509`,
`ω≈2,509`, różnica `<1e-9`). Pobudzenie węzła 1 daje dokładnie 2
widoczne piki w odpowiedzi.

**Defekt `Δτ1` (sprzężenie osiowe) rozszczepia zdegenerowany dublet** —
klasyczne łamanie symetrii, dokładny mechaniczny odpowiednik "defekt
objawia się w rezonansie":

| Δτ1 | ω (singlet) | ω (dublet, rozszczepiony) |
|---|---|---|
| 0% | 1,0154 | 2,5089 / 2,5089 |
| 10% | 1,0154 | 2,5436 / 2,6117 |
| 30% | 1,0154 | 2,6117 / 2,8060 |
| 60% | 1,0154 | 2,7106 / 3,0745 |

Singlet praktycznie nietknięty (`<0,01` przesunięcia); rozszczepienie
dubletu rośnie monotonicznie z siłą defektu.

**Defekt `Δr1` (sztywność węzła) przesuwa GŁÓWNIE singlet**, dublet
rozszczepia się dużo słabiej (przy `Δr1=60%`: singlet `1,0154→1,1053`,
dublet `2,5089→2,5089/2,5928`) — jakościowo **inny odcisk** w widmie niż
`Δτ1`. To sam w sobie sprawdzalny wynik: z samego kształtu widma
(co się rozszczepia, co się przesuwa) dałoby się w zasadzie wnioskować,
jaki typ defektu zaszedł (promień vs skręt węzła), bez bezpośredniej
obserwacji geometrii.

**Krok 7 — rezonans jako kryterium rewizji.** W przetestowanym zakresie
(`Δτ1` do +120%, `Δr1` do +60%): dobroć `Q` pików rośnie tylko
nieznacznie (np. `Q≈12,44→12,53` dla słabszego piku przy `Δτ1=60%`;
`Q≈31,26→38,04` dla silniejszego), stosunek amplitud sąsiadów do węzła
pobudzanego pozostaje w granicach `0,5–1,0` bez nieproporcjonalnego
wzrostu. **Wniosek: w tym zakresie układ jest stabilny — defekt zmienia
KSZTAŁT widma (przesunięcie/rozszczepienie, diagnostycznie użyteczne),
ale nie eskaluje destrukcyjnie.** Zapisana reguła: sygnał/geometria bez
destrukcyjnego rezonansu = taka, w której defekt przesuwa/rozszczepia
piki, ale nie zwiększa ich dobroci `Q` ani stosunku amplitud sąsiadów
ponad ustaloną wielokrotność linii bazowej (w testach: próg `3×Q₀` i
`1,5×` dla stosunku amplitud — progi robocze, nieskalibrowane na
realnych danych, patrz §5).

**Odkryty niuans (nie planowany, ale odnotowany uczciwie):** przy
większych defektach jedna z dwóch rozszczepionych gałęzi dubletu bywa
słabo sprzężona z pobudzeniem ograniczonym do samego węzła 1 — widoczna
w częstościach własnych, ale nie zawsze jako wyraźny, osobny pik w
`|X₁(ω)|`. To sugeruje, że wybór PUNKTU pobudzenia (nie tylko jego
siły) wpływa na to, którą część rozszczepionego widma w ogóle da się
zaobserwować z danego miejsca pomiaru — osobny wątek do zbadania, nie
rozstrzygnięty tutaj.

## 4. Wniosek

Trzy pytania użytkownika mają teraz konkretne, przetestowane
odpowiedzi: układ = pierścień 3 sprzężonych oscylatorów (Wariant C),
pobudzenie = harmoniczne, lokalne na węźle 1, pomiar = amplituda/dobroć
odpowiedzi ustalonej na każdym węźle. Defekt węzła 1 mierzalnie i w
sposób jakościowo zależny od TYPU defektu (`Δτ1` vs `Δr1`) zmienia
widmo rezonansowe całego układu — to jest właśnie "rewizja przez
rezonans": lokalna zmiana ujawnia się jako globalna zmiana widma,
możliwa do zaobserwowania z dowolnego węzła, nie tylko z tego, gdzie
faktycznie jest defekt.

## 5. Co NIE zostało zrobione (uczciwe ograniczenia zakresu)

- `Δz1` (przesunięcie wzdłuż osi) nie wpływa na ten model dynamiczny w
  ogóle — tylko na punkt równowagi. Model dynamiczny dla `Δz1` wymagałby
  innej reprezentacji (np. nieliniowego sprzężenia zależnego od
  odległości wzdłuż osi), nie zrobione tutaj.
- `K_SCALE=5.0`, `KC_SCALE=5.0`, `γ=0.08` to punkty startowe dobrane do
  tego eksperymentu, **nieskalibrowane** na żadnym realnym rozkładzie —
  analogicznie do `min_curvature` w `the_geo_pro_4d.py`.
- Progi stabilności z kroku 7 (`3×Q₀`, `1,5×` stosunku amplitud) są
  progami roboczymi tego testu regresyjnego, nie ustalonymi granicami
  fizycznymi — przy większym zakresie defektu (`Δτ1>120%`) układ może
  zachowywać się jakościowo inaczej, nieprzebadane.
- Model testowany wyłącznie na jednym punkcie geometrycznym (idealny
  trójwęzeł 1:2:3) — nie sprawdzono innych parametryzacji ani nie
  potwierdzono uogólnienia na inne krzywe węzłowe.
- Zjawisko "ciemnej gałęzi" rozszczepionego dubletu (§3) zaobserwowane,
  ale nie wyjaśnione analitycznie (np. przez rozkład na reprezentacje
  nieprzywiedlne grupy `C₃`) — zostawione jako otwarty wątek.

## Źródła

- Kod: [`../../core/trefoil_resonance_model.py`](../../core/trefoil_resonance_model.py)
- Testy: [`../../tests/test_trefoil_resonance_model.py`](../../tests/test_trefoil_resonance_model.py)
- Geometria bazowa (κ, τ idealnego trójwęzła): [`TIMDR_Trefoil_FrenetTorsion.md`](./TIMDR_Trefoil_FrenetTorsion.md)
- Rozgraniczenie znaczeń "rezonans": [`../GLOSSARY_EN_PL.md`](../GLOSSARY_EN_PL.md),
  [`../theory/Resonance_M_Operator_Empiryczny.md`](../theory/Resonance_M_Operator_Empiryczny.md) §0
