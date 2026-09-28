@echo off
REM Odswieza czesc automatyczna STAN_PROJEKTU.md z tabeli wynikow w README.
cd /d "%~dp0"
set PY=python
where python >nul 2>nul || set PY=py
%PY% scripts\stan_projektu.py
pause
