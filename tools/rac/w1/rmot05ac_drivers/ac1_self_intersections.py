import sys, json, numpy as np, pymeshlab
sys.argv=['x']; exec(open('/home/claude/wayfarer-design/tools/rac/w1/rmot05ac_drivers/ac1_checks.py').read().split('b, a, pp')[0])
U='/mnt/user-data/uploads/RaceBodies/source/Gorrund-Neutral-C'
VB,FB,_=load_glb(U+'/05AB1/GO-05AB1_macro_corrected_clean.glb'); VA,FA,_=load_glb(U+'/05AC/GO-05AC_AC1.glb')
def si(V,F):
    k,iv=np.unique(np.round(V,6),axis=0,return_inverse=True); ms=pymeshlab.MeshSet(); ms.add_mesh(pymeshlab.Mesh(k,iv.ravel()[F]))
    ms.compute_selection_by_self_intersections_per_face(); return np.where(ms.current_mesh().face_selection_array())[0]
sB=si(VB,FB); sA=si(VA,FA); new=np.setdiff1d(sA,sB)
r=dict(self_intersecting_faces_before=int(len(sB)),after=int(len(sA)),new=int(len(new)),method='pymeshlab per-face, welded by position (faces index-aligned between exports)')
print(r); json.dump(r,open('/home/claude/wayfarer-design/reviews/rac-rmot05ac2-evidence/checks/ac1_self_intersections.json','w'),indent=1)
