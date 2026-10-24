# hand_quick.py OUT H [k=v ...] : quick hand-frame build of the SDF hand (no forearm blend) for look-dev
import sys, numpy as np, trimesh, json
sys.path.insert(0,'/tmp/claude-0/src3d/v5/tools')
from hand_model import hand_sdf, DEF, scaled
from build_part import evaluate, polygonize
p=scaled(DEF)
for kv in sys.argv[3:]:
    k,v=kv.split('='); grp,key=k.split('.'); p[grp][key]=json.loads(v)
h=float(sys.argv[2])
D,lo,h,cnt=evaluate(lambda P: hand_sdf(P,p),np.array([-4.0,-9,-11]),np.array([31,15,7]),h)
V,F=polygonize(D,lo,h); m=trimesh.Trimesh(V,F,process=False); trimesh.smoothing.filter_taubin(m,lamb=0.5,nu=0.53,iterations=20)
m=max(m.split(only_watertight=False),key=lambda q:len(q.faces)); np.savez(sys.argv[1],V=np.asarray(m.vertices),Q=np.asarray(m.faces)); print(len(m.vertices))
