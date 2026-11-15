# Hipoteza 9 → 3 i „rurka” sygnału w dynamicznym TIMDR

**Data:** 2026-11-14. **Status:** propozycja konstrukcji do decyzji autora, nie aksjomat ani zwalidowany operator.

## Decyzja, której nie wolno podejmować automatycznie

Autor proponuje: przed analizą spektrum określić jednostkową postać sygnału, a jeśli reprezentacja ma dziewięć wymiarów, przejść geometrycznie do trzech; intuicja „zwinięcia sygnału w rurkę”. To jest **hipoteza reprezentacyjna**, nie wynik poprzednich pilotów.

W istniejącej specyfikacji TIMDR domena M/S to `x:T→R^d`, a G dotyczy dopuszczalnej powierzchni w `R³`; K ma własną domenę modalności. Żaden z tych zapisów sam przez się nie narzuca redukcji dowolnego `R⁹` do `R³`. Chronoproces `Ξ=(T,x,Γ,φ)` zachowuje niezależne rzuty.

## Trzy różne konstrukcje

1. **Jednostkowanie:** `u(t)=x(t)/||x(t)||` dla `x(t)≠0`. Daje `u∈S⁸` dla `x∈R⁹`, a nie `R³`. Traci amplitudę, którą trzeba zachować osobno `r(t)=||x(t)||`, jeżeli interesuje nas widmo amplitudowe. Punkt `x=0` wymaga jawnej reguły.
2. **Projekcja:** `p(t)=P u(t)∈R³`, gdzie `P:R⁹→R³` jest jawnie zdefiniowana i ustalona niezależnie od testu. Może utracić częstotliwości, fazy i strukturę sprzężeń. Wymaga porównania widm i błędu rekonstrukcji.
3. **Rurka:** dla krzywej bazowej `c(t)∈R³` i ruchomej ramki normalnej `n₁(t),n₂(t)`, powierzchnia `Γ(t,θ)=c(t)+ρ(t)[cosθ n₁(t)+sinθ n₂(t)]`. Jest to **rzeczywista powierzchnia** przy regularności i braku degeneracji, w przeciwieństwie do pojedynczej krzywej 1D. Zmienna `θ` jest parametrem rodziny przekrojów; jej interpretacja fizyczna nie jest dana automatycznie. Wymaga rozstrzygnięcia ramki (np. transport minimalnego obrotu), promienia, możliwych samoprzecięć i sposobu kodowania pozostałych sześciu stopni swobody.

**Ważne:** projekcja `R⁹→R³` nie jest równoznaczna z konstrukcją powierzchni rurkowej. „Zwinięcie” może być użyte jako intuicja, ale bez mapy nie oznacza bezstratnego zachowania informacji.

## Proponowana architektura bez utraty źródła

```text
surowy x(t)∈R⁹ ────────────────┬── M/S: oryginalny sygnał, zdarzenia
                              ├── K: widmo i faza oryginału (referencja)
                              └── (r(t),u(t)) ── P ── c(t)∈R³
                                                   ├── G: Γ(t,θ), jeśli dopuszczalna
                                                   └── K: widmo projekcji (porównanie)
```

Oryginał i jego znacznik czasu pozostają zachowane; nie zakładać, że sygnał ma znaną kategorię. Dla widma kluczowe jest **porównanie oryginału i reprezentacji** w tych samych oknach czasowych. Gdy `Γ` nie jest powierzchnią regularną, operator kształtu G jest niezdefiniowany — `UNKNOWN`, nie zastępcza „krzywizna”.

## Eksperyment rozstrzygający

- Zdefiniować pochodzenie dziewięciu współrzędnych (9 kanałów? 3×3? dziewięć cech? stopnie swobody układu?) oraz co oznacza „jednostkowa” (normowanie, atom sygnału, jedna modalność czy coś innego).
- Dla sygnałów testowych z różnymi częstotliwościami w poszczególnych kanałach porównać widma `x` i `Px`; wyznaczyć komponenty w jądrze `P` i utraconą energię.
- Przetestować warianty `P` ustalone z góry, uczone tylko na treningu i kontrolę losową, bez strojenia na teście.
- Dla rurki sprawdzić regularność `∂tΓ×∂θΓ≠0`, zachowanie kolejności czasu i wpływ promienia na widmo/krzywiznę.
- Osobno sprawdzić dynamikę zmian `P(t)`: jeśli mapa zmienia się w czasie, sama może generować pozorne częstotliwości.
- Testować zachowanie częstotliwości, amplitud, faz i zdarzeń, opóźnienie detekcji oraz klasę UNKNOWN.

## Pytanie do rozstrzygnięcia przed implementacją

**Skąd w TIMDR bierze się dokładnie dziewięć składowych?** Bez definicji tych dziewięciu współrzędnych nie można dobrać geometrycznie sensownego operatora 9→3 ani ocenić, czy „rurka” zachowuje właściwą informację.

Nie zmieniać aksjomatów M/S, G i K do czasu formalizacji i walidacji mapy.
