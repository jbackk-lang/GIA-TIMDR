# Wynik 001 — kontrolowany zanik składnika sygnału

Data: 2026-11-19. **Eksperyment syntetyczny, nie odkrycie fizyczne ani pełny test CHF.**

120 s przy fs=360 Hz, dwa sinusoidalne składniki 7 i 13 Hz oraz szum Gaussa (SD 0.13). W pięciu chwilach 16, 35, 58, 79, 103 s usunięto na 0.28 s składnik 13 Hz. Filtry Butterwortha 5–9 i 11–15 Hz zastosowano do całego sygnału przed podziałem na okna 0.25 s (krok 0.05 s). Zbadano RMS, energię górnego pasma, koncentrację różnicy faz i zmienność lokalnej koncentracji faz. Dla każdej miary wybrano pięć największych bezwzględnych odchyleń robust-z, z odstępem minimum 1 s. Dopasowanie: ±0.5 s od środka wstrzykniętego zdarzenia.

| Miara | Trafione z 5 |
|---|---:|
| RMS | 0 |
| Energia pasma 11–15 Hz | **5** |
| Koncentracja różnicy faz | 4 |
| Niestabilność relacji fazowej | 4 |

**Interpretacja:** prosty RMS nie wychwycił zaników, natomiast odpowiednio dobrana klasyczna miara energii pasma wykryła wszystkie. Miary fazowe wykryły 4/5, zatem **brak dowodu przewagi lub nowości CHF**. Ustawienia pasm są świadomie dopasowane do konstrukcji syntetycznego sygnału; to kontrola dodatnia, nie niezależna walidacja. Użyta koncentracja fazy to prosta sonda, a nie pełna implementacja helisy/trinode/bridges.

Wyniki są deterministyczne dla seed=71 i wymagają niezależnego odtworzenia w CI oraz testu na danych naturalnych. Nie interpretować jako p-value, klinicznej diagnozy ani skuteczności w rzeczywistym środowisku.

Następnie: zdarzenia zachowujące energię każdego pasma i przybliżone widmo mocy, zmieniające tylko strukturę czasową; kontrola STFT, matrix profile, koherencja, bispektrum i surogaty; dopiero wtedy pełny CHF.
