@echo off
rem Saurin RP6 creator-state fits, closure v003: refine the three heaviest states under the strict composition rule. Double-click to start or resume.
cd /d "%~dp0"
copy /y tools\sa6_pd2_fit_v3.py tools\sa6_pd2_fit.py >nul
set "FIT_OUT=out_v3"
set "FIT_STATES=MUHI,FAHI,MUFAHI"
set "INIT_LAYER=%~dp0init_v3"
set "COMP_MASK=1"
set "SEGBULGE=1"
set "ROUNDS=6"
venv\Scripts\python.exe run_fits2.py 3
pause
