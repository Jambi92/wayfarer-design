# gate_v006_deltas.py V006.npz OUT.json MASKS.npz : v005 -> v006 delta accounting per order section 21.
# Region masks by dominant skin weight (every vertex in exactly one region); the axilla deformation-support region is reported separately.
import sys, json, numpy as np
sys.path.insert(0,'/tmp/claude-0/rp2/tools')
from ident_apply import SS
R='/tmp/claude-0/rp2/'
X=np.load(sys.argv[1])['V'].astype(float); V5=np.load(R+'fin/v005.npz')['V'].astype(float)
W={k:SS()@v for k,v in np.load(R+'weights_body.npz').items()}
ks=list(W); dom=np.array(ks)[np.argmax(np.stack([W[k] for k in ks]),0)]
grp=lambda *names: np.isin(dom,names)
z=V5[:,2]
head=grp('head','ears')
neck_traps=grp('neck_01')|(grp('spine_03','clavicle_l','clavicle_r')&(z>172)&(np.abs(V5[:,0])<16))
shoulders=grp('clavicle_l','clavicle_r')&~neck_traps
torso=grp('spine_01','spine_02','spine_03')&~neck_traps
pelvis=grp('pelvis')
upper_arms=grp('upperarm_l','upperarm_r'); forearms=grp('lowerarm_l','lowerarm_r'); hands=grp('hand_l','hand_r','fingers_l','fingers_r')
thighs=grp('thigh_l','thigh_r'); calves=grp('calf_l','calf_r'); feet=grp('foot_l','foot_r','ball_l','ball_r')
M=dict(head=head,neck_traps=neck_traps,shoulders=shoulders,torso=torso,pelvis=pelvis,upper_arms=upper_arms,forearms=forearms,hands=hands,thighs=thighs,calves=calves,feet=feet)
ax=(np.abs(np.abs(V5[:,0])-18.5)<5)&(np.abs(V5[:,1]-1)<7)&(np.abs(V5[:,2]-164)<6)
d=np.linalg.norm(X-V5,axis=1)*10
np.savez_compressed(sys.argv[3],**M,deformation_support_axilla=ax,displacement_from_v005_mm=d.astype(np.float32))
out={}; anym=np.zeros(len(X),bool)
st_=lambda m: dict(vertices=int(m.sum()),moved_gt_0p5mm=int((m&(d>0.5)).sum()),mean_mm=float(d[m].mean()) if m.any() else 0.0,max_mm=float(d[m].max()) if m.any() else 0.0)
for k,m in M.items(): anym|=m; out[k]=st_(m)
out['deformation_support_axilla (overlaps torso / upper_arms)']=st_(ax)
o=~anym; out['outside_all_masks']=st_(o)
out['all']=dict(moved_gt_0p5mm=int((d>0.5).sum()),mean_mm=float(d.mean()),max_mm=float(d.max()))
st=lambda V: float(V[:,2].max()-V[:,2].min())
out['stature_cm']=dict(v005=st(V5),v006=st(X),delta_mm=(st(X)-st(V5))*10)
out['bbox_delta_mm']=dict(min=((X.min(0)-V5.min(0))*10).tolist(),max=((X.max(0)-V5.max(0))*10).tolist())
json.dump(out,open(sys.argv[2],'w'),indent=1)
for k,v in out.items(): print(k,v)
