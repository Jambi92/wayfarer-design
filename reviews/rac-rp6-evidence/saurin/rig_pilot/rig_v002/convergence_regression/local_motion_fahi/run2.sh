#!/bin/bash
# mfx/run2.sh: variants B (step-mode grid spacing 0.125) and C (gridkeys: keys on the 0.25 grid, family samples not snapped), restricted to hip_flex70_xpos
cd /home/claude/wayfarer-design/tools/rac/rp/saurin_rp6_v001; X=/tmp/claude-0/rp6/mfx; BD=/tmp/claude-0/rp6/blend_bodies
export RP6_RIG=v002 RP6_WD=/tmp/claude-0/rp6/base6 RP6_BASE_CORR=SA_RP6_correctives_v004.json RP6_LAYERS=SA_RP6_creator_layers_v006.json OMP_NUM_THREADS=1 PLEAT_GATE=1 PLEAT_ALLOW_UNION=/tmp/claude-0/rp6/union/allow/pleat_union_END_FAHI.npz
export BAKE_RECIPE=standard BAKE_PK_MINW=0.25 BAKE_GATE_ALIGNED_ALLOW=1 BAKE_MOTION_REFIT=1 BAKE_LOCAL_MARGIN=0.03 BAKE_ONLY_POSES=hip_flex70_xpos BAKE_INIT=$X/it2/BK_END_FAHI.json
v() { BAKE_EXTRA=$X/$1/extra.json python3 sa6_bake.py fit END_FAHI $BD $X/$1 > $X/$1/fit.log 2>&1; echo "$1 $(grep BAKED $X/$1/fit.log | cut -c1-120)"; MOTION_ONLY=hip_flex70_xpos python3 sa6_bake_motion.py END_FAHI $BD $X/$1 $X/$1 2>&1 | grep -v Warn | tail -1; }
BAKE_MOTION_REFIT_MODE=grid BAKE_MOTION_GRID=0.125 v B &
BAKE_MOTION_REFIT_MODE=gridkeys BAKE_MOTION_GRID=step v C &
wait; echo MFX2_DONE
