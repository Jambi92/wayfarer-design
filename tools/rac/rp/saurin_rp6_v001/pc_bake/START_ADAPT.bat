@echo off
rem Saurin RP6 bake benchmark pass 2: adaptive angle sampling (sweep -> refit at failing angles), one body at a time, low priority. Resumes.
cd /d "%~dp0"
"..\SaurinRP6_fits\venv\Scripts\python.exe" run_adapt.py
pause
