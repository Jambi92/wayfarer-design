#!/bin/bash
# run4.sh TAG : build, colour, sim to L4 (N+smooth, final PN), selfx L0,L2,L4, hand dev
cd /home/claude/stc/rp1e
python3 buildcage.py cage_$1.npz R L > /dev/null && python3 cagecol.py cage_$1.npz ${COL:-col_handtest.npy} > /dev/null
SIMMODE=N SMR=2 FINALMODE=${FINALMODE:-PN} FSMR=${FSMR:-0} timeout 3000 /home/claude/stc/bin/python3 sim.py -- cage_$1.npz cage_$1_col.npy ${TG:-tg_m25} 4 sim_$1 2>&1 | grep -c LEVEL > /dev/null
for k in 0 2 4; do timeout 3000 /home/claude/stc/bin/python3 selfx_npz.py -- sim_$1_L$k.npz 2>&1 | grep SELFX; done
python3 sxzones.py sim_$1_L0_sx.npy sim_$1_L2_sx.npy sim_$1_L4_sx.npy | sed 's/np.str_(//g; s/)//g' | grep -o "hand_[LR]': [0-9]*" | tr '\n' ' '; echo
python3 dev.py sim_$1_L4.npz | grep hand
