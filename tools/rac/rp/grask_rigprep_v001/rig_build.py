# rig_build.py (bpy module) -- python3(bpy) rig_build.py -- V003.blend LANDMARKS.json OUT.blend OUT_rig.json OUT_weights.npz
# Derived DIAGNOSTIC rig only. Opens the frozen v003 file read-only, never saves it: the result is written with save_as to a NEW path.
# Armature from the adjudicated landmark package (production frame, Blender metres); diagnostic automatic (bone-heat) weights.
import bpy, sys, os, json, time, numpy as np, mathutils
a = sys.argv[sys.argv.index('--') + 1:]
SRC, LMF, OUT, OUTJ, OUTW = a[:5]
L = json.load(open(LMF))['joints']; B = lambda k: mathutils.Vector(L[k]['position_blender_m'])
bpy.ops.wm.open_mainfile(filepath=SRC)
body = [o for o in bpy.data.objects if o.type == 'MESH'][0]
RV = os.environ.get('RIG_VERSION', 'v001') if 'os' in dir() else 'v001'
body.name = 'GR_U_REF_RP2_rigdiag_%s_body' % RV; body.data.name = body.name
body['rac_status'] = 'DIAGNOSTIC DERIVED COPY (%s) of GR_U_REF_RP2_retopo_v003 (frozen parent untouched). Not production. Diagnostic weights only.' % RV
arm_d = bpy.data.armatures.new('GR_U_REF_RP2_rigdiag_%s_armature' % RV); arm = bpy.data.objects.new('GR_U_REF_RP2_rigdiag_%s_rig' % RV, arm_d)
bpy.context.scene.collection.objects.link(arm); bpy.context.view_layer.objects.active = arm; arm.select_set(True)
bpy.ops.object.mode_set(mode='EDIT'); eb = arm_d.edit_bones
BONES = []   # (name, head_key, tail_key or vector, parent, deform, frame_key)
def add(n, h, t, par, deform=True, fk=None): BONES.append((n, h, t, par, deform, fk or h))
add('root', 'root', ('vec', (0, 0, 0.15)), None, False)
add('pelvis', 'pelvis', 'spine_01', 'root')
chain = ['spine_01', 'spine_02', 'spine_03', 'thoracic_01', 'thoracic_02', 'thoracic_03', 'neck_base', 'head_pivot', 'crown']
prev = 'pelvis'
for i in range(len(chain) - 1):
    n = {'neck_base': 'neck', 'head_pivot': 'head'}.get(chain[i], chain[i]); add(n, chain[i], chain[i + 1], prev); prev = n
for s in 'lr':
    add('eye_' + s, 'eye_' + s, ('fwd', 0.02), 'head', False)
    add('thigh_' + s, 'hip_' + s, 'knee_' + s, 'pelvis'); add('shin_' + s, 'knee_' + s, 'ankle_' + s, 'thigh_' + s); add('foot_' + s, 'ankle_' + s, 'ball_' + s, 'shin_' + s)
    add('hallux_p1_' + s, 'hallux_mtp_' + s, 'hallux_ip_' + s, 'foot_' + s); add('hallux_p2_' + s, 'hallux_ip_' + s, 'hallux_tip_' + s, 'hallux_p1_' + s)
    for t in ('toe2', 'toe3', 'toe4', 'toe5'):
        add('%s_p1_%s' % (t, s), '%s_mtp_%s' % (t, s), '%s_pip_%s' % (t, s), 'foot_' + s); add('%s_p2_%s' % (t, s), '%s_pip_%s' % (t, s), '%s_dip_%s' % (t, s), '%s_p1_%s' % (t, s))
        add('%s_p3_%s' % (t, s), '%s_dip_%s' % (t, s), '%s_tip_%s' % (t, s), '%s_p2_%s' % (t, s))
    add('clavicle_' + s, 'sternoclavicular_' + s, 'glenohumeral_' + s, 'thoracic_03'); add('scapula_' + s, 'scapula_medial_proxy_' + s, 'acromion_' + s, 'clavicle_' + s)
    add('upperarm_' + s, 'glenohumeral_' + s, 'elbow_' + s, 'clavicle_' + s); add('forearm_' + s, 'elbow_' + s, 'wrist_' + s, 'upperarm_' + s)
    add('hand_' + s, 'wrist_' + s, 'middle_mcp_' + s, 'forearm_' + s)
    for f in ('index', 'middle', 'ring', 'pinky'):
        add('%s_p1_%s' % (f, s), '%s_mcp_%s' % (f, s), '%s_pip_%s' % (f, s), 'hand_' + s); add('%s_p2_%s' % (f, s), '%s_pip_%s' % (f, s), '%s_dip_%s' % (f, s), '%s_p1_%s' % (f, s))
        add('%s_p3_%s' % (f, s), '%s_dip_%s' % (f, s), '%s_tip_%s' % (f, s), '%s_p2_%s' % (f, s))
    add('thumb_mc_' + s, 'thumb_cmc_' + s, 'thumb_mcp_' + s, 'hand_' + s); add('thumb_p1_' + s, 'thumb_mcp_' + s, 'thumb_ip_' + s, 'thumb_mc_' + s)
    add('thumb_p2_' + s, 'thumb_ip_' + s, 'thumb_tip_' + s, 'thumb_p1_' + s)
for n, h, t, par, de, fk in BONES:
    b = eb.new(n); b.head = B(h)
    if isinstance(t, tuple): b.tail = B(h) + (mathutils.Vector(t[1]) if t[0] == 'vec' else mathutils.Vector((0, -t[1], 0)))
    else: b.tail = B(t)
    fr = L[fk].get('frame')
    if fr and 'blender_columns_XYZ' in fr: b.align_roll(mathutils.Vector(fr['blender_columns_XYZ'][2]))
    b.use_deform = de; b.use_connect = False
    if par: b.parent = eb[par]
bpy.ops.object.mode_set(mode='OBJECT')
# diagnostic automatic weights (bone heat)
bpy.ops.object.select_all(action='DESELECT'); body.select_set(True); arm.select_set(True); bpy.context.view_layer.objects.active = arm
for vg in list(body.vertex_groups):
    if vg.name.startswith('LOOP_'): continue
t0 = time.time()
import os
if os.environ.get('WEIGHTS_NPZ'):                                   # v002+: assign a logged diagnostic weight array instead of bone heat
    bpy.ops.object.parent_set(type='ARMATURE_NAME'); zw = np.load(os.environ['WEIGHTS_NPZ']); Wn = zw['W']; wn = [str(n) for n in zw['names']]
    for j, n in enumerate(wn):
        vg = body.vertex_groups.get(n) or body.vertex_groups.new(name=n); w = Wn[:, j]; nz = np.nonzero(w > 0)[0]
        for v in nz: vg.add([int(v)], float(w[v]), 'REPLACE')
    body['rac_diag_weights'] = 'assigned from %s' % os.path.basename(os.environ['WEIGHTS_NPZ'])
else:
    bpy.ops.object.parent_set(type='ARMATURE_AUTO')
t1 = time.time()
deform = [b.name for b in arm_d.bones if b.use_deform]
idx = {vg.name: vg.index for vg in body.vertex_groups}
nV = len(body.data.vertices); W = np.zeros((nV, len(deform)), np.float32); col = {n: i for i, n in enumerate(deform)}
gi = {idx[n]: col[n] for n in deform if n in idx}
for v in body.data.vertices:
    for g in v.groups:
        if g.group in gi: W[v.index, gi[g.group]] = g.weight
zero = int((W.sum(1) <= 0).sum()); missing = [n for n in deform if n not in idx or W[:, col[n]].max() == 0]
rig = dict(bones=[dict(name=b.name, parent=b.parent.name if b.parent else None, deform=b.use_deform, head=list(b.head_local), tail=list(b.tail_local),
                       matrix_local=[list(r) for r in b.matrix_local], length=b.length) for b in arm_d.bones],
           deform_order=deform, heat_seconds=t1 - t0, zero_weight_vertices=zero, bones_without_weights=missing)
np.savez_compressed(OUTW, W=W, names=np.array(deform))
json.dump(rig, open(OUTJ, 'w'), indent=1)
bpy.ops.wm.save_as_mainfile(filepath=OUT, compress=True, copy=False)
print('RIG bones', len(arm_d.bones), 'deform', len(deform), 'heat_s %.1f' % (t1 - t0), 'zero_w', zero, 'no_weight_bones', missing)
