import numpy as np, json, sys, scipy.sparse as sp, scipy.sparse.csgraph as cg, trimesh
sys.path.insert(0,'/tmp/claude-0/rt')
from common import *
V,F=load_src(); L=json.load(open('lm_src.json'))
C=V[F].mean(1); fl=label_points(C,L)
m=trimesh.Trimesh(V,F,process=False); fa=m.face_adjacency
for it in range(3):
    same=fl[fa[:,0]]==fl[fa[:,1]]; e=fa[same]
    G=sp.coo_matrix((np.ones(len(e)),(e[:,0],e[:,1])),shape=(len(F),len(F)))
    nc,cl=cg.connected_components(G,directed=False)
    sizes=np.bincount(cl); changed=0
    for lab in np.unique(fl):
        comps=np.unique(cl[fl==lab]); 
        if len(comps)<=1: continue
        big=comps[np.argmax(sizes[comps])]
        for c in comps:
            if c==big: continue
            idx=np.nonzero(cl==c)[0]
            # neighbour labels across the island border
            nb=np.concatenate([fa[np.isin(fa[:,0],idx),1],fa[np.isin(fa[:,1],idx),0]]); nl=fl[nb]; nl=nl[nl!=lab]
            if len(nl): fl[idx]=np.bincount(nl).argmax(); changed+=1
    print('islands relabelled',changed)
    if changed==0: break
np.save('flab.npy',fl)
# vertex label = majority of incident faces
M=sp.coo_matrix((np.ones(F.size),(F.ravel(),np.repeat(fl,3))),shape=(len(V),len(PARTS))).tocsr(); vl=np.asarray(M.argmax(1)).ravel()
np.save('vlab.npy',vl)
import collections; print({PARTS[k]:v for k,v in sorted(collections.Counter(fl).items())})
