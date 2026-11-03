@echo off
rem Saurin RP6 creator-state corrective fits - double-click to start (or re-run to resume). Everything stays inside this folder on E:.
cd /d "%~dp0"
set PY=
where py >nul 2>nul && set PY=py -3
if not defined PY where python >nul 2>nul && set PY=python
if not defined PY (
  echo Python 3 was not found. Install it from https://www.python.org/downloads/ ^(tick "Add python.exe to PATH"^), then double-click this file again.
  pause & exit /b 1
)
if not exist venv\Scripts\python.exe (
  echo Setting up a private Python environment in this folder ^(one time, a few minutes^)...
  %PY% -m venv venv || (echo venv creation failed & pause & exit /b 1)
  venv\Scripts\python.exe -m pip install --quiet --upgrade pip
  venv\Scripts\python.exe -m pip install --quiet numpy==2.5.3 scipy==1.18.1 libigl==2.6.3 || venv\Scripts\python.exe -m pip install --quiet numpy scipy libigl || (echo package install failed & pause & exit /b 1)
)
venv\Scripts\python.exe run_fits.py %*
pause
