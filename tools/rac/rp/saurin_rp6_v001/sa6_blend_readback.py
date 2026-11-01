# sa6_blend_readback.py CFG BLEND WEIGHTS.npz CORRECTIVES.json OUT.json : fresh-process read-back of an RP6 rig-pilot .blend (order a407015 §21, §25, §27).
#   Run with the bpy 5.2.2 interpreter.  Opens the FROZEN RP5 .blend first (read only, never saved) for the neutral comparison, then the RP6 file.
#   Checks: scene objects / types / transforms / modifiers / constraints / parenting / external dependencies; mesh topology (vertex / face count, face
#   order = frozen Q, topology sha256), semantic attribute, neutral positions vs the frozen RP5 .blend AND vs the float64 embedding; armature bones / parents /
#   deform flags / heads / tails; vertex groups = deform bones, weights vs the weight npz; shape keys vs the corrective npz; drivers (count, targets, simple
#   expressions, value 0 at rest); RIG_PREP action.  Then poses evaluated by Blender's own depsgraph (armature modifier + driven shape keys) vs the audit
#   evaluator (sa6_pose LBS + sa6_correctives) on a pose sample.
import sys, os, json, hashlib, numpy as np, bpy, mathutils
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sa6_common as C, sa6_pose as SP, sa6_correctives as CC, sa6_fit as FT
argv = sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else sys.argv[1:]; CFG, BL, WF, CF, OUT = argv[:5]
d = C.load(); Vf = d['V1'] if CFG == 'M' else d['V2']; Q = d['Q']; res = dict(status='RP6 RIG PILOT / NOT FROZEN', configuration=CFG, file=os.path.basename(BL), sha256=hashlib.sha256(open(BL, 'rb').read()).hexdigest())
# frozen RP5 blend (read only)
rp5 = C.FZ + '/SA_%s_REF_RP5_freeze_candidate_v001.blend' % CFG; h5 = hashlib.sha256(open(rp5, 'rb').read()).hexdigest()
bpy.ops.wm.open_mainfile(filepath=rp5); m5 = [o for o in bpy.data.objects if o.type == 'MESH'][0].data; V5 = np.zeros(len(m5.vertices) * 3, np.float32); m5.vertices.foreach_get('co', V5); V5 = V5.reshape(-1, 3)
assert hashlib.sha256(open(rp5, 'rb').read()).hexdigest() == h5 == C.FROZEN[os.path.basename(rp5)]
bpy.ops.wm.open_mainfile(filepath=BL)
objs = {o.name: o for o in bpy.data.objects}; mesh = [o for o in objs.values() if o.type == 'MESH']; arms = [o for o in objs.values() if o.type == 'ARMATURE']
res['objects'] = {n: dict(type=o.type, parent=o.parent.name if o.parent else None, location=list(o.location), rotation=list(o.rotation_euler), scale=list(o.scale),
                          modifiers=[(m.name, m.type) for m in o.modifiers], constraints=len(o.constraints)) for n, o in objs.items()}
assert len(mesh) == 1 and len(arms) == 1 and len(objs) == 2; ob = mesh[0]; arm = arms[0]; me = ob.data
res['external'] = dict(images=len(bpy.data.images), libraries=len(bpy.data.libraries), materials=len(bpy.data.materials), node_groups=len(bpy.data.node_groups), texts=len(bpy.data.texts),
                       uv_layers=len(me.uv_layers), pose_constraints=sum(len(pb.constraints) for pb in arm.pose.bones))
nv = len(me.vertices); co = np.zeros(nv * 3, np.float32); me.vertices.foreach_get('co', co); co = co.reshape(-1, 3)
lt = np.zeros(len(me.polygons), np.int32); me.polygons.foreach_get('loop_total', lt); lv = np.zeros(len(me.loops), np.int32); me.loops.foreach_get('vertex_index', lv)
Qb = lv.reshape(-1, 4).astype(np.int64) if (lt == 4).all() else None
sem = np.zeros(len(me.polygons), np.int32); me.attributes['semantic'].data.foreach_get('value', sem); labs = json.loads(ob['semantic_table'])
res['mesh'] = dict(vertices=nv, faces=len(me.polygons), all_quads=bool((lt == 4).all()), face_order_equal=bool(Qb is not None and np.array_equal(Qb, Q)),
                   topology_sha256=hashlib.sha256(np.ascontiguousarray(Qb).tobytes()).hexdigest(), topology_match=hashlib.sha256(np.ascontiguousarray(Qb).tobytes()).hexdigest() == C.TOPO,
                   semantic_equal=bool(all(labs[s] == str(f) for s, f in zip(sem, d['face_sem']))),
                   neutral_vs_frozen_RP5_blend_max_abs=float(np.abs(co - V5).max()), neutral_vs_frozen_RP5_blend_identical=bool(np.array_equal(co, V5)),
                   neutral_vs_float64_embedding_max_abs_cm=float(np.abs(co.astype(float) - Vf).max()), float32_half_ulp_at_max_coord_cm=float(np.spacing(np.float32(np.abs(Vf).max())) / 2))
os.makedirs(os.environ.get('RB_DIR', '/tmp/claude-0/rp6'), exist_ok=True); np.save(os.path.join(os.environ.get('RB_DIR', '/tmp/claude-0/rp6'), 'neutral_disp_%s.npy' % CFG), np.linalg.norm(co.astype(float) - V5.astype(float), axis=1))
# armature
P = json.load(open(C.EV6 + '/SA_RP6_joint_placement_%s_v001.json' % CFG))['bones']; ad = arm.data
bh = max(max(np.abs(np.array(b.head_local) - P[b.name]['head']).max(), np.abs(np.array(b.tail_local) - P[b.name]['tail']).max()) for b in ad.bones)
res['armature'] = dict(bones=len(ad.bones), deform=sum(b.use_deform for b in ad.bones), control=[b.name for b in ad.bones if not b.use_deform],
                       parents_match=all((b.parent.name if b.parent else None) == P[b.name]['parent'] for b in ad.bones), head_tail_max_abs_cm=float(bh),
                       deform_flags_match=all(b.use_deform == P[b.name]['deform'] for b in ad.bones))
# weights
import scipy.sparse as sp
z = np.load(WF); S = sp.csr_matrix((z['data'], z['indices'], z['indptr']), shape=tuple(z['shape'])).toarray(); DB = [str(b) for b in z['bones']]
Wb = np.zeros((nv, len(DB)), np.float32); gi = {g.index: DB.index(g.name) for g in ob.vertex_groups}
for v in me.vertices:
    for g in v.groups: Wb[v.index, gi[g.group]] = g.weight
res['weights'] = dict(groups=len(ob.vertex_groups), groups_equal_deform_bones=sorted(g.name for g in ob.vertex_groups) == sorted(b.name for b in ad.bones if b.use_deform),
                      max_abs_vs_npz=float(np.abs(Wb - S).max()), max_influences=int((Wb > 0).sum(1).max()), sum_err_max=float(np.abs(Wb.sum(1) - 1).max()))
# shape keys / drivers
cj = json.load(open(CF)); cz = np.load(CF.replace('.json', '.npz')); kbs = me.shape_keys.key_blocks; mk = 0.0; nk = 0
basis = np.zeros(nv * 3, np.float32); kbs['Basis'].data.foreach_get('co', basis); basis = basis.reshape(-1, 3)
for f in cj['families']:
    for k in f['keys']:
        kb = kbs[k['name']]; a = np.zeros(nv * 3, np.float32); kb.data.foreach_get('co', a); a = a.reshape(-1, 3); dlt = np.zeros((nv, 3)); dlt[cz[k['name'] + '_idx']] = cz[k['name'] + '_d']
        mk = max(mk, float(np.abs((a.astype(float) - basis.astype(float)) - dlt).max())); nk += 1
drv = me.shape_keys.animation_data.drivers if me.shape_keys.animation_data else []
bpy.context.scene.frame_set(1); dg = bpy.context.evaluated_depsgraph_get(); dg.update()
vals = [kb.value for kb in kbs[1:]]
res['shape_keys'] = dict(count=len(kbs) - 1, expected=nk, basis_equal_neutral=bool(np.array_equal(basis, co)), delta_max_abs_vs_npz_cm=mk,
                         drivers=len(drv), drivers_simple_expression=sum(1 for fc in drv if fc.driver.is_simple_expression), drivers_valid=sum(1 for fc in drv if fc.driver.is_valid),
                         rest_values_max=float(max(vals) if vals else 0.0), relative_to_basis=all(kb.relative_key.name == 'Basis' for kb in kbs[1:]))
res['rig_prep_action'] = dict(present='RIG_PREP' in bpy.data.actions, assigned=bool(arm.animation_data and arm.animation_data.action))
res['units'] = dict(object_scale=list(ob.scale), armature_scale=list(arm.scale), note=ob.get('units'))
# ---- Blender-evaluated poses vs the audit evaluator ----
R = SP.Rig(CFG, WF); Cr = CC.Correctives.load(R, CF); PS = FT.pose_set(R)
sample = [k for k in ('knee_90_xpos', 'elbow_130_xneg', 'fist_xpos', 'grasp_xneg', 'thumb_opposition_xpos', 'shoulder_abd90_xpos', 'hip_flex70_xneg', 'toe_ext30_xpos', 'tail_root_lateral_30',
                      'tail_twist_30', 'jaw_open_20', 'neck_rot_40', 'trunk_twist_30', 'gate:tail_combined', 'gate:hand_splay_xneg', 'gate:jaw32_head_pitch_up') if k in PS]
Mr = {b.name: np.array(b.matrix_local) for b in ad.bones}
def m4(Rm, t): M = np.eye(4); M[:3, :3] = Rm; M[:3, 3] = t; return M
ev = {}
for pn in sample:
    T = R.pose(PS[pn])
    for b in ad.bones:
        Tb = m4(*T[b.name]); Tp = m4(*T[b.parent.name]) if b.parent else np.eye(4)
        basis_m = np.linalg.inv(Mr[b.name]) @ np.linalg.inv(Tp) @ Tb @ Mr[b.name]; pb = arm.pose.bones[b.name]; pb.rotation_mode = 'QUATERNION'; pb.matrix_basis = mathutils.Matrix(basis_m.tolist())
    bpy.context.view_layer.update(); bpy.context.scene.frame_set(1); dg = bpy.context.evaluated_depsgraph_get(); dg.update()
    oe = ob.evaluated_get(dg); m2 = oe.to_mesh(); pe = np.zeros(nv * 3, np.float32); m2.vertices.foreach_get('co', pe); pe = pe.reshape(-1, 3); oe.to_mesh_clear()
    Pp = R.skin(T, R.V + Cr.delta(T)); e = np.linalg.norm(pe - Pp, axis=1); fl = int((R.relcos(pe.astype(float), T) < 0).sum())
    act = sum(1 for kb in me.shape_keys.key_blocks[1:] if kb.value > 1e-6)
    ev[pn] = dict(max_err_cm=round(float(e.max()), 6), p99_err_cm=round(float(np.percentile(e, 99)), 6), blender_eval_flips=fl, active_keys=act); print(pn, ev[pn], flush=True)
for pb in arm.pose.bones: pb.matrix_basis = mathutils.Matrix.Identity(4)
res['blender_vs_audit_evaluator'] = ev; res['blender_vs_audit_max_err_cm'] = max(v['max_err_cm'] for v in ev.values()); res['blender_eval_flips_total'] = sum(v['blender_eval_flips'] for v in ev.values())
json.dump(res, open(OUT, 'w'), indent=1); print(json.dumps({k: v for k, v in res.items() if k not in ('objects', 'blender_vs_audit_evaluator')}, indent=0))
