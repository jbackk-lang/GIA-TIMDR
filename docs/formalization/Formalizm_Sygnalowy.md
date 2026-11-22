GIA-TIMDR: Formalizm Sygnałowy
Cel
Formalizm sygnałowy GIA-TIMDR stanowi próbę opisu procesów, struktur i zjawisk nie poprzez obiekty statyczne, lecz poprzez sygnały, ich wzajemne relacje oraz ewolucję w czasie.

Podstawowym założeniem jest traktowanie każdego obserwowalnego zjawiska jako sygnału posiadającego:

amplitudę,
fazę,
kierunek zmian,
pole oddziaływania,
historię czasową.
W tym ujęciu rzeczywistość jest układem sygnałów, a obiekty pojawiają się jako trwałe konfiguracje sygnałowe.

Definicja sygnału
Sygnał opisujemy funkcją:

S(t)=
\{A(t),F(t),P(t),R(t)
\}
gdzie:

$A(t)$ – amplituda,
$F(t)$ – częstotliwość,
$P(t)$ – faza,
$R(t)$ – relacje z innymi sygnałami.
Chronoproces
Podstawowym nośnikiem wszystkich sygnałów jest Chronoproces.

C=(S_1,S_2,S_3,
\ldots,S_n)
Chronoproces nie przechowuje obiektów.

Przechowuje wyłącznie historię zmian sygnałów.

Każda struktura istnieje tylko tak długo, jak długo utrzymuje się spójność sygnałowa.

Pole sygnałowe
Dla sygnału definiujemy pole:

\Phi(x,y,t)
określające zasięg oddziaływania.

Pole może być:

lokalne,
rozproszone,
rezonansowe,
wygasające.
Przykładowa funkcja pola:

\Phi(r)=A 
\cdot e^{-kr}
gdzie:

$r$ – odległość,
$k$ – współczynnik zaniku.
Rezonans
Dwa sygnały tworzą rezonans gdy:

|F_1-F_2|<
\epsilon
oraz

|P_1-P_2|<
\delta
Rezonans powoduje wzrost stabilności układu.

R_{12}=A_1A_2
\cos(P_1-P_2)
Wygaszanie sygnałów
Jeżeli amplituda spada poniżej wartości granicznej:

A(t)
sygnał uznawany jest za wygaszony.

W modelu TIMDR zanik sygnału nie oznacza usunięcia informacji.

Oznacza utratę aktywności operacyjnej.

Obszar stabilności
Dla sygnału definiujemy promień stabilności:

r_s
który tworzy okrąg stabilności.

x^2+y^2=r_s^2
Interpretacja:

wewnątrz okręgu sygnał zachowuje spójność,
na granicy występuje stan przejściowy,
poza granicą następuje dekoherencja.
Klasyfikacja struktur trójkątnych
Dla punktu:

f(P)=x^2+y^2-r_s^2
otrzymujemy:

$f(P)<0$ punkt wewnątrz pola,
$f(P)=0$ punkt graniczny,
$f(P)>0$ punkt poza polem.
Dla trójkąta $T=(A,B,C)$:

S_T=(sgn(f(A)),sgn(f(B)),sgn(f(C)))
powstają klasy:

Stabilna
(-,-,-)
Cała struktura znajduje się w polu stabilności.

Graniczna
Mieszane znaki.

Przynajmniej część struktury znajduje się poza polem.

Niestabilna
(+,+,+)
Cała struktura znajduje się poza polem.

Współczynnik zanurzenia
Definiujemy:

\Psi(T)
=
\frac{Pole(T
\cap K)}
{Pole(T)}
gdzie:

$T$ – trójkąt,
$K$ – obszar stabilności.
Własności:

0 
\leq 
\Psi 
\leq 1
Interpretacja:

$\Psi=1$ pełna stabilność,
$\Psi=0$ brak związku z polem,
$0<\Psi<1$ stan przejściowy.
Formalizm relacyjny
Relacja między sygnałami:

L_{ij}
=
w_aA+w_fF+w_pP
gdzie:

$w_a$ – waga amplitudy,
$w_f$ – waga częstotliwości,
$w_p$ – waga fazy.
Relacje tworzą graf sygnałowy:

G=(V,E)
gdzie:

wierzchołki są sygnałami,
krawędzie są relacjami.
Interpretacja GIA
W GIA sygnał nie jest jedynie przebiegiem czasowym.

Sygnał jest podstawową jednostką ontologiczną modelu.

Obiekty, pojęcia, procesy, zdarzenia i zależności są strukturami sygnałowymi utrzymującymi się w Chronoprocesie.

Zastosowania
Modelowanie wiedzy
Reprezentacja pojęć jako stabilnych struktur rezonansowych.

Sztuczna inteligencja
Budowa pamięci i rozumowania na podstawie pól sygnałowych zamiast statycznych tokenów.

Analiza procesów
Modelowanie systemów dynamicznych:

ekonomicznych,
społecznych,
biologicznych,
technologicznych.
Detekcja anomalii
Zmiany rezonansu i utrata spójności sygnałowej mogą wskazywać na anomalie.

Fizyka i systemy złożone
Badanie przejść fazowych, stabilności struktur i procesów samoorganizacji.

Hipoteza TIMDR
Rzeczywistość może być opisana jako wielowarstwowa sieć sygnałów osadzonych w Chronoprocesie.

Obiekty nie są bytami pierwotnymi.

Pierwotne są sygnały, ich rezonanse, zaniki oraz relacje.

Wiedza jest stanem uporządkowania sygnałów.

Inteligencja jest zdolnością do budowy, stabilizacji oraz aktualizacji takich struktur.
