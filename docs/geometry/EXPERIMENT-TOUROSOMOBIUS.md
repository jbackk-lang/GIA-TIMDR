# Eksperyment: Przestrzeń Skrętów Potrójnego Tourosomobius  
Analiza wszystkich kombinacji skrętów Λ–τ–ρ oraz klasyfikacja:  
**stabilny / niedokończony / rozdzielony / trywialny**.

---

## 1. Parametry eksperymentu

Zakresy skrętów:

- **Λ (Möbius)**: 0, 1/2, 1, 3/2, 2  
- **τ (torus)**: 0, 1, 2, 3  
- **ρ (helisa)**: 0, 1, 2, 3  

Łącznie: **80 konfiguracji**.

---

## 2. Klasy wyników

### **A. Struktury stabilne (pełne skręty)**
Warunek:
- Λ ∈ {1, 2}  
- τ ≥ 2  
- ρ ≥ 2  

Wynik:
- pełny potrójny tourosomobius  
- zachowany warunek borromejski  
- brak niedokończeń  
- pełna klasa węzła torusowo‑Möbiusowo‑helikalnego  

Przykłady:
- (Λ=1, τ=2, ρ=2)  
- (Λ=2, τ=3, ρ=3)  
- (Λ=1, τ=3, ρ=2)

---

### **B. Niedokończenia (półskręty)**
Warunek:
- Λ = 1/2 lub 3/2  
- lub ρ = 1/2 (jeśli dopuszczone)  

Wynik:
- struktura spójna topologicznie  
- informacyjnie „pęknięta”  
- brak pełnej orientowalności  
- idealne do modelowania błędów i przerw  

Przykłady:
- (Λ=1/2, τ=2, ρ=3)  
- (Λ=3/2, τ=1, ρ=2)  
- (Λ=1, τ=2, ρ=1/2)

---

### **C. Rozdziały (branching)**
Warunek:
- Λ i τ niezgodne  
- różne klasy globalne przy tej samej dynamice ρ  

Wynik:
- struktura rozszczepia się na różne gałęzie  
- różne interpretacje przy tej samej dynamice  
- częściowa utrata borromejskości  

Przykłady:
- (Λ=1, τ=1, ρ=3)  
- (Λ=2, τ=1, ρ=2)  
- (Λ=1, τ=3, ρ=1)

---

### **D. Struktury trywialne**
Warunek:
- Λ = 0  
- τ = 0  
- ρ = 0  

Wynik:
- zwykły torus  
- brak skrętu  
- brak transformacji  
- brak rozdziału i niedokończeń  

Przykład:
- (Λ=0, τ=0, ρ=0)

---

## 3. Tabela wyników (skrót)

| Λ | τ | ρ | Klasyfikacja |
|---|---|---|--------------

# Pełna tabela kombinacji skrętów Λ–τ–ρ

Zakresy:
- Λ: 0, 1/2, 1, 3/2, 2  
- τ: 0, 1, 2, 3  
- ρ: 0, 1, 2, 3  

Klasyfikacja (uproszczona, zgodna z eksperymentem):
- **trywialny**: Λ=0, τ=0, ρ=0  
- **niedokończony**: Λ=1/2 lub 3/2  
- **stabilny**: Λ∈{1,2} i τ≥2 i ρ≥2  
- **torusowy**: Λ=0, τ>0, ρ=0  
- **helikalny**: Λ=0, τ=0, ρ>0  
- **mieszany**: Λ=0, τ>0, ρ>0  
- **rozdzielony**: pozostałe przypadki z Λ∈{1,2}, nie spełniające warunku stabilny

---

# Tabela 80 kombinacji skrętów Λ–τ–ρ

Klasyfikacja:
- **trywialny** – Λ=0, τ=0, ρ=0  
- **niedokończony** – Λ=1/2 lub 3/2  
- **stabilny** – Λ∈{1,2} i τ≥2 i ρ≥2  
- **rozdzielony** – Λ∈{1,2} i nie spełnia warunku stabilny  
- **torusowy** – Λ=0, τ>0, ρ=0  
- **helikalny** – Λ=0, τ=0, ρ>0  
- **mieszany** – Λ=0, τ>0, ρ>0  

---

## Pełna tabela

| Λ   | τ | ρ | Klasyfikacja |
|-----|---|---|--------------|
| 0   | 0 | 0 | trywialny |
| 0   | 0 | 1 | helikalny |
| 0   | 0 | 2 | helikalny |
| 0   | 0 | 3 | helikalny |
| 0   | 1 | 0 | torusowy |
| 0   | 1 | 1 | mieszany |
| 0   | 1 | 2 | mieszany |
| 0   | 1 | 3 | mieszany |
| 0   | 2 | 0 | torusowy |
| 0   | 2 | 1 | mieszany |
| 0   | 2 | 2 | mieszany |
| 0   | 2 | 3 | mieszany |
| 0   | 3 | 0 | torusowy |
| 0   | 3 | 1 | mieszany |
| 0   | 3 | 2 | mieszany |
| 0   | 3 | 3 | mieszany |
| 1/2 | 0 | 0 | niedokończony |
| 1/2 | 0 | 1 | niedokończony |
| 1/2 | 0 | 2 | niedokończony |
| 1/2 | 0 | 3 | niedokończony |
| 1/2 | 1 | 0 | niedokończony |
| 1/2 | 1 | 1 | niedokończony |
| 1/2 | 1 | 2 | niedokończony |
| 1/2 | 1 | 3 | niedokończony |
| 1/2 | 2 | 0 | niedokończony |
| 1/2 | 2 | 1 | niedokończony |
| 1/2 | 2 | 2 | niedokończony |
| 1/2 | 2 | 3 | niedokończony |
| 1/2 | 3 | 0 | niedokończony |
| 1/2 | 3 | 1 | niedokończony |
| 1/2 | 3 | 2 | niedokończony |
| 1/2 | 3 | 3 | niedokończony |
| 1   | 0 | 0 | rozdzielony |
| 1   | 0 | 1 | rozdzielony |
| 1   | 0 | 2 | rozdzielony |
| 1   | 0 | 3 | rozdzielony |
| 1   | 1 | 0 | rozdzielony |
| 1   | 1 | 1 | rozdzielony |
| 1   | 1 | 2 | rozdzielony |
| 1   | 1 | 3 | rozdzielony |
| 1   | 2 | 0 | rozdzielony |
| 1   | 2 | 1 | rozdzielony |
| 1   | 2 | 2 | stabilny |
| 1   | 2 | 3 | stabilny |
| 1   | 3 | 0 | rozdzielony |
| 1   | 3 | 1 | rozdzielony |
| 1   | 3 | 2 | stabilny |
| 1   | 3 | 3 | stabilny |
| 3/2 | 0 | 0 | niedokończony |
| 3/2 | 0 | 1 | niedokończony |
| 3/2 | 0 | 2 | niedokończony |
| 3/2 | 0 | 3 | niedokończony |
| 3/2 | 1 | 0 | niedokończony |
| 3/2 | 1 | 1 | niedokończony |
| 3/2 | 1 | 2 | niedokończony |
| 3/2 | 1 | 3 | niedokończony |
| 3/2 | 2 | 0 | niedokończony |
| 3/2 | 2 | 1 | niedokończony |
| 3/2 | 2 | 2 | niedokończony |
| 3/2 | 2 | 3 | niedokończony |
| 3/2 | 3 | 0 | niedokończony |
| 3/2 | 3 | 1 | niedokończony |
| 3/2 | 3 | 2 | niedokończony |
| 3/2 | 3 | 3 | niedokończony |
| 2   | 0 | 0 | rozdzielony |
| 2   | 0 | 1 | rozdzielony |
| 2   | 0 | 2 | rozdzielony |
| 2   | 0 | 3 | rozdzielony |
| 2   | 1 | 0 | rozdzielony |
| 2   | 1 | 1 | rozdzielony |
| 2   | 1 | 2 | rozdzielony |
| 2   | 1 | 3 | rozdzielony |
| 2   | 2 | 0 | rozdzielony |
| 2   | 2 | 1 | rozdzielony |
| 2   | 2 | 2 | stabilny |
| 2   | 2 | 3 | stabilny |
| 2   | 3 | 0 | rozdzielony |
| 2   | 3 | 1 | rozdzielony |
| 2   | 3 | 2 | stabilny |
| 2   | 3 | 3 | stabilny |

       |
