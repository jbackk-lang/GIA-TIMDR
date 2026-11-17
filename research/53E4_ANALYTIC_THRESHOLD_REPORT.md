# 53E.4 — analityczna granica opłacalności

2026-11-17. Zweryfikowano lokalnym uruchomieniem Pythona 18 kombinacji modelu 53E.3. Status `ANALYTIC_VERIFIED`; porównanie wzoru i symulacji: błąd < 6e-10 J (zaokrąglenia raportowania).

Oszczędność pamięci przy n użyciach: `S(n)=n(C-R-H)-(C+W-R)`.
Odzysk z niezależnego strumienia odpadowego: `E(n)=w*eta_c*eta_d*(1-(1-l)^n)/l` dla l>0, a `E(n)=n*w*eta_c*eta_d` dla l=0.
Netto: `B(n)=S(n)+E(n)-K-n*k`, gdzie K to jednorazowy koszt urządzenia odzysku, k jego koszt na cykl.

Przy parametrach 53E.3, bez K i k: próg 2 użycia dla w=0, 0.001 i 0.005 J/cykl. Przy K=0.02 J i k=0: odpowiednio 4, 4, 3 użycia.

Przykład dla w=0.001 J/cykl: n=1: -0.002450 J; n=2: 0.0078944 J; n=5: 0.0388945572 J; n=10: 0.0904546038 J; n=50: 0.4988196602 J; n=100: 1.0017021889 J.

**Ograniczenia:** wartości energii w J są hipotetycznymi założeniami, a nie pomiarem. Nie wolno podwójnie liczyć tej samej energii jako unikniętych obliczeń i odzysku. Wynik nie dowodzi, że informacja magazynuje energię odzyskiwalną. Próg zależy od kosztu nośnika, sprzętu odzysku i profilu użyć.

Lokalne artefakty w sesji: `/mnt/data/53E/53E4_ANALYTIC_THRESHOLD.py` i `/mnt/data/53E/53E4_RESULTS.json`.
