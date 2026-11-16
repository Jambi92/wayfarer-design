@echo off
rem Saurin RP6 per-body bake benchmark - double-click to start or resume. One body at a time, low priority. Uses the private Python of ..\SaurinRP6_fits.
cd /d "%~dp0"
"..\SaurinRP6_fits\venv\Scripts\python.exe" run_bake.py
pause
