import numpy as np, sys, matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
from matplotlib.collections import PolyCollection
# render a mesh (source weld or sim npz) in a box from 4 views; Blender frame
mp=sys.argv[1]; box=np.array([float(v) for v in sys.argv[2].split(',')]).reshape(3,2); out=sys.argv[3]
if mp=='src':
    w=np.load('/home/claude/stc/rp1/weld.npz'); V=w['V'].astype(float); Q=w['F']
else:
    z=np.load(mp); V=z['V']*np.array([1,-1,1]); Q=z['Q'] if 'Q' in z.files else z['F']
Q=np.asarray(Q); c=np.array([V[q[q>=0]].mean(0) for q in Q]) if Q.shape[1]==4 else V[Q].mean(1)
m=((c>box[:,0])&(c<box[:,1])).all(1); idx=np.where(m)[0]
views=[('front (from -Y)',np.array([0,1,0]),(0,2),False),('side (from +X)',np.array([-1,0,0]),(1,2),True),('top (from +Z)',np.array([0,0,-1]),(0,1),False),('3/4',None,None,False)]
fig,axs=plt.subplots(1,4,figsize=(28,8)); L=np.array([0.3,-0.6,0.7]); L/=np.linalg.norm(L)
for a,(nm,vd,ij,inv) in zip(axs,views):
    if vd is None:
        # oblique: rotate about z by -35deg, tilt 25deg
        th=np.radians(-35); ph=np.radians(20)
        Rz=np.array([[np.cos(th),-np.sin(th),0],[np.sin(th),np.cos(th),0],[0,0,1]]); Rx=np.array([[1,0,0],[0,np.cos(ph),-np.sin(ph)],[0,np.sin(ph),np.cos(ph)]])
        W=(Rx@Rz@V.T).T; vd=np.array([0,1,0]); ij=(0,2)
    else: W=V
    cw=np.array([W[q[q>=0]].mean(0) for q in Q[idx]]) if Q.shape[1]==4 else W[Q[idx]].mean(1)
    order=idx[np.argsort(-(cw@vd))]
    polys=[];cols=[]
    for k in order:
        q=Q[k][Q[k]>=0]; p=W[q]; n=np.cross(p[1]-p[0],p[2]-p[0]); n/=np.linalg.norm(n)+1e-12
        sh=0.3+0.7*abs(n@L); polys.append(p[:,list(ij)]); cols.append((sh,sh,sh*0.95))
    a.add_collection(PolyCollection(polys,facecolors=cols,edgecolors='none'))
    P=np.vstack(polys); a.set_xlim(P[:,0].min(),P[:,0].max()); a.set_ylim(P[:,1].min(),P[:,1].max())
    if inv: a.invert_xaxis()
    a.set_aspect('equal'); a.set_title(nm); a.grid(alpha=.2)
plt.savefig(out,dpi=55,bbox_inches='tight')
