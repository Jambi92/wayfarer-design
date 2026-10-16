#!/bin/bash
# usage: gates.sh BASE_VF.npz CHECKPOINT.blend OUTPREFIX
cd /home/claude/ag
/home/claude/bpyenv/bin/python /home/claude/wayfarer-design/tools/rac/w1/rmot05ad_drivers/ad_ac1_gates.py "$1" "$2" prot_all.npy identity.npy /home/claude/ag >/dev/null 2>&1
cp ac1_VF.npz "$3_VF.npz"
python3 -I - "$1" "$3" <<'PY' 2>&1 | grep -v -i "plugin\|cannot load\|libOpenGL\|^$\|Warning"
import sys, json, numpy as np, pymeshlab
base, pre = sys.argv[1], sys.argv[2]
R=json.load(open('ac1_gates_partial.json'))
B=np.load(base); VB,F=B['V'],B['F']; VA=np.load(pre+'_VF.npz')['V']
k,iv=np.unique(np.round(VA,7),axis=0,return_inverse=True); ms=pymeshlab.MeshSet(); ms.add_mesh(pymeshlab.Mesh(k,iv.ravel()[F])); ms.compute_selection_by_self_intersections_per_face()
s=np.flatnonzero(ms.current_mesh().face_selection_array()); R['self_intersecting_faces']=dict(ac1=int(len(s)))
z0=VB[:,2].min(); d=np.linalg.norm(VA-VB,axis=1)*1000
Pz=np.load('protected_05AF.npz'); R['protected_max_disp_mm']={k:round(float(d[Pz[k]].max()),4) for k in Pz.files}
n=lambda V: np.cross(V[F[:,1]]-V[F[:,0]],V[F[:,2]]-V[F[:,0]]); fl=np.flatnonzero((n(VB)*n(VA)).sum(1)<0)
R['flip_sites_cm']=[[round(float(x)*100,1) for x in (p[0],p[1],p[2]-z0)] for p in VA[F[fl]].mean(1)]
if len(s): cs=VA[F[s]].mean(1); R['si_sites_z_cm']=[round(float((cs[:,2]-z0).min()*100),1),round(float((cs[:,2]-z0).max()*100),1)]
json.dump(R,open(pre+'_gates.json','w'),indent=1)
for k in ['topology_identical','pairs_opened_gt_0_01mm','self_intersecting_faces','flipped_faces','degenerate_faces','position_welded_ac1','moved_z_from_floor_cm','moved_vertices','max_displacement_mm','p99_moved_mm','height_cm','bbox_extent_cm','protected_max_disp_mm','flip_sites_cm','si_sites_z_cm']: print(k, R.get(k))
PY
