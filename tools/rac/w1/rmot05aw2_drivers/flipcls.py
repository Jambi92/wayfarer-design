import numpy as np,sys;sys.path.insert(0,'/home/claude/aw1');import aw1lib as L
V=np.load(sys.argv[1])['V'];F=L.F
n=lambda X: np.cross(X[F[:,1]]-X[F[:,0]],X[F[:,2]]-X[F[:,0]]);u=lambda a:a/np.linalg.norm(a,axis=1)[:,None]
N0=u(n(L.V0));N1=u(n(V));vn0=L.vnormals(L.V0)
for _ in range(10): vn0=L.Avg@vn0
S=u(vn0[F].mean(1));mv=np.linalg.norm(V-L.V0,axis=1)>1e-9;fm=mv[F].any(1)
idx=np.where(fm&((N0*N1).sum(1)<0))[0]
for i in idx: print(i,'base·surf %.2f now·surf %.2f'%(N0[i]@S[i],N1[i]@S[i]))
