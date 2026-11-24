@echo off
rem Stops the pass-8 knot fits (superseded by pass 9). Keeps out\layers8 and out\nodes8 as they are.
powershell -NoProfile -Command "Get-CimInstance Win32_Process | Where-Object { ($_.CommandLine -match 'run_v2_pass8[.]py' -or $_.CommandLine -match 'tools8') -and $_.CommandLine -notmatch 'powershell' } | ForEach-Object { Write-Output ('stop ' + $_.ProcessId); Stop-Process -Id $_.ProcessId -Force -ErrorAction SilentlyContinue }"
echo STOP DONE
pause
