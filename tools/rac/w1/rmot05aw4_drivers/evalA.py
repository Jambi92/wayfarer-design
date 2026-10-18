import numpy as np,sys; sys.path.insert(0,'/home/claude/aw1'); import aw1lib as L
PL=np.load('plates.npy',allow_pickle=True).item()
H=np.zeros(len(L.V0)); up=np.ones(len(L.V0))
for P in PL.values(): H=np.maximum(H,P['w'])
X0=np.load('C3_VF.npz')['V']; n0=L.vnormals(X0)
def ang(X):
    vn=L.vnormals(X); s=vn.copy()
    for _ in range(4): s=L.Avg@s
    s/=np.linalg.norm(s,axis=1)[:,None]; return np.degrees(np.arccos(np.clip((vn*s).sum(1),-1,1)))
def conc(X): vn=L.vnormals(X); return ((L.Avg@X-X)*vn).sum(1)*1000
edge=(H>0.03)&(H<0.7)
core=H>0.9
for f in sys.argv[1:]:
    X=np.load(f)['V']; a=ang(X); c=conc(X); dz=((X-X0)*n0).sum(1)*1000
    print(f,'edge ang p90/p99 %.1f/%.1f  conc p99 %.4f  core drop mean/max %.3f/%.3f mm'%(*np.percentile(a[edge],[90,99]),np.percentile(c[edge],99),-dz[core].mean(),-dz[core].min()))
