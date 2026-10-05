import numpy as np, sys; sys.path.insert(0,'/tmp/claude-0/rodin/v2'); sys.path.insert(0,'/tmp/claude-0/rodin/v1')
import claws, rv
F=np.load('/tmp/claude-0/rodin/c12/g15_surf.npz')['F']
for k in (0.8,1.0,1.15,1.3):
    P=claws.warp(k,k); rv.render(P,F,'/tmp/claude-0/rodin/v2/CL_%03d'%int(k*100),"fside:90:3:24:22:3:16;ftop:20:55:24:20:4:18;hfront:0:0:39:11:84:16;hside:90:0:39:11:84:16",res=600); print(k,flush=True)
