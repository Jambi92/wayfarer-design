#!/bin/bash
# usage: run_e.sh TAG LEVELS  (design_R/L.json already built)
set -e
cd /home/claude/stc/rp1e
python3 buildcage.py cage_$1.npz R L > /dev/null
python3 cagecol.py cage_$1.npz col_handtest.npy > /dev/null
SIMMODE=${SIMMODE:-N} SMR=${SMR:-2} SMF=${SMF:-0.5} SMI=${SMI:-2} timeout 3000 /home/claude/stc/bin/python3 sim.py -- cage_$1.npz cage_$1_col.npy ${TG:-tg_ht} $2 sim_$1 2>&1 | grep -c LEVEL > /dev/null
for k in $(seq 0 $(( $2 < 2 ? $2 : 2 ))); do timeout 3000 /home/claude/stc/bin/python3 selfx_npz.py -- sim_$1_L$k.npz 2>&1 | grep SELFX; done
python3 sxzones.py $(for k in $(seq 0 $(( $2 < 2 ? $2 : 2 ))); do echo sim_$1_L$k\_sx.npy; done) | sed 's/np.str_(//g; s/)//g'
