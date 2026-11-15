# TIMDR — checkpoint 51B.15a–51B.15d (2026-11-15)

Status: zapis roboczy programu badawczego, z rozdzieleniem twierdzeń, konstrukcji, hipotez i ograniczeń. Kontynuacja po checkpoint 51B.13b–51B.14d. Numer 14D jest oznaczeniem etapu, NIE wymiarem osadzenia.

## 51B.15 — geometria informacyjna Chronoprocesu
Ontologia Chronoprocesu C=(E,a,N,C,P), gdzie a=(MIN,MAX,Δt), pozostaje oddzielona od geometrii. Przestrzeń stanów predykcyjno-relacyjnych S_Φ można reprezentować przez ρ:S_Φ→M, gdzie (M,g) jest opcjonalną rozmaitością informacyjną. Wiązka π:V→M, połączenie ∇, holonomia i przepływ są dodatkowymi strukturami, a nie konsekwencją dotychczasowych aksjomatów. T³ jako przestrzeń faz i skręcenie typu Möbiusa w wiązce to wyłącznie szczególny model. Torus orientowalny; wiązka może być nieorientowalna. Warunek holonomii Hol_γ(∇)Φ_p=Φ_p (dla danego wektora) jest słabszy od Hol_γ(∇)=Id. Zgodność ∇g=0 nie implikuje trywialnej holonomii. Wcześniejsza całka ∮∇_μΦ^i dx^μ nie jest bez dodatkowej identyfikacji włókien poprawnym globalnym warunkiem domknięcia. Wcześniejsze równanie ewolucji metryki z Γ^k_ij xdot^k nie było poprawnie zestawione tensorowo; gradientowe przepływy wymagają zdefiniowania przestrzeni, metryki i funkcjonału F. Minimalizacja KL nie wynika z samej deklaracji F.

## 51B.15a — wierność
Dla skończonego S_Φ istnieje injekcja ρ:S_Φ↪T³; przy topologii dyskretnej S_Φ jest to osadzenie topologiczne na skończony podzbiór rozmaitości Hausdorffa. Dowód przez wybór różnych punktów. Jest to fakt kardynalno-topologiczny, bez treści dynamicznej. Dla relacji R⊆S^k można przenieść ją na obraz: R_ρ(ρ(s₁),...,ρ(s_k)) iff R(s₁,...,s_k). Nie znaczy to, że R jest wyznaczana przez g, krzywiznę lub holonomię. Jeśli reprezentacja wykorzystuje włókno, wymagana może być injektywność pełnego kodu (ρ,ψ).

## 51B.15b — dynamika i zakaz scalania
Dla deterministycznego δ_e i injektywnego ρ funkcja F_e=ρ∘δ_e∘ρ^{-1} na obrazie daje automatyczną zgodność F_e(ρ(s))=ρ(δ_e(s)), ale jest konstrukcją ad hoc. Problem nietrywialny: F_e z narzuconej klasy (gładkie, metryczne, przepływy, wspólne prawo).
Twierdzenie: jeśli ρ∘δ=φ_τ∘ρ, gdzie φ_τ jest mapą czasu lokalnego przepływu gładkiego pola i zdefiniowana na wszystkich kodowanych stanach, to δ jest injektywna, bo φ_τ jest injektywna na dziedzinie. Dla skończonego S i całkowitej δ:S→S oznacza to permutację. Kontrprzykład a→c, b→c nie może być realizowany w ten sposób. Gładki przepływ NIE musi zachowywać arbitralnej relacji porządku na S; wymaga to dodatkowych aksjomatów. Możliwe pozorne scalenie na bazie przy rozdzieleniu pełnych stanów w włóknie, ale nie jest to dowód, że rzeczywisty TIMDR zachowuje wszystkie informacje fizyczne.

## 51B.15c — koszt pamięci i przeszkoda globalna
Niech π:Ṡ→S surjekcja, δ̃:Ṡ→Ṡ bijekcja i π∘δ̃=δ∘π na całym Ṡ. Wtedy δ(S)=δ(π(Ṡ))=π(δ̃(Ṡ))=π(Ṡ)=S. Dla skończonego S δ jest zatem bijektywna. Zatem nieinjektywna skończona δ nie ma globalnego bijektywnego rozszerzenia spełniającego te warunki, nawet dla nieskończonego Ṡ.
Dla kodowania jednego kroku s↦(δ(s),q(s)) injektywność wymaga i wystarcza |Q|≥max_y |δ^{-1}(y)|, gdy etykiety q można dowolnie przypisać; B_min=ceil(log₂ max_y|δ^{-1}(y)|) bitów kodu o stałej długości. To nie jest automatycznie entropia Shannona, która wymaga rozkładu prawdopodobieństwa. Dla a,b→c potrzeba 1 bit. Dla odzyskania stanu początkowego z δ^n(s) koszt B_n=ceil(log₂ max_y |(δ^n)^{-1}(y)|) ≤ceil(log₂|S|). Dla odtwarzania etykietowanych historii długości n kończących się w y, B_n^hist≥ceil(log₂ max_y M_n(y)); gdy M_n(y)≥2^{cn}, wzrost co najmniej liniowy. Liczba bitów nie wyznacza sama wymiaru włókna ciągłego; potrzebne ograniczenia rozdzielczości/szumu.

## 51B.15d — historie i odwracalne rozszerzenia
Dla deterministycznej δ:S→S: H_n={(s₀,...,s_n):s_{i+1}=δ(s_i)}, H_fin=⊔_{n≥0}H_n. Operator dopisywania A(h)=(h,δ(last h)) jest injektywny, ale nie surjektywny (H₀ nie ma poprzedników).
Naturalne rozszerzenie dwustronne Ŝ={(s_k)_{k∈Z}:s_{k+1}=δ(s_k)}; przesunięcie σ jest bijektywne i π₀∘σ=δ∘π₀. π₀ nie musi być surjektywne. Dla skończonego S pozostają tylko orbity cykliczne, stany przejściowe odpadają.
Formalna realizacja wszystkich stanów początkowych: Ṡ=S×Z, δ̃(s,k)=(s,k+1) bijekcja; obszar operacyjny S×N₀; π₊(s,k)=δ^k(s) dla k≥0, więc π₊δ̃=δπ₊ na tym obszarze, nie globalnie na całym Ṡ. Konstrukcja nie optymalizuje pamięci, a parametr s w Ṡ przechowuje identyfikator stanu początkowego.
Dla historii etykietowanych/stochastycznych należy zdefiniować alfabet, dopuszczalność ścieżek i obserwacje; sama funkcja deterministyczna δ nie generuje wykładniczo wielu ścieżek z pojedynczego stanu początkowego.
Problem geometryczny: szukać ρ̃:Ṡ↪V i dyfeomorfizmu F:V→V z Fρ̃=ρ̃δ̃ na obrazie oraz zgodną obserwacją na obszarze operacyjnym. Jeszcze silniejsze: F ma być mapą czasu gładkiego przepływu. Nie każdy dyfeomorfizm jest taką mapą.

## Otwarte 51B.15e
Warunki realizacji odwracalnego rozszerzenia historii przez gładką dynamikę na skończeniewymiarowej rozmaitości; rozróżnić dowolne kodowanie zbiorów, topologiczne osadzenie, dyfeomorfizm, mapę czasu przepływu, stabilność, szum i ograniczoną rozdzielczość. Pamiętać o różnicy: rekonstrukcja stanu początkowego vs pełnej etykietowanej historii vs geometrii relacyjnej. Nie ogłaszać fizycznej zasady zachowania informacji bez osobnych aksjomatów i dowodów.

## Korekty terminologiczne
„Próg bitowy” B_min jest najgorszym przypadkiem długości kodu, nie „entropią wsteczną” bez prawdopodobieństw. Topologiczna/geometryczna realizacja nie wynika z samej injekcji. „Odwracalna realizacja” zawsze określa: globalność projekcji, obszar zgodności, rodzaj mapy i to, co ma być odtwarzalne.
