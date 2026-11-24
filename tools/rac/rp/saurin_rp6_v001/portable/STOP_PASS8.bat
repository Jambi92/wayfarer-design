@echo off
rem Stops pass 8 (run_v2_pass8.py and its fits) and removes its partial outputs so it can restart cleanly.
powershell -NoProfile -Command "Get-CimInstance Win32_Process | Where-Object { ($_.CommandLine -match 'run_v2_pass8[.]py' -or $_.CommandLine -match 'tools8') -and $_.CommandLine -notmatch 'powershell' } | ForEach-Object { Write-Output ('stop ' + $_.ProcessId); Stop-Process -Id $_.ProcessId -Force -ErrorAction SilentlyContinue }"
timeout /t 5 /nobreak >nul
if exist "%~dp0out\layers8" rmdir /s /q "%~dp0out\layers8"
if exist "%~dp0out\nodes8" rmdir /s /q "%~dp0out\nodes8"
if exist "%~dp0out\base_v004_eval" rmdir /s /q "%~dp0out\base_v004_eval"
if exist "%~dp0out\jobs_p8.json" del /q "%~dp0out\jobs_p8.json"
echo STOP DONE
pause
