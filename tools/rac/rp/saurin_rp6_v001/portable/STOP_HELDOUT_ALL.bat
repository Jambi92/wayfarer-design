@echo off
rem Stops the held-out recheck of package 248508ec (superseded by base v004 / pass 8): the run_heldout_v2.py schedulers and every bake process working in out_ho_248508ec. Outputs stay on disk as a record.
powershell -NoProfile -Command "Get-CimInstance Win32_Process | Where-Object { ($_.CommandLine -match 'run_heldout_v2[.]py' -or $_.CommandLine -match 'out_ho_248508ec') -and $_.CommandLine -notmatch 'powershell' } | ForEach-Object { Write-Output ('stop ' + $_.ProcessId); Stop-Process -Id $_.ProcessId -Force -ErrorAction SilentlyContinue }"
echo STOP DONE
pause
