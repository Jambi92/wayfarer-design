@echo off
rem Saurin RP6 rig v002 pass 7: state layers + knots refitted with the special gates. Double-click to start or resume.
cd /d "%~dp0"
"..\SaurinRP6_fits\venv\Scripts\python.exe" run_v2_gates.py
pause
