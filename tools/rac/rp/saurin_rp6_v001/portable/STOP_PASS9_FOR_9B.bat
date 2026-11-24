@echo off
rem Stops the pass-9 fits and the first pass-9b start (superseded by pass 9b with the audit-scope pleat gate). Keeps out\layers9 (finished layers + checkpoints);
rem removes the first pass-9b progress (out\layers9b, its logs and job record) so pass 9b starts clean.
cd /d "%~dp0"
powershell -NoProfile -Command "Get-CimInstance Win32_Process | Where-Object { ($_.CommandLine -match 'run_v2_pass9' -or $_.CommandLine -match 'tools9') -and $_.CommandLine -notmatch 'powershell' } | ForEach-Object { Write-Output ('stop ' + $_.ProcessId); Stop-Process -Id $_.ProcessId -Force -ErrorAction SilentlyContinue }"
timeout /t 5 /nobreak >nul
if exist out\layers9b rmdir /s /q out\layers9b
if exist out\jobs_p9b.json del /q out\jobs_p9b.json
if exist out\init9b.json del /q out\init9b.json
del /q out\logs\p9b_*.log 2>nul
if exist data9b\states9b.txt del /q data9b\states9b.txt
echo STOP DONE
pause
