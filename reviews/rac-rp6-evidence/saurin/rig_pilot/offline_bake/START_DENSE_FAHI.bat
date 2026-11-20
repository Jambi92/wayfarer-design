@echo off
rem Dense audit of the END_FAHI repair bake (out_v2w it2). Output -> run_dense_w.log
cd /d "%~dp0"
"..\SaurinRP6_fits\venv\Scripts\python.exe" run_dense.py > run_dense_w.log 2>&1
