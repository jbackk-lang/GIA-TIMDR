# ============================================================
#   CORE INIT — centralny interfejs TIMDR
# ============================================================
#
# UWAGA (2026-09-12): `timdr_core.py`, `j_compression.py`, `pipeline.py`
# (wczesny, porzucony prototyp "kompresji bajtowej" TIMDR, T->I->M->I(t)->R->E
# na bajtach) zostaly usuniete audytem AUDIT_AND_CLEANUP_2026-09-12.md -
# zero testow, zero uzycia z zewnatrz poza wzajemnymi importami tego trio.
# Ten __init__.py zostal odpowiednio oczyszczony, zeby `import core` /
# `from core.X import Y` (uzywane przez cala reszte pakietu i testy) dalej
# dzialalo - PRZED ta poprawka usuniecie samych plikow zrodlowych
# zepsuloby import KAZDEGO modulu w core/, bo Python wykonuje __init__.py
# pakietu przy kazdym imporcie submodulu.
# ============================================================

__all__: list = []
