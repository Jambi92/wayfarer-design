# ident_build.py PARAMS.json OUT.npz [--base-only] : build the identity delta on the body and the production candidate.
import sys, json, numpy as np, igl
sys.path.insert(0,'/tmp/claude-0/rp2/tools')
import ident_head as IH
from ident_targets import compose
R='/tmp/claude-0/rp2/'
p=json.load(open(sys.argv[1])); H=np.load(R+'hstar.npz'); V=H['V'].astype(float); Q=H['Q']
Wb={k:v for k,v in np.load(R+'weights_body.npz').items()}
T=np.r_[Q[:,[0,1,2]],Q[:,[0,2,3]]]; N=-igl.per_vertex_normals(V,T)      # physical outward (left-handed frame)
D=np.zeros_like(V)
if 'targets' in p: D+=compose(p['targets'])
if p.get('head'): D+=IH.head_delta(V+D,Wb,N,p['head'])
if p.get('ear'):
    for s in (1,-1): D+=IH.ear_delta(V+D,Wb,p['ear'],s)
if p.get('ear_relief'):
    D+=IH.relief(V+D,Q,IH.ss(Wb['ears']/0.9),p['ear_relief'])
if p.get('body'):
    import ident_body as IB; D+=IB.body_delta(V+D,Wb,N,p['body'])
np.save(sys.argv[2].replace('.npz','_D.npy'),D)
np.savez(sys.argv[2].replace('.npz','_base.npz'),V=V+D,Q=Q)
if '--base-only' not in sys.argv:
    from ident_apply import apply
    P=apply(D, base=p.get('prod_base','cand_h4_12.npz')); np.savez(sys.argv[2],**P)
print('delta max cm %.2f, moved>0.1mm %d'%(np.linalg.norm(D,axis=1).max(),(np.linalg.norm(D,axis=1)>0.01).sum()))
