# neutralize.py IN OUT : band-pass attenuation of tertiary detail (fine: skin/veins/striation; medium: etched muscle separations), mass preserved
import sys, numpy as np, igl, scipy.sparse as sp, json
from scipy.sparse.linalg import factorized
sys.path.insert(0,'/tmp/claude-0/src3d/tools'); sys.path.insert(0,'/tmp/claude-0/rp2/tools')
from lowpass import lowpass
from cotfair import ss
d=np.load(sys.argv[1]); X=d['V'].astype(float); F=d['Q'].astype(np.int64); Q4=np.c_[F,F[:,0]]; n=len(X)
p=json.loads(sys.argv[3]) if len(sys.argv)>3 else {}
LF=p.get('lam_fine',0.4); LM=p.get('lam_med',4.0); FL=p.get('field_lam',100.0)
L=igl.cotmatrix(X,F); M=igl.massmatrix(X,F,igl.MASSMATRIX_TYPE_BARYCENTRIC)
def smooth(lam):
    s=factorized((M-lam*L).tocsc()); B=M@X; return np.stack([s(B[:,j]) for j in range(3)],1)
def bandpass(lam):
    S=X-smooth(lam); return S-lowpass(Q4,n,S,FL)
bf=bandpass(LF); bm=bandpass(LM)-bf
x,f,z=X.T; ax=np.abs(x)
face=ss((z-189)/3)*(1-ss((ax-9)/3))
ear=ss((ax-6.0)/1.5)*ss((z-193)/2)*(1-ss((z-214)/2))
hand=ss((ax-21)/2)*ss((114-z)/3)
foot=ss((12-z)/3)
ear=np.maximum(ear,ss((z-189)/3)*ss((ax-5.5)/1.5))
body=np.clip(1-face-ear-hand-foot,0,1)
af=p.get('af_body',0.35)*body+p.get('af_face',0.6)*face+1.0*ear+p.get('af_hand',0.35)*hand+p.get('af_foot',1.0)*foot
am=p.get('am_body',0.5)*body+1.0*face+1.0*ear+p.get('am_hand',0.9)*hand+1.0*foot
keep=np.load(p['keep']) if p.get('keep') else np.zeros(n)
af=af+(1-af)*keep; am=am+(1-am)*keep
Y=X-(1-af)[:,None]*bf-(1-am)[:,None]*bm
np.savez(sys.argv[2],V=Y,Q=F)
dd=np.linalg.norm(Y-X,axis=1); print('neutralize: mean %.3f p95 %.3f max %.3f cm'%(dd.mean(),np.percentile(dd,95),dd.max()))
# volume check
def vol(V): T=V[F]; return np.einsum('ij,ij->i',T[:,0],np.cross(T[:,1],T[:,2])).sum()/6/1000
print('volume L before %.2f after %.2f'%(vol(X),vol(Y)))
