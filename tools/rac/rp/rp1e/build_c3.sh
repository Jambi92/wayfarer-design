set -e; cd /home/claude/stc/rp1e
LIPOFF=0.3 MINNEW=3037 python3 midcleft.py t_fitH3.npz t_fitH3_col.npy c3a.npz "1557,1550;1558,1563" 27,-35,4 0.3 | tail -2
python3 - <<'PY'
import numpy as np, json
z=np.load('c3a.npz'); V=z['V'].copy(); c=np.load('c3a_col.npy').copy()
mv={2782:(23.36,-41.97,146.36),2752:(23.47,-42.30,146.30),2812:(23.17,-42.30,146.40),
    2783:(23.38,-41.86,147.29),2753:(23.42,-42.15,147.20),2813:(23.22,-42.15,147.40)}
for k,p in mv.items(): V[k]=p
RR=json.load(open('design_v010_rings.json'))
for i in range(5,16): c[RR['L']['J'][i]]=1
for i in range(15,29): c[RR['R']['J'][i]]=1
np.savez_compressed('c3.npz',V=V,F=z['F']); np.save('c3_col.npy',c); print('C3',V.shape,z['F'].shape)
PY
/home/claude/stc/bin/python3 selfx_npz.py -- c3.npz 2>&1 | grep SELFX
