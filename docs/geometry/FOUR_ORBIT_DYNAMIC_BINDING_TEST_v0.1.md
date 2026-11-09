# Test sprzężenia dynamicznego czterech orbit (v0.1)

**Data:** 2026-11-09  
**Zakres:** sprawdzenie, czy wspólna struktura czterech orbit może być podtrzymywana przez wewnętrzne sprzężenie, bez narzucania sztywnego ruchu.  
**Status:** analiza mechaniczna modelu minimalnego i numeryczny test lokalnej sztywności; nie jest to model grawitacji ani walidacja fizyczna TIMDR.

## 1. Punkt wyjścia: jeden czworościan, sześć więzi

Cztery nici mają wspólny motyw początkowy:
\[
X_0(0),X_1(0),X_2(0),X_3(0)\in\mathbb R^3.
\]
Aby związać je wzajemnie bez narzucania wspólnego ruchu, najprostszy model używa sześciu więzi między każdą parą wierzchołków. Niech
\[
d_{ij}^{(0)}=\|X_i(0)-X_j(0)\|,\qquad 0\le i<j\le3.
\]
Wprowadźmy energię:
\[
U_{\rm bind}(X)=\frac12\sum_{i<j}k_{ij}
\left(\|X_i-X_j\|-d_{ij}^{(0)}\right)^2,\qquad k_{ij}>0.
\]
Równania ruchu:
\[
m_i\ddot X_i=-\nabla_{X_i}U_{\rm bind}-\gamma_i\dot X_i+F_i^{\rm ext}.
\]
Jest to minimalny model więzi geometrycznej (sprężynowy tetraedr), a nie grawitacja.

## 2. Co model gwarantuje

- Wszystkie sześć odległości jest karanych energetycznie, jeśli odchylą się od wartości odniesienia.
- Energia ma minimum przy konfiguracji początkowej i przy dowolnym jej wspólnym przesunięciu/obrocie.
- Dla niekoplanarnego czworościanu komplet sześciu krawędzi określa jego kształt z dokładnością do ruchu sztywnego i odbicia. Przy ustalonej orientacji lokalnie pozostaje sześć stopni swobody wewnętrznej, które są stabilizowane przez więzi.
- Model może podtrzymywać kształt czworościanu przy małych zaburzeniach, jeżeli macierz mas jest dodatnia, tłumienie nieujemne, a sztywności dodatnie.

Ważne: nie jest to oddziaływanie długiego zasięgu. Więzi są jawnie zadane między parami punktów.

## 3. Co model NIE gwarantuje

W konfiguracji spoczynkowej wszystkie sprężyny mają długość odniesienia, więc:
\[
\nabla U_{\rm bind}=0.
\]
Jeśli punkty startują ze spoczynku, układ pozostaje w spoczynku. Samo sprzężenie sprężynowe nie uruchamia wspólnej helisy.

Jeśli wszystkie cztery punkty zostaną zadane jako jeden sztywny ruch śrubowy, odległości pozostaną stałe, więc sprężyny o długościach naturalnych \(d_{ij}^{(0)}\) nie będą działać. Taki ruch jest kinematycznie dozwolony, ale nie jest przez te sprężyny samoczynnie generowany ani podtrzymywany. Do ruchu śrubowego potrzebny jest napęd/warunek początkowy albo szczególny stan naprężenia wstępnego, którego równowagę trzeba osobno wykazać.

To rozróżnia:
1. **więź:** układ nie rozpada się geometrycznie;
2. **synchronizacja:** fazy/ruchy pozostają skoordynowane;
3. **napęd:** energia lub moment wprawia strukturę w ruch;
4. **pole fizyczne:** ma własną dynamikę, źródła, jednostki i prawo sprzężenia.

Nie wolno wyciągać punktów 2–4 z samego istnienia więzi.

## 4. Test lokalnej sztywności dla ogólnego czworościanu

Dla potencjału sprężynowego hesjan w minimum ma bloki:
\[
H_{ii}=\sum_{j\ne i}k_{ij}n_{ij}n_{ij}^{T},\qquad
H_{ij}=-k_{ij}n_{ij}n_{ij}^{T},
\]
gdzie \(n_{ij}=(X_i-X_j)/d_{ij}^{(0)}\).

Dla przykładowego czworościanu:
\[
X_0=(0,0,0),\quad X_1=(2,0.2,0.1),\quad
X_2=(0.3,3,0.2),\quad X_3=(0.1,0.4,4),
\]
przy \(k_{ij}=1\), widmo hesjanu numerycznie wynosi:
\[
(0,0,0,0,0,0,\,
0.910035,\,
1.086103,\,
1.290766,\,
2.044105,\,
2.668991,\,
4.000000).
\]
Sześć wartości zerowych odpowiada trzem translacjom i trzem obrotom całego czworościanu. Sześć dodatnich wartości oznacza dodatnią sztywność sześciu modów wewnętrznych. To numeryczny przykład lokalnej sztywności modelu K4, nie dowód istnienia fizycznej siły TIMDR.

## 5. Czy to może przypominać grawitację?

Grawitacja Newtonowska miałaby potencjał par:
\[
U_G=-\sum_{i<j}\frac{Gm_im_j}{\|X_i-X_j\|}.
\]
Jest to jakościowo inny model niż sprężyny:
- siła jest przyciągająca i zależy od odwrotności kwadratu odległości;
- nie ma naturalnej długości odniesienia dla każdej krawędzi;
- sam układ czterech mas nie zachowuje na ogół sztywnego kształtu czworościanu;
- bez dodatkowych warunków początkowych/sił odśrodkowych układ może się zapadać lub silnie deformować.

Aby mówić o analogii grawitacyjnej w TIMDR, trzeba wskazać, co jest źródłem pola, co jest „ładunkiem/masą” nici, jak pole propaguje i jak oddziałuje na trajektorie. Sama wspólna oś lub zachowanie odległości nie wystarczają.

## 6. Wspólny start i jednoczesność

W dyskretnym twierdzeniu BC cztery orbity to klasy reszt modulo 4:
\[
X_j(k)=T^k(v_j).
\]
To zapewnia wspólny indeks kroku \(k\). Ciągła interpolacja \(X_j(s)=\exp(s\Xi)v_j\) jest dodatkową konwencją kinematyczną: wybór generatora \(\Xi\) (logarytmu ruchu \(T\)) może mieć różne gałęzie obrotu. Rekurencja dyskretna sama nie określa fizycznego zegara ani tempa ewolucji. W eksperymencie trzeba więc zdefiniować wspólny parametr czasu i prędkość kątową/postęp niezależnie.

## 7. Rozstrzygnięcie i następny test

**Wynik:** można zbudować jawne sprzężenie, które lokalnie stabilizuje kształt czterech nici jako czworościan. Minimalny model K4 jest matematycznie spójny i ma sześć modów wewnętrznych stabilizowanych więziami. Nie generuje jednak sam z siebie ruchu śrubowego ani pola grawitacyjnego.

Następny rozstrzygający test nie powinien dodawać dowolnego „pola” jako kolejnego parametru. Należy porównać trzy modele przy identycznych warunkach początkowych:
- A: brak sprzężenia;
- B: sześć więzi K4;
- C: jawny potencjał przyciągający Newtona jako kontrola analogii grawitacyjnej.

Mierzyć: sześć odległości, objętość/orientację czworościanu, środek masy, moment pędu, odchylenie od wspólnej osi i fazy czterech orbit. Model C jest wyłącznie kontrolą matematyczną, nie propozycją utożsamienia TIMDR z grawitacją.

**Konkluzja:** istnieje konkretny sposób powiązania czterech nici — sześć wzajemnych więzi geometrycznych. Jest to pierwszy minimalny mechanizm stabilizacji kształtu. Pytanie o mechanizm, który dodatkowo synchronizuje i napędza wspólny ruch, pozostaje otwarte.
