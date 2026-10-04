import sys, numpy as np
sys.path.insert(0,'/tmp/claude-0/rb'); sys.path.insert(0,'/tmp/claude-0/rodin/g1')
import wf_saurin_head65 as H5
H=H5.H
x=np.linspace(4,7.5,281); u=np.linspace(3.5,7.5,321); X,U=np.meshgrid(x,u)
out={}
for fv in [4.5,4,3.5,3,2.5,2,1.5]:
    out[str(fv)]=H.head_sdf(X,np.full_like(X,fv),U,H5.RINGS,-59.0)
np.savez(sys.argv[1],**out)
