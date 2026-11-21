@echo off
rem STANDARD Saurin RP6 per-body bake (approved recipe). Usage: START_STANDARD.bat BODY [BODY ...]  (needs its own order). Output out_std\
cd /d "%~dp0"
"..\SaurinRP6_fits\venv\Scripts\python.exe" run_standard.py %* > run_standard.log 2>&1
