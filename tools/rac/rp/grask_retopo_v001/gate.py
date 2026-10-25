# gate.py PROD.npz OUT.json : topology / density / T-3 / T-4 audit of the retopo
import numpy as np, sys, json, collections, scipy.sparse as sp
from scipy.sparse.csgraph import connected_components
sys.path.insert(0,'/tmp/claude-0/rt'); from common import *
z=np.load(sys.argv[1]); V=z['V']; Q=z['Q']; FP=z['FP']; nV=len(V)
SV,SF=load_src()
R={}
E=np.concatenate([Q[:,[0,1]],Q[:,[1,2]],Q[:,[2,3]],Q[:,[3,0]]]); Es=np.sort(E,1)
ue,inv,cnt=np.unique(Es,axis=0,return_inverse=True,return_counts=True)
R['verts']=int(nV); R['faces']=int(len(Q)); R['quads']=int(len(Q)); R['tris']=0; R['ngons']=0; R['quad_pct']=100.0
R['boundary_edges']=int((cnt==1).sum()); R['nonmanifold_edges']=int((cnt>2).sum())
du,dc=np.unique(E,axis=0,return_counts=True); R['winding_inconsistent_edges']=int((dc>1).sum())
A=sp.coo_matrix((np.ones(len(ue)),(ue[:,0],ue[:,1])),shape=(nV,nV)); nc,_=connected_components(A,directed=False); R['components']=int(nc)
R['unused_verts']=int(nV-len(np.unique(Q)))
R['duplicate_faces']=int(len(Q)-len(np.unique(np.sort(Q,1),axis=0)))
R['repeated_vertex_faces']=int((np.array([len(set(q)) for q in Q])<4).sum())
# coincident vertices
k=np.round(V*1e4).astype(np.int64); _,c2=np.unique(k,axis=0,return_counts=True); R['coincident_verts']=int((c2>1).sum())
n=np.cross(V[Q[:,2]]-V[Q[:,0]],V[Q[:,3]]-V[Q[:,1]]); area=0.5*np.linalg.norm(n,axis=1)
R['degenerate_faces(area<1e-4cm2)']=int((area<1e-4).sum())
T=np.r_[Q[:,[0,1,2]],Q[:,[0,2,3]]]
vol=np.einsum('ij,ij->i',V[T[:,0]],np.cross(V[T[:,1]],V[T[:,2]])).sum()/6; R['volume_cm3']=float(vol); R['normals_outward']=bool(vol>0)
# valence / poles
val=np.bincount(ue.ravel(),minlength=nV); R['valence_hist']={int(a):int(b) for a,b in zip(*np.unique(val,return_counts=True))}
poles=np.nonzero(val!=4)[0]; R['poles']=int(len(poles))
# zones
def zone(p):
    if p.startswith('ear'): return 'ears'
    if p.startswith(('hand','thumb','index','middle','ring','pinky')): return 'hands'
    if p.startswith(('foot','hallux','toe')): return 'feet'
    return 'trunk_limbs'
names=[PARTS[p] if not isinstance(p,str) else p for p in FP]
Z=np.array([zone(p) for p in names]); fc=V[Q].mean(1)
Z[(Z=='trunk_limbs')&(np.array(names)=='axial')&((fc[:,2]>190)|((fc[:,2]>185)&(fc[:,1]>2)))]='head_face'   # head above the chin/neck-base line + under-chin
# angles / aspect
ang=[]
for i in range(4):
    a=V[Q[:,(i-1)%4]]-V[Q[:,i]]; b=V[Q[:,(i+1)%4]]-V[Q[:,i]]
    ang.append(np.degrees(np.arccos(np.clip((a*b).sum(1)/np.maximum(np.linalg.norm(a,axis=1)*np.linalg.norm(b,axis=1),1e-12),-1,1))))
ang=np.stack(ang,1)
el=np.stack([np.linalg.norm(V[Q[:,(i+1)%4]]-V[Q[:,i]],axis=1) for i in range(4)],1)
asp=np.maximum(el[:,0]+el[:,2],1e-9)/np.maximum(el[:,1]+el[:,3],1e-9); asp=np.maximum(asp,1/asp)
H=V[:,2].max()-V[:,2].min(); R['stature_cm']=float(H)
ceil={'head_face':0.0025*H,'ears':0.0025*H,'hands':0.003*H,'feet':0.003*H,'trunk_limbs':0.006*H}
R['zones']={}
for zn in ['head_face','ears','hands','feet','trunk_limbs']:
    m=Z==zn; a=ang[m]; e=el[m]
    R['zones'][zn]=dict(faces=int(m.sum()),angle_in_45_135_pct=float(100*((a>=45)&(a<=135)).all(1).mean()),angle_min=float(a.min()),angle_max=float(a.max()),
        aspect_le4_pct=float(100*(asp[m]<=4).mean()),aspect_max=float(asp[m].max()),
        edge_median_mm=float(10*np.median(e)),edge_p99_mm=float(10*np.percentile(e,99)),edge_max_mm=float(10*e.max()),ceiling_mm=float(10*ceil[zn]),
        density_pass=bool(10*np.percentile(e,99)<=10*ceil[zn]),quad_pct=100.0)
R['angle_in_45_135_pct_all']=float(100*((ang>=45)&(ang<=135)).all(1).mean()); R['aspect_le4_pct_all']=float(100*(asp<=4).mean())
R['bbox_min']=V.min(0).tolist(); R['bbox_max']=V.max(0).tolist()
R['src_bbox_min']=SV.min(0).tolist(); R['src_bbox_max']=SV.max(0).tolist(); R['src_stature_cm']=float(SV[:,2].max()-SV[:,2].min())
R['T3_stature_diff_mm']=float(10*(H-R['src_stature_cm'])); R['T3_bbox_maxdiff_mm']=float(10*np.abs(np.r_[V.min(0)-SV.min(0),V.max(0)-SV.max(0)]).max())
np.save(sys.argv[1].replace('.npz','_poles.npy'),poles)
json.dump(R,open(sys.argv[2],'w'),indent=1)
print(json.dumps({k:v for k,v in R.items() if k!='zones'},indent=0)); [print(k,v) for k,v in R['zones'].items()]
