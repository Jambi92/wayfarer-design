# qrelax.py IN OUT ITERS : quad-quality relaxation -- vertices of quads outside the T-4 targets (angles 45-135, aspect <=4)
# and their 1-ring take tangential uniform-Laplacian steps, then guarded projection back onto the source.
import numpy as np, sys
sys.path.insert(0,'/tmp/claude-0/rt')
from subproj import Projector, vertex_part, neighbors, vnormals
inp,out,IT=sys.argv[1],sys.argv[2],int(sys.argv[3])
z=np.load(inp); V=z['V'].copy(); Q=z['Q']; FP=z['FP']
PR=Projector(); vp,M=vertex_part(Q,FP,len(V)); band=np.asarray((M>0).sum(1)).ravel()>1
A=neighbors(Q,len(V)); deg=np.asarray(A.sum(1)).ravel()
def bad(V):
    ang=[]
    for i in range(4):
        a=V[Q[:,(i-1)%4]]-V[Q[:,i]]; b=V[Q[:,(i+1)%4]]-V[Q[:,i]]
        ang.append((a*b).sum(1)/np.maximum(np.linalg.norm(a,axis=1)*np.linalg.norm(b,axis=1),1e-12))
    ang=np.degrees(np.arccos(np.clip(np.stack(ang,1),-1,1)))
    el=np.stack([np.linalg.norm(V[Q[:,(i+1)%4]]-V[Q[:,i]],axis=1) for i in range(4)],1)
    asp=(el[:,0]+el[:,2])/np.maximum(el[:,1]+el[:,3],1e-12); asp=np.maximum(asp,1/np.maximum(asp,1e-12))
    return ~(((ang>=45)&(ang<=135)).all(1)&(asp<=4))
for it in range(IT):
    b=bad(V); print('iter',it,'bad quads',b.sum())
    reg=np.zeros(len(V),bool); reg[Q[b].ravel()]=True; reg|=(A@reg.astype(float))>0
    idx=np.nonzero(reg)[0]
    N=vnormals(V,Q); avg=(A@V)/deg[:,None]; d=avg-V; d-=(d*N).sum(1)[:,None]*N
    V[idx]+=0.5*d[idx]
    V[idx]=PR.project(V[idx],vp[idx],band[idx],N[idx])
print('final bad',bad(V).sum())
np.savez(out,V=V,Q=Q,FP=FP)
