@echo off
rem Saurin RP6 pass 9c: fresh standard rebake of END_MUFAHI on package b9f3b808 with the dense pleat allowance (data9c\union, tools11).
rem The pass-9b END_MUFAHI run (out_std_b9f3b808\END_MUFAHI) never converged on hip_flex70_xpos: the union was measured at 0.25 / 0.5 / 0.75 / 1.0 only,
rem so the heavy belly fold that rig v001 also forms between those fractions failed the 0.025-step sweep and the fit fought it (K up to 6 cm, ping-pong).
rem Stops that run first (its files stay on disk as the record), then starts the fresh bake in out_std_b9f3b808_u2\END_MUFAHI. Everything else is the standard.
cd /d "%~dp0"
powershell -NoProfile -Command "Get-CimInstance Win32_Process | Where-Object { $_.CommandLine -match 'END_MUFAHI' -and $_.CommandLine -notmatch 'powershell' -and $_.CommandLine -notmatch 'P9C' } | ForEach-Object { Write-Output ('stop ' + $_.ProcessId); Stop-Process -Id $_.ProcessId -Force -ErrorAction SilentlyContinue }"
set STD_REPO=repo9
set STD_TOOLS=tools11
set STD_LAYERS=SA_RP6_creator_layers_v006.json
set STD_BASE=SA_RP6_correctives_v004.json
set STD_PLEAT=1
set STD_UNION=data9c\union
set STD_OUT_TAG=_u2
start "Saurin RP6 END_MUFAHI p9c" cmd /c ""..\SaurinRP6_fits\venv\Scripts\python.exe" run_standard_v2.py END_MUFAHI & pause"
