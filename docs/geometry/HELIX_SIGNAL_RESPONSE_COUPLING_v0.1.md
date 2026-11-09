# HELIX–SIGNAL COUPLING: informacja, odpowiedź helisy i pamięć (v0.1)

**Data:** 2026-11-09  
**Cel:** przesunąć środek ciężkości badań z katalogowania własności helisy na badanie wpływu sygnału/informacji na helisę oraz jej odpowiedzi.  
**Status:** synteza architektury badawczej i audyt istniejących komponentów; nie jest to jeszcze potwierdzony model fizyczny.

## 1. Pytanie nadrzędne

Nie pytamy ponownie, czy helisa ma pamięć, zdolność samonaprawy, stabilność lub inne właściwości znane z wcześniejszych badań. Pytamy:

**Jak sygnał wprowadzony do helisy zmienia jej stan, jaką odpowiedź generuje helisa i czy odpowiedź zależy od historii wcześniejszych sygnałów?**

Minimalny cykl:
`u(t) → H → y(t)`
z pamięcią stanu:
`z(t+1)=F(z(t),u(t)); y(t)=G(z(t),u(t))`.

- `u(t)`: kontrolowany sygnał wejściowy (amplituda, częstotliwość, faza, polaryzacja/orientacja, sekwencja, modulacja).
- `z(t)`: stan helisy przed pobudzeniem (stan geometryczny i wewnętrzny, jeśli jest jawnie reprezentowany).
- `y(t)`: obserwowalna odpowiedź (zmiana geometrii, fazy, amplitudy, widma, propagacji, koherencji lub inna wielkość zdefiniowana przez konkretny model).
- `F,G`: nieznane/hipotetyczne prawa sprzężenia, które należy zidentyfikować i przetestować, a nie założyć.

## 2. Co już istnieje w GIA-TIMDR i czego nie należy mylić

### G-Rezonans — najbliższy istniejący komponent geometryczno-dynamiczny
`core/geometric_resonance_operator.py` opisuje zamkniętą krzywą z węzłami mechanicznymi jako układ:
`M x'' + Γ x' + Kx = F(t)`,
z pobudzeniem lokalnym i odpowiedzią częstotliwościową. Geometria wpływa na macierz sztywności przez κ i |τ|.

To jest najbliższy istniejący model odpowiedzi na pobudzenie, ale ma ograniczenia:
- wejście jest zewnętrzną siłą harmoniczną, a nie ogólną informacją/sygnałem;
- wyjście to mechaniczna odpowiedź węzłów i widmo;
- model jest liniowy i ma stałe parametry;
- użycie |τ| usuwa znak chiralności z siły sprzężenia;
- dokumentacja deklaruje brak walidacji na realnej zmierzonej krzywej 3D.

Nie wolno nazywać tego pełnym modelem odpowiedzi informacyjnej helisy ani dowodem pamięci/samonaprawy.

### Gałąź modalna K
`(f, φ, A)` opisuje modalności i ich synchronizację. To opis sygnałów/modalności, nie automatycznie dynamika odpowiedzi geometrii.

### Gałąź sygnałowa M/S
Operator anomalii/defektu/rezonansu sygnałowego klasyfikuje szeregi czasowe. Jej „rezonans” jako koincydencja progów jest czymś innym niż rezonans mechaniczny G lub dopasowanie fazowe K.

### Model T — teoria pola
`Model_T_Field_Theory.md` zawiera ogólny szkic pól informacyjnego, modalnego, rezonansowego i emergentnego. To formalny kierunek, ale sam szkic nie definiuje jeszcze mierzalnego prawa sprzężenia sygnał–helisa.

## 3. Właściwy obiekt badań: odpowiedź helisy na klasę sygnału

Sygnał trzeba opisywać nie tylko jako „pobudzenie”, ale jego strukturą:
- amplituda / energia;
- częstotliwość i widmo;
- faza i jej przebieg;
- orientacja/chiralność;
- czas trwania i obwiednia;
- modulacja i kolejność symboli/zdarzeń;
- korelacje między kanałami/gałęziami.

Odpowiedź należy mierzyć niezależnie w kilku kanałach:
- geometryczny: przemieszczenie, deformacja, zmiana krzywizny/torsji;
- fazowy: przesunięcie fazy, synchronizacja, utrata/odzyskanie lock;
- widmowy: przesunięcie modów, amplituda, Q, transfer;
- propagacyjny: opóźnienie, tłumienie, dyspersja, rozpraszanie;
- informacyjny: rozróżnialność wejść, zachowanie/odtwarzanie payloadu, błąd rekonstrukcji;
- pamięciowy: zależność odpowiedzi na ten sam sygnał od historii wcześniejszego pobudzenia;
- regeneracyjny: powrót do stanu odniesienia po usunięciu zakłócenia, mierzony oddzielnie od samego powrotu częstotliwości.

## 4. Kluczowe rozróżnienie: odpowiedź, pamięć i samonaprawa

Nie utożsamiać:
1. **Reakcji** — wyjście zmienia się podczas pobudzenia.
2. **Pamięci** — identyczne wejście daje różne wyjście zależnie od wcześniejszego stanu/historii.
3. **Adaptacji** — parametry odpowiedzi zmieniają się po treningu/powtarzanym sygnale.
4. **Samonaprawy** — po zakłóceniu obserwowalne zmienne wracają do niezależnie określonego stanu odniesienia.
5. **Odzyskiwania informacji** — payload lub stan informacyjny jest odtworzony, a nie tylko częstotliwość/energia wróciła do normy.

Wcześniejszy `PHASE_RECOVERY_VALIDATION_PROTOCOL.md` słusznie rozdziela odzyskanie częstotliwości od fazy, przebiegu i informacji. Ta dyscyplina obowiązuje również w badaniu helisy.

## 5. Minimalny eksperyment rozstrzygający — ten sam sygnał, różna historia

Najbardziej informacyjny pierwszy test nie powinien być ogromnym sweepem parametrów. Powinien sprawdzić, czy helisa odpowiada na sygnał z pamięcią stanu:

- przygotuj dwa stany początkowe helisy: świeży/odniesienia i po uprzednim pobudzeniu;
- podaj identyczny sygnał testowy `u(t)`;
- zmierz pełną odpowiedź `y(t)` w tych samych kanałach;
- porównaj z kontrolą bez wcześniejszego pobudzenia i z kontrolą bez sprzężenia;
- następnie zastosuj kontrolowane zakłócenie i osobno zmierz relaksację oraz odzyskanie informacji.

Jeżeli odpowiedź na identyczne wejście zależy od historii, mamy mierzalny efekt pamięci wejście–wyjście. Jeśli nie, nie wolno zakładać pamięci w badanym kanale.

## 6. Zasady projektu i falsyfikacji

- Zamrozić definicję sygnału, stan początkowy, kanał odpowiedzi i metrykę przed eksperymentem.
- Użyć kontroli pozytywnej (znana odpowiedź układu) i negatywnej (brak sprzężenia / sygnał niepowiązany).
- Rozdzielić zmianę geometrii od zmiany samego sygnału pomiarowego.
- Zachować znak fazy i chiralność; nie redukować ich do wartości bezwzględnych.
- Porównać odpowiedź helisy z prostszym układem kontrolnym przy tym samym wejściu, energii, paśmie i warunkach.
- Raportować efekt, nie tylko p-value; brak istotności uznać za wynik negatywny tylko przy odpowiedniej mocy.
- Nie stroić modelu na danych testowych.

## 7. Co jest teraz poza zakresem

Nie kontynuować jako głównego celu samego sweepu κ, τ, promienia tunelu ani progu redukcji. Zachować te wielkości jako zmienne opisujące obiekt i potencjalne predyktory odpowiedzi. Nie zmieniać aksjomatów G/K/M ani nie scalać różnych znaczeń rezonansu bez jawnego mostu matematycznego.

## 8. Kryterium sukcesu

Powstaje zweryfikowana mapa:
`(sygnał, stan początkowy, historia, geometria) → odpowiedź helisy`.

Dopiero ta mapa pozwoli ocenić, czy helisa wnosi użyteczną funkcję: selektywność sygnałową, pamięć zależną od historii, kodowanie orientacji/fazy, odporność, adaptację, regenerację lub odzyskiwanie informacji. Każda z tych właściwości wymaga osobnego wyniku i porównania kontrolnego.

**Konkluzja:** geometria helisy jest obiektem i nośnikiem dynamiki. Głównym przedmiotem badań staje się sprzężenie sygnał–helisa–odpowiedź, ze szczególnym naciskiem na zależność odpowiedzi od historii i rozróżnienie pamięci od samonaprawy.
