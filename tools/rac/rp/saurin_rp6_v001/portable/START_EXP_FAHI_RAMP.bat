@echo off
rem Saurin RP6 pass 9c diagnostics (not a bake): END_FAHI hip_flex70_xpos refit from it5 with the motion ramp (BAKE_MOTION_RAMP) on 4 grid / beta pairs.
rem tools13 = tools12 + sa6_bake.py (motion ramp) + sa6_bake_full.py (recipe records it).
cd /d "%~dp0"
if not exist tools13\sa6_bake.py xcopy /Q /I /Y tools12 tools13 >nul
copy /Y data9c\t13\*.py tools13\ >nul
set STD_REPO=repo9
set STD_TOOLS=tools13
start "Saurin RP6 END_FAHI ramp exp" cmd /c ""..\SaurinRP6_fits\venv\Scripts\python.exe" exp_grid_v2.py END_FAHI hip_flex70_xpos out_std_b9f3b808\END_FAHI\it5 data9c\extra_it6_END_FAHI.json data9b\union\pleat_union_END_FAHI.npz exp_fahi_ramp_it6 0.25:0.5,0.25:1,0.33333:0.6,0.4:0.8 & pause"
