@echo off
rem Saurin RP6 creator-state fits, closure v004: high fat + muscle-fat from the base correctives with the final rules (strict LBS reference, creator-inverted quads composition-owned). Double-click to start or resume.
cd /d "%~dp0"
copy /y tools\sa6_pd2_fit_v4.py tools\sa6_pd2_fit.py >nul
set "FIT_OUT=out_v4"
set "FIT_STATES=FAHI,MUFAHI"
set "COMP_MASK=1"
set "SEGBULGE=1"
set "ROUNDS=8"
venv\Scripts\python.exe run_fits2.py 3
pause
