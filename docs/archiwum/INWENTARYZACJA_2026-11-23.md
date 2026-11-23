# Inwentaryzacja archiwum — 2026-11-23

## Zakres i metoda

Inwentaryzacja obejmuje wszystkie pliki zwrócone przez skrypt PowerShell uruchomiony w lokalnej kopii repozytorium dla katalogu `docs/archiwum/`. Raport CSV został przekazany do analizy 2026-11-23.

Dla każdego pliku zapisano ścieżkę względną, rozmiar, rozszerzenie i SHA-256. Porównanie sum SHA-256 wykazało **0 grup identycznych plików** w zbadanym katalogu.

## Wynik

- Liczba plików: **5**
- Łączny rozmiar: **112 480 B**
- Liczba grup identycznych SHA-256: **0**
- Pliki do usunięcia na podstawie tej kontroli: **brak**

| Plik | Rozmiar (B) | SHA-256 |
|---|---:|---|
| `AUDYT_2026-11-14.md` | 1 956 | `18AA2E598E2A45F7FC58A30B72CC57A2C5C4813CDA64DC3F97728F1B8559480F` |
| `HISTORIA_README.md` | 73 704 | `80F481E11540E0DA93A19C2BCECBC5E5100191EE61A822942E1027B4121694D6` |
| `PODSUMOWANIE_PROJEKTU_2026-09-23.md` | 20 802 | `8E53776409B23D94E70C8ABC48DE12C0E91E0E5F2DDC2B9D5C64D97FDE2399F4` |
| `README.md` | 2 025 | `D073ED68F2BFC55B65A796217137F1FE59C51E08DE33ACCF34CA36F80B5D3BBC` |
| `WYNIKI_EKSPERYMENTOW_MIGAWKA_README_2026-11-14.md` | 13 993 | `E4AFA3E1949E74F01B6B9EA5CA5B0B51BCA426D503F600A0590A14A5A3037F30` |

## Wnioski i ograniczenia

1. W zbadanym katalogu nie znaleziono identycznych bajtowo kopii według SHA-256.
2. Żaden z pięciu plików nie został wskazany do usunięcia.
3. Kontrola dotyczy wyłącznie `docs/archiwum/`; nie rozstrzyga o duplikatach w pozostałych katalogach repozytorium.
4. Ten raport nie jest pełnym audytem wszystkich odnośników Markdown. Odnośniki względne, kotwice i odnośniki do katalogów wymagają osobnego testu.
5. Sumy SHA-256 odzwierciedlają lokalny stan repozytorium z chwili wygenerowania przekazanego CSV. Po późniejszych zmianach plików inwentaryzację należy powtórzyć.

## Decyzja

Zachować wszystkie pięć plików. Nie wykonywać automatycznego scalania ani kasowania na podstawie samego podobieństwa nazw lub treści.
