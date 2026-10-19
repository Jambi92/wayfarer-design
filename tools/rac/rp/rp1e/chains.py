import numpy as np, sys, json
s=sys.argv[1]
z=np.load('sreeb_%s.npz'%s); used=z['used']; comp=z['comp']; bands=z['bands']; D=z['D']
vl=np.load('vlab_%s.npy'%s)[:,1]
V=np.load('/home/claude/stc/rp1/weld.npz')['V'][used]
out={}
for k in range(vl.max()+1):
    cs=np.unique(comp[vl==k]); rows=[]
    for c in sorted(cs,key=lambda c:bands[c]):
        P=V[comp==c]; cen=P.mean(0); U,S,Wt=np.linalg.svd(P-cen,full_matrices=False)
        rows.append(dict(band=int(bands[c]),n=len(P),c=cen.round(3).tolist(),sv=(S/np.sqrt(len(P))*2).round(2).tolist()))
    out[k]=rows
    print(k,[ (r['band'],r['n'],r['c']) for r in rows])
json.dump(out,open('chains_%s.json'%s,'w'))
