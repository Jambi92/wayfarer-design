@echo off
rem END_MUFAHI pass-2 repair with the dense audit. Output -> run_mufahi_dense.log
cd /d "%~dp0"
"..\SaurinRP6_fits\venv\Scripts\python.exe" run_mufahi_dense.py > run_mufahi_dense.log 2>&1
