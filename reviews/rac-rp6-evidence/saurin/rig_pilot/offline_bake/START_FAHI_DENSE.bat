@echo off
rem END_FAHI repair 2 (dense). Output -> run_fahi_dense.log
cd /d "%~dp0"
"..\SaurinRP6_fits\venv\Scripts\python.exe" run_fahi_dense.py > run_fahi_dense.log 2>&1
