#!/bin/bash
cd /home/claude/wayfarer-design/tools/rac/rp/saurin_rp6_v001; export SA_W=/tmp/claude-0/rp5clean OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 SWEEP_SET=all SWEEP_STEP_OTHER=0.125
for n in $(cat /tmp/claude-0/rp6/a2l$1); do
  f=/tmp/claude-0/rp6/adapt2/$n/adapt_$n.json
  grep -q final $f 2>/dev/null && continue
  chmod -R u+w /tmp/claude-0/rp6/adapt2/$n 2>/dev/null; t=$(date +%s); nice python3 sa6_bake_adapt.py $n /tmp/claude-0/rp6/blend_bodies /tmp/claude-0/rp6/pcbake /tmp/claude-0/rp6/adapt2/$n 3 >> /tmp/claude-0/rp6/adapt2/log_$1.txt 2>&1
  echo "{\"body\": \"$n\", \"stage\": \"adapt2\", \"host\": \"cloud\", \"wall_s\": $(( $(date +%s) - t ))}" >> /tmp/claude-0/rp6/adapt2/timings.jsonl
done
echo ALLDONE >> /tmp/claude-0/rp6/adapt2/log_$1.txt
