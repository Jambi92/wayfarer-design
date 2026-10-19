#!/bin/bash
# fsim.sh TAG LEVELS : sim existing cage_TAG.npz (+meta), feet self-intersections per level
cd /home/claude/stc/rp1e
/home/claude/stc/bin/python3 selfx.py -- cage_$1.npz sx_$1.json 2>&1 | grep SELFX | tr '\n' ' '
python3 cagecolf.py cage_$1.npz ${COL:-col_foot.npy} > /dev/null
SIMMODE=N SMR=2 FINALMODE=PN FSMR=0 timeout 3000 /home/claude/stc/bin/python3 sim.py -- cage_$1.npz cage_$1_col.npy ${TG:-tg_ft} $2 sim_$1 2>&1 | grep -c LEVEL > /dev/null
for k in $(seq 1 $2); do timeout 3000 /home/claude/stc/bin/python3 selfx_npz.py -- sim_$1_L$k.npz 2>&1 | grep -q SELFX; python3 -c "
import numpy as np; C=np.load('sim_$1_L${k}_sx.npy'); m=C[:,2]<17; print('L$k feet', m.sum(), 'L', (m&(C[:,0]>0)).sum(), 'R', (m&(C[:,0]<0)).sum(), end=' | ')"; done; echo
