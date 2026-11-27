#!/bin/bash
# mfx/run.sh: END_FAHI hip_flex70_xpos local-motion fix experiments (cloud). 1) control: motion of the PC it3 artifact; 2) variant A: it3 fit restricted to the pose with BAKE_MOTION_GRID=floor
cd /home/claude/wayfarer-design/tools/rac/rp/saurin_rp6_v001; X=/tmp/claude-0/rp6/mfx; BD=/tmp/claude-0/rp6/blend_bodies
export RP6_RIG=v002 RP6_WD=/tmp/claude-0/rp6/base6 RP6_BASE_CORR=SA_RP6_correctives_v004.json RP6_LAYERS=SA_RP6_creator_layers_v006.json OMP_NUM_THREADS=1 PLEAT_GATE=1 PLEAT_ALLOW_UNION=/tmp/claude-0/rp6/union/allow/pleat_union_END_FAHI.npz
export BAKE_RECIPE=standard BAKE_PK_MINW=0.25 BAKE_GATE_ALIGNED_ALLOW=1 BAKE_MOTION_REFIT=1 BAKE_MOTION_REFIT_MODE=grid BAKE_LOCAL_MARGIN=0.03
MOTION_ONLY=hip_flex70_xpos python3 sa6_bake_motion.py END_FAHI $BD $X/it3 $X/it3 2>&1 | grep -v Warn | tail -1 &
cp $X/it3/extra.json $X/A/extra.json
BAKE_MOTION_GRID=floor BAKE_ONLY_POSES=hip_flex70_xpos BAKE_INIT=$X/it2/BK_END_FAHI.json BAKE_EXTRA=$X/A/extra.json python3 sa6_bake.py fit END_FAHI $BD $X/A > $X/A/fit.log 2>&1
tail -3 $X/A/fit.log
MOTION_ONLY=hip_flex70_xpos python3 sa6_bake_motion.py END_FAHI $BD $X/A $X/A 2>&1 | grep -v Warn | tail -1
wait; echo MFX_DONE
