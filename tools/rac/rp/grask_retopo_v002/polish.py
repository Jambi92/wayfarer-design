# polish.py IN.npz OUT.npz ROUNDS : alternate normal-ray projection (Blender BVH), tangential relaxation and guarded nearest projection
import numpy as np, sys, subprocess, os
sys.path.insert(0,'/tmp/claude-0/rt')
from subproj import Projector, vertex_part, neighbors, vnormals
from common import *
inp,out,R=sys.argv[1],sys.argv[2],int(sys.argv[3])
z=np.load(inp); V=z['V']; Q=z['Q']; FP=z['FP']
PR=Projector(); vp,M=vertex_part(Q,FP,len(V)); band=np.asarray((M>0).sum(1)).ravel()>1
A=neighbors(Q,len(V)); deg=np.asarray(A.sum(1)).ravel()
tmp='/tmp/claude-0/rt/_rp_%d.npz'%os.getpid()
for r in range(R):
    np.savez(tmp,V=V,Q=Q,FP=FP)
    subprocess.run(['/home/claude/stc/bin/python3','/tmp/claude-0/rt/rayproj.py','--',tmp,tmp,'2.0'],check=True,stdout=subprocess.DEVNULL)
    V=np.load(tmp)['V']
    for it in range(2):
        N=vnormals(V,Q); avg=(A@V)/deg[:,None]; dlt=avg-V; dlt-=(dlt*N).sum(1)[:,None]*N
        V=PR.project(V+0.5*dlt,vp,band,N)
np.savez(out,V=V,Q=Q,FP=FP)
