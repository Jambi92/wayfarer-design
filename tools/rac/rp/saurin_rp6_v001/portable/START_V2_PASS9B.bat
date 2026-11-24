@echo off
rem Saurin RP6 rig v002 pass 9b: the 19 state layers (pleat gate = audit scope) then the 20 knots. Double-click to start or resume.
cd /d "%~dp0"
"..\SaurinRP6_fits\venv\Scripts\python.exe" run_v2_pass9b.py
pause
