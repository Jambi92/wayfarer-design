#!/bin/bash
# refit.sh NAME INIT_ARTIFACT : gate-failure refit pipeline (resumable): fit (BAKE_INIT + BAKE_EXTRA incl. gate: poses) -> eval (34 x 4) -> full sweep -> special gates
N=$1; INIT=$2; D=/tmp/claude-0/rp6/adapt3/$N/it2; BD=/tmp/claude-0/rp6/blend_bodies; TL=/tmp/claude-0/rp6/adapt3/timings.jsonl
cd /home/claude/wayfarer-design/tools/rac/rp/saurin_rp6_v001; export SA_W=/tmp/claude-0/rp5clean OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1
st(){ echo "{\"body\": \"$N\", \"stage\": \"$1\", \"host\": \"cloud\", \"wall_s\": $(( $(date +%s) - t )), \"rc\": $2}" >> $TL; }
if [ ! -f $D/BK_$N.json ]; then t=$(date +%s); BAKE_INIT=$INIT BAKE_EXTRA=$D/extra.json nice python3 sa6_bake.py fit $N $BD $D >> $D/../log_$N.txt 2>&1; st fit $?; fi
if [ ! -f $D/EV_$N.json ]; then t=$(date +%s); nice python3 sa6_bake.py eval $N $BD $D >> $D/../log_$N.txt 2>&1; st eval $?; fi
if [ ! -f $D/SW_$N.json ]; then t=$(date +%s); SWEEP_SET=all SWEEP_STEP_OTHER=0.125 nice python3 sa6_bake_sweep.py $N $BD $D $D >> $D/../log_$N.txt 2>&1; st sweep $?; fi
if [ ! -f $D/GT_$N.json ]; then t=$(date +%s); GATES_CKPT=$D/GT_$N.partial.json nice python3 sa6_bake_gates.py $N $BD $D $D >> $D/../log_$N.txt 2>&1; st gates $?; fi
echo REFITDONE $N
