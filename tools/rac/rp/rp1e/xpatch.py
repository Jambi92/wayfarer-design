# xpatch.py IN.npz IN_col.npy OUT.npz SPEC.json : explicit designed patch. SPEC: {"remove":[[face verts]...],
#  "new":{"name":[x,y,z,col]}, "move":{"id":[x,y,z]}, "faces":[[id or name,...]...]}
import numpy as np, sys, json
from orient import orient_patch, check
z=np.load(sys.argv[1]); V=z['V'].astype(float).tolist(); F=[list(map(int,f[f>=0])) for f in z['F']]; cc=np.load(sys.argv[2]).tolist()
S=json.load(open(sys.argv[4]))
rm=[sorted(f) for f in S['remove']]; keep=[]; nrm=0
for f in F:
    if sorted(f) in rm: nrm+=1
    else: keep.append(f)
assert nrm==len(rm),('removed',nrm,'of',len(rm))
ids={}
for nm,p in S['new'].items(): V.append(p[:3]); cc.append(int(p[3])); ids[nm]=len(V)-1
for i,p in S.get('move',{}).items(): V[int(i)]=p
Fn=[[ids[x] if isinstance(x,str) else int(x) for x in f] for f in S['faces']]
Fn=orient_patch(keep,Fn); G=keep+Fn; d,b=check(G)
if d or b: raise SystemExit('topology dup %d bnd %d'%(d,b))
Fa=np.full((len(G),4),-1)
for k,f in enumerate(G): Fa[k,:len(f)]=f
np.savez_compressed(sys.argv[3],V=np.array(V),F=Fa); np.save(sys.argv[3].replace('.npz','_col.npy'),np.array(cc))
json.dump(ids,open(sys.argv[3].replace('.npz','_new.json'),'w')); print('V',len(V),'F',len(G),'new',ids)
