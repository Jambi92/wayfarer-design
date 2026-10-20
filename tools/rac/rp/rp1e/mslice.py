# mslice.py "[(axis,val,(xmin,xmax,ymin,ymax)),...]" PROD[,PROD2] MASKFACES.npy[,..] OUT : source sections (black; mask faces magenta) + product (red)
import numpy as np, sys; sys.path.insert(0,'/home/claude/stc/rp1e'); from ploops import plane_loops
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
specs=eval(sys.argv[1]); prods=[p for p in sys.argv[2].split(',') if p!='-']; masks=[np.load(m) for m in sys.argv[3].split(',') if m!='-']; out=sys.argv[4]
mk=set(np.concatenate(masks).tolist()) if masks else set()
PR=[]
for p in prods:
    z=np.load(p); V=z['V'].copy(); V[:,1]*=-1; PR.append((V,z['F'].astype(np.int64)))
nc=min(4,len(specs)); nr=(len(specs)+nc-1)//nc; fig,ax=plt.subplots(nr,nc,figsize=(6*nc,6*nr)); ax=np.atleast_1d(ax).ravel()
for a,(axis,val,lim) in zip(ax,specs):
    n=np.zeros(3); n[axis]=1; i,j=[k for k in range(3) if k!=axis]
    cen=np.zeros(3); cen[axis]=val; cen[i]=(lim[0]+lim[1])/2; cen[j]=(lim[2]+lim[3])/2; r=max(lim[1]-lim[0],lim[3]-lim[2])
    for l in plane_loops(cen,n,cen,r):
        P=l['pts']; fm=np.array([f in mk for f in l['faces']])
        for k in range(len(l['faces'])):
            a.plot(P[k:k+2,i],P[k:k+2,j],'m-' if fm[k] else 'k-',lw=2.2 if fm[k] else 1.2)
    for (V,F),c in zip(PR,'rbg'):
        sel=np.linalg.norm(V[F].mean(1)-cen,axis=1)<r
        for l in plane_loops(cen,n,cen,r,V=V,F=F[sel]):
            a.plot(l['pts'][:,i],l['pts'][:,j],c+'-',lw=0.7)
    a.set_xlim(lim[0],lim[1]); a.set_ylim(lim[2],lim[3]); a.set_aspect('equal'); a.grid(alpha=.3); a.set_title('%s=%g'%('xyz'[axis],val))
plt.tight_layout(); plt.savefig(out,dpi=60)
