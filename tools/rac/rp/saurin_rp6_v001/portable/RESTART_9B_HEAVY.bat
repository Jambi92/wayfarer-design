@echo off
rem Pass 9b heavy-body restart: MUFAHI and FAHI restart from their pass-8 layers (the pass-9 strict-gate fits left corrective pleats + volume
rem misses in the composition-masked belly / pelvis at hip_flex70 / trunk_twist that the audit-scope refit cannot remove). Close the pass-9b window first.
cd /d "%~dp0"
powershell -NoProfile -Command "Get-CimInstance Win32_Process | Where-Object { ($_.CommandLine -match 'run_v2_pass9b' -or $_.CommandLine -match 'tools9b') -and $_.CommandLine -notmatch 'powershell' } | ForEach-Object { Write-Output ('stop ' + $_.ProcessId); Stop-Process -Id $_.ProcessId -Force -ErrorAction SilentlyContinue }"
timeout /t 5 /nobreak >nul
for %%S in (MUFAHI FAHI) do (
  del /q out\layers9b\ckpt\CF_ckpt_%%S.json out\layers9b\ckpt\CF_ckpt_%%S.npz 2>nul
  copy /y out\layers8\CF_state_%%S.json data9b\init_auto\CF_state_%%S.json >nul
  copy /y out\layers8\CF_state_%%S.npz data9b\init_auto\CF_state_%%S.npz >nul
  echo %%S restarts from out\layers8
)
echo MUFAHI FAHI: out\layers8 (pass-9 ckpt dropped) > data9b\init_heavy_restart.txt
echo READY - starting pass 9b again
"..\SaurinRP6_fits\venv\Scripts\python.exe" run_v2_pass9b.py
pause
