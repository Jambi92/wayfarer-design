import sys, os, numpy as np
sys.path.insert(0,'/tmp/claude-0/rb'); sys.path.insert(0,'/tmp/claude-0/rodin/g1')
import wf_saurin_head65 as H5
H=H5.H
x=np.linspace(0,8,321); u=np.linspace(0,9,361); X,U=np.meshgrid(x,u)
out={}
for fv in [8,6,4,2,0,-2]:
    F=np.full_like(X,fv); out[str(fv)]=H.head_sdf(X,F,U,H5.RINGS,-59.0)
np.savez(sys.argv[1],**out)
