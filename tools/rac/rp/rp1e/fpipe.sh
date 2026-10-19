#!/bin/bash
# fpipe.sh TAG : design (fpL/fpR) -> build -> untangle -> colour -> sim L3 (N, smooth) feet folds + dev
cd /home/claude/stc/rp1e
python3 footdesign.py L fpL.json >/dev/null && python3 footdesign.py R fpR.json >/dev/null && python3 buildfoot.py ui_v005.npz cage_$1r.npz L R >/dev/null || exit 1
python3 -c "
import numpy as np, json
z=np.load('cage_$1r.npz'); meta=json.load(open('cage_$1r_meta.json')); mov=np.zeros(len(z['V']),bool)
for s,m in meta.items():
    for nm,r in m['rings'].items():
        if nm!='K': mov[r]=True
    for nm,T in m['tubes'].items(): mov[T[0]]=True
np.save('mov_$1.npy',mov)"
timeout 2000 /home/claude/stc/bin/python3 separate.py -- cage_$1r.npz mov_$1.npy nopins.json 0.15 80 cage_$1.npz 2>&1 | grep -c ITER > /dev/null; cp cage_$1r_meta.json cage_$1_meta.json
/home/claude/stc/bin/python3 selfx.py -- cage_$1.npz sx_$1.json 2>&1 | grep SELFX | tr '\n' ' '
SKIP0=0 TC=2 python3 cagecolf.py cage_$1.npz col_foot2.npy > /dev/null
SIMMODE=N SMR=2 FINALMODE=N FSMR=2 ./fsim2.sh $1 ${LEV:-3} $1 | tr '\n' ' '
python3 dev.py sim_$1_L${LEV:-3}.npz | grep -i foot | awk '{print $1, $3, $5, $7}' | tr '\n' ' '; echo
