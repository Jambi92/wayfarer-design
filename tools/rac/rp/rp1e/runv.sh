#!/bin/bash
# runv.sh TAG CAGE COL MODE FINALN [SMR]
cd /home/claude/stc/rp1e
FNSMR=${FNSMR:-0} bash bsim6.sh $1 $2 $3 tg_r2m5 4 $4 $5 0 ${6:-2} > $1.log 2>&1
timeout 2000 /home/claude/stc/bin/python3 selfx_pairs.py -- sim_$1_L4.npz >/dev/null 2>&1
timeout 3000 /home/claude/stc/bin/python3 classify.py -- sim_$1_L4.npz cls_$1.json 2>&1 | grep -E "^ +[0-9]+ " > $1.cls
echo DONE $1
