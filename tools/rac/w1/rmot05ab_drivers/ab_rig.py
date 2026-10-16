# RM-OT-05AB: temporary rigid-segment armature on a WORKING copy of donor C, driven by estimated joint centres and the accepted W1
# ARM macro shares (order 05AB s4-s5). The surface is moved ONLY by Blender's Armature modifier (linear-blend skinning) with bone
# pose scales along each segment axis: thigh/shin lengthened, upper arm/forearm shortened; hands, feet and the trunk (incl. head,
# neck, tail) rigid. No per-vertex shape is scripted. The trunk root is lifted so the soles return to the ground plane.
# Reads the pinned AA baseline .blend (hash-checked); writes only new files into OUTDIR (scratch). The donor GLB and the AA
# baseline are never written.
# Usage: python3 ab_rig.py -- BASELINE.blend SHA256 JOINTS.json WEIGHTS.npz PLAN.json OUTDIR TAG
#   PLAN.json: {"crotch_target_pct":48.5,"fingertip_target_pct":44.3,"knee_target_pct":26.87,"leg_extra_cm":0,"arm_extra_cm":0}
import bpy, sys, json, hashlib, os, numpy as np
from mathutils import Vector
a = sys.argv[sys.argv.index('--') + 1:]; blend, exp, jp, wp, pp, od, tag = a
h = hashlib.sha256(open(blend, 'rb').read()).hexdigest(); assert h == exp, ('baseline hash mismatch', h)
bpy.ops.wm.open_mainfile(filepath=blend); o = bpy.data.objects['GO-05AA_C_working']
J = json.load(open(jp)); P = json.load(open(pp)); OFF = np.array([6.888, -39.481, 0.0])
jt = {k: (np.array(v) + OFF) / 100 for k, v in J.items() if isinstance(v, list) and len(v) == 3}   # Blender metres
H = J['H']; crotch = J['crotch_z']
dL = (P['crotch_target_pct'] / 100 * H - crotch) / (1 - P['crotch_target_pct'] / 100) + P.get('leg_extra_cm', 0); Hn = H + dL
plan = dict(baseline_sha256=h, plan=P, leg_lengthening_cm=round(dL, 3), new_height_cm=round(Hn, 3))
# armature
arm = bpy.data.armatures.new('GO-05AB_temp_rig'); ao = bpy.data.objects.new('GO-05AB_temp_rig', arm); bpy.context.scene.collection.objects.link(ao)
bpy.context.view_layer.objects.active = ao; bpy.ops.object.mode_set(mode='EDIT'); eb = arm.edit_bones
def bone(n, hd, tl, parent=None, connect=False, inh='FULL'):
    b = eb.new(n); b.head = Vector(hd); b.tail = Vector(tl); b.parent = eb[parent] if parent else None; b.use_connect = connect; b.inherit_scale = inh; return b
hipmid = (jt['hip_L'] + jt['hip_R']) / 2; bone('trunk', hipmid, hipmid + np.array([0, 0, 0.5]))
for s in 'LR':
    th = jt['hip_' + s].copy(); po = P.get('thigh_pivot_crotch_offset_cm')
    if po is not None:                     # checkpoint 2: thigh segment pivots on its axis at the crotch plane (= weight boundary)
        k = jt['knee_' + s]; zc = (J['crotch_z'] + po) / 100; th = k + (zc - k[2]) / (th[2] - k[2]) * (th - k)
    jt['thighhead_' + s] = th
    bone('thigh_' + s, th, jt['knee_' + s], 'trunk')
    bone('shin_' + s, jt['knee_' + s], jt['ankle_' + s], 'thigh_' + s, True, 'NONE')
    bone('foot_' + s, jt['ankle_' + s], jt['toe_' + s], 'shin_' + s, True, 'NONE')
    bone('upperarm_' + s, jt['shoulder_' + s], jt['elbow_' + s], 'trunk')
    bone('forearm_' + s, jt['elbow_' + s], jt['wrist_' + s], 'upperarm_' + s, True, 'NONE')
    bone('hand_' + s, jt['wrist_' + s], jt['fingertip_' + s], 'forearm_' + s, True, 'NONE')
bpy.ops.object.mode_set(mode='OBJECT')
# vertex groups from the geodesic weights (welded -> all duplicates), batched by quantised weight
Wd = np.load(wp); names = [str(x) for x in Wd['names']]; Wt = Wd['weights_welded'][Wd['welded_index']]
for i, n in enumerate(names):
    vg = o.vertex_groups.new(name=n); q = np.round(Wt[:, i] * 1000).astype(int)
    for val in np.unique(q[q > 0]): vg.add(np.where(q == val)[0].tolist(), val / 1000, 'REPLACE')
mod = o.modifiers.new('GO-05AB_temp_rig', 'ARMATURE'); mod.object = ao; mod.use_vertex_groups = True; mod.use_deform_preserve_volume = False
# pose scales from the macro targets
pb = ao.pose.bones; sc = {}
knee_new = P['knee_target_pct'] / 100 * Hn
for s in 'LR':
    hz, kz, az = jt['thighhead_' + s][2] * 100, J['knee_' + s][2], J['ankle_' + s][2]
    sc['thigh_' + s] = ((hz + dL) - knee_new) / (hz - kz); sc['shin_' + s] = (knee_new - az) / (kz - az)
    tip_target = P['fingertip_target_pct'] / 100 * Hn + P.get('arm_extra_cm', 0)
    rise = tip_target - (J['fingertip_' + s][2] + dL); seg = J['shoulder_' + s][2] - J['wrist_' + s][2]
    sc['upperarm_' + s] = sc['forearm_' + s] = 1 - rise / seg
for n, v in sc.items(): pb[n].scale = (1.0, v, 1.0)
plan['segment_scales'] = {k: round(v, 4) for k, v in sc.items()}
def evaluated():
    dg = bpy.context.evaluated_depsgraph_get(); dg.update(); ev = o.evaluated_get(dg); m2 = ev.to_mesh()
    X = np.empty(len(m2.vertices) * 3); m2.vertices.foreach_get('co', X); ev.to_mesh_clear(); return X.reshape(-1, 3)
X = evaluated(); lift = -X[:, 2].min(); pb['trunk'].location = (0.0, lift, 0.0)    # trunk local Y = world +Z
X = evaluated(); plan['root_lift_cm'] = round(lift * 100, 3)
bpy.context.view_layer.update()
plan['posed_joints_cm'] = {b.name: [round(c * 100, 2) for c in (ao.matrix_world @ b.head)] for b in pb}
plan['rest_joints_cm'] = {b.name: [round(c * 100, 2) for c in (ao.matrix_world @ b.bone.head_local)] for b in pb}
os.makedirs(od, exist_ok=True)
bpy.ops.wm.save_as_mainfile(filepath=os.path.join(od, 'GO-05AB_macro_corrected_rig_%s.blend' % tag), compress=True)
# frozen derivative: evaluated mesh as a new object, rig removed (topology identical by construction)
dg = bpy.context.evaluated_depsgraph_get(); nm = bpy.data.meshes.new_from_object(o.evaluated_get(dg)); nm.name = 'GO-05AB_macro_corrected_mesh'
fo = bpy.data.objects.new('GO-05AB_macro_corrected', nm); bpy.context.scene.collection.objects.link(fo)
fo['donor_sha256'] = '513bc9e2c5c4ba1da0a5a33661f230181bf18a24c50e0af0d49acdf5521dccf6'; fo['aa_baseline_sha256'] = h; fo['checkpoint'] = tag
for ob in (o, ao): bpy.data.objects.remove(ob, do_unlink=True)
bpy.ops.wm.save_as_mainfile(filepath=os.path.join(od, 'GO-05AB_macro_corrected_%s.blend' % tag), compress=True)
Y = np.empty(len(nm.vertices) * 3); nm.vertices.foreach_get('co', Y); nm.calc_loop_triangles()
T = np.empty(len(nm.loop_triangles) * 3, np.int32); nm.loop_triangles.foreach_get('vertices', T)
np.savez(os.path.join(od, 'corrected_%s.npz' % tag), V=Y.reshape(-1, 3).astype(np.float32), F=T.reshape(-1, 3))
# GLB of the frozen derivative for the existing review / gate tools (geometry only)
bpy.ops.object.select_all(action='DESELECT'); fo.select_set(True); bpy.context.view_layer.objects.active = fo
bpy.ops.export_scene.gltf(filepath=os.path.join(od, 'GO-05AB_macro_corrected_%s.glb' % tag), use_selection=True, export_format='GLB',
                          export_materials='NONE', export_normals=True, export_texcoords=True, export_apply=False)
json.dump(plan, open(os.path.join(od, 'plan_%s.json' % tag), 'w'), indent=1); print(json.dumps({k: plan[k] for k in plan if 'joints' not in k}, indent=1))
