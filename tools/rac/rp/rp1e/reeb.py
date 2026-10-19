import numpy as np, sys, json, heapq
from scipy import ndimage as ndi
from scipy.sparse import coo_matrix
from scipy.sparse.csgraph import dijkstra
s=sys.argv[1]; er=int(sys.argv[2])
z=np.load('/home/claude/stc/rp1e/hand_%s.npz'%s); hand=z['hand']; lo=z['lo']; h=float(z['h'])
L=json.load(open('landmarks_source.json'))['wrist_'+s]
pp=np.array(L['plane_point'])*np.array([1,-1,1]); nn=np.array(L['plane_normal'])*np.array([1,-1,1])   # analysis->blender frame
he=ndi.binary_erosion(hand,iterations=er)
lab,n=ndi.label(he); sz=np.bincount(lab.ravel()); sz[0]=0; he=lab==sz.argmax()
idx=np.argwhere(he); P=lo+idx*h; N=len(idx)
dpl=(P-pp)@nn
# voxel graph 26-neighbour
ix=-np.ones(he.shape,np.int64); ix[tuple(idx.T)]=np.arange(N)
rows=[];cols=[];ws=[]
for dx in (-1,0,1):
  for dy in (-1,0,1):
    for dz in (-1,0,1):
      if (dx,dy,dz)<=(0,0,0): continue
      j=np.full(N,-1); q=idx+[dx,dy,dz]; ok=(q>=0).all(1)&(q<np.array(he.shape)).all(1); j[ok]=ix[tuple(q[ok].T)]
      k=j>=0; rows.append(np.where(k)[0]); cols.append(j[k]); ws.append(np.full(k.sum(),np.sqrt(dx*dx+dy*dy+dz*dz)*h))
r=np.concatenate(rows);c=np.concatenate(cols);ww=np.concatenate(ws)
G=coo_matrix((ww,(r,c)),shape=(N,N)).tocsr()
src=np.where(dpl<dpl.min()+0.8)[0]; print('N',N,'sources',len(src))
D=dijkstra(G,directed=False,indices=src,min_only=True)
np.savez_compressed('/home/claude/stc/rp1e/geo_%s.npz'%s,idx=idx,D=D,lo=lo,h=h,shape=he.shape)
# Reeb: components of level bands
step=0.6; nb=int(np.ceil(D[np.isfinite(D)].max()/step))
for b in range(nb):
    m=(D>=b*step)&(D<(b+1)*step); 
    sub=np.zeros(he.shape,bool); sub[tuple(idx[m].T)]=True
    l2,k=ndi.label(sub,structure=np.ones((3,3,3)))
    sizes=np.bincount(l2[tuple(idx[m].T)])[1:]
    print('%5.1f cm: %d comps sizes %s'%(b*step,k,sorted(sizes.tolist(),reverse=True)[:7]))
# ---- watershed segmentation from band seeds
from skimage.segmentation import watershed
Dv=np.full(he.shape,np.inf,np.float32); Dv[tuple(idx.T)]=D
def comps(lo_,hi_):
    sub=(Dv>=lo_)&(Dv<hi_); l2,k=ndi.label(sub,structure=np.ones((3,3,3))); sz=np.bincount(l2.ravel()); sz[0]=0
    return l2,[i for i in np.argsort(-sz) if sz[i]>500]
tb=float(sys.argv[3]); fb=float(sys.argv[4])
markers=np.zeros(he.shape,np.int32)
markers[(Dv<tb-2.0)]=1                                     # palm/proximal
l2,cs=comps(fb,fb+0.6); print('finger band comps',len(cs))
cent=[np.argwhere(l2==c).mean(0)*h+lo for c in cs]
for k,c in enumerate(cs): markers[l2==c]=k+2
lt,ct=comps(tb,tb+0.6); thumbc=ct[1]; tm=lt==thumbc   # second-largest comp at the thumb band = thumb
# which finger-band comp is the thumb continuation: geodesic connectivity via watershed later; mark thumb seed separately
markers[tm]=9
Dv2=np.where(np.isfinite(Dv),Dv,0)
lab=watershed(Dv2,markers,mask=he)
# thumb label: comps whose label overlaps thumb continuation -> merge the finger seed that is reached from thumb
print({int(k):int((lab==k).sum()) for k in np.unique(lab) if k})
np.savez_compressed('/home/claude/stc/rp1e/lab_%s.npz'%s,lab=lab.astype(np.int8),lo=lo,h=h,cent=np.array(cent))
