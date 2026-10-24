# ext_clean.py IN OUT : remove generator micro-noise (pits, specks) on hands and feet before the anatomy sculpt (fine band only, mass kept)
import sys, numpy as np, igl, json
from scipy.sparse.linalg import factorized
sys.path.insert(0,'/tmp/claude-0/src3d/tools'); sys.path.insert(0,'/tmp/claude-0/rp2/tools')
from lowpass import lowpass
from cotfair import ss
d=np.load(sys.argv[1]); X=d['V'].astype(float); F=d['Q'].astype(np.int64); n=len(X); Q4=np.c_[F,F[:,0]]
g=json.loads(sys.argv[3]) if len(sys.argv)>3 else {}
L=igl.cotmatrix(X,F); M=igl.massmatrix(X,F,igl.MASSMATRIX_TYPE_BARYCENTRIC)
def sm(lam):
    s=factorized((M-lam*L).tocsc()); B=M@X; return np.stack([s(B[:,j]) for j in range(3)],1)
S1=sm(g.get('l1',0.15)); S2=sm(g.get('l2',1.5))
b1=X-S1; b1=b1-lowpass(Q4,n,b1,g.get('lp1',8.0)); b2=S1-S2; b2=b2-lowpass(Q4,n,b2,30.0)
x,f,z=X.T; ax=np.abs(x)
w=np.maximum(ss((ax-21)/1.5)*ss((110-z)/2)*ss((z-62)/2), ss((14-z)/2))
Y=X-(w*g.get('k1',0.85))[:,None]*b1-(w*g.get('k2',0.35))[:,None]*b2
out={k:d[k] for k in d.files}; out['V']=Y; out['ext_clean_move_mm']=np.linalg.norm(Y-X,axis=1)*10
np.savez(sys.argv[2],**out); print('clean max mm %.2f p95 %.2f'%(out['ext_clean_move_mm'].max(),np.percentile(out['ext_clean_move_mm'][w>0.5],95)))
