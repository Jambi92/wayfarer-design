import sys,json,numpy as np, matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
sys.path.insert(0,'/home/claude/stc/rp1e')
from planeslice import plane_loops
from cleftfloor import trace
S=json.load(open(sys.argv[1])); j=int(sys.argv[2]); out=sys.argv[3]
Lp=np.array(S['line'],float); seg=np.linalg.norm(np.diff(Lp,axis=0),axis=1); s=np.r_[0,np.cumsum(seg)]; C=S['cols']
o=np.array(S['out'],float); o/=np.linalg.norm(o)
u=(j+0.5)/C*s[-1]; k=int(np.clip(np.searchsorted(s,u),1,len(s)-1)); al=(u-s[k-1])/seg[k-1]; f0=Lp[k-1]+(Lp[k]-Lp[k-1])*al; t=(Lp[k]-Lp[k-1])/seg[k-1]
e2=-(o-(o@t)*t); e2/=np.linalg.norm(e2); e1=np.cross(t,e2)
L=[P for P,cl in plane_loops(f0,t) if cl and np.linalg.norm(P-f0,axis=1).min()<S.get('rad',4.0)]
L2=[np.c_[(P-f0)@e1,(P-f0)@e2] for P in L]
pth=trace(0.0,(S.get('startx',0.0),-S.get('start',0.8)),(0,1),loops2d=L2); print('path',None if pth is None else len(pth))
for l in L2: plt.plot(*np.vstack([l,l[:1]]).T,'k-')
plt.plot(0,-S.get('start',0.8),'ro'); plt.plot(0,0,'gx')
if pth: P=np.array([p for p,w in pth]); plt.plot(P[:,0],P[:,1],'b.-')
plt.gca().set_aspect('equal'); plt.xlim(-1.5,1.5); plt.ylim(-1.5,1.5); plt.grid(); plt.savefig(out,dpi=70)
