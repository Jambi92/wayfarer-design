import json, numpy as np, scipy.sparse as sp
from scipy.sparse.csgraph import connected_components
from scipy.spatial import cKDTree
V=np.load('/home/claude/at/final/ac3.npz')['V'].astype(float); F=np.load('/home/claude/ao/prep1/after_VF.npz')['F']; z0=V[:,2].min()
k,inv=np.unique(np.round(V,7),axis=0,return_inverse=True); inv=inv.ravel(); Fw=inv[F]; fc=k[Fw].mean(1); tree=cKDTree(fc)
def lg(c,r):
    idx=np.array(tree.query_ball_point(c,r)); f=Fw[idx]
    vs=np.unique(f); remap=-np.ones(len(k),int); remap[vs]=np.arange(len(vs)); f=remap[f]
    E=np.sort(np.concatenate([f[:,[0,1]],f[:,[1,2]],f[:,[2,0]]]),1); Eu,cnt=np.unique(E,axis=0,return_counts=True); bE=Eu[cnt==1]
    A=sp.coo_matrix((np.ones(len(bE)),(bE[:,0],bE[:,1])),shape=(len(vs),len(vs))); nc,lab=connected_components(A,directed=False); nb=len(np.unique(lab[np.unique(bE)])) if len(bE) else 0
    A=sp.coo_matrix((np.ones(len(Eu)),(Eu[:,0],Eu[:,1])),shape=(len(vs),len(vs))); ncomp,_=connected_components(A,directed=False)
    chi=len(vs)-len(Eu)+len(f); return (2*ncomp-chi-nb)/2
rng=np.random.default_rng(0); samp=k[rng.choice(len(k),4000,replace=False)]
# thin samples to ~4 cm spacing
keep=[]; t=None
for p in samp:
    if not keep or np.min(np.linalg.norm(np.array(keep)-p,axis=1))>0.04: keep.append(p)
hits=[]
for i,c in enumerate(keep):
    g=lg(c,0.06)
    if g>=1: hits.append([round(c[0]*100,1),round(c[1]*100,1),round((c[2]-z0)*100,1),g])
print('centres',len(keep),'hits',len(hits)); 
for h in hits: print(h)
json.dump(hits,open('au_genus_scan.json','w'))
