import sys, numpy as np, trimesh
sys.path.insert(0,'/tmp/claude-0/src3d/v4/tools')
import hand_model
from hand_model import hand_sdf, DEF, scaled
from hand_frame import frame
from build_part import evaluate, polygonize, remesh
p=scaled(DEF)
for kv in sys.argv[2:]:
    k,v=kv.split('='); p['nail'][k]=float(v)
W,M=frame('L'); c=np.array([26.5,3,79.5])
D,lo,h,cnt=evaluate(lambda P: hand_sdf((P-W)@M,p),c-2.8,c+2.8,0.05)
V,F=polygonize(D,lo,h); m=trimesh.Trimesh(V,F,process=False); trimesh.smoothing.filter_taubin(m,lamb=0.5,nu=0.53,iterations=20)
V,F=remesh(np.asarray(m.vertices),F,int(len(F)*0.226)); np.savez(sys.argv[1],V=V,Q=F)
