@echo off
rem Saurin RP6 pass 9b: second held-out runner (from the other end of the list) on base v004 + creator layers v006, started when the standard bakes free the cores.
rem RUNNING.lock keeps the two runners off one body. Double-click to start or resume.
cd /d "%~dp0"
set STD_REPO=repo9
set STD_TOOLS=tools10
set STD_LAYERS=SA_RP6_creator_layers_v006.json
set STD_BASE=SA_RP6_correctives_v004.json
start "Saurin RP6 held-out recheck (rev)" cmd /c ""..\SaurinRP6_fits\venv\Scripts\python.exe" run_heldout_v2.py 10 rev & pause"
