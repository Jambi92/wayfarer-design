# stage4_assemble.py OUT.npz : v015 production with (a) the non-digit hand region projected onto rev107 and (b) the ten
# draped digit patches (R22/R23 with the distal bridge cut + capped). Protected outside-hand vertices are copied exactly.
import sys,pickle,numpy as np,json; sys.path.insert(0,'/tmp/claude-0/hand/tools'); from hm import *
out=sys.argv[1]
V,Q=load15(); Vp=np.load('/tmp/claude-0/hand/Vproj.npy'); vp=pickle.load(open('/tmp/claude-0/hand/vpatch.pkl','rb'))
prot=np.load('/tmp/claude-0/hand/v015_to_r107_d.npy')<1e-4
Vn=Vp.copy(); Vn[prot]=V[prot]
remove=np.zeros(len(Q),bool); remove[vp['_strip']]=True
newV=[]; newQ=[]; nv=len(V); rep={}
for k,p in vp.items():
    if k.startswith('_'): continue
    z=np.load('/tmp/claude-0/hand/drape_%s.npz'%k); g=z['gid']; X3=z['X3']; Ql=z['Ql']
    remove[p['faces']]=True
    loc2glob=g.copy(); nn=(g<0).sum(); loc2glob[g<0]=np.arange(nv,nv+nn); nv+=nn
    ex=g>=0; assert not prot[g[ex]].any()
    Vn[g[ex]]=X3[ex]; newV.append(X3[~ex]); newQ.append(loc2glob[Ql]); rep[k]=dict(quads=len(Ql),new_vertices=int(nn))
Vall=np.vstack([Vn]+newV); Qall=np.vstack([Q[~remove]]+newQ)
used=np.zeros(len(Vall),bool); used[Qall.ravel()]=True
# drop vertices no longer referenced (interior of the deleted bridge strip); keep order
mp=-np.ones(len(Vall),int); mp[used]=np.arange(used.sum()); Qall=mp[Qall]; Vall=Vall[used]
print('vertices',len(Vall),'quads',len(Qall),'dropped',(~used).sum())
# protected bookkeeping: old v015 index -> new index
old2new=mp[:len(V)]
Fall=np.vstack([Qall[:,[0,1,2]],Qall[:,[0,2,3]]])
np.savez_compressed(out,V=Vall*np.array([1,-1,1]),Q=Qall,F=Fall,old2new=old2new,prot=prot)
json.dump(rep,open(out.replace('.npz','_digits.json'),'w'),indent=1)
