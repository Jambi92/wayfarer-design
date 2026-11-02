# sa6_blend_export.py CFG(M|F) WEIGHTS.npz CORRECTIVES.json OUT.blend : Saurin RP6 rig-pilot Blender file (order a407015 §20-§21, §25).
#   Run with the bpy 5.2.2 interpreter (/home/claude/stc/bin/python3).  Scene contents (nothing else):
#     mesh object  SA_<CFG>_REF_RP6_body  : the frozen RP5 neutral cage exactly (barycentric embedding realised on SA_RP5_WORK_v001, same vertex / face order,
#                                           face attribute 'semantic'); object scale 0.01 (cm data -> m), identity location / rotation (RP5 convention);
#                                           one Armature modifier (LBS: preserve-volume OFF, vertex groups ON); not parented; vertex groups = the 107 deform bones; shape keys: Basis (= neutral) + one key per corrective sample.
#     armature     SA_<CFG>_RP6_rig       : 108 bones (107 deform + root control), rest = the frozen reference stance, heads / tails / rolls from
#                                           SA_RP6_joint_placement_<CFG>_v001.json; object scale 0.01; no constraints, no helper / diagnostic objects.
#     drivers: one driven custom property per driving degree of freedom on the mesh object, ob['tw###'] = the swing-twist twist angle (deg) of the bone's
#              LOCAL rotation about the family axis (expressed in the bone's rest frame), read from the pose-bone quaternion (TRANSFORMS, LOCAL_SPACE,
#              QUATERNION): 114.59*atan((ax*qx+ay*qy+az*qz)/qw); every family key value = clamp(min((t-l)/(s-l),(r-t)/(r-s)),0,1) of its property
#              (outermost sample held at 1); every pose key value = product of tents clamp(1-|t_j-s_j|/|s_j|,0,1).  Simple expressions only (no Python).
#              Rest pose -> every twist 0 -> every key exactly 0.  Dependency: armature -> object properties -> shape-key values (acyclic).
#     action RIG_PREP (fake user, not assigned): the rig-prep stance (shoulder abduction to 45 deg from vertical, everything else reference).
#   No images / materials / UVs / node groups / libraries / external files.
import sys, os, json, hashlib, numpy as np, bpy, mathutils
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); import sa6_common as C
argv = sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else sys.argv[1:]; CFG, WF, CF, OUT = argv[:4]
d = C.load(); Q = d['Q']; V = d['V1'] if CFG == 'M' else d['V2']; P = json.load(open(C.EV6 + '/SA_RP6_joint_placement_%s_v001.json' % CFG))['bones']
z = np.load(WF); import scipy.sparse as sp; S = sp.csr_matrix((z['data'], z['indices'], z['indptr']), shape=tuple(z['shape'])).tocsc(); DB = [str(b) for b in z['bones']]
cj = json.load(open(CF)); cz = np.load(CF.replace('.json', '.npz'))
fsem = d['face_sem']; labs = sorted(set(map(str, fsem))); lid = {l: i for i, l in enumerate(labs)}; fsi = np.array([lid[str(x)] for x in fsem], np.int32)
topo = hashlib.sha256(np.ascontiguousarray(Q).tobytes()).hexdigest(); assert topo == C.TOPO
tag = 'SA_%s_REF_RP6' % CFG
bpy.ops.wm.read_factory_settings(use_empty=True)
for coll in list(bpy.data.collections): bpy.data.collections.remove(coll)
sc = bpy.context.scene
# ---- armature ----
ad = bpy.data.armatures.new(tag + '_rig'); arm = bpy.data.objects.new(tag + '_rig', ad); sc.collection.objects.link(arm); arm.scale = (0.01, 0.01, 0.01)
bpy.context.view_layer.objects.active = arm; bpy.ops.object.mode_set(mode='EDIT')
order = []
def visit(b):
    order.append(b); [visit(c) for c in P if P[c]['parent'] == b]
[visit(b) for b in P if P[b]['parent'] is None]
for b in order:
    eb = ad.edit_bones.new(b); eb.head = P[b]['head']; eb.tail = P[b]['tail']
    if P[b]['parent']: eb.parent = ad.edit_bones[P[b]['parent']]
    eb.use_connect = False; eb.use_deform = bool(P[b]['deform'])
    if 'local_axes' in P[b]: eb.align_roll(mathutils.Vector(P[b]['local_axes']['z']))
bpy.ops.object.mode_set(mode='OBJECT')
# ---- mesh ----
me = bpy.data.meshes.new(tag + '_body'); me.from_pydata(V.tolist(), [], Q.tolist()); me.update(); me.validate(verbose=False)
at = me.attributes.new('semantic', 'INT', 'FACE'); at.data.foreach_set('value', fsi.tolist())
ob = bpy.data.objects.new(tag + '_body', me); sc.collection.objects.link(ob); ob.scale = (0.01, 0.01, 0.01)   # not parented (a parent would compound the 0.01 scale); the Armature modifier references the rig
for j, b in enumerate(DB):
    vg = ob.vertex_groups.new(name=b); col = S.getcol(j); idx = col.indices; val = col.data
    for u in np.unique(val):
        vg.add(idx[val == u].tolist(), float(u), 'REPLACE')
mod = ob.modifiers.new('Armature', 'ARMATURE'); mod.object = arm; mod.use_vertex_groups = True; mod.use_bone_envelopes = False; mod.use_deform_preserve_volume = False
# ---- shape keys + drivers ----
ob.shape_key_add(name='Basis', from_mix=False); key = me.shape_keys; key.use_relative = True
Bm = {b.name: np.array(b.matrix_local.to_3x3()) for b in ad.bones}
TW = {}                                                      # one driven twist-angle property per (bone, axis) on the mesh object: ob["tw###"] (deg)
def twprop(bone, axis):
    k = bone + '|' + ','.join('%.5f' % x for x in axis)
    if k in TW: return TW[k]
    nm = 'tw%03d' % len(TW); TW[k] = nm; ob[nm] = 0.0; al = Bm[bone].T @ np.asarray(axis, float); al /= np.linalg.norm(al)
    fc = ob.driver_add('["%s"]' % nm); drv = fc.driver; drv.type = 'SCRIPTED'
    for vn, ch in (('qw', 'ROT_W'), ('qx', 'ROT_X'), ('qy', 'ROT_Y'), ('qz', 'ROT_Z')):
        var = drv.variables.new(); var.name = vn; var.type = 'TRANSFORMS'; t = var.targets[0]; t.id = arm; t.bone_target = bone; t.transform_type = ch
        t.transform_space = 'LOCAL_SPACE'; t.rotation_mode = 'QUATERNION'
    drv.expression = '114.591559*atan((%.7f*qx+%.7f*qy+%.7f*qz)/qw)' % tuple(al)
    while fc.modifiers: fc.modifiers.remove(fc.modifiers[0])
    return nm
def keydriver(kb, props, expr):
    fc = kb.driver_add('value'); drv = fc.driver; drv.type = 'SCRIPTED'
    for vn, nm in props:
        var = drv.variables.new(); var.name = vn; var.type = 'SINGLE_PROP'; var.targets[0].id = ob; var.targets[0].data_path = '["%s"]' % nm
    drv.expression = expr; assert len(expr) < 256, expr
    while fc.modifiers: fc.modifiers.remove(fc.modifiers[0])
nkeys = 0
for f in cj['families']:
    bone = f['bone']; nm = twprop(bone, f['axis_parent_frame'])
    samples = [k['sample_deg'] for k in f['keys']]; pts = sorted(samples + [0.0])
    for k in f['keys']:
        s = k['sample_deg']; i = pts.index(s); l = pts[i - 1] if i > 0 else None; r = pts[i + 1] if i + 1 < len(pts) else None
        kb = ob.shape_key_add(name=k['name'], from_mix=False); kb.slider_min = 0.0; kb.slider_max = 1.0; kb.relative_key = key.key_blocks['Basis']
        co = V.copy(); idx = cz[k['name'] + '_idx']; co[idx] += cz[k['name'] + '_d'].astype(np.float64); kb.data.foreach_set('co', co.astype(np.float32).ravel())
        if l is not None and r is not None: e = 'clamp(min((t-(%.5f))/%.5f,(%.5f-t)/%.5f),0,1)' % (l, s - l, r, r - s)
        elif r is None: e = 'clamp((t-(%.5f))/%.5f,0,1)' % (l, s - l)
        else: e = 'clamp((%.5f-t)/%.5f,0,1)' % (r, r - s)
        keydriver(kb, [('t', nm)], e); nkeys += 1
for pk in cj.get('pose_keys', []):
    kb = ob.shape_key_add(name=pk['name'], from_mix=False); kb.slider_min = 0.0; kb.slider_max = 1.0; kb.relative_key = key.key_blocks['Basis']
    co = V.copy(); idx = cz[pk['name'] + '_idx']; co[idx] += cz[pk['name'] + '_d'].astype(np.float64); kb.data.foreach_set('co', co.astype(np.float32).ravel())
    props = []; terms = []
    for j, dr in enumerate(pk['drivers']):
        vn = 'abcdef'[j]; props.append((vn, twprop(dr['bone'], dr['axis_parent_frame']))); terms.append('clamp(1-abs(%s-(%.4f))/%.4f,0,1)' % (vn, dr['sample_deg'], abs(dr['sample_deg'])))
    keydriver(kb, props, '*'.join(terms)); nkeys += 1
# ---- rig-prep action ----
act = bpy.data.actions.new('RIG_PREP'); act.use_fake_user = True
prep = json.load(open(C.EV6 + '/SA_RP6_rig_prep_%s_v001.json' % CFG)) if os.path.exists(C.EV6 + '/SA_RP6_rig_prep_%s_v001.json' % CFG) else None
arm.animation_data_create(); arm.animation_data.action = act
for b in ad.bones: arm.pose.bones[b.name].rotation_mode = 'QUATERNION'
if prep:
    for b, q in prep['basis_quaternions_wxyz'].items():
        pb = arm.pose.bones[b]; pb.rotation_quaternion = q; pb.keyframe_insert('rotation_quaternion', frame=1)
        pb.rotation_quaternion = (1, 0, 0, 0)
arm.animation_data.action = None
for k, v in dict(status='RP6 RIG PILOT / NOT FROZEN', race='Saurin', stage='RP6', configuration='c1 SA-M188' if CFG == 'M' else 'c2 SA-F188', topology_sha256=topo,
                 frozen_source='reviews/rac-rp5-evidence/saurin/full_cage/final_consolidation (SAURIN_RP5_FREEZE.json); RP5 files not modified',
                 weights=os.path.basename(WF), correctives=os.path.basename(CF), skeleton='SA_RP6_skeleton_v001.json', semantic_table=json.dumps(labs),
                 units='mesh / armature data in cm; object scale 0.01 (cm -> m)', frame='x right (+x = subject left, _l), y forward, z up', deformation='linear blend skinning + pose-driven corrective shape keys').items():
    ob[k] = v
arm['status'] = 'RP6 RIG PILOT / NOT FROZEN'; sc['status'] = 'RP6 RIG PILOT / NOT FROZEN'
bpy.ops.wm.save_as_mainfile(filepath=OUT, compress=os.environ.get('BLEND_COMPRESS', '0') == '1')
print(tag, 'saved', os.path.getsize(OUT), 'keys', nkeys, 'groups', len(ob.vertex_groups), 'bones', len(ad.bones))
