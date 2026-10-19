#!/bin/bash
# bsim2.sh TAG CAGE.npz CAGECOL.npy TPREFIX LEV : coarse selfx, sim, selfx per level, zones
cd /home/claude/stc/rp1e
cp $2 cage_$1.npz; python3 - <<PY
import numpy as np
from scipy.spatial import cKDTree
V=np.load('cage_$1.npz')['V']; cc=np.load('$3').copy()
g=np.load('cage_g5b.npz')['V']; gc=np.load('cage_g5b_col.npy'); d2,j=cKDTree(g).query(V); m=(d2<0.01)&(gc[j]!=2); cc[m]=gc[j][m]
np.save('cage_$1_col.npy',cc)
PY
/home/claude/stc/bin/python3 selfx_npz.py -- cage_$1.npz 2>&1 | grep SELFX
SIMMODE=N SMR=2 FINALMODE=N FSMR=2 timeout 3000 /home/claude/stc/bin/python3 sim.py -- cage_$1.npz cage_$1_col.npy $4 $5 sim_$1 2>&1 | grep -c LEVEL > /dev/null
for k in $(seq 1 $5); do timeout 1500 /home/claude/stc/bin/python3 selfx_npz.py -- sim_$1_L$k.npz 2>&1 | grep -q SELFX; done
python3 zsx.py $(for k in $(seq 1 $5); do echo sim_$1_L${k}_sx.npy; done)
