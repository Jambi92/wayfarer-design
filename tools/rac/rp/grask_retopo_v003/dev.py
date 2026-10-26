# dev.py PROD.npz [OUT.json] : bidirectional surface deviation production <-> v005 by zone (mm)
import numpy as np, sys, json, igl
sys.path.insert(0,'/tmp/claude-0/rt')
from common import *
z=np.load(sys.argv[1]); PV=z['V'].astype(float); PQ=z['Q'].astype(np.int64)
PT=np.concatenate([PQ[:,[0,1,2]],PQ[:,[0,2,3]]]) if PQ.shape[1]==4 else PQ
SV,SF=load_src(); vl=np.load('/tmp/claude-0/rt/vlab.npy')
PS=np.vstack([PV,PV[PQ].mean(1)]) if PQ.shape[1]==4 else PV
d_ps=np.sqrt(igl.point_mesh_squared_distance(PS,SV,SF)[0])*10
d_sp=np.sqrt(igl.point_mesh_squared_distance(SV,PV,PT)[0])*10
from scipy.spatial import cKDTree
pl=vl[cKDTree(SV).query(PS)[1]]; PV_=PV; PV=PS
x,f,zz=SV.T
head=(zz>186)
zones={'head_face':lambda lab,P: (P[:,2]>186)&(lab==PID['axial']),
       'ears':lambda lab,P: np.isin(lab,[PID['ear_l'],PID['ear_r']]),
       'hand_l':lambda lab,P: np.isin(lab,[PID[p] for p in PARTS if p.endswith('_l') and (p.startswith(('hand','thumb','index','middle','ring','pinky')))]),
       'hand_r':lambda lab,P: np.isin(lab,[PID[p] for p in PARTS if p.endswith('_r') and (p.startswith(('hand','thumb','index','middle','ring','pinky')))]),
       'foot_l':lambda lab,P: np.isin(lab,[PID[p] for p in PARTS if p.endswith('_l') and (p.startswith(('foot','hallux','toe')))]),
       'foot_r':lambda lab,P: np.isin(lab,[PID[p] for p in PARTS if p.endswith('_r') and (p.startswith(('foot','hallux','toe')))]),
       'body_general':lambda lab,P: np.ones(len(lab),bool)}
out={}
for k,fn in zones.items():
    ms=fn(vl,SV); mp=fn(pl,PV)
    a=d_sp[ms]; b=d_ps[mp]
    st=lambda v: dict(median=float(np.median(v)),p95=float(np.percentile(v,95)),max=float(v.max())) if len(v) else None
    out[k]=dict(src_to_prod=st(a),prod_to_src=st(b))
    f_=lambda v: '%.3f/%.3f/%6.2f'%(np.median(v),np.percentile(v,95),v.max()) if len(v) else '-'
    print('%-13s src->prod %s | prod->src %s'%(k,f_(a),f_(b)))
np.save(sys.argv[1].replace('.npz','_dsp.npy'),d_sp); np.save(sys.argv[1].replace('.npz','_dps.npy'),d_ps)
if len(sys.argv)>2: json.dump(out,open(sys.argv[2],'w'),indent=1)
