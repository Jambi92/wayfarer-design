@echo off
rem Saurin RP6 rig v002 pass 9b: standard bakes (BASE_c1, BASE_c2, END_FAHI, END_MUFAHI) + held-out recheck (18 bodies) on base v004 + creator layers v006.
rem repo9 = repo8 without the superseded layers v005 + the v006 package (already placed in repo9); tools10 = the committed tools; pleat allowance data9b\union.
rem Opens two windows (standard, held-out). Double-click to start or resume; safe to close a window and re-run.
cd /d "%~dp0"
robocopy "%~dp0repo8" "%~dp0repo9" /E /XC /XN /XO /XF SA_RP6_creator_layers_v005* /NFL /NDL /NP /NJH /NJS
set STD_REPO=repo9
set STD_TOOLS=tools10
set STD_LAYERS=SA_RP6_creator_layers_v006.json
set STD_BASE=SA_RP6_correctives_v004.json
set STD_PLEAT=1
start "Saurin RP6 standard bakes" cmd /c ""..\SaurinRP6_fits\venv\Scripts\python.exe" run_standard_v2.py BASE_c1 BASE_c2 END_FAHI END_MUFAHI & pause"
start "Saurin RP6 held-out recheck" cmd /c ""..\SaurinRP6_fits\venv\Scripts\python.exe" run_heldout_v2.py 4 & pause"
