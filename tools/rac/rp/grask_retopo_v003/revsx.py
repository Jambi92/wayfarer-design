# revsx.py PRE.npz POST.npz OUT.npz : undo repair moves around self-intersections (revert vertices of intersecting faces
# + 2 rings to their pre-repair positions) until the mesh has no intersecting face pairs
import numpy as np, sys, subprocess, os
sys.path.insert(0,'/tmp/claude-0/rt'); from subproj import neighbors
A_=np.load(sys.argv[1]); B_=np.load(sys.argv[2]); V0=A_['V']; V=B_['V'].copy(); Q=B_['Q']; FP=B_['FP']
Nb=neighbors(Q,len(V)); tmp='/tmp/claude-0/rt/_rv_%d'%os.getpid()
for it in range(8):
    np.savez(tmp+'.npz',V=V,Q=Q,FP=FP)
    o=subprocess.run(['/home/claude/stc/bin/python3','/tmp/claude-0/rp2/sxq.py',tmp+'.npz',tmp+'_sx.npy'],capture_output=True,text=True).stdout
    pr=np.load(tmp+'_sx.npy'); print('iter',it,'pairs',len(pr),flush=True)
    if len(pr)==0: break
    m=np.zeros(len(V),bool); m[Q[pr.ravel()].ravel()]=True
    for _ in range(2+it): m|=(Nb@m.astype(float))>0
    V[m]=V0[m]
np.savez(sys.argv[3],V=V,Q=Q,FP=FP); [os.remove(f) for f in (tmp+'.npz',tmp+'_sx.npy') if os.path.exists(f)]
