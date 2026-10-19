import numpy as np, json, sys
cg=sys.argv[1]
z=np.load(cg); V=z['V']; F=z['F']; meta=json.load(open(cg.replace('.npz','_meta.json')))
adj={}
for f in F:
    f=f[f>=0]
    for i in range(len(f)): a,b=f[i],f[(i+1)%len(f)]; adj.setdefault(int(a),set()).add(int(b)); adj.setdefault(int(b),set()).add(int(a))
def flood(seeds,stop):
    seen=set(seeds); st=list(seeds)
    while st:
        v=st.pop()
        for u in adj[v]:
            if u in stop or u in seen: continue
            seen.add(u); st.append(u)
    return seen
J={'L':[786,788,790,792,794,796,798,800,802,804],'R':list(range(806,825,2))}
# remap to new cage indices? cage_e21f indices differ from v004 (hands removed/compacted) -> use meta W0 and positions
seg={}
z0=np.load('/home/claude/stc/rp1/ck/v004a.npz'); V0=z0['Vc']*[1,-1,1]
from scipy.spatial import cKDTree
T=cKDTree(V)
for s in 'LR':
    ring=[int(T.query(V0[v])[1]) for v in J[s]]
    print(s,'junction loop', all(len([x for x in adj[v] if x in ring])==2 for v in ring))
    arm=flood(meta[s]['W0'],set(ring))
    seg[s]=dict(junction=ring,arm=sorted(arm))
    print(s,'arm+hand verts',len(arm))
json.dump(seg,open(cg.replace('.npz','_seg.json'),'w'))
