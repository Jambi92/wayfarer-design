@echo off
rem Offline bake pass 2: min pose-key width, gate-aligned allowance, motion gate. Output -> run_v2.log
cd /d "%~dp0"
"..\SaurinRP6_fits\venv\Scripts\python.exe" run_v2.py > run_v2.log 2>&1
