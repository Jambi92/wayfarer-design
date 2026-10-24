# finalize4.py : asm.npz -> v004.npz (right-forefoot ground restore) + technical stats + freeze proof
import sys, json, numpy as np, trimesh, igl, collections
R='/tmp/claude-0/src3d/v5/'
A=np.load(R+'w/asm.npz'); V=A['V'].astype(float).copy(); F=A['Q'].astype(np.int64)
B=np.load(R+'v004.npz'); BV=B['V'].astype(float); BF=B['Q'].astype(np.int64)
x,f,z=V.T
# --- ground restore on the right forefoot (toes rebuilt; heel/arch untouched) ---
gfix=np.zeros(len(V))
for sg in (-1,):
    mask=(sg*x>3)&(z<6)
    w=np.clip(1-z/4,0,1)*mask*np.clip((f-15)/2,0,1)
    k=w>1e-9; s=float((z[k]/w[k]).min())
    gfix=s*w*10; V[:,2]=z-s*w; i=np.nonzero(k)[0][np.argmin(z[k]/w[k])]; V[i,2]=0.0; print('right forefoot ground shift cm',round(s,4))
zmin=V[:,2].min(); V[:,2]-=0 if abs(zmin)<1e-6 else zmin*0  # no global shift: heel already at 0
print('zmin',V[:,2].min(),'zmax',V[:,2].max())
np.savez(R+'v005.npz',V=V,Q=F,replaced=A['replaced'],seam=A['seam'],ground_fix_mm=gfix)
# --- technical ---
m=trimesh.Trimesh(V,F,process=False)
e=np.sort(m.edges,1); u,c=np.unique(e,axis=0,return_counts=True)
area=m.area_faces; Fs=np.sort(F,1); dupf=len(F)-len(np.unique(Fs,axis=0))
_,inv=np.unique(np.round(V,7),axis=0,return_inverse=True); coinc=len(V)-inv.max()-1
tech=dict(V=len(V),F=len(F),boundary=int((c==1).sum()),nonmanifold=int((c>2).sum()),euler=int(len(V)-len(u)+len(F)),
  pieces=len(m.split(only_watertight=False)),degenerate=int((area<1e-10).sum()),dup_faces=int(dupf),coincident=int(coinc),
  volume_L=float(m.volume/1000),bbox=[V.min(0).round(3).tolist(),V.max(0).round(3).tolist()],height=float(V[:,2].max()-V[:,2].min()),
  edge_cm=dict(median=float(np.median(m.edges_unique_length)),min=float(m.edges_unique_length.min()),max=float(m.edges_unique_length.max())))
tech['genus']=(2-tech['euler'])//2
print(json.dumps(tech))
json.dump(tech,open(R+'w/tech4.json','w'),indent=1)
# --- freeze proof ---
d4=np.sqrt(igl.point_mesh_squared_distance(V,BV,BF)[0])*10
d3=np.sqrt(igl.point_mesh_squared_distance(BV,V,F)[0])*10
np.save(R+'w/dist4.npy',d4)
M3=np.load('/tmp/claude-0/src3d/out3/GR_U_REF_RP2_SOURCE_3D_v003_refinement_masks.npz')
_,nn=trimesh.proximity.ProximityQuery(trimesh.Trimesh(BV,BF,process=False)).vertex(V) if False else (None,None)
from scipy.spatial import cKDTree
nn=cKDTree(BV).query(V)[1]
def regs(P,eyew):
    x,f,z=P.T; ax=np.abs(x)
    hand=(ax>15)&(z>60)&(z<112); foot=(z<14)&(f>10.5)&(ax>3)
    eyes=eyew>0
    ears=(ax>6.0)&(z>186)&(z<206)&(f<4)&~eyes
    head=(z>178)&~eyes&~ears
    torso=(z>112)&(z<=178)&(ax<17)
    arms=(ax>15)&(z>=112)&(z<170)&~torso
    legs=(z<112)&~hand&~foot&(ax<=17)|((z<14)&~foot&~hand)
    return dict(hand_L=hand&(x>0),hand_R=hand&(x<0),foot_L=foot&(x>0),foot_R=foot&(x<0),head_face=head,eyes=eyes,ears=ears,
                torso_pelvis_back=torso,arms_above_wrist=arms,legs_above_forefoot=legs&~foot,rest_all=~hand&~foot)
EW=M3['eye_weight']+(M3['eye_move_mm']>1e-6); V3=np.load('/tmp/claude-0/src3d/v4/v003.npz')['V']; EW=EW[cKDTree(V3).query(BV)[1]]; r4=regs(V,EW[nn]); r3=regs(BV,EW)
st={}
for k in r4:
    a=d4[r4[k]]; b=d3[r3[k]]
    st[k]=dict(v005_verts=int(r4[k].sum()),v005_to_v004_max_mm=float(a.max()) if len(a) else 0,v005_to_v004_p95_mm=float(np.percentile(a,95)) if len(a) else 0,
               v004_to_v005_max_mm=float(b.max()) if len(b) else 0,moved_gt_0p1mm=int((a>0.1).sum()))
json.dump(st,open(R+'w/freeze_stats.json','w'),indent=1)
for k,v in st.items(): print(k,{a:round(b,3) if isinstance(b,float) else b for a,b in v.items()})
