import numpy as np, sys, matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
from matplotlib.collections import PolyCollection
box=np.array([float(v) for v in sys.argv[1].split(',')]).reshape(3,2); dp=sys.argv[2]; out=sys.argv[3]; vmax=float(sys.argv[4]) if len(sys.argv)>4 else 5
w=np.load('/home/claude/stc/rp1/weld.npz'); V=w['V'].astype(float); Q=w['F']; d=np.load(dp)
c=V[Q].mean(1); m=((c>box[:,0])&(c<box[:,1])).all(1); idx=np.where(m)[0]; dv=d[Q[idx]].mean(1)
views=[('front (from -Y)',np.array([0,1,0]),(0,2),False),('side (from +X)',np.array([-1,0,0]),(1,2),True),('top (from +Z)',np.array([0,0,-1]),(0,1),False),('3/4',None,None,False)]
fig,axs=plt.subplots(1,4,figsize=(28,8)); L=np.array([0.3,-0.6,0.7]); L/=np.linalg.norm(L); cm=plt.get_cmap('jet')
for a,(nm,vd,ij,inv) in zip(axs,views):
    if vd is None:
        th=np.radians(-35); ph=np.radians(20)
        Rz=np.array([[np.cos(th),-np.sin(th),0],[np.sin(th),np.cos(th),0],[0,0,1]]); Rx=np.array([[1,0,0],[0,np.cos(ph),-np.sin(ph)],[0,np.sin(ph),np.cos(ph)]])
        W=(Rx@Rz@V.T).T; vd=np.array([0,1,0]); ij=(0,2)
    else: W=V
    cw=W[Q[idx]].mean(1); o=np.argsort(-(cw@vd))
    polys=[];cols=[]
    for k,dd in zip(idx[o],dv[o]):
        p=W[Q[k]]; n=np.cross(p[1]-p[0],p[2]-p[0]); n/=np.linalg.norm(n)+1e-12; sh=0.45+0.55*abs(n@L)
        c0=np.array(cm(min(dd/vmax,1))[:3]); polys.append(p[:,list(ij)]); cols.append(tuple(c0*sh))
    a.add_collection(PolyCollection(polys,facecolors=cols,edgecolors='none'))
    P=np.vstack(polys); a.set_xlim(P[:,0].min(),P[:,0].max()); a.set_ylim(P[:,1].min(),P[:,1].max())
    if inv: a.invert_xaxis()
    a.set_aspect('equal'); a.set_title(nm+' (dev, blue 0 → red %.1f mm)'%vmax)
plt.savefig(out,dpi=55,bbox_inches='tight')
