# RM-OT-05AB1 cp3: open the cp2 rig scene (hash-checked), replace ONLY the trunk / upperarm_L / upperarm_R vertex-group weights that
# changed in the cleaned weight set (quantised to 1e-4), let the existing Armature modifier produce the surface, and write NEW files:
# the cp3 rig scene, the frozen applied clean baseline (.blend) and a geometry GLB. cp2 files are never written.
# Usage: python3 ab1_apply_cp3.py -- RIG_cp2.blend SHA256 WEIGHTS_cp3.npz OUTDIR
import bpy, sys, json, hashlib, os, numpy as np
a = sys.argv[sys.argv.index('--') + 1:]; blend, exp, wp, od = a
h = hashlib.sha256(open(blend, 'rb').read()).hexdigest(); assert h == exp, ('rig hash mismatch', h)
bpy.ops.wm.open_mainfile(filepath=blend); o = bpy.data.objects['GO-05AA_C_working']; ao = bpy.data.objects['GO-05AB_temp_rig']; me = o.data
n = len(me.vertices); names = [g.name for g in o.vertex_groups]
W0 = np.zeros((n, len(names)), np.float64)
for v in me.vertices:
    for ge in v.groups: W0[v.index, ge.group] = ge.weight
Wn = np.load(wp); assert [str(x) for x in Wn['names']] == names; W1 = Wn['W'].astype(np.float64)
rep = dict(rig_cp2_sha256=h, groups={})
for g in ('trunk', 'upperarm_L', 'upperarm_R'):
    i = names.index(g); old = W0[:, i]; new = np.round(W1[:, i], 4); ch = np.where(np.abs(new - old) > 5e-5)[0]; vg = o.vertex_groups[g]
    rem = ch[new[ch] <= 0];
    if len(rem): vg.remove(rem.tolist())
    add = ch[new[ch] > 0]
    for val in np.unique(new[add]): vg.add(add[new[add] == val].tolist(), float(val), 'REPLACE')
    rep['groups'][g] = dict(changed_weights=int(len(ch)), removed=int(len(rem)), max_abs_change=round(float(np.abs(new[ch] - old[ch]).max()) if len(ch) else 0.0, 4))
other = [k for k in names if k not in ('trunk', 'upperarm_L', 'upperarm_R')]
rep['other_groups_untouched'] = other
chv = np.zeros(n, bool)
W2 = np.zeros((n, len(names)))
for v in me.vertices:
    for ge in v.groups: W2[v.index, ge.group] = ge.weight
chv = np.abs(W2 - W0).max(1) > 5e-5; rep['changed_vertices'] = int(chv.sum()); rep['changed_weight_entries'] = int((np.abs(W2 - W0) > 5e-5).sum())
rep['other_groups_max_change'] = float(np.abs(W2[:, [names.index(k) for k in other]] - W0[:, [names.index(k) for k in other]]).max())
pose = {b.name: (tuple(round(x, 6) for x in b.location), tuple(round(x, 6) for x in b.scale), tuple(round(x, 6) for x in b.rotation_quaternion)) for b in ao.pose.bones}
rep['pose_unchanged_note'] = 'pose bones, bone rest positions, modifier and topology are read from cp2 and not edited'
os.makedirs(od, exist_ok=True)
o['checkpoint'] = '05AB1-cp3'
bpy.ops.wm.save_as_mainfile(filepath=os.path.join(od, 'GO-05AB1_macro_corrected_rig_cp3.blend'), compress=True)
dg = bpy.context.evaluated_depsgraph_get(); nm = bpy.data.meshes.new_from_object(o.evaluated_get(dg)); nm.name = 'GO-05AB1_macro_corrected_clean_mesh'
fo = bpy.data.objects.new('GO-05AB1_macro_corrected_clean', nm); bpy.context.scene.collection.objects.link(fo)
fo['donor_sha256'] = '513bc9e2c5c4ba1da0a5a33661f230181bf18a24c50e0af0d49acdf5521dccf6'; fo['aa_baseline_sha256'] = 'c17ac3c2b213cf877e952fe2089eb0545d661b4ffa14ca197fa42ea954df7bac'
fo['rig_cp2_sha256'] = h; fo['checkpoint'] = '05AB1-cp3'
for ob in (o, ao): bpy.data.objects.remove(ob, do_unlink=True)
bpy.ops.wm.save_as_mainfile(filepath=os.path.join(od, 'GO-05AB1_macro_corrected_clean.blend'), compress=True)
Y = np.empty(len(nm.vertices) * 3); nm.vertices.foreach_get('co', Y); nm.calc_loop_triangles()
T = np.empty(len(nm.loop_triangles) * 3, np.int32); nm.loop_triangles.foreach_get('vertices', T)
np.savez(os.path.join(od, 'corrected_cp3.npz'), V=Y.reshape(-1, 3).astype(np.float32), F=T.reshape(-1, 3))
bpy.ops.object.select_all(action='DESELECT'); fo.select_set(True); bpy.context.view_layer.objects.active = fo
bpy.ops.export_scene.gltf(filepath=os.path.join(od, 'GO-05AB1_macro_corrected_clean.glb'), use_selection=True, export_format='GLB',
                          export_materials='NONE', export_normals=True, export_texcoords=True, export_apply=False)
json.dump(rep, open(os.path.join(od, 'apply_cp3.json'), 'w'), indent=1); print(json.dumps(rep, indent=1))
