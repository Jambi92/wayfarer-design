# sl3.py AXIS VALS BOX OUT [mesh.npz:color ...]  source (black) + meshes sliced
import numpy as np, sys, matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
from earsl import slice_loops
def mslice(V,F,ax_i,val):
    d=V[:,ax_i]-val; F=np.asarray(F)
    if F.shape[1]==4:
        q=F[F[:,3]>=0]; t=F[F[:,3]<0][:,:3]; T=np.vstack([q[:,[0,1,2]],q[:,[0,2,3]],t])
    else: T=F
    sg=np.sign(d[T]); T=T[(sg.min(1)<0)&(sg.max(1)>0)]; segs=[]
    for tri in T:
        qq=[]
        for i,j in ((0,1),(1,2),(2,0)):
            a,b=tri[i],tri[j]
            if d[a]*d[b]<0: al=d[a]/(d[a]-d[b]); qq.append(V[a]+(V[b]-V[a])*al)
        if len(qq)==2: segs.append(qq)
    return segs
ax_i=int(sys.argv[1]); vals=[float(x) for x in sys.argv[2].split(',')]; box=[float(x) for x in sys.argv[3].split(',')]; outp=sys.argv[4]
meshes=[]
for a in sys.argv[5:]:
    pp=a.split(':'); p,c=pp[0],pp[1]; z=np.load(p); V=z['V'].copy()
    if len(pp)>2: V[:,1]*=-1
    meshes.append((V,z['Q'] if 'Q' in z.files else z['F'],c))
oth=[k for k in range(3) if k!=ax_i]; n=len(vals); c=4; r=(n+c-1)//c
fig,axs=plt.subplots(r,c,figsize=(5*c,5*r)); axs=np.array(axs).ravel()
for a,val in zip(axs,vals):
    for P,cl in slice_loops(ax_i,val): a.plot(P[:,oth[0]],P[:,oth[1]],'k-',lw=0.8)
    for V,F,col in meshes:
        bx=np.array(box); 
        for p,q in mslice(V,F,ax_i,val): a.plot([p[oth[0]],q[oth[0]]],[p[oth[1]],q[oth[1]]],col+'-',lw=0.8)
    a.set_xlim(box[0],box[1]); a.set_ylim(box[2],box[3]); a.set_aspect('equal'); a.set_title('%s=%.1f'%('xyz'[ax_i],val)); a.grid(alpha=.3)
plt.tight_layout(); plt.savefig(outp,dpi=60)
