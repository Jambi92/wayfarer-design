# secsim.py axis val box out sim1.npz [sim2.npz ...] : source (black) + sim L-meshes (colours) sections; sim y flipped
import numpy as np,sys
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
ax=int(sys.argv[1]); val=float(sys.argv[2]); box=[float(x) for x in sys.argv[3].split(',')]; out=sys.argv[4]
def sec(V,F):
    d=V[:,ax]-val; s=np.sign(d[F]); T=F[(s.min(1)<0)&(s.max(1)>0)]; segs=[]
    for t in T:
        p=[]
        for a,b in ((0,1),(1,2),(2,0)):
            if d[t[a]]*d[t[b]]<0: u=d[t[a]]/(d[t[a]]-d[t[b]]); p.append(V[t[a]]+u*(V[t[b]]-V[t[a]]))
        if len(p)==2: segs.append(p)
    return segs
o=[i for i in range(3) if i!=ax]
w=np.load('/home/claude/stc/rp1/weld.npz'); plt.figure(figsize=(9,9))
for p,q in sec(w['V'].astype(float),w['F']): plt.plot([p[o[0]],q[o[0]]],[p[o[1]],q[o[1]]],'k-',lw=1.2)
cs=['r','b','g','m']
for k,f in enumerate(sys.argv[5:]):
    z=np.load(f); V=z['V'].copy(); V[:,1]*=-1
    for p,q in sec(V,z['F']): plt.plot([p[o[0]],q[o[0]]],[p[o[1]],q[o[1]]],cs[k]+'-',lw=0.6)
plt.axis('scaled'); plt.xlim(box[0],box[1]); plt.ylim(box[2],box[3]); plt.grid(alpha=.3); plt.savefig(out,dpi=100)
