import numpy as np, sys, matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
# horizontal sections: source black, production (analysis npz) red, cage (Blender npz) green
prod=sys.argv[1]; cg=sys.argv[2]; zs=[float(x) for x in sys.argv[3].split(',')]; box=[float(x) for x in sys.argv[4].split(',')]; out=sys.argv[5]
w=np.load('/home/claude/stc/rp1/weld.npz'); V=w['V'].astype(float); F=w['F']
P=np.load(prod); PV=P['V']*np.array([1,-1,1]); PQ=P['Q']
z=np.load(cg); C=z['V']; CF=z['F']
def segs(V,F,z0,a,col,lw):
    sel=(V[:,0]>box[0]-3)&(V[:,0]<box[1]+3)&(V[:,1]>box[2]-3)&(V[:,1]<box[3]+3)&(np.abs(V[:,2]-z0)<6)
    F=F[np.array([sel[f[f>=0]].all() for f in F])]
    d=V[:,2]-z0
    for f in F:
        f=f[f>=0]; n=len(f); pts=[]
        for i in range(n):
            a_,b_=f[i],f[(i+1)%n]
            if d[a_]*d[b_]<0: u=d[a_]/(d[a_]-d[b_]); pts.append(V[a_]+(V[b_]-V[a_])*u)
        if len(pts)>=2: p=np.array(pts[:2]); a.plot(p[:,0],p[:,1],c=col,lw=lw)
fig,ax=plt.subplots(1,len(zs),figsize=(8*len(zs),8))
for a,z0 in zip(np.atleast_1d(ax),zs):
    segs(V,F,z0,a,'k',1); segs(PV,PQ,z0,a,'r',1.2); segs(C,CF,z0,a,'g',2)
    a.set_xlim(box[0],box[1]); a.set_ylim(box[2],box[3]); a.set_aspect('equal'); a.grid(True); a.set_title('z=%.1f'%z0)
plt.savefig(out,dpi=40,bbox_inches='tight')
