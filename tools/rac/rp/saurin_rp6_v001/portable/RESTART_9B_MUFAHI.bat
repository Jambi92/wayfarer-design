@echo off
rem Pass 9b heavy-body restart: MUFAHI restarts from its pass-8 layer with the pleat allowance at 88 deg (v001 edges within 2 deg of the threshold; one hip_flex70_xpos edge at v001 90.0 / layer 90.x never cleared) (the pass-9 strict-gate fits left corrective pleats + volume
rem misses in the composition-masked belly / pelvis at hip_flex70 / trunk_twist that the audit-scope refit cannot remove). Close the pass-9b window first.
cd /d "%~dp0"
powershell -NoProfile -Command "Get-CimInstance Win32_Process | Where-Object { ($_.CommandLine -match 'run_v2_pass9b' -or $_.CommandLine -match 'tools9b') -and $_.CommandLine -notmatch 'powershell' } | ForEach-Object { Write-Output ('stop ' + $_.ProcessId); Stop-Process -Id $_.ProcessId -Force -ErrorAction SilentlyContinue }"
timeout /t 5 /nobreak >nul
for %%S in (MUFAHI) do (
  del /q out\layers9b\ckpt\CF_ckpt_%%S.json out\layers9b\ckpt\CF_ckpt_%%S.npz out\layers9b\CF_state_%%S.json out\layers9b\CF_state_%%S.npz 2>nul
  copy /y out\layers8\CF_state_%%S.json data9b\init_auto\CF_state_%%S.json >nul
  copy /y out\layers8\CF_state_%%S.npz data9b\init_auto\CF_state_%%S.npz >nul
  echo %%S restarts from out\layers8
)
del /q "out\nodes9b\CK_MUFAHI@*" 2>nul
echo MUFAHI: out\layers8, allowance 88 deg > data9b\init_mufahi_restart2.txt
echo READY - starting pass 9b again
"..\SaurinRP6_fits\venv\Scripts\python.exe" run_v2_pass9b.py
pause
