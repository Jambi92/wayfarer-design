#!/bin/bash
# bsim.sh TAG SRC_COL CAGE.npz LEV : targets from SRC_COL, cage colours by nearest + foot override (g5b), sim, selfx per level, zones
cd /home/claude/stc/rp1e
python3 targets.py $2 tg_$1 2.5 0.7 > /dev/null
python3 - <<PY
import numpy as np
from scipy.spatial import cKDTree
z=np.load('$3'); V=z['V']; S=np.load('/home/claude/stc/rp1/weld.npz')['V']; col=np.load('$2')
d,i=cKDTree(S).query(V); cc=col[i].copy()
g=np.load('cage_g5b.npz')['V']; gc=np.load('cage_g5b_col.npy'); d2,j=cKDTree(g).query(V); m=(d2<0.01)&(gc[j]!=2); cc[m]=gc[j][m]
np.save('cage_$1_col.npy',cc); import shutil; shutil.copy('$3','cage_$1.npz')
PY
SIMMODE=N SMR=2 FINALMODE=N FSMR=2 timeout 3000 /home/claude/stc/bin/python3 sim.py -- cage_$1.npz cage_$1_col.npy tg_$1 $4 sim_$1 2>&1 | grep -c LEVEL > /dev/null
for k in $(seq 1 $4); do timeout 1500 /home/claude/stc/bin/python3 selfx_npz.py -- sim_$1_L$k.npz 2>&1 | grep -q SELFX; done
python3 zsx.py $(for k in $(seq 1 $4); do echo sim_$1_L${k}_sx.npy; done)
