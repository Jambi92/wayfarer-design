# tan_relax.py IN OUT MASKKEY iters : tangential (in-surface) vertex relaxation inside a mask, re-projected onto the input surface.
import sys, numpy as np, igl, scipy.sparse as sp
a=sys.argv; P=dict(np.load(a[1])); V=P['V'].astype(float); Q=P['Q']; m=P[a[3]].astype(float) if a[3] in P else np.load(a[3]); it=int(a[4])
n=len(V); e=np.r_[Q[:,[0,1]],Q[:,[1,2]],Q[:,[2,3]],Q[:,[3,0]]]
A=sp.coo_matrix((np.ones(2*len(e)),(np.r_[e[:,0],e[:,1]],np.r_[e[:,1],e[:,0]])),(n,n)).tocsr(); A.data[:]=1; d=np.asarray(A.sum(1)).ravel()
T=np.r_[Q[:,[0,1,2]],Q[:,[0,2,3]]]; V0=V.copy()
w=np.clip(m,0,1)[:,None]
for k in range(it):
    N=igl.per_vertex_normals(V,T); c=(A@V)/d[:,None]; t=c-V; t-= (t*N).sum(1)[:,None]*N
    V=V+0.5*w*t
    if k%3==2 or k==it-1:
        sel=np.nonzero(m>0.01)[0]; _,_,cp=igl.point_mesh_squared_distance(V[sel],V0,T); V[sel]=cp
P['V']=V; np.savez(a[2],**P); print('moved max mm %.3f'%(np.linalg.norm(V-V0,axis=1).max()*10))
