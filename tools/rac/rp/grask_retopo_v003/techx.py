# techx.py PROD.npz OUT.json : extra technical gate -- manifold VERTICES (each vertex's faces form one closed fan),
# Euler characteristic / genus (no unwanted handles), components, both aspect statistics, angle limits
import numpy as np, sys, json, collections
z=np.load(sys.argv[1]); V=z['V']; Q=z['Q']
E=np.concatenate([Q[:,[0,1]],Q[:,[1,2]],Q[:,[2,3]],Q[:,[3,0]]]); Es=np.sort(E,1); ue,cnt=np.unique(Es,axis=0,return_counts=True)
nV=len(np.unique(Q)); chi=nV-len(ue)+len(Q)
# vertex manifoldness: link edges (the edge opposite... use corner neighbours) must form a single cycle
link=collections.defaultdict(list)
for q in Q:
    for i in range(4):
        v=q[i]; a=q[(i+1)%4]; b=q[(i-1)%4]; link[v].append((a,b))
bad=0
for v,es in link.items():
    adj=collections.defaultdict(list)
    for a,b in es: adj[a].append(b); adj[b].append(a)
    if any(len(x)!=2 for x in adj.values()): bad+=1; continue
    start=es[0][0]; seen={start}; cur=start; prev=None
    while True:
        nx=[w for w in adj[cur] if w!=prev]; 
        if not nx: break
        nx=nx[0]
        if nx==start: break
        if nx in seen: break
        seen.add(nx); prev,cur=cur,nx
    if len(seen)!=len(adj): bad+=1
from scipy.sparse import coo_matrix; from scipy.sparse.csgraph import connected_components
A=coo_matrix((np.ones(len(ue)),(ue[:,0],ue[:,1])),shape=(len(V),len(V))); nc=connected_components(A,directed=False)[0]-(len(V)-nV)
ang=[]
for i in range(4):
    a=V[Q[:,(i-1)%4]]-V[Q[:,i]]; b=V[Q[:,(i+1)%4]]-V[Q[:,i]]
    ang.append(np.degrees(np.arccos(np.clip((a*b).sum(1)/np.maximum(np.linalg.norm(a,axis=1)*np.linalg.norm(b,axis=1),1e-12),-1,1))))
ang=np.stack(ang,1); el=np.stack([np.linalg.norm(V[Q[:,(i+1)%4]]-V[Q[:,i]],axis=1) for i in range(4)],1)
asum=(el[:,0]+el[:,2])/np.maximum(el[:,1]+el[:,3],1e-12); asum=np.maximum(asum,1/asum); aedge=el.max(1)/el.min(1)
R=dict(nonmanifold_vertices=int(bad),euler_characteristic=int(chi),genus=int((2-chi)//2),components=int(nc),
  aspect_opposite_sum=dict(definition='max(sum of opposite edges ratio, inverse)',max=float(asum.max()),over_4=int((asum>4).sum()),over_8=int((asum>8).sum())),
  aspect_edge=dict(definition='longest edge / shortest edge',max=float(aedge.max()),over_4=int((aedge>4).sum()),over_6=int((aedge>6).sum()),over_8=int((aedge>8).sum()),over_10=int((aedge>10).sum())),
  angle_min=float(ang.min()),angle_max=float(ang.max()),hard_angle=int(((ang.min(1)<20)|(ang.max(1)>160)).sum()))
json.dump(R,open(sys.argv[2],'w'),indent=1); print(json.dumps(R))
