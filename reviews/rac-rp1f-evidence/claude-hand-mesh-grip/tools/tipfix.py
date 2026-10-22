# tipfix.py KEY : remove near-degenerate quads (3D area / edge) of a draped patch by 1-ring re-placement inside the domain
import sys,numpy as np; sys.path.insert(0,'/tmp/claude-0/hand/tools'); from drape import *; from patches import boundary_loops
k=sys.argv[1]; z=dict(np.load('/tmp/claude-0/hand/drape_%s.npz'%k)); P2=z['P2']; Q=z['Ql']
D=Domain(z['Xl'],z['Fl'],z['U']); sgn=np.sign(np.median(orient2(P2,Q)))
bl=np.array(boundary_loops(Q)[0][0]); fixed=np.zeros(len(P2),bool); fixed[bl]=True
rng=np.random.default_rng(1)
vq=[[] for _ in range(len(P2))]
for qi,q in enumerate(Q):
    for v in q: vq[v].append(qi)
def quality(X,qs):
    P=X[Q[qs]]; a=np.linalg.norm(np.cross(P[:,1]-P[:,0],P[:,3]-P[:,0]),axis=1)+np.linalg.norm(np.cross(P[:,1]-P[:,2],P[:,3]-P[:,2]),axis=1)
    e=np.linalg.norm(P-np.roll(P,1,1),axis=2).min(1); return np.minimum(a/2/1e-6, e/1e-3).min()   # normalized: 1 = 1e-6 cm2 area / 1e-3 cm edge
for rep in range(6):
    X=D.lift(P2,D.locate(P2))
    P=X[Q]; a=np.linalg.norm(np.cross(P[:,1]-P[:,0],P[:,3]-P[:,0]),axis=1); e=np.linalg.norm(P-np.roll(P,1,1),axis=2).min(1)
    bad=np.where((a<1e-6)|(e<1e-3))[0]
    print('rep',rep,'near-degenerate quads',len(bad),'min area %.2e min edge mm %.4f'%(a.min(),e.min()*10))
    if len(bad)==0: break
    for v in np.unique(Q[bad]):
        if fixed[v]: continue
        st=np.array(vq[v]); ring=np.unique(Q[st]); ring=ring[ring!=v]
        lo=P2[ring].min(0); hi=P2[ring].max(0)
        cands=np.vstack([P2[v],P2[ring].mean(0),lo+(hi-lo)*rng.random((300,2))])
        best=None; old=P2[v].copy()
        for c in cands:
            P2[v]=c
            if (orient2(P2,Q[st])*sgn).min()<=1e-14: continue
            Xs=X.copy(); Xs[v]=D.lift(c[None],D.locate(c[None]))[0]; qv=quality(Xs,st)
            if best is None or qv>best[0]: best=(qv,c.copy())
        P2[v]=best[1] if best is not None else old
X=D.lift(P2,D.locate(P2)); print('folds',int((orient2(P2,Q)*sgn<=1e-14).sum()))
z['P2']=P2; z['X3']=X; np.savez('/tmp/claude-0/hand/drape_%s.npz'%k,**z)
