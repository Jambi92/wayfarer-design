#!/bin/bash
# RAC W1i driver AS RUN: build the final W1i set from a gn6 parameter file. Usage: final6.sh params.json
set -e
P=$1
S=/tmp/claude-0/-home-claude-wayfarer-design/19af7d50-3b61-5fda-9fe0-7a30770fb334/scratchpad; F=$S/w1f; G=$S/w1g; T=/home/claude/wayfarer-design/tools/rac/w1
cd $T/w1i_drivers
python3 -c "
import sys, json; sys.path.insert(0, '.'); import gn6 as gn5, gn3
x = json.load(open('$P'))['x']; B, sc = gn5.unpack(x)
r, C = gn3.build('GO', 'GO', B, sc, wd=gn3.G + '/final')
json.dump({'x': x, 'names': gn5.NAMES, 'bone_scales': B, 'sculpt': sc, 'envelope': r}, open(gn3.G + '/final/GO_params.json', 'w'), indent=1)
print('GO', r['r6']['stature'])"
cp $G/final/GO-LEAN_rest.npz $G/final/GO-LEAN_r6.npz $G/final_lean/
for t in 0.0 0.5 1.0; do cp $G/final/skp_GO/t$t/GO_meas.json $G/skp/t$t/GO_meas.json; done; cp $G/final/skp_GO/GO_skp.json $G/skp/; cp $G/final/GO_cib.json $G/cib/
cd $T
python3 run_candidate.py $G/final GO $F/final/MF-M-R_rest.npz > $G/final/GO.rc.log 2>&1
cp $G/final/GO_meas.json $G/cand/
mkdir -p $G/go16; for s in rest r6; do cp $G/final/grid_GO/GO-C025025_$s.npz $G/go16/GOR-BODY-16_$s.npz; done
python3 run_candidate.py $G/go16 GOR-BODY-16 $F/final/MF-M-R_rest.npz > $G/go16/rc.log 2>&1
rm -rf $G/stress; python3 w1i_drivers/stress6.py $G/final/GO_params.json $G/stress
echo FINAL BUILD DONE
