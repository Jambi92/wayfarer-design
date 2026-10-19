# build candidate C1 = v011g + hand/head local limit-surface fit + foot L toe-cleft creases + L axilla pinch columns
set -e; cd /home/claude/stc/rp1e
LIPOFF=0.3 MINNEW=3037 python3 midcleft.py t_fitH2.npz t_fitH2_col.npy c1a.npz "1557,1550;1558,1563" 27,-35,4 0.3 | tail -2
python3 - <<'PY'
import json
json.dump({"path":[1556,3338,1551],"tip":[None,[31.33,-54.49,4.22],None],"A":[[30.9,-55.4,4.22]],"B":[[31.5,-55.4,4.22]]},open('c1b_spec.json','w'))
PY
python3 pathbevel.py c1a.npz c1a_col.npy c1b.npz c1b_spec.json
python3 - <<'PY'
import numpy as np, json
z=np.load('c1b.npz'); V=z['V'].copy(); c=np.load('c1b_col.npy').copy()
mv={2782:(23.36,-41.97,146.36),2752:(23.47,-42.30,146.30),2812:(23.17,-42.30,146.40),
    2783:(23.38,-41.86,147.29),2753:(23.42,-42.15,147.20),2813:(23.22,-42.15,147.40)}
for k,p in mv.items(): V[k]=p
R=json.load(open('design_v010_rings.json'))['L']
for i in range(5,16): c[R['J'][i]]=1
np.savez_compressed('c1.npz',V=V,F=z['F']); np.save('c1_col.npy',c); print('C1',V.shape,z['F'].shape)
PY
/home/claude/stc/bin/python3 selfx_npz.py -- c1.npz 2>&1 | grep SELFX
