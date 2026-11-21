@echo off
rem Saurin RP6 rig v002 corrective rebuild (base c1/c2 + 19 creator-state layers). Double-click to start or resume.
cd /d "%~dp0"
"..\SaurinRP6_fits\venv\Scripts\python.exe" run_v2.py
pause
