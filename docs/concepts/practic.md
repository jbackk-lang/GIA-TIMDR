# RDZEŃ WYKONAWCZY TIMDR/GIA/FUNDAMENTAL v1.0
# (z warstwą psychologiczną)

###############################################
# 1. OBIEKT WYKONAWCZY
###############################################
Obiekt := konfiguracja, która spełnia:
  T ≠ ∅        # ma pole
  I ≠ ∅        # ma dane
  M określone  # ma skręt/perspektywę
  I(t) śledzi  # ma dynamikę
  R ≥ R_min    # jest spójna
  E ≠ ∅        # daje emergencję

###############################################
# 2. OPERATORY WYKONAWCZE TIMDR
###############################################
T(X)      := wybór planszy (kontekstu) dla X
I(X)      := ekstrakcja danych z X
M_p(X)    := X widziane z perspektywy p
I_t(X)    := X w chwili t
ΔI(X)     := zmiana X w czasie
R(X)      := spójność X z polem i sobą
E(S)      := stabilny obiekt wyłoniony z S

###############################################
# 3. GIA — SEMANTYKA WYKONAWCZA
###############################################
Znacznik      := minimalna jednostka znaczenia
Gest          := operacja na znacznikach (skręt, negacja, uogólnienie)
Konfiguracja  := znacznik + gesty + pole
G(X)          := mapa: obiekt → konfiguracja semantyczna

###############################################
# 4. FUNDAMENTAL — FILTR WYKONAWCZY
###############################################
FUND(S):
  if R(S) < R_min: return "szum"
  else: return E(S)

###############################################
# 5. WARSTWA PSYCHOLOGICZNA (WYKONAWCZA)
###############################################
# Psychologia = procesy wewnętrzne jako obiekty TIMDR

Emocja := Obiekt:
  T = pole somatyczno-poznawcze
  I = sygnał (pobudzenie, kierunek)
  M = interpretacja (skręt)
  I(t) = czas trwania
  R = zgodność z kontekstem
  E = działanie / decyzja

Myśl := Gest semantyczny + konfiguracja znaczeń

Schemat := trwały obiekt o wysokim R, powtarzalny w czasie

Impuls := konfiguracja o niskim R, szybka, nietrwała

Reguła:
  Psychologia = dynamika ΔI + skręty M + rezonans R

###############################################
# 6. MECHANIZM WYKONAWCZY (JAK TO DZIAŁA)
###############################################
execute(X):
  S1 = T(X)
  S2 = I(S1)
  S3 = M_p(S2)
  S4 = I_t(S3)
  S5 = R(S4)
  return FUND(S5)

###############################################
# 7. PRZYKŁAD PSYCHOLOGICZNY (WYKONAWCZY)
###############################################
# "Złość"
X = "złość"

execute(X):
  T → ciało + sytuacja
  I → pobudzenie + kierunek
  M → interpretacja: zagrożenie / granica
  I(t) → narastanie
  R → czy adekwatna do pola?
  E → działanie: obrona / komunikat / impuls

###############################################
# 8. PRZYKŁAD JĘZYKOWY
###############################################
# "Nie rozumiem"
X = "nie rozumiem"

execute(X):
  T → pole komunikacyjne
  I → brak mapy znaczeń
  M → skręt: frustracja / ciekawość
  I(t) → narastanie lub wygasanie
  R → czy spójne z kontekstem?
  E → prośba o doprecyzowanie / wycofanie / agresja
