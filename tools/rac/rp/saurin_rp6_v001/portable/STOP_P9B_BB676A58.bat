@echo off
rem Stops the pass-9b standard bakes and held-out recheck on package bb676a58 (knot M208-B@0.75 with its jaw keys; superseded by the fixed v006, b9f3b808).
rem Outputs stay on disk as a record. Then run START_P9B_BAKES.bat again.
powershell -NoProfile -Command "Get-CimInstance Win32_Process | Where-Object { ($_.CommandLine -match 'run_heldout_v2[.]py' -or $_.CommandLine -match 'run_standard_v2[.]py' -or $_.CommandLine -match 'bb676a58') -and $_.CommandLine -notmatch 'powershell' } | ForEach-Object { Write-Output ('stop ' + $_.ProcessId); Stop-Process -Id $_.ProcessId -Force -ErrorAction SilentlyContinue }"
echo STOP DONE
