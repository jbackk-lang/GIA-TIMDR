# TIMDR 51B.16q — Izolacja procesu i status niezależnej walidacji LRAT

Checkpoint: 2026-11-15.

## Wykonane
W lokalnym prototypie /mnt/data/timdr_51b16q/ utworzono `isolated.py`: weryfikacja manifestu SHA-256 i dowodu LRAT przez proces potomny. Limity POSIX RLIMIT_AS (domyślnie 512 MiB), RLIMIT_CPU, timeout wall-clock oraz limit bajtów wejścia. W przypadku przekroczenia zasobów lub awarii zwracany jest UNVERIFIED, nie VALID_NEGATIVE. Model, CNF i manifest pozostają w semantyce 51B.16p.

`cd /mnt/data/timdr_51b16q && python -m unittest -v`: 12/12 testów zaliczonych (8 wcześniejszych + 4 nowe: poprawny certyfikat, manipulacja modelem, przekroczony limit wejścia, błędny payload). Początkowy limit 128 MiB powodował fałszywe niepowodzenie testu, podniesiono go do 512 MiB.

Archiwum: /mnt/data/timdr_51b16q_prototype.zip.

## Niewykonane
Brak uruchomienia rzeczywiście niezależnego zewnętrznego checkera LRAT. Proces potomny korzysta z tej samej implementacji: izolacja procesu nie jest cross-validation. Nie wykonano analizy rozbieżności z zewnętrznym checkerem. Brak pełnej izolacji bezpieczeństwa: nie ma seccomp, kontenera, separacji uprawnień ani ochrony dostępu do sieci/systemu plików. Nie jest to dowód formalnej poprawności ani pełnej zgodności LRAT.

## Warunek zamknięcia
Uruchomienie niezależnego checkera LRAT na dokładnie tych samych CNF i LRAT, udokumentowanie jego wersji, komend, korpusu i wszystkich rozbieżności. Do tego czasu etap 51B.16q pozostaje częściowo otwarty.
