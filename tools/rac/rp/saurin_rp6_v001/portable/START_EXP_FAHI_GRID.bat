@echo off
rem Saurin RP6 pass 9c diagnostics (not a bake): END_FAHI hip_flex70_xpos refit from it5 with the it6 sample list on five motion key grids, in parallel,
rem each checked on that pose (motion local rule, sweep 0.025, dense 0.0025). tools12 = tools11 + sa6_bake_sweep.py SWEEP_ONLY + sa6_pleat_audit.py diagnostics.
cd /d "%~dp0"
if not exist tools12\sa6_bake.py xcopy /Q /I /Y tools11 tools12 >nul
copy /Y data9c\t12\*.py tools12\ >nul
set STD_REPO=repo9
set STD_TOOLS=tools12
start "Saurin RP6 END_FAHI grid exp" cmd /c ""..\SaurinRP6_fits\venv\Scripts\python.exe" exp_grid_v2.py END_FAHI hip_flex70_xpos out_std_b9f3b808\END_FAHI\it5 data9c\extra_it6_END_FAHI.json data9b\union\pleat_union_END_FAHI.npz exp_fahi_grid_it6 0.5,0.4,0.33333,0.3,0.25 & pause"
