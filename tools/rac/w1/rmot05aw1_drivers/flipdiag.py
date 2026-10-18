import numpy as np,sys;sys.path.insert(0,'/home/claude/aw1');import aw1lib as L
V=np.load(sys.argv[1])['V'];F=L.F
n=lambda X: np.cross(X[F[:,1]]-X[F[:,0]],X[F[:,2]]-X[F[:,0]])
N1=n(V);N0=n(L.V0);vn0=L.vnormals(L.V0)
for _ in range(10): vn0=L.Avg@vn0
vn0/=np.linalg.norm(vn0,axis=1)[:,None];sref=vn0[F].mean(1)
mv=np.linalg.norm(V-L.V0,axis=1)>1e-9;fm=mv[F].any(1)
a=np.where(fm&((N0*N1).sum(1)<0))[0];b=np.where(fm&((N1*sref).sum(1)<0))[0];c=np.where(fm&((N0*sref).sum(1)<0))[0]
print('flip vs base',a,'src-inverted in base?',[(N0[i]@sref[i])<0 for i in a]);print('inverted now',b,'inverted in base',c)
for i in b: print(i,'area mm2',np.linalg.norm(N1[i])/2*1e6,'pos',V[F[i]].mean(0))
