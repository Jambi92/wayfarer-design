@echo off
rem Saurin RP6 pass 9c: END_FAHI resumed from it5 for refits 6-7 with the hip_flex70_xpos motion key grid at 0.5 (tools13; BAKE_MOTION_RAMP stays off).
rem Grid experiment exp_fahi_grid_it6 (refit of that pose from it5 with the it6 samples): 0.5 = converged, motion local -0.028 cm (pass), sweep clean,
rem dense 3 samples at 0.6625-0.6675 (fed to it7); 1/3 / 0.25 / 0.4 / 0.3 failed motion (+0.055 / +0.034 / +0.105 / +0.372).
rem Also stops the ramp experiment (exp_fahi_ramp_it6): the ramp moves pose keys only and the excursion is family-driven (0.4_r0.8 = 0.4 exactly).
cd /d "%~dp0"
powershell -NoProfile -Command "Get-CimInstance Win32_Process | Where-Object { $_.CommandLine -match 'exp_fahi_ramp_it6' -and $_.CommandLine -notmatch 'powershell' } | ForEach-Object { Write-Output ('stop ' + $_.ProcessId); Stop-Process -Id $_.ProcessId -Force -ErrorAction SilentlyContinue }"
set STD_REPO=repo9
set STD_TOOLS=tools13
set STD_LAYERS=SA_RP6_creator_layers_v006.json
set STD_BASE=SA_RP6_correctives_v004.json
set STD_PLEAT=1
set STD_MAXIT=7
set BAKE_MOTION_GRID_POSE=hip_flex70_xpos=0.5
start "Saurin RP6 END_FAHI it6" cmd /c ""..\SaurinRP6_fits\venv\Scripts\python.exe" run_standard_v2.py END_FAHI & pause"
