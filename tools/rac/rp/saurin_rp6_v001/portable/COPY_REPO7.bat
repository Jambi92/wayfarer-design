@echo off
rem Pass 7: copies repo\ to repo7\ (the pass-7 package goes into repo7; the running bakes keep repo\).
robocopy "%~dp0repo" "%~dp0repo7" /E /NFL /NDL /NP
echo COPY DONE
pause
