# adopt.sh NEW.npz CHAINREMAP(from cur) : make NEW the current cage; update remap_v011_to_cur, rings_cur.json, fsm_cur.txt (remapped, no new verts)
N=$1; R=$2
python3 - $N $R <<'PY'
import numpy as np, json, sys, shutil
N,R=sys.argv[1:3]; m=np.load(R)
r=np.load('remap_v011_to_cur.npy'); np.save('remap_v011_to_cur.npy',np.array([m[x] if x>=0 else -1 for x in r]))
J=json.load(open('rings_cur.json'))
for s in J:
    for k in J[s]: J[s][k]=[int(m[i]) if m[i]>=0 else -1 for i in J[s][k]]
json.dump(J,open('rings_cur.json','w'))
old=[int(t) for t in open('fsm_cur.txt').read().split()]
open('fsm_cur.txt','w').write(' '.join(map(str,sorted(set(int(m[i]) for i in old if m[i]>=0)))))
shutil.copy(N,'cur.npz'); shutil.copy(N.replace('.npz','_col.npy'),'cur_col.npy'); print('adopted',N,len(np.load(N)['V']))
PY
