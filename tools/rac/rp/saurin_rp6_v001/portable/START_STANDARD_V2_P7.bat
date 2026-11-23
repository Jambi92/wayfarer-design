@echo off
rem Saurin RP6 rig v002 standard bakes of END_FAHI / END_MUFAHI on the pass-7 package (repo7\, tools7\). Double-click to start or resume.
cd /d "%~dp0"
set STD_REPO=repo7
set STD_TOOLS=tools7
"..\SaurinRP6_fits\venv\Scripts\python.exe" run_standard_v2.py END_FAHI END_MUFAHI
pause
