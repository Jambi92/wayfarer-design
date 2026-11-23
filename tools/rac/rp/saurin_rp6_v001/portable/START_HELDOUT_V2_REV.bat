@echo off
rem Second held-out runner, from the other end of the list (RUNNING.lock keeps two runners off one body).
cd /d "%~dp0"
"..\SaurinRP6_fits\venv\Scripts\python.exe" run_heldout_v2.py 4 rev
pause
