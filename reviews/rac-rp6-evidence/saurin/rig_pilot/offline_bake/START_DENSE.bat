@echo off
rem Dense between-sample audit of the pass-2 bakes. Output -> run_dense.log
cd /d "%~dp0"
"..\SaurinRP6_fits\venv\Scripts\python.exe" run_dense.py > run_dense.log 2>&1
