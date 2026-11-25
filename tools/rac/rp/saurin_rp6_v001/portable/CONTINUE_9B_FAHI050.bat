@echo off
rem Pass 9b: knot FAHI@0.50 ended unconverged after 4 rounds (1 flip at lower_axial_flex_25 100%%, 4 -> 1 in the last two rounds). Continue it from its
rem checkpoint with ROUNDS=8 (same tools / env as run_v2_pass9b.py). Runs beside the pass-9b window.
cd /d "%~dp0"
del /q "out\nodes9b\CK_FAHI@0.50.json" "out\nodes9b\CK_FAHI@0.50.npz" 2>nul
set RP6_RIG=v002
set RP6_REPO=%~dp0repo8
set RP6_BASE_CORR=SA_RP6_correctives_v004.json
set SA_W=%~dp0data
set RP6_WD=%~dp0data8
set OMP_NUM_THREADS=1
set OPENBLAS_NUM_THREADS=1
set MKL_NUM_THREADS=1
set PD2_GATES=1
set FAIR_SCOPE=arm
set PLEAT_GATE=1
set PLEAT_ALLOW=%~dp0data9b\allow
set PYTHONIOENCODING=utf-8
set ROUNDS=8
"..\SaurinRP6_fits\venv\Scripts\python.exe" tools9b\sa6_node_fit.py FAHI@0.50 bodies out\layers9b out\nodes9b >> "out\logs\p9b_node_FAHI@0.50.log" 2>&1
echo FAHI@0.50 DONE - tell Claude.
pause
