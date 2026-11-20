@echo off
rem Revised motion gate on the final bakes. Output -> run_mo.log
cd /d "%~dp0"
"..\SaurinRP6_fits\venv\Scripts\python.exe" run_mo.py > run_mo.log 2>&1
