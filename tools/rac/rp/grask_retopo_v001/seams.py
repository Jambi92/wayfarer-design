# seams.py PROD.npz LOOPS.json OUT.json : UV seam-plan PROPOSAL (no UVs are made). Seams = tagged authored loops at
# segment boundaries + geodesic edge paths (Dijkstra on the edge graph) through anatomical waypoints on low-visibility sides.
import numpy as np, sys, json, scipy.sparse as sp
from scipy.sparse.csgraph import dijkstra
from scipy.spatial import cKDTree
sys.path.insert(0,'/tmp/claude-0/rt'); sys.path.insert(0,'/tmp/claude-0/src3d/v5/tools')
import hands as HM, foot_model as fm
from hand_model import finger_chain
from hand_frame import frame
z=np.load(sys.argv[1]); V=z['V']; Q=z['Q']; loops=json.load(open(sys.argv[2]))
L={k:np.array(v['p']) for k,v in json.load(open('/tmp/claude-0/rt/lm_src.json')).items()}
E=np.unique(np.sort(np.concatenate([Q[:,[0,1]],Q[:,[1,2]],Q[:,[2,3]],Q[:,[3,0]]]),1),axis=0)
w=np.linalg.norm(V[E[:,0]]-V[E[:,1]],axis=1)
G=sp.coo_matrix((np.r_[w,w],(np.r_[E[:,0],E[:,1]],np.r_[E[:,1],E[:,0]])),shape=(len(V),len(V))).tocsr()
kd=cKDTree(V); near=lambda p: int(kd.query(p)[1])
def path(pts):
    ids=[near(p) for p in pts]; out=[ids[0]]
    for a,b in zip(ids[:-1],ids[1:]):
        _,pred=dijkstra(G,indices=a,return_predecessors=True,limit=np.linalg.norm(V[a]-V[b])*3+5)
        seg=[b]
        while seg[-1]!=a: seg.append(int(pred[seg[-1]]))
        out+=seg[::-1][1:]
    return out
S={}
for k in ('neck_189','shoulder_port_l','shoulder_port_r','groin_split_l','groin_split_r','wrist_palm_l_0','wrist_palm_r_0','ankle_l_0','ankle_r_0','ear_root_l','ear_root_r'):
    if k in loops: S['loop:'+k]=dict(kind='closed_loop',reason='segment boundary on an authored loop',verts=loops[k])
back=V[(np.abs(V[:,0])<0.5)]
nape=back[np.argmin(np.abs(back[:,2]-189)+0.2*back[:,1])]; crown=L['crown']
sac=back[(back[:,2]>112)&(back[:,2]<118)]; sac=sac[np.argmin(sac[:,1])]
S['path:back_midline']=dict(kind='open',reason='posterior midline, nape to sacrum',verts=path([nape,np.array([0,-14,160]),np.array([0,-14,135]),sac]))
S['path:head_back']=dict(kind='open',reason='occipital midline, nape to crown (hidden by hair/helmets)',verts=path([nape,np.array([0,-10,205]),crown]))
for s,sg in (('l',1),('r',-1)):
    e=L['elbow_'+s]; wr=L['wrist_'+s]; W_,M_=frame(s.upper())
    S['path:arm_inner_'+s]=dict(kind='open',reason='medial (inner) arm, axilla to ulnar wrist',verts=path([L['glenohumeral_'+s]+np.array([-sg*4,0,-26]),e+np.array([-sg*6,0,0]),wr+np.array([-sg*3,-2,1])]))
    S['path:leg_inner_'+s]=dict(kind='open',reason='medial (inner) leg, groin to medial ankle',verts=path([L['hip_'+s]+np.array([-sg*6,0,-12]),L['knee_'+s]+np.array([-sg*8,0,0]),L['ankle_'+s]+np.array([-sg*5,0,0])]))
    hm=L['hallux_mtp_'+s]
    S['path:foot_medial_'+s]=dict(kind='open',reason='medial foot border, ankle to hallux base (sole/dorsum split)',verts=path([L['ankle_'+s]+np.array([-sg*5,0,-4]),hm+np.array([-sg*3,-4,0]),hm+np.array([-sg*3,0,0])]))
    for nm,f in HM.P_['fingers'].items():
        Jc,_,_=finger_chain(f['mcp'],f['L'],f['splay'],f['flex']); Jw=[W_+M_@j for j in Jc]
        side=M_@np.array([0,1.0,0])*(1 if nm!='index' else 1)
        S['path:%s_side_%s'%(nm,s)]=dict(kind='open',reason='digit side line (palm/dorsum split)',verts=path([Jw[0]+side*1.0,Jw[1]+side*1.0,Jw[2]+side*0.9,Jw[3]]))
    for t in fm.DEF['toes']:
        Jt,_,_=fm.chain(t); P=np.array(Jt); P[:,0]*=sg
        S['path:%s_side_%s'%(t['n'],s)]=dict(kind='open',reason='toe plantar-side line',verts=path([P[0]+np.array([0,0,-1.2]),P[-1]+np.array([0,0,-0.8])]))
json.dump(dict(note='PROPOSAL ONLY - no UVs created; seams stored as edge attribute seam_proposal in the .blend',seams=S),open(sys.argv[3],'w'))
print(len(S),'seams',sum(len(v['verts']) for v in S.values()),'verts')
