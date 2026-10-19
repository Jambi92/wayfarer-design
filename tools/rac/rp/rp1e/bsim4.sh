#!/bin/bash
# bsim3.sh TAG CAGE.npz CAGECOL.npy TPREFIX LEV : production-like stack (N + 2x[Smooth,N] per level; final level P+N for body, feet 6/7/8 N+smooth)
cd /home/claude/stc/rp1e
[ "$2" != "cage_$1.npz" ] && cp $2 cage_$1.npz; [ "$3" != "cage_$1_col.npy" ] && cp $3 cage_$1_col.npy
/home/claude/stc/bin/python3 selfx_npz.py -- cage_$1.npz 2>&1 | grep SELFX
SIMMODE=N SMR=2 FINALMODE=PN FSMR=0 FINALN=6,7,8,13,14,15 timeout 4000 /home/claude/stc/bin/python3 sim.py -- cage_$1.npz cage_$1_col.npy $4 $5 sim_$1 2>&1 | grep -c LEVEL > /dev/null
for k in $(seq 1 $5); do timeout 2500 /home/claude/stc/bin/python3 selfx_npz.py -- sim_$1_L$k.npz 2>&1 | grep -q SELFX; done
python3 zsx.py $(for k in $(seq 1 $5); do echo sim_$1_L${k}_sx.npy; done)
python3 dev.py sim_$1_L$5.npz
