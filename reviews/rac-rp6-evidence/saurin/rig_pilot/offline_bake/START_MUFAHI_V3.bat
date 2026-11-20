@echo off
rem END_MUFAHI repair 2. Output -> run_mufahi_v3.log
cd /d "%~dp0"
"..\SaurinRP6_fits\venv\Scripts\python.exe" run_mufahi_v3.py > run_mufahi_v3.log 2>&1
