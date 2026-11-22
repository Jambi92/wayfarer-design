@echo off
rem Stops only the END_FAHI / END_MUFAHI standard-bake workers (superseded by pass 7); BASE_c1 / BASE_c2 keep running.
powershell -NoProfile -Command "Get-CimInstance Win32_Process | Where-Object { $_.CommandLine -match 'python' -and $_.CommandLine -match 'END_(FAHI|MUFAHI)' } | ForEach-Object { Write-Output ('stop ' + $_.ProcessId + ' ' + $_.CommandLine); Stop-Process -Id $_.ProcessId -Force }"
pause
