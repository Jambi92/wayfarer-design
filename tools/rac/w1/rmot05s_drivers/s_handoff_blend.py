# RM-OT-05S direct-edit handoff scene (native Blender .blend, saved headless with bpy 5.0.1).
# Objects: GO-05S-S3 (working mesh; edit only inside the EDIT_* vertex groups), F1_source_reference and B2_reference
# (hidden, locked). Vertex groups on the working mesh:
#   EDIT_posterior / EDIT_anterior : vertices used only by 05S interface faces (labels 4/5) - free to sculpt / retopologize
#   FROZEN_interface_boundary      : interface boundary ring (exact source / B2 vertices) - must not move
#   FOCUS_posterior_crinkle         : the unresolved posterior fold-edge zone (theta -86..-106, s 2..8) for the sculptor
# Face attribute 'rac_label' (0 source, 2/3 05Q inferred, 4 05S transition, 5 05S inferred skin).
# Usage: python3 s_handoff_blend.py --res GO-05S-S3.obj --labels GO-05S-S3_face_labels.npy --src F1_working.obj --b2 B2.obj --frame patch_selection.json --out X.blend
import argparse, json, sys, os, numpy as np, bpy
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); import s_lib
ap = argparse.ArgumentParser(); ap.add_argument('--res'); ap.add_argument('--labels'); ap.add_argument('--src'); ap.add_argument('--b2'); ap.add_argument('--frame'); ap.add_argument('--out'); a = ap.parse_args()
def load_obj(p):
    V = []; F = []
    for l in open(p):
        if l.startswith('v '): V.append([float(t) for t in l.split()[1:4]])
        elif l.startswith('f '): F.append([int(t.split('/')[0]) - 1 for t in l.split()[1:4]])
    return np.array(V), np.array(F)
bpy.ops.wm.read_factory_settings(use_empty=True); sc = bpy.context.scene; sc.unit_settings.system = 'METRIC'; sc.unit_settings.scale_length = 0.01
def mk(name, V, F):
    me = bpy.data.meshes.new(name); me.from_pydata(V.tolist(), [], F.tolist()); me.update(); ob = bpy.data.objects.new(name, me); sc.collection.objects.link(ob); return ob, me
V, F = load_obj(a.res); lab = np.load(a.labels); ob, me = mk('GO-05S-S3_working', V, F)
at = me.attributes.new('rac_label', 'INT', 'FACE'); at.data.foreach_set('value', lab.astype(np.int32))
newf = np.where((lab == 4) | (lab == 5))[0]; oldf = np.where((lab != 4) & (lab != 5))[0]
vnew = np.zeros(len(V), bool); vnew[F[newf].ravel()] = True; vold = np.zeros(len(V), bool); vold[F[oldf].ravel()] = True
edit = vnew & ~vold; ring = vnew & vold
fr = s_lib.Frame(a.frame); t, s, r = fr.tsr(V)
groups = dict(EDIT_posterior=edit & (t < 0), EDIT_anterior=edit & (t > 0), FROZEN_interface_boundary=ring,
              FOCUS_posterior_crinkle=edit & (t > -106) & (t < -86) & (s > 2) & (s < 8))
for g, m in groups.items():
    vg = ob.vertex_groups.new(name=g); vg.add(np.where(m)[0].tolist(), 1.0, 'REPLACE')
for nm, p in (('F1_source_reference', a.src), ('B2_reference', a.b2)):
    Vr, Fr = load_obj(p); o2, _ = mk(nm, Vr, Fr); o2.hide_set(True); o2.hide_render = True; o2.hide_select = True
ob.select_set(True); bpy.context.view_layer.objects.active = ob
bpy.ops.wm.save_as_mainfile(filepath=os.path.abspath(a.out), compress=True)
print(json.dumps({g: int(m.sum()) for g, m in groups.items()}), os.path.getsize(a.out))
