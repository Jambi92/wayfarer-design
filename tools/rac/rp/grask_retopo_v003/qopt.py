# qopt.py IN OUT ITERS [soft] : local quad-shape optimisation -- vertices of quads beyond the limits (+2 rings) move toward
# the mean of (uniform Laplacian, parallelogram-rule) targets, tangentially, then guarded re-projection onto v005.
# Moves that would fold a quad or make it worse are reverted per vertex.
import numpy as np, sys, scipy.sparse as sp
sys.path.insert(0,'/tmp/claude-0/rt')
from subproj import Projector, vertex_part, neighbors, vnormals
z=np.load(sys.argv[1]); V=z['V'].copy(); Q=z['Q']; FP=z['FP']; IT=int(sys.argv[3]); SOFT=len(sys.argv)>4 and sys.argv[4]=='soft'
import os; WB=float(os.environ.get('QWB','0')); WP=float(os.environ.get('QWP','0.5')); STEP=float(os.environ.get('QSTEP','0.5')); PB=float(os.environ.get('QPB','0')); PMAX=float(os.environ.get('QPMAX','0.03'))
PR=Projector(); vp,M=vertex_part(Q,FP,len(V)); band=np.asarray((M>0).sum(1)).ravel()>1
A=neighbors(Q,len(V)); deg=np.asarray(A.sum(1)).ravel()
nV=len(V); nF=len(Q)
VF=sp.coo_matrix((np.ones(4*nF),(Q.ravel(),np.repeat(np.arange(nF),4))),shape=(nV,nF)).tocsr()
def quality(V):
    ang=[]
    for i in range(4):
        a=V[Q[:,(i-1)%4]]-V[Q[:,i]]; b=V[Q[:,(i+1)%4]]-V[Q[:,i]]
        ang.append(np.degrees(np.arccos(np.clip((a*b).sum(1)/np.maximum(np.linalg.norm(a,axis=1)*np.linalg.norm(b,axis=1),1e-12),-1,1))))
    ang=np.stack(ang,1); el=np.stack([np.linalg.norm(V[Q[:,(i+1)%4]]-V[Q[:,i]],axis=1) for i in range(4)],1)
    asp=(el[:,0]+el[:,2])/np.maximum(el[:,1]+el[:,3],1e-12); asp=np.maximum(asp,1/np.maximum(asp,1e-12))
    # badness: 0 inside targets, grows outside
    b=np.maximum(0,45-ang.min(1))/45+np.maximum(0,ang.max(1)-135)/45+np.maximum(0,asp-4)/4
    hard=(ang.min(1)<20)|(ang.max(1)>160)|(asp>8)
    return b,hard,ang,asp
def fnorm(V):
    n=np.cross(V[Q[:,2]]-V[Q[:,0]],V[Q[:,3]]-V[Q[:,1]]); return n/np.maximum(np.linalg.norm(n,axis=1),1e-12)[:,None]
n0=fnorm(V)
for it in range(IT):
    b,hard,_,_=quality(V); sel=hard if not SOFT else (b>0)
    print('iter',it,'hard',int(hard.sum()),'soft',int((b>0).sum()),flush=True)
    reg=np.zeros(nV,bool); reg[Q[sel].ravel()]=True
    for _ in range(2): reg|=(A@reg.astype(float))>0
    idx=np.nonzero(reg)[0]
    # parallelogram targets: for each quad corner k, target of Q[:,k] = Q[k-1]+Q[k+1]-Q[k+2]
    T=np.zeros_like(V); W=np.zeros(nV); wq=1.0+WB*b      # bad quads pull harder on their corners
    for k in range(4):
        t=V[Q[:,(k-1)%4]]+V[Q[:,(k+1)%4]]-V[Q[:,(k+2)%4]]
        np.add.at(T,Q[:,k],t*wq[:,None]); np.add.at(W,Q[:,k],wq)
    par=T/np.maximum(W,1e-9)[:,None]; lap=(A@V)/deg[:,None]
    N=vnormals(V,Q); d=(1-WP)*lap+WP*par-V; d-=(d*N).sum(1)[:,None]*N
    Vn=V.copy(); Vn[idx]=V[idx]+STEP*d[idx]
    Pj=PR.project(Vn[idx],vp[idx],band[idx],N[idx])
    if PB>0:   # partial snap: allow a bounded offset from the surface (<= PMAX cm) so sliver corners can open in sharp creases
        off=Vn[idx]-Pj; ln=np.linalg.norm(off,axis=1); sc=np.minimum(1.0,PMAX/np.maximum(ln,1e-12))
        Vn[idx]=Pj+off*(sc*PB)[:,None]
    else: Vn[idx]=Pj
    # revert vertices whose incident quads got worse in total, or flipped vs the original normal
    b1,_,_,_=quality(Vn); fl=(fnorm(Vn)*n0).sum(1)<0.2
    worse=(VF@(b1+fl*10.0))>(VF@(b))+1e-9
    Vn[worse]=V[worse]; V=Vn
b,hard,ang,asp=quality(V); print('final hard',int(hard.sum()),'soft',int((b>0).sum()),'min ang %.1f max ang %.1f max asp %.1f'%(ang.min(),ang.max(),asp.max()))
np.savez(sys.argv[2],V=V,Q=Q,FP=FP)
