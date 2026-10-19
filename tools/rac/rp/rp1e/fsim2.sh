#!/bin/bash
# fsim2.sh TAG LEV OUTTAG  with env SIMMODE SMR SMF SMI FINALMODE ; feet counts at last level only
cd /home/claude/stc/rp1e
timeout 3000 /home/claude/stc/bin/python3 sim.py -- cage_$1.npz cage_$1_col.npy ${TG:-tg_ft2} $2 sim_$3 2>&1 | grep -c LEVEL > /dev/null
k=$2; timeout 3000 /home/claude/stc/bin/python3 selfx_npz.py -- sim_$3_L$k.npz 2>&1 | grep -q SELFX; python3 -c "
import numpy as np; C=np.load('sim_$3_L${k}_sx.npy'); m=C[:,2]<17; print('$3 L$k feet', m.sum(), 'L', (m&(C[:,0]>0)).sum(), 'R', (m&(C[:,0]<0)).sum())"
