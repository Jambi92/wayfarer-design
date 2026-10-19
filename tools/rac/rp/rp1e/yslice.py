import numpy as np,sys
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
w=np.load('/home/claude/stc/rp1/weld.npz'); S=w['V'].astype(float); F=w['F']
ax=int(sys.argv[1]); val=float(sys.argv[2]); box=[float(x) for x in sys.argv[3].split(',')]; out=sys.argv[4]
cage=np.load(sys.argv[5]) if len(sys.argv)>5 else None
d=S[:,ax]-val; segs=[]
T=F[(np.sign(d[F]).min(1)<0)&(np.sign(d[F]).max(1)>0)]
for t in T:
    p=[]
    for a,b in ((0,1),(1,2),(2,0)):
        if d[t[a]]*d[t[b]]<0: s=d[t[a]]/(d[t[a]]-d[t[b]]); p.append(S[t[a]]+s*(S[t[b]]-S[t[a]]))
    if len(p)==2: segs.append(p)
o=[i for i in range(3) if i!=ax]
plt.figure(figsize=(8,8))
for p,q in segs:
    if box[0]<p[o[0]]<box[1] and box[2]<p[o[1]]<box[3]: plt.plot([p[o[0]],q[o[0]]],[p[o[1]],q[o[1]]],'k-',lw=0.7)
if cage is not None:
    V=cage['V']; m=np.where((abs(V[:,ax]-val)<float(sys.argv[6]))&(V[:,o[0]]>box[0])&(V[:,o[0]]<box[1])&(V[:,o[1]]>box[2])&(V[:,o[1]]<box[3]))[0]
    plt.plot(V[m,o[0]],V[m,o[1]],'r.')
    for i in m: plt.text(V[i,o[0]],V[i,o[1]],str(i),fontsize=6,color='r')
plt.axis('equal'); plt.xlim(box[0],box[1]); plt.ylim(box[2],box[3]); plt.grid(alpha=.3); plt.savefig(out,dpi=110)
