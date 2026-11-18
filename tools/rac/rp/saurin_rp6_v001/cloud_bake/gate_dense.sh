#!/bin/bash
# dense.sh NAME POSES : 0.025-grid between-sample check (0.025..0.975, excluding 0.25/0.5/0.75) of the gate poses that drove the refit
N=$1; D=/tmp/claude-0/rp6/adapt3/$N/it2; [ -f $D/dense/GT_$N.json ] && exit 0; mkdir -p $D/dense
F=$(python3 -c "print(','.join('%.3f'%(k*0.025) for k in range(1,40) if k not in (10,20,30)))")
cd /home/claude/wayfarer-design/tools/rac/rp/saurin_rp6_v001; export SA_W=/tmp/claude-0/rp5clean OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1
t=$(date +%s); GATES_CKPT=$D/dense/GT_$N.partial.json GATES_ONLY=$2 GATES_FRACS=$F nice python3 sa6_bake_gates.py $N /tmp/claude-0/rp6/blend_bodies $D $D/dense >> $D/../log_$N.txt 2>&1
echo "{\"body\": \"$N\", \"stage\": \"gates_dense\", \"host\": \"cloud\", \"wall_s\": $(( $(date +%s) - t )), \"rc\": $?}" >> /tmp/claude-0/rp6/adapt3/timings.jsonl
