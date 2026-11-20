@echo off
rem END_MUFAHI repairability check (outside the 3-refit cap): one refit with the gate-aligned fit allowance. Output -> run_repair.log
cd /d "%~dp0"
"..\SaurinRP6_fits\venv\Scripts\python.exe" run_repair.py > run_repair.log 2>&1
