@echo off
rem Saurin RP6 rig v002 held-out recheck (18 benchmark bodies) on the pass-7 package. Double-click to start or resume.
cd /d "%~dp0"
"..\SaurinRP6_fits\venv\Scripts\python.exe" run_heldout_v2.py 4
pause
