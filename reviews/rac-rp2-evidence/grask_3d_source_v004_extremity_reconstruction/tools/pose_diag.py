# pose_diag.py POSE OUT : standalone diagnostic hand in a different pose (same anatomy parameters) -- not part of the source
import sys, copy, numpy as np
sys.path.insert(0,'/tmp/claude-0/src3d/v4/tools')
import hand_model
from hand_model import hand_sdf, DEF, scaled
from build_part import evaluate, polygonize, remesh
pose=sys.argv[1]; out=sys.argv[2]
p=scaled(DEF)
if pose=='open':
    for f in p['fingers'].values(): f['flex']=[2,4,2]
    p['thumb']['flex']=[4,6]; p['thumb']['dir']=[0.70,0.62,-0.30]
elif pose=='fist':
    fl={'index':[78,96,58],'middle':[82,98,60],'ring':[84,100,62],'pinky':[86,100,62]}
    for k,f in p['fingers'].items(): f['flex']=fl[k]; f['splay']=f['splay']*0.3
    import os, json as _j
    p['thumb']['dir']=_j.loads(os.environ.get('TD','[0.5,-0.45,-0.74]')); p['thumb']['flex']=_j.loads(os.environ.get('TF','[30,34]')); p['thumb']['flexsign']=float(os.environ.get('TS','1'))
fun=lambda P: hand_sdf(P,p)
D,lo,h,cnt=evaluate(fun,np.array([-6,-10,-14]),np.array([31,15,8]),float(__import__('os').environ.get('PH','0.07')))
V,F=polygonize(D,lo,h); V,F=remesh(V,F,200000)
import trimesh; m=trimesh.Trimesh(V,F); m=max(m.split(only_watertight=False),key=lambda q:len(q.faces))
np.savez(out,V=np.asarray(m.vertices),Q=np.asarray(m.faces)); print(pose,len(m.vertices))
