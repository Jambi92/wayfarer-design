import numpy as np, json, sys
cg=sys.argv[1]; z=np.load(cg); F=z['F']; V=z['V']; meta=json.load(open(cg.replace('.npz','_meta.json')))
names={}
for s,m in meta.items():
    for nm,r in m['rings'].items():
        for j,v in enumerate(r): names[v]='%s%s.%d'%(s,nm,j)
    for nm,T in m['tubes'].items():
        for k,r in enumerate(T):
            for j,v in enumerate(r): names[v]='%s%s.%d.%d'%(s,nm,k,j)
pairs=json.load(open(sys.argv[2]))
for i,j in pairs:
    print([names.get(int(v),int(v)) for v in F[i][F[i]>=0]],'X',[names.get(int(v),int(v)) for v in F[j][F[j]>=0]])
