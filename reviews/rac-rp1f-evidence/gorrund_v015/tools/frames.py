# per-digit distal frames from the v014 production (blender cm): tip T (geodesic farthest from the palm boundary), distal axis e1
import numpy as np, json, scipy.sparse as sp
from scipy.sparse.csgraph import dijkstra
z=np.load('/home/claude/wayfarer-design/reviews/rac-rp1e-evidence/designs/design_v014_production_L4.npz'); V=z['V']*np.array([1,-1,1]); Q=z['Q']
vcol=np.load('/tmp/claude-0/rp1f/vcol.npy')
E=np.vstack([Q[:,[i,(i+1)%4]] for i in range(4)])
out={}
hands={'L':dict(digits=[17,18,19,20],palm=3,up=[1,0,0]),'R':dict(digits=[21,22,23,24],palm=12,up=[-1,0,0])}
for h,H in hands.items():
    for c in H['digits']:
        m=vcol==c; idx=np.where(m)[0]; loc=-np.ones(len(V),int); loc[idx]=np.arange(len(idx))
        e=E[m[E[:,0]]&m[E[:,1]]]; w=np.linalg.norm(V[e[:,0]]-V[e[:,1]],axis=1)
        G=sp.coo_matrix((w,(loc[e[:,0]],loc[e[:,1]])),shape=(len(idx),len(idx))).tocsr()
        bnd=np.unique(E[(m[E[:,0]])&(vcol[E[:,1]]==H['palm'])][:,0])
        if len(bnd)==0: bnd=np.unique(E[m[E[:,0]]&~m[E[:,1]]][:,0])
        d=dijkstra(G,indices=loc[bnd],min_only=True); D=d.max(); T=idx[np.argmax(d)]
        ring=idx[(d>D-1.6)&(d<D-0.9)]; e1=V[T]-V[ring].mean(0); e1/=np.linalg.norm(e1)
        out['%s_%d'%(h,c)]=dict(tip=V[T].round(3).tolist(),tip_vid=int(T),axis=e1.round(3).tolist(),length_cm=round(float(D),2),up=H['up'])
        print(h,c,out['%s_%d'%(h,c)])
json.dump(out,open('/tmp/claude-0/rp1f/frames.json','w'),indent=1)
