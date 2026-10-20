# python3 misses.py PROD.npz deviation_arrays.npz [exclude_src_vertex_mask.npy,...] : clusters of over-limit deviation (blender frame coords)
import sys, numpy as np
from scipy.spatial import cKDTree
from scipy.sparse.csgraph import connected_components
from scipy.sparse import coo_matrix
P=np.load(sys.argv[1]); D=np.load(sys.argv[2]); w=np.load('/home/claude/stc/rp1/weld_a.npz'); S=w['V']
zz=np.load('/home/claude/stc/rp1/zones.npz'); zone=zz['zone']; names=list(zz['names'])
lim=np.array([3.0 if n=='general' else 1.5 for n in names])
dsp=D['src_to_prod_mm']; dv=D['prod_vert_to_src_mm']; zv=D['prod_vert_zone']
ex=np.zeros(len(S),bool)
for f in (sys.argv[3].split(',') if len(sys.argv)>3 else []): ex[np.load(f)]=True
def clus(X,val,tag):
    if len(X)==0: print(tag,'none'); return
    kd=cKDTree(X); e=np.array(list(kd.query_pairs(0.5)));n=len(X)
    g=coo_matrix((np.ones(len(e)),(e[:,0],e[:,1])),shape=(n,n)) if len(e) else coo_matrix((n,n)); k,l=connected_components(g,directed=False)
    out=sorted([(val[l==c].max(),int((l==c).sum()),(X[l==c][val[l==c].argmax()]*[1,-1,1]).round(2).tolist()) for c in range(k)],reverse=True)
    print(tag,len(X),'pts',k,'clusters')
    for o in out[:40]: print('  %.2f mm n=%d at %s'%o)
m=(dsp>lim[zone])&~ex; clus(S[m],dsp[m],'SRC->PROD over')
for i,nm in enumerate(names):
    mm=m&(zone==i); 
    if mm.any(): print('   zone',nm,int(mm.sum()),'max %.2f'%dsp[mm].max())
m2=dv>lim[zv]; clus(P['V'][m2],dv[m2],'PROD->SRC over')
