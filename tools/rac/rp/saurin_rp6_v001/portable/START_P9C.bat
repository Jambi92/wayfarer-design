@echo off
rem Saurin RP6 pass 9c: (1) fresh END_MUFAHI standard rebake with the dense pleat allowance, (2) END_FAHI resumed for a 5th refit. tools11 / repo9.
rem (1) = START_P9C_END_MUFAHI.bat: stops the unconverged 9b END_MUFAHI run (record stays), starts out_std_b9f3b808_u2\END_MUFAHI with data9c\union.
rem (2) END_FAHI it4 ended with hip_flex70_xpos only: one K-made pleat edge at 0.275 / 0.30 (outside both the 4-fraction and the dense allowance) and a
rem     0.058 cm local-motion excess. The it4 failures feed it5 on the same allowance (data9b\union) and the same 1/3 motion grid as it4.
cd /d "%~dp0"
powershell -NoProfile -Command "Get-CimInstance Win32_Process | Where-Object { $_.CommandLine -match 'END_MUFAHI' -and $_.CommandLine -notmatch 'powershell' -and $_.CommandLine -notmatch 'P9C' } | ForEach-Object { Write-Output ('stop ' + $_.ProcessId); Stop-Process -Id $_.ProcessId -Force -ErrorAction SilentlyContinue }"
set STD_REPO=repo9
set STD_TOOLS=tools11
set STD_LAYERS=SA_RP6_creator_layers_v006.json
set STD_BASE=SA_RP6_correctives_v004.json
set STD_PLEAT=1
start "Saurin RP6 END_MUFAHI p9c" cmd /c "set STD_UNION=data9c\union& set STD_OUT_TAG=_u2& "..\SaurinRP6_fits\venv\Scripts\python.exe" run_standard_v2.py END_MUFAHI & pause"
start "Saurin RP6 END_FAHI it5" cmd /c "set STD_MAXIT=5& set BAKE_MOTION_GRID_POSE=hip_flex70_xpos=0.33333& "..\SaurinRP6_fits\venv\Scripts\python.exe" run_standard_v2.py END_FAHI & pause"
