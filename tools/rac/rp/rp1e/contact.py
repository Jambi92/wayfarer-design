import numpy as np, sys, json
from scipy.spatial import cKDTree
s=sys.argv[1]; roles=json.loads(sys.argv[2]); thr=float(sys.argv[3])
q=np.load('segH_%s.npz'%s); u=q['used']; l=q['lab']; V=np.load('/home/claude/stc/rp1/weld.npz')['V'][u]
names={int(k):v for k,v in roles.items()}; names[9]='palm'
T={k:cKDTree(V[l==k]) for k in names}
for a in names:
    for b in names:
        if a>=b: continue
        d,_=T[b].query(V[l==a],distance_upper_bound=thr); m=np.isfinite(d)
        if m.sum()==0: continue
        P=V[l==a][m]
        print('%-7s~%-7s n=%5d  z %.1f..%.1f  centre %s'%(names[a],names[b],m.sum(),P[:,2].min(),P[:,2].max(),P.mean(0).round(1)))
