@echo off
rem END_FAHI pass-2 repair: pose-key floor 1/4 of the full angle. Output -> run_fahi_w25.log
cd /d "%~dp0"
"..\SaurinRP6_fits\venv\Scripts\python.exe" run_fahi_w25.py > run_fahi_w25.log 2>&1
