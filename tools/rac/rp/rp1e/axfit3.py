"""Usage: python3 axfit3.py CAGE_IN CAGECOL_IN TPREFIX OUT [INSET ITERS HOPS] SIDES...  (uses axloop_SIDE.json, ccurve_SIDE.npy)"""
import numpy as np, sys, json, igl, networkx as nx
a=sys.argv[1:]; cin,colin,tp,out=a[:4]; INSET=float(a[4]); ITERS=int(a[5]); HOPS=int(a[6]); sides=a[7:]
z=np.load(cin); V=z['V'].astype(float).copy(); V0=V.copy(); F=z['F']; cc=np.load(colin).copy()
import collections
adj=collections.defaultdict(set)
for f in F:
    f=f[f>=0]
    for j in range(len(f)): p,q=int(f[j]),int(f[(j+1)%len(f)]); adj[p].add(q); adj[q].add(p)
from scipy.spatial import cKDTree
mv=json.load(open('/home/claude/wayfarer-design/reviews/rac-rp1e-evidence/axilla_ui_moves_e30.json'))
P=np.array(list(mv.values())); _,Mi=cKDTree(V0).query(P)
free=set(); fixed=set()
for s in sides:
    sg=-1 if s=='R' else 1
    L=json.load(open('axloop_%s.json'%s)); P1=L['P1']; loop=L['loop']; Q=np.load('ccurve_%s.npy'%s)
    # snap P1 by arc-length proportion
    seg=np.r_[0,np.cumsum(np.linalg.norm(np.diff(V0[P1],axis=0),axis=1))]; t=seg/seg[-1]
    cl=np.r_[0,np.cumsum(np.linalg.norm(np.diff(Q,axis=0),axis=1))]; cl/=cl[-1]
    for v,tt in zip(P1,t): k=int(np.argmin(abs(cl-tt))); V[v]=Q[k]
    fixed|=set(loop)
    # sides by flood
    G=nx.Graph()
    for i in adj:
        for j in adj[i]:
            if i<j and i not in set(loop) and j not in set(loop): G.add_edge(i,j)
    # arm component = the smaller one touching the loop (arm+hand); trunk = the big one
    comps=sorted(nx.connected_components(G),key=len)
    arm=comps[0] if len(comps)>1 else set()
    near=set(P1)
    for h in range(HOPS): near|=set(n for v in near for n in adj[v])
    for v in near:
        if v in set(loop) or cc[v] not in (1,2): continue
        cc[v]=2 if v in arm else 1
        free.add(v)
    free|=set(int(i) for i in Mi if V0[i,0]*sg>0 and int(i) not in set(loop))
    print(s,'P1',len(P1),'loop',len(loop),'arm comp',len(arm),'near',len(near))
free=np.array(sorted(free-fixed),int)
TG={c:(lambda t:(t['V'].astype(float),t['F'].astype(np.int64)))(np.load('%s_c%d.npz'%(tp,c))) for c in (1,2)}
def place():
    for c,(TV,TF) in TG.items():
        idx=free[cc[free]==c]
        if not len(idx): continue
        S2,I,C=igl.point_mesh_squared_distance(V[idx],TV,TF)
        T3=TV[TF[I]]; N=np.cross(T3[:,1]-T3[:,0],T3[:,2]-T3[:,0]); N/=np.linalg.norm(N,axis=1)[:,None]
        V[idx]=C-INSET*N
for it in range(ITERS):
    place(); Vn=V.copy()
    for i in free: Vn[i]=0.5*V[i]+0.5*V[list(adj[i])].mean(0)
    V[:]=Vn
place()
np.savez_compressed(out,V=V,F=F); np.save(out.replace('.npz','_col.npy'),cc)
sh=np.linalg.norm(V-V0,axis=1); print('free',len(free),'moved >1mm',int((sh>0.1).sum()),'max shift %.2f'%sh.max())
