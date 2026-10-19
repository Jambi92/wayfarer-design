# fitcage.py IN.npz OUT.npz "centres" R [L] [lam] [iters] : local least-squares fit of the cage limit surface (level L) to the
# per-colour source targets, for cage verts within R cm of the centres (minus HOLD verts, env HOLD="id,id,..").
import sys, os, numpy as np, scipy.sparse as sp
from scipy.sparse.linalg import lsqr
from scipy.spatial import cKDTree
sys.path.insert(0,'/home/claude/stc/rp1e')
from ccmat import cc_matrix, limit_matrix
inp,out=sys.argv[1],sys.argv[2]; cen=np.array(eval(sys.argv[3]),float).reshape(-1,3); R=float(sys.argv[4])
L=int(sys.argv[5]) if len(sys.argv)>5 else 3; lam=float(sys.argv[6]) if len(sys.argv)>6 else 0.3; it=int(sys.argv[7]) if len(sys.argv)>7 else 3
z=np.load(inp); V0=z['V'].astype(float); F=[list(map(int,f[f>=0])) for f in z['F']]; col=np.load(inp.replace('.npz','_col.npy'))
n=len(V0); hold=set(int(t) for t in os.environ.get('HOLD','').split(',') if t)
free=np.array([i for i in range(n) if np.min(np.linalg.norm(cen-V0[i],axis=1))<R and i not in hold])
M,FL=cc_matrix(n,F,L); M=limit_matrix(M.shape[0],FL)@M; M=M.tocsc()
cols=sorted(set(col.tolist())); oh=sp.csr_matrix((np.ones(n),(np.arange(n),np.searchsorted(cols,col))),shape=(n,len(cols)))
W=(M@oh).toarray(); dom=np.array(cols)[W.argmax(1)]
Mf=M[:,free]; rows=np.unique(Mf.nonzero()[0]); infl=np.asarray(abs(Mf[rows]).sum(1)).ravel(); rows=rows[infl>0.2]
Mf=Mf[rows].tocsr(); fixed=np.setdiff1d(np.arange(n),free)
kd={c:(lambda t:(cKDTree(t['V']),t['V']))(np.load('tg_r2m5_c%d.npz'%c)) for c in set(dom[rows].tolist())}
# cage umbrella Laplacian on free verts (keep original detail): rows = free verts
nb=[set() for _ in range(n)]
for f in F:
    for i in range(len(f)): nb[f[i]].add(f[(i+1)%len(f)]); nb[f[(i+1)%len(f)]].add(f[i])
Lr=[];Lc=[];Ld=[]
for r,v in enumerate(free):
    Lr.append(r);Lc.append(v);Ld.append(1.0)
    for u in nb[v]: Lr.append(r);Lc.append(u);Ld.append(-1.0/len(nb[v]))
Lap=sp.csr_matrix((Ld,(Lr,Lc)),shape=(len(free),n)); Lap0=Lap@V0
V=V0.copy()
for k in range(it):
    P=M[rows]@V; T=np.zeros_like(P)
    for c in kd:
        m=dom[rows]==c; T[m]=kd[c][1][kd[c][0].query(P[m])[1]]
    err0=np.linalg.norm(P-T,axis=1); wgt=np.where(err0<float(os.environ.get('OUTL','0.6')),1.0,0.0)
    # solve for free coords: [Mf; sqrt(lam) Lap_f] x = [T - Mfix Vfix; sqrt(lam)(Lap0 - Lap_fix Vfix)]
    Mfix=M[rows][:,fixed]; Lf=Lap[:,free]; Lx=Lap[:,fixed]
    Wd=sp.diags(wgt); A=sp.vstack([Wd@Mf, np.sqrt(lam)*Lf]).tocsr()
    for d in range(3):
        b=np.r_[wgt*(T[:,d]-Mfix@V[fixed,d]), np.sqrt(lam)*(Lap0[:,d]-Lx@V[fixed,d])]
        V[free,d]=lsqr(A,b,x0=V[free,d],atol=1e-10,btol=1e-10,iter_lim=5000)[0]
    P=M[rows]@V; print('iter',k,'free',len(free),'pts',len(rows),'err mean/max before %.3f/%.3f'%(err0.mean(),err0.max()),'move max %.2f'%np.linalg.norm(V-V0,axis=1).max())
np.savez_compressed(out,V=V,F=z['F']); np.save(out.replace('.npz','_col.npy'),col)
