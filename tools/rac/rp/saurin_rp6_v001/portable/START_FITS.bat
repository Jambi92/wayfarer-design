@echo off
rem Saurin RP6 creator-state corrective fits - double-click to start (or re-run to resume). Everything stays inside this folder on E:.
cd /d "%~dp0"
set "UV_CACHE_DIR=%~dp0.uv\cache"
set "UV_PYTHON_INSTALL_DIR=%~dp0.uv\python"
if not exist venv\Scripts\python.exe (
  echo Setting up a private Python 3.13 in this folder ^(one time, a few minutes^)...
  if not exist .uv\uv.exe (
    if not exist .uv\x mkdir .uv\x
    tar -xf uv-0.13.7-py3-none-win_amd64.whl -C .uv\x || (echo could not unpack uv & pause & exit /b 1)
    copy /y .uv\x\uv-0.13.7.data\scripts\uv.exe .uv\uv.exe >nul
  )
  .uv\uv.exe venv --managed-python --python 3.13 venv || (echo Python setup failed & pause & exit /b 1)
  .uv\uv.exe pip install --python venv\Scripts\python.exe numpy==2.5.3 scipy==1.18.1 libigl==2.6.3 || (echo package install failed & pause & exit /b 1)
)
venv\Scripts\python.exe run_fits.py %*
pause
