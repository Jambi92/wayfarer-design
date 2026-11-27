@echo off
rem Saurin RP6 pass 9b: resume the END_FAHI standard bake for a 4th refit (STD_MAXIT=4) on tools11.
rem it3 ended with one local-motion miss on hip_flex70_xpos (0.044 cm over the allowance; it2 and it3 identical). The motion-fed pose is refit on a
rem 1/3 key grid (BAKE_MOTION_GRID_POSE); the step grid misses, the doubled floor diverges (cloud experiments mfx/). Everything else is the standard.
cd /d "%~dp0"
set STD_REPO=repo9
set STD_TOOLS=tools11
set STD_LAYERS=SA_RP6_creator_layers_v006.json
set STD_BASE=SA_RP6_correctives_v004.json
set STD_PLEAT=1
set STD_MAXIT=4
set BAKE_MOTION_GRID_POSE=hip_flex70_xpos=0.33333
start "Saurin RP6 END_FAHI it4" cmd /c ""..\SaurinRP6_fits\venv\Scripts\python.exe" run_standard_v2.py END_FAHI & pause"
