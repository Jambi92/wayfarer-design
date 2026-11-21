@echo off
rem Saurin RP6 rig v002 STANDARD bakes (BASE_c1, BASE_c2, END_FAHI, END_MUFAHI). Double-click to start or resume. Output out_std\
cd /d "%~dp0"
"..\SaurinRP6_fits\venv\Scripts\python.exe" run_standard_v2.py %*
pause
