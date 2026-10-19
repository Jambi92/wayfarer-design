import numpy as np, sys, json, matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
s=sys.argv[1]; cg=sys.argv[2]; zs=[float(x) for x in sys.argv[3].split(',')]; box=[float(x) for x in sys.argv[4].split(',')]; out=sys.argv[5]
w=np.load('/home/claude/stc/rp1/weld.npz'); V=w['V'].astype(float); F=w['F']
z=np.load(cg); C=z['V']; CF=z['F']
def secsegs(V,F,z0):
    d=V[:,2]-z0; out=[]
    for f in F:
        f=f[f>=0]; n=len(f); pts=[]
        for i in range(n):
            a,b=f[i],f[(i+1)%n]
            if d[a]*d[b]<0: u=d[a]/(d[a]-d[b]); pts.append(V[a]+(V[b]-V[a])*u)
        if len(pts)>=2: out.append(pts[:2])
    return out
sel=(V[:,0]>box[0]-3)&(V[:,0]<box[1]+3)&(V[:,1]>box[2]-3)&(V[:,1]<box[3]+3)
Fs=F[sel[F].all(1)]
fig,ax=plt.subplots(1,len(zs),figsize=(8*len(zs),8))
for a,z0 in zip(np.atleast_1d(ax),zs):
    for p in secsegs(V,Fs[(np.abs(V[Fs][:,:,2]-z0).min(1)<2)],z0): p=np.array(p); a.plot(p[:,0],p[:,1],c='k',lw=1)
    for p in secsegs(C,CF,z0): p=np.array(p); a.plot(p[:,0],p[:,1],c='r',lw=2)
    near=np.abs(C[:,2]-z0)<1.0; a.plot(C[near,0],C[near,1],'o',c='orange',ms=4)
    a.set_xlim(box[0],box[1]); a.set_ylim(box[2],box[3]); a.set_aspect('equal'); a.grid(True); a.set_title('z=%.1f'%z0)
plt.savefig(out,dpi=40,bbox_inches='tight')
