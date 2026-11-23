@echo off
rem Stops only the run_heldout_v2.py scheduler process; the per-body sa6_bake_full workers it started keep running (their bodies carry RUNNING.lock).
powershell -NoProfile -Command "Get-CimInstance Win32_Process | Where-Object { $_.CommandLine -match 'run_heldout_v2[.]py' -and $_.CommandLine -notmatch 'powershell' } | ForEach-Object { Write-Output ('stop ' + $_.ProcessId + ' ' + $_.CommandLine); Stop-Process -Id $_.ProcessId -Force }"
pause
