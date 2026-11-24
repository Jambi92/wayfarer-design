@echo off
rem Saurin RP6 rig v002 pass 8: state layers + knots refitted on base correctives v004. Double-click to start or resume.
cd /d "%~dp0"
"..\SaurinRP6_fits\venv\Scripts\python.exe" run_v2_pass8.py
pause
