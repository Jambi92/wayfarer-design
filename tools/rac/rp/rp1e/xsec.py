import numpy as np, sys, matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
# sections of source (black) and a production mesh (red) by planes axis=const
ax_=int(sys.argv[1]); vals=[float(v) for v in sys.argv[2].split(',')]; box=[float(v) for v in sys.argv[3].split(',')]; prod=sys.argv[4]; out=sys.argv[5]
w=np.load('/home/claude/stc/rp1/weld.npz'); V=w['V'].astype(float); F=w['F']
P=np.load(prod); PV=P['V']*np.array([1,-1,1]); PF=P['F']
oth=[i for i in range(3) if i!=ax_]
def sec(V,F,c,col,a):
    d=V[:,ax_]-c; m=(np.sign(d[F]).min(1)<0)&(np.sign(d[F]).max(1)>0); T=F[m]
    for t in T:
        pts=[]
        for i,j in ((0,1),(1,2),(2,0)):
            if d[t[i]]*d[t[j]]<0: u=d[t[i]]/(d[t[i]]-d[t[j]]); pts.append(V[t[i]]+(V[t[j]]-V[t[i]])*u)
        if len(pts)==2:
            p=np.array(pts)
            if (p[:,oth[0]]>box[0]).all() and (p[:,oth[0]]<box[1]).all() and (p[:,oth[1]]>box[2]).all() and (p[:,oth[1]]<box[3]).all():
                a.plot(p[:,oth[0]],p[:,oth[1]],c=col,lw=1)
n=len(vals); fig,ax=plt.subplots(1,n,figsize=(8*n,8))
for a,c in zip(np.atleast_1d(ax),vals):
    sel=lambda X:(X[:,oth[0]]>box[0]-2)&(X[:,oth[0]]<box[1]+2)&(X[:,oth[1]]>box[2]-2)&(X[:,oth[1]]<box[3]+2)
    m1=sel(V); F1=F[m1[F].all(1)]; sec(V,F1,c,'k',a)
    m2=sel(PV); F2=PF[m2[PF].all(1)]; sec(PV,F2,c,'r',a)
    a.set_aspect('equal'); a.set_title('axis %d = %.1f'%(ax_,c)); a.grid(True); a.set_xlim(box[0],box[1]); a.set_ylim(box[2],box[3])
plt.savefig(out,dpi=45,bbox_inches='tight')
