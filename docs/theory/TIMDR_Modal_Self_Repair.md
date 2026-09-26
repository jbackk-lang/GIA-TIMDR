# Samonaprawiający się model modalny — most K ↔ Chronoproces

Status: **konstrukcja z testami syntetycznymi** (2026-09-27). Kod: `core/modal_self_repair.py`, testy:
`tests/test_modal_self_repair.py` (8/8). Nie jest jeszcze wynikiem na danych rzeczywistych.

## 1. Idea (J. Kielich)

Most do gałęzi modalnej leży między Chronoprocesem a synchronizacją modelu do samonaprawy: model nie tylko porównuje
modalności między sobą, ale **sam przestraja się**, aż zsynchronizuje się z sygnałem.

## 2. Modalności z rury analitycznej

W Chronoprocesie gałąź K czyta φ: T → (f, φ, A). Rura analityczna (`TIMDR_Analytic_Tube.md`) daje to dla każdego pasma
nośnego b: promień A_b(t), fazę φ_b(t), skręt ω_b(t). **Każda rura pasma jest modalnością**; jej „oddech” (widmo A_b)
tworzy mapę rezonansu R_b(α) (tło = 1).

## 3. Model i pętla samonaprawy

Model przewiduje częstotliwości modalne f_k(s) = m_k · s · f_r0 (m_k — mnożnik z geometrii, np. BPFO, BPFI;
f_r0 — nominalna częstotliwość obrotowa; s — współczynnik prędkości, nominalnie 1). Pętla:

1. **Hipoteza:** k = argmax jakości synchronizacji modelu nominalnego (s = 1).
2. **Oczka:** w_b ∝ max(R_b(f_k(s)) − 1, 0) — rury, które rezonują z przewidywaniem (sito samokorygujące).
3. **Pomiar:** przesiane widmo S = Σ w_b R_b; dla harmonicznych h = 1…H szczyt w oknie h·f_k(s)·(1 ± δ/h)
   (interpolacja paraboliczna) → oszacowanie ŝ_h = f_szczytu / (h · m_k · f_r0).
4. **Naprawa:** s ← s + g · (ŝ − s), ŝ = średnia ŝ_h ważona wysokością szczytów; |s − 1| ≤ s_max.
5. Powtórz do zbieżności (|Δs| < 10⁻⁵).

Parametry (jawne, ustalone przed danymi rzeczywistymi): H = 4, δ = 3%, g = 0,7, s_max = 6%, do 25 iteracji.

**Wyjście:** naprawiony model ŝ, **wielkość naprawy** |ŝ − 1|, **jakość synchronizacji** Q(s) = średnia po harmonicznych
najsilniejszego rezonansu rury przy f_k(s) (okno ±1%), przed i po naprawie.

## 4. Sprawdzenie syntetyczne

Uderzenia z częstotliwością BPFO przy prędkości różnej od nominalnej (dzwonienie 5,5 kHz, szum):

| Prawdziwe s | Naprawione ŝ | Q przed | Q po | Iteracje |
|---|---|---|---|---|
| 1,030 | 1,0299 | 2,7 | 65,3 | 9 |
| 0,975 | 0,9751 | 2,9 | 61,1 | 9 |
| 1,000 | 1,0001 | 57,8 | 57,8 | 4 |
| sam szum | 1,011 | 2,8 | 3,0 | — |

Rozstrojenie o 3% niemal gasi synchronizację modelu nominalnego (Q ≈ tło); samonaprawa przywraca ją w kilku krokach
z dokładnością 0,01%. Na szumie naprawa jest ograniczona, a Q pozostaje przy tle — model nie „wmawia” sobie rezonansu.

## 5. Pokrewieństwa i granice

- Znani kuzyni: śledzenie rzędów (order tracking) i pętla fazowa (PLL); porównanie z nimi wymagane przy teście.
- Hipoteza do sprawdzenia: (a) sito z naprawionym modelem rozpoznaje stan łożyska lepiej niż z nominalnym;
  (b) wielkość naprawy i przyrost Q niosą informację diagnostyczną. Rozwój: Paderborn, pomiary 1–15; rezerwa 16–20.
- Most łączy: Chronoproces (wspólny czas, rury), K (zgodność częstotliwości i fazy modalności z modelem) i samokorektę
  sita (oczka ustalane przez rezonans).

## 6. Samonaprawa w czasie — zmienna prędkość (turbiny wiatrowe)

Kod: `core/modal_speed_tracking.py`, testy: `tests/test_modal_speed_tracking.py` (4/4).

Gdy prędkość pływa w trakcie nagrania, jedna stała korekta s nie wystarcza. Model (rzędy uszkodzeń, np. BPFO = 3,05
obrotu) zostaje stały, a **naprawiana jest oś czasu**:

1. **Śledzenie prędkości z samych drgań:** w ramkach 2 s (krok 0,25 s) wybierane jest f maksymalizujące sumę widma przy
   k·f dla rzędów odniesienia k (domyślnie 1, 2, 3: wał, jego harmoniczne, przejście łopat). Pierwsza ramka przeszukuje
   cały zakres [f_lo, f_hi], każda następna tylko ±5% wokół poprzedniego oszacowania — samonaprawa krok po kroku.
2. **Oś kątowa:** θ(t) = ∫ f_r dt; obwiednie rur pasm nośnych (pasma w Hz, bo rezonanse konstrukcji są stałe w Hz)
   przeliczone na równe kroki kąta.
3. **Sito w rzędach:** mapa rezonansu R_b(rząd) i sito samokorygujące przy rzędzie uszkodzenia (cechy QO_k).

Tachometr nie jest wejściem metody — służy wyłącznie do oceny śledzenia.

Sprawdzenie syntetyczne (prędkość rośnie 5 → 7,5 obr/s w 10 s, wał 1× i 3× + uderzenia co 1/3,5 obrotu, szum):
średni błąd śledzenia prędkości **0,74%**; sito w osi kątowej 3,35 wobec 2,44 dla modelu o stałej prędkości (szczyt
~2,5× wyższy) i 1,25 dla turbiny zdrowej.

Plan testu: Fraunhofer LBF (prawdziwa turbina 750 W, prędkość zmienna, tachometr, uszkodzenia łożyska) —
(a) dokładność śledzenia względem tachometru, (b) czy sito w osi kątowej rozpoznaje uszkodzenie lepiej niż sito
o stałej prędkości i klasyczne cechy. Rozwój na części nagrań, zamrożenie, jedna ocena na reszcie.
