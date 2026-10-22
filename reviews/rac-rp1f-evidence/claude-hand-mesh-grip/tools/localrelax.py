# localrelax.py KEY RADIUS_CM ITERS : continue the surface relaxation of a draped patch only around its tiny-quad clusters
import sys,numpy as np; sys.path.insert(0,'/tmp/claude-0/hand/tools'); from drape import *; from patches import boundary_loops
k=sys.argv[1]; rad=float(sys.argv[2]); iters=int(sys.argv[3])
z=dict(np.load('/tmp/claude-0/hand/drape_%s.npz'%k)); P2=z['P2']; Q=z['Ql']; D=Domain(z['Xl'],z['Fl'],z['U']); sgn=np.sign(np.median(orient2(P2,Q)))
bl=np.array(boundary_loops(Q)[0][0]); fixed=np.zeros(len(P2),bool); fixed[bl]=True
t=D.locate(P2); X=D.lift(P2,t)
ar=np.linalg.norm(np.cross(X[Q[:,1]]-X[Q[:,0]],X[Q[:,3]]-X[Q[:,0]]),axis=1); med=np.median(ar)
tiny=np.where(ar<0.02*med)[0]; print('tiny quads',len(tiny))
cen=X[Q[tiny]].mean(1)
from scipy.spatial import cKDTree
dd=cKDTree(cen).query(X)[0]; mov=(dd<rad)&~fixed; print('movable',mov.sum())
n=len(P2); vf=[[] for _ in range(n)]
for qi,q in enumerate(Q):
    for v in q: vf[v].append(qi)
mf=max(len(l) for l in vf); vfi=np.zeros((n,mf),int); vfm=np.zeros((n,mf),bool)
for i,l in enumerate(vf): vfi[i,:len(l)]=l; vfm[i,:len(l)]=True
E=np.unique(np.sort(np.vstack([Q[:,[i,(i+1)%4]] for i in range(4)]),1),axis=0)
nb=[[] for _ in range(n)]
for a_,b_ in E: nb[a_].append(b_); nb[b_].append(a_)
md=max(len(l) for l in nb); nbi=np.zeros((n,md),int); nbm=np.zeros((n,md),bool)
for i,l in enumerate(nb): nbi[i,:len(l)]=l; nbm[i,:len(l)]=True
vqk=np.zeros_like(vfi)
for i in range(n):
    for j,qi in enumerate(vf[i]): vqk[i,j]=int(np.where(Q[qi]==i)[0][0])
idx=np.where(mov)[0]
for it in range(iters):
    c=X[Q].mean(1); ar=0.5*(np.linalg.norm(np.cross(X[Q[:,1]]-X[Q[:,0]],X[Q[:,3]]-X[Q[:,0]]),axis=1)+np.linalg.norm(np.cross(X[Q[:,1]]-X[Q[:,2]],X[Q[:,3]]-X[Q[:,2]]),axis=1))
    w=ar[vfi]*vfm; cen_=(c[vfi]*w[...,None]).sum(1)/(w.sum(1)[:,None]+1e-30)
    mean=(X[nbi]*nbm[...,None]).sum(1)/nbm.sum(1)[:,None]
    Lp=0.5*(cen_-X)+0.2*(mean-X)+0.3*(square_targets(X,Q,vfi,vqk,vfm)-X)
    d2=np.einsum('nij,nj->ni',D.Jp[t],Lp)*0.5; d2[~mov]=0
    prev=set(np.where(orient2(P2,Q)*sgn<=1e-14)[0]); Pn=P2+d2
    for rr in range(60):
        o=orient2(Pn,Q)*sgn; nbq=np.array([q for q in np.where(o<=1e-14)[0] if q not in prev],int)
        if len(nbq)==0: break
        bv=np.unique(Q[nbq]); Pn[bv]=P2[bv]
    P2=Pn; t=D.locate(P2); X=D.lift(P2,t)
    if it%200==0:
        ar=np.linalg.norm(np.cross(X[Q[:,1]]-X[Q[:,0]],X[Q[:,3]]-X[Q[:,0]]),axis=1); print('it',it,'tiny',int((ar<0.02*med).sum()),'min area %.2e'%ar.min(),'folds',int((orient2(P2,Q)*sgn<=1e-14).sum()),flush=True)
z['P2']=P2; z['X3']=X; np.savez('/tmp/claude-0/hand/drape_%s.npz'%k,**z)
