# pairana.py SIM.npz box : analyse self-x pairs in a box (Blender frame, y flipped from sim): normal dot, centroid distance, topological distance
import numpy as np, sys, collections
z=np.load(sys.argv[1]); V=z['V'].copy(); V[:,1]*=-1; Q=z['Q']; P=np.load(sys.argv[1].replace('.npz','_pairs.npy'))
b=np.array([float(t) for t in sys.argv[2].split(',')]).reshape(3,2)
C=np.array([V[q[q>=0]].mean(0) for q in Q]) 
def nrm(q):
    q=q[q>=0]; n=np.cross(V[q[2]]-V[q[0]],V[q[3%len(q)]]-V[q[1]]); return n/(np.linalg.norm(n)+1e-12)
sel=[(i,j) for i,j in P if ((C[i]>b[:,0])&(C[i]<b[:,1])).all()]
print('pairs in box',len(sel))
# face adjacency for topological distance (BFS limited)
v2f=collections.defaultdict(list)
for k,q in enumerate(Q):
    for v in q[q>=0]: v2f[v].append(k)
def tdist(a,bb,lim=12):
    seen={a:0}; fr=[a]
    for d in range(1,lim+1):
        nf=[]
        for f in fr:
            for v in Q[f][Q[f]>=0]:
                for g in v2f[v]:
                    if g not in seen: seen[g]=d; nf.append(g)
        if bb in seen: return seen[bb]
        fr=nf
    return 99
import random; random.seed(0)
smp=random.sample(sel,min(60,len(sel)))
st=[(float(nrm(Q[i])@nrm(Q[j])),float(np.linalg.norm(C[i]-C[j])),tdist(i,j)) for i,j in smp]
st=np.array(st); print('normal dot pct',np.percentile(st[:,0],[10,50,90]).round(2),'centroid dist',np.percentile(st[:,1],[10,50,90]).round(3),'topo dist',np.percentile(st[:,2],[10,50,90]))
fs=np.array([C[i] for i,j in sel]); print('face size (edge) median %.3f'%np.median([np.linalg.norm(V[Q[i][0]]-V[Q[i][1]]) for i,j in sel[:200]]))
