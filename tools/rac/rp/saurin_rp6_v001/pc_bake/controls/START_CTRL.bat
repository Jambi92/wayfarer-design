@echo off
rem Saurin RP6 control sweeps (order a13cae71): 4 control bodies x 4 pose shards in parallel, low priority. Resumes.
cd /d "%~dp0"
"..\SaurinRP6_fits\venv\Scripts\python.exe" run_ctrl.py
