@echo off
rem Pass 8 setup: repo8 = repo7 + the base v004 package already placed in repo8 (new file names only).
robocopy "%~dp0repo7" "%~dp0repo8" /E /XC /XN /XO /NFL /NDL /NP
copy /Y "%~dp0data\W_M.npz" "%~dp0data8\W_M.npz"
copy /Y "%~dp0data\W_F.npz" "%~dp0data8\W_F.npz"
echo SETUP DONE
pause
