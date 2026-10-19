import numpy as np, sys, matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
w=np.load('/home/claude/stc/rp1/weld.npz'); S=w['V']; F=w['F']
ax_i=int(sys.argv[1]); vals=[float(x) for x in sys.argv[2].split(',')]; outp=sys.argv[3]; sg=float(sys.argv[4]) if len(sys.argv)>4 else 1
oth=[k for k in range(3) if k!=ax_i]
n=len(vals); c=4; r=(n+c-1)//c
fig,axs=plt.subplots(r,c,figsize=(5*c,5*r)); axs=np.array(axs).ravel()
for a,val in zip(axs,vals):
    d=S[:,ax_i]-val; sgn=np.sign(d[F]); T=F[(sgn.min(1)<0)&(sgn.max(1)>0)]
    segs=[]
    for t in T:
        q=[]
        for i,j in ((0,1),(1,2),(2,0)):
            if d[t[i]]*d[t[j]]<0: al=d[t[i]]/(d[t[i]]-d[t[j]]); q.append(S[t[i]]+(S[t[j]]-S[t[i]])*al)
        if len(q)==2: segs.append(q)
    for p,q in segs:
        if p[2]>183 and p[1]<-30: a.plot([p[oth[0]],q[oth[0]]],[p[oth[1]],q[oth[1]]],'k-',lw=0.8)
    a.set_aspect('equal'); a.set_title('%s=%.1f'%('xyz'[ax_i],val)); a.grid(alpha=0.3)
plt.tight_layout(); plt.savefig(outp,dpi=60)
