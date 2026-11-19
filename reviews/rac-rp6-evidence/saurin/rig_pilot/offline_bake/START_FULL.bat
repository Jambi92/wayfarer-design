@echo off
rem Saurin RP6 offline bake validation (order 8e3b7b4d): 4 bodies in parallel x 4 pose shards, low priority. Resumes.
cd /d "%~dp0"
"..\SaurinRP6_fits\venv\Scripts\python.exe" run_full.py
