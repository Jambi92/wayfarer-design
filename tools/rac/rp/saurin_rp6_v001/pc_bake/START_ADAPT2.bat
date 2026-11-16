@echo off
rem Saurin RP6 bake benchmark pass 3: full-suite between-sample sweep + adaptive refit, one body at a time, low priority. Resumes.
cd /d "%~dp0"
"..\SaurinRP6_fits\venv\Scripts\python.exe" run_adapt2.py
pause
