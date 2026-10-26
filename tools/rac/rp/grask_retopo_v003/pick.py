# pick.py CAMJSON u v [side] : 3D surface point (v005, analysis cm) under image pixel (u,v) of a handview render
import numpy as np, json, sys, trimesh
sys.path.insert(0,'/tmp/claude-0/rt'); from common import *
C=json.load(open(sys.argv[1])); u,v=float(sys.argv[2]),float(sys.argv[3]); side=sys.argv[4] if len(sys.argv)>4 else 'r'
c=np.array(C['c']); x=np.array(C['x']); y=np.array(C['y']); h=C['h']; px=C['px']; d=-np.cross(x,y)   # analysis frame is a reflection of blender's: view dir = -(x cross y)
SV,SF=load_src(); flab=np.load('/tmp/claude-0/rt/flab.npy')
HP=[i for i,p in enumerate(PARTS) if p.endswith('_'+side) and p.startswith(('hand','thumb','index','middle','ring','pinky'))]
m=trimesh.Trimesh(SV,SF[np.isin(flab,HP)],process=False)
o=c+x*(u/px-0.5)*2*h+y*(0.5-v/px)*2*h+d*80
loc,_,_=m.ray.intersects_location([o],[-d])
p=loc[np.argmin(np.linalg.norm(loc-o,axis=1))]; print(json.dumps(np.round(p,3).tolist()))
