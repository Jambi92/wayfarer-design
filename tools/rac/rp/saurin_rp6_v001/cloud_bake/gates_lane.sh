#!/bin/bash
# lane L WAITBODY : after WAITBODY's it1 sweep is final, run special gates (G) and control sweeps (C) from gates/list$L, one at a time
cd /home/claude/wayfarer-design/tools/rac/rp/saurin_rp6_v001; export SA_W=/tmp/claude-0/rp5clean OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1
G=/tmp/claude-0/rp6/gates
while [ ! -f /tmp/claude-0/rp6/adapt2/$2/it1/SW_$2.json ]; do sleep 60; done
while read k n dir; do
  t=$(date +%s)
  if [ $k = G ]; then [ -f $G/GT_$n.json ] && continue; GATES_CKPT=$G/GT_$n.partial.json nice python3 sa6_bake_gates.py $n /tmp/claude-0/rp6/blend_bodies $dir $G >> $G/log_$1.txt 2>&1; st=gates
  else D=/tmp/claude-0/rp6/ctrl/$n; [ -f $D/SW_$n.json ] && continue; SWEEP_SET=all SWEEP_STEP_OTHER=0.125 nice python3 sa6_bake_sweep.py $n /tmp/claude-0/rp6/blend_bodies $D $D >> /tmp/claude-0/rp6/ctrl/log_$n.txt 2>&1; st=control_sweep; fi
  echo "{\"body\": \"$n\", \"stage\": \"$st\", \"host\": \"cloud\", \"wall_s\": $(( $(date +%s) - t ))}" >> $G/timings.jsonl
done < $G/list$1
echo LANEDONE $1
