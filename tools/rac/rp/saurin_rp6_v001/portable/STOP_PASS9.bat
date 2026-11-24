@echo off
rem Stops pass 9 (run_v2_pass9.py and its fits) and removes its partial outputs so it can restart cleanly.
powershell -NoProfile -Command "Get-CimInstance Win32_Process | Where-Object { ($_.CommandLine -match 'run_v2_pass9[.]py' -or $_.CommandLine -match 'tools9') -and $_.CommandLine -notmatch 'powershell' } | ForEach-Object { Write-Output ('stop ' + $_.ProcessId); Stop-Process -Id $_.ProcessId -Force -ErrorAction SilentlyContinue }"
timeout /t 5 /nobreak >nul
if exist "%~dp0out\layers9" rmdir /s /q "%~dp0out\layers9"
if exist "%~dp0out\nodes9" rmdir /s /q "%~dp0out\nodes9"
if exist "%~dp0out\jobs_p9.json" del /q "%~dp0out\jobs_p9.json"
echo STOP DONE
pause
