# GO-RD0-SOURCE: F1 isolated from the recovered GLB, oriented to RAC frame (cm, Z up, +Y anterior, +X body left, ground z=0)
import trimesh, numpy as np, json, hashlib
D='/tmp/claude-0/-home-claude-wayfarer-design/19af7d50-3b61-5fda-9fe0-7a30770fb334/scratchpad'
m=trimesh.load(D+'/n/c0s_1.obj',process=False); V=m.vertices.copy()
XC=-76.1; FLOOR=V[:,2].min(); CROWN=119.5      # crown = cranial vault top under the mane, ears/tufts excluded
S=229.0/(CROWN-FLOOR)
W=np.c_[-(V[:,0]-XC), -V[:,1], V[:,2]-FLOOR]*S   # 180 deg about Z: front (-Y in render frame) -> +Y
yc=np.median(W[(W[:,2]>140)&(W[:,2]<170),1]); W[:,1]-=yc
trimesh.Trimesh(W,m.faces,process=False).export(D+'/rd/GO-RD0-SOURCE.obj')
rec=dict(source='base.glb sha256 78ecfa87d169380ecb46ece3f0c0df3491d10e4547038a3c35c06df933f38a7b',figure='F1 (comp 0 split, front figure)',
 glb_to_work='(x,-z,y)*100', midline_x=XC, floor=float(FLOOR), crown_excl_ears_mane=CROWN, scale_factor=S, y_shift=float(yc),
 rac_frame='X=-(x-XC)*S, Y=-y*S-yshift, Z=(z-floor)*S', target_stature_cm=229.0, bounds=W.min(0).round(2).tolist()+W.max(0).round(2).tolist(),
 verts=len(W), faces=len(m.faces))
json.dump(rec,open(D+'/rd/GO-RD0-SOURCE_record.json','w'),indent=1); print(rec)
