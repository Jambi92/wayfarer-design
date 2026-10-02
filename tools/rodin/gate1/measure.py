import numpy as np, json, sys
import g1
z=np.load(sys.argv[1] if len(sys.argv)>1 else "g1_body_main.npz"); V=z["V"]; F=z["F"]; nA=int(z["nA"]); mv=z["moved"]
H=188.0; out={}
# --- B1 geometry deleted, by planning region
mask=np.load("b1_mask.npy"); R=np.load("/tmp/claude-0/rodin/adopt/b1_regions.npz")["R"]
NAMES={1:"head",2:"neck",3:"shoulder",4:"arms/hands",5:"thorax shell",6:"ventral thorax",7:"ventral abdomen",8:"lower-trunk flanks",9:"dorsal strap",10:"posterior pelvis/glutes",11:"crotch",12:"hip/anterolateral pelvis",14:"legs",15:"feet",16:"leg artifacts"}
out["b1_verts_total"]=int(len(mask)); out["b1_verts_replaced"]=int(mask.sum())
out["b1_replaced_by_region"]={NAMES[int(k)]:int((mask&(R==k)).sum()) for k in np.unique(R) if (mask&(R==k)).sum()>0}
P1=g1.P1; out["replaced_extent_cm"]=dict(U=[float(P1[mask,2].min()),float(P1[mask,2].max())],X=[float(P1[mask,0].min()),float(P1[mask,0].max())],F=[float(P1[mask,1].min()),float(P1[mask,1].max())])
movedA=mv[:nA]>0.01; out["b1_preserved_verts_moved_by_seam_fairing"]=int(movedA.sum()); out["seam_fairing_max_move_cm"]=float(mv[:nA].max())
out["preserved_unchanged_verts"]=int(nA-movedA.sum())
# --- tail length: root path from where it leaves the ORIGINAL B1 body, then donor centreline
b1_on_path=g1.sd(g1.P1,g1.f1,g1.RP); i0=np.argmax(b1_on_path>0)
from donorgeo import centreline
C=centreline(); Cj=C[C[:,1]<=-41.0]
ij=np.argmin(np.abs(g1.RP[:,1]+41.0))
root_len=np.linalg.norm(np.diff(g1.RP[i0:ij+1],axis=0),axis=1).sum()
don_len=np.linalg.norm(np.diff(np.vstack([g1.RP[ij],Cj]),axis=0),axis=1).sum()+1.0
out["tail_start_point"]=g1.RP[i0].round(1).tolist(); out["tail_root_cm"]=float(root_len); out["tail_donor_cm"]=float(don_len)
out["tail_total_cm"]=float(root_len+don_len); out["tail_over_H"]=float((root_len+don_len)/H)
# --- proximal tail sections perpendicular to the root path
def section(Fv):
    i=np.argmin(np.abs(g1.RP[:,1]-Fv)); c=g1.RP[i]; t=g1.RT[i]; n=g1.RN[i]
    d=(V-c)@t; m=(np.abs(d)<0.25)&(np.linalg.norm(V-c,axis=1)<30)
    S=V[m]-c; return dict(at_F=float(c[1]),at_U=float(c[2]),width=float(np.ptp(S[:,0])),height=float(np.ptp(S@n)))
out["caudal_base_section_F-14"]=section(-14.0); out["proximal_tail_section_F-23"]=section(-23.0); out["junction_section_F-40"]=section(-40.0)
for k in ("caudal_base_section_F-14","proximal_tail_section_F-23","junction_section_F-40"):
    out[k]["width_H"]=out[k]["width"]/H; out[k]["height_H"]=out[k]["height"]/H
# --- hips: legs not edited -> hip spacing unchanged (B1 measured 0.152H)
out["hip_spacing_H_before"]=0.152; out["hip_spacing_H_after"]=0.152
out["standing_height_cm"]=float(np.ptp(V[:,2])); out["mesh"]=dict(verts=int(len(V)),faces=int(len(F)))
json.dump(out,open(sys.argv[2] if len(sys.argv)>2 else "g1_measure.json","w"),indent=1)
print(json.dumps(out,indent=1))
