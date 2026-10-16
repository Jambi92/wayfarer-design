#!/bin/bash
# usage: run_gates.sh BLEND
cd /home/claude/ae
/home/claude/bpyenv/bin/python /home/claude/wayfarer-design/tools/rac/w1/rmot05ad_drivers/ad_ac1_gates.py after_VF.npz "$1" protect_05AE_index.npy /home/claude/ae/identity.npy /home/claude/ae >/dev/null 2>&1
python3 -I - <<'PY' 2>&1 | grep -v -i "plugin\|cannot load\|libOpenGL\|^$\|Warning"
import json, numpy as np, pymeshlab
from scipy.spatial import cKDTree
R=json.load(open('ac1_gates_partial.json'))
B=np.load('after_VF.npz'); VB,F=B['V'],B['F']; VA=np.load('ac1_VF.npz')['V']
def si(V):
    k,iv=np.unique(np.round(V,7),axis=0,return_inverse=True); ms=pymeshlab.MeshSet(); ms.add_mesh(pymeshlab.Mesh(k,iv.ravel()[F])); ms.compute_selection_by_self_intersections_per_face(); return np.flatnonzero(ms.current_mesh().face_selection_array())
s=si(VA); R['self_intersecting_faces']=dict(base=0,ac1=int(len(s)))
z0=VB[:,2].min()
n=lambda V: np.cross(V[F[:,1]]-V[F[:,0]],V[F[:,2]]-V[F[:,0]]); fl=np.flatnonzero((n(VB)*n(VA)).sum(1)<0)
c=VA[F[fl]].mean(1); R['flip_sites_cm']=[[round(x*100,1) for x in (p[0],p[1],p[2]-z0)] for p in c]
if len(s): cs=VA[F[s]].mean(1); R['si_sites_z_cm']=[round(float((cs[:,2]-z0).min()*100),1),round(float((cs[:,2]-z0).max()*100),1)]
json.dump(R,open('ac1_gates.json','w'),indent=1)
for k in ['topology_identical','pairs_opened_gt_0_01mm','max_pair_gap_mm','self_intersecting_faces','flipped_faces','degenerate_faces','position_welded_ac1','moved_z_from_floor_cm','moved_outside_117_170cm','protected_vertices_moved','max_displacement_mm','height_cm','flip_sites_cm','si_sites_z_cm']: print(k, R.get(k))
PY
