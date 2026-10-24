# f32safe.py IN OUT : remove self-intersections that appear only after float32 storage in the Blender frame.
# Checked on both quad diagonals (any engine triangulation) and on float64 and float32. Loop: round to the stored representation, find pairs, relax the 3-ring of the pair vertices (Laplacian, fixed border), repeat.
import numpy as np, subprocess, sys
R='/tmp/claude-0/rp2/'; P=dict(np.load(sys.argv[1])); V=P['V'].astype(float); Q=P['Q']
e=np.r_[Q[:,[0,1]],Q[:,[1,2]],Q[:,[2,3]],Q[:,[3,0]]]; n=len(V)
nb=[[] for _ in range(n)]
for a,b in e: nb[a].append(b); nb[b].append(a)
def stored(V): Vb=(np.c_[V[:,0],-V[:,1],V[:,2]]/100).astype(np.float32).astype(float); return np.c_[Vb[:,0],-Vb[:,1],Vb[:,2]]*100
for it in range(20):
    for tag,X,QQ in (('f64-d02',V,Q),('f64-d13',V,Q[:,[1,2,3,0]]),('f32-d02',stored(V),Q),('f32-d13',stored(V),Q[:,[1,2,3,0]])):
        np.savez('/tmp/f32t.npz',V=X,Q=QQ); out=subprocess.run(['/home/claude/stc/bin/python3',R+'sxq.py','/tmp/f32t.npz','/tmp/f32p.npy'],capture_output=True,text=True).stdout
        k=int([l for l in out.splitlines() if l.startswith('PAIRS')][0].split()[1]); pr=np.load('/tmp/f32p.npy') if k else np.zeros((0,2),int)
        if k: break
    print('iter',it,tag,'pairs',k)
    if k==0: break
    S=set(QQ[pr.ravel()].ravel().tolist())
    for _ in range(3): S|={j for i in list(S) for j in nb[i]}
    S=np.array(sorted(S))
    for _ in range(10):
        V[S]=0.5*V[S]+0.5*np.array([V[nb[i]].mean(0) for i in S])
P['V']=V; np.savez(sys.argv[2],**P)
