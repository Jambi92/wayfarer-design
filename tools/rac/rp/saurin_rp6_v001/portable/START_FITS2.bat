@echo off
rem Saurin RP6 creator-state fits, closure v002: the three heaviest states (high fat, high muscle, muscle + fat) with the composition-fold mask and
rem the segment flesh bulge.  Double-click to start or resume.  Output in out_v2.  Everything stays inside this folder on E:.
cd /d "%~dp0"
set "FIT_OUT=out_v2"
set "FIT_STATES=MUHI,FAHI,MUFAHI"
set "COMP_MASK=1"
set "SEGBULGE=1"
set "ROUNDS=6"
venv\Scripts\python.exe run_fits2.py 3
pause
