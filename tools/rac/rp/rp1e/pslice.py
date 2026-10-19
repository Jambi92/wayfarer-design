import numpy as np, matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt, sys
sys.path.insert(0,'/home/claude/stc/rp1e')
from earsl import slice_loops
def tslice(V,F,axis,val):
    d=V[:,axis]-val; s=np.sign(d[F]); T=F[(s.min(1)<0)&(s.max(1)>0)]; segs=[]
    for t in T:
        pts=[]
        for i,j in ((0,1),(1,2),(2,0)):
            a,b=t[i],t[j]
            if d[a]*d[b]<0: al=d[a]/(d[a]-d[b]); pts.append(V[a]+(V[b]-V[a])*al)
        if len(pts)==2: segs.append(pts)
    return np.array(segs)
specs=eval(sys.argv[1]); prods=sys.argv[2].split(','); out=sys.argv[3]
fig,ax=plt.subplots(1,len(specs),figsize=(7*len(specs),7)); ax=np.atleast_1d(ax)
cols=['r','b','g','m']
for a,(axis,val,lim) in zip(ax,specs):
    i,j=[k for k in range(3) if k!=axis]
    for L,c in slice_loops(axis,val): a.plot(L[:,i],L[:,j],'k-',lw=1.2)
    for pi,p in enumerate(prods):
        z=np.load(p); V=z['V'].copy(); V[:,1]*=-1; F=z['F']
        m=np.all((V[:,[i,j]]>[lim[0]-1,lim[2]-1])&(V[:,[i,j]]<[lim[1]+1,lim[3]+1]),axis=1)
        keep=m[F].all(1); S=tslice(V,F[keep],axis,val)
        for s in S: a.plot(s[:,i],s[:,j],cols[pi]+'-',lw=0.6)
    a.set_xlim(lim[0],lim[1]); a.set_ylim(lim[2],lim[3]); a.set_aspect('equal'); a.grid(alpha=.3); a.set_title('%d=%g  %s'%(axis,val,prods))
plt.tight_layout(); plt.savefig(out,dpi=70)
