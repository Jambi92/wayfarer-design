#!/bin/bash
S=/tmp/claude-0/-home-claude/5d878de4-8c1b-50e0-ba42-c281a04c82ab/scratchpad/swchunk.sh
for n in c2-F-N@0.25 c2-F-N@0.40; do
  for i in 1 2 3 4 5; do
    while pgrep -f "sa6_bake_sweep.py $n " >/dev/null; do sleep 30; done
    [ -f /tmp/claude-0/rp6/adapt2/$n/it1/SW_$n.json ] && break
    $S $n 3000 it1
  done &
done
wait
