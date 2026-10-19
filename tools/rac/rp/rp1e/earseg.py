import numpy as np, sys, collections
from scipy.sparse import coo_matrix
from scipy.sparse.csgraph import connected_components
s=sys.argv[1]; sg=1 if s=='L' else -1; thr=float(sys.argv[2]) if len(sys.argv)>2 else 1.0
w=np.load('/home/claude/stc/rp1/weld.npz'); V=w['V'].astype(float); F=w['F'].astype(np.int64)
d=np.load('sim_b4_L3_dsp.npy'); zone=np.load('/home/claude/stc/rp1/zones.npz')['zone']
box=(V[:,0]*sg>4)&(V[:,0]*sg<24)&(V[:,1]>-62)&(V[:,1]<-36)&(V[:,2]>186)&(V[:,2]<210)
m=box&(d>thr)
Fm=F[m[F].all(1)]
E=np.concatenate([Fm[:,[0,1]],Fm[:,[1,2]],Fm[:,[2,0]]])
G=coo_matrix((np.ones(len(E)),(E[:,0],E[:,1])),shape=(len(V),len(V)))
k,lab=connected_components(G,directed=False)
sz=np.bincount(lab[m]); big=np.argmax(sz); ear=(lab==big)&m
# close small holes: dilate then erode on face adjacency (1 ring)
print(s,'ear verts',ear.sum(),'bbox',V[ear].min(0).round(1),V[ear].max(0).round(1))
np.save('ear_%s.npy'%s,np.where(ear)[0])
# boundary edges of the ear region
Fe=F[ear[F].all(1)]; ed=collections.Counter()
for f in Fe:
    for a,b in ((f[0],f[1]),(f[1],f[2]),(f[2],f[0])): ed[(min(a,b),max(a,b))]+=1
bnd=[e for e,c in ed.items() if c==1]; print('boundary edges',len(bnd))
# loops
adj=collections.defaultdict(list)
for a,b in bnd: adj[a].append(b); adj[b].append(a)
seen=set(); loops=[]
for st in adj:
    if st in seen: continue
    loop=[st]; seen.add(st); prev=None; cur=st
    while True:
        nx=[n for n in adj[cur] if n!=prev and n not in seen]
        if not nx: break
        prev,cur=cur,nx[0]; loop.append(cur); seen.add(cur)
    loops.append(loop)
loops.sort(key=len,reverse=True); print('loops',[len(l) for l in loops[:8]])
np.save('earroot_%s.npy'%s,np.array(loops[0]))
L=V[loops[0]]; print('root loop bbox',L.min(0).round(1),L.max(0).round(1),'length %.1f'%np.linalg.norm(np.diff(np.vstack([L,L[:1]]),axis=0),axis=1).sum())
