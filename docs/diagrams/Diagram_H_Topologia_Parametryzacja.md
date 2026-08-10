# Diagram H — Topologiczna mapa torus–Möbius z parametryzacją

## 1. Parametryzacja torusa

Torus definiujemy jako:



\[
T(u,v) = 
\begin{cases}
x = (R + r\cos v)\cos u \\
y = (R + r\cos v)\sin u \\
z = r\sin v
\end{cases}
\]



gdzie:
- \(u \in [0, 2\pi)\) — kierunek główny (cykl makro),
- \(v \in [0, 2\pi)\) — cykl poprzeczny (mikro),
- \(R\) — promień główny,
- \(r\) — promień przekroju.

ASCII:

             u →
     ┌───────────────────────┐
     │        TORUS          │
     │    (R + r cos v)      │
     │         ○───○         │
   v ↓      ○         ○
             ○───────○
     └───────────────────────┘

Informacja krąży po torusie w dwóch cyklach:
- **u** — cykl globalny,
- **v** — cykl lokalny.

---

## 2. Parametryzacja pasma Möbiusa



\[
M(u,v) =
\begin{cases}
x = \left(1 + \frac{v}{2}\cos\frac{u}{2}\right)\cos u \\
y = \left(1 + \frac{v}{2}\cos\frac{u}{2}\right)\sin u \\
z = \frac{v}{2}\sin\frac{u}{2}
\end{cases}
\]



gdzie:
- \(u \in [0, 2\pi)\),
- \(v \in [-1, 1]\).

ASCII:

        u →
   ┌───────────────────────┐
   │      MÖBIUS BAND      │
   │   twist: u/2          │
   │   width: v            │
   │   ────╲     ╱────     │
   │        ╲   ╱          │
   │         ╲ ╱           │
   │         ╱ ╲           │
   └───────────────────────┘

Pasmo Möbiusa wprowadza:
- **odwrócenie orientacji**,  
- **skok fazowy**,  
- **zmianę modalności**.

---

## 3. Region przejściowy: Torus → Möbius

ASCII:

        TORUS                     MÖBIUS
   ┌──────────────┐         ┌──────────────┐
   │  u,v cycles   │  --->  │  twist u/2    │
   │  stable flow  │         │  phase flip   │
   └───────┬────────┘         └───────┬──────┘
           │                            │
           ▼                            ▼
   ┌──────────────────────────────────────────┐
   │      TRANSITION REGION (TR)              │
   │  - bifurcation zone                      │
   │  - modal shift                           │
   │  - resonance amplification               │
   └──────────────────────────────────────────┘

---

## 4. Przepływ informacji przez strukturę

ASCII:

   u-cycle (global)
   ┌───────────────────────────────┐
   │   TORUS                       │
   │   I(u,v) →→→→→→→→→→→→→→→→→→   │
   └───────────────┬───────────────┘
                   │
                   ▼
   ┌───────────────────────────────┐
   │   TRANSITION REGION           │
   │   Δφ ≈ π (phase inversion)    │
   └───────────────┬───────────────┘
                   │
                   ▼
   ┌───────────────────────────────┐
   │   MÖBIUS BAND                 │
   │   I(u/2, v) — twisted flow    │
   └───────────────────────────────┘

---

## 5. Znaczenie fizyczne

- Torus → stabilne cykle informacyjne  
- Möbius → zmiana orientacji i modalności  
- Region przejściowy → rezonans, bifurkacja, amplifikacja  
- Całość → **mechanizm powstawania struktur rezonansowych TIMDR**
