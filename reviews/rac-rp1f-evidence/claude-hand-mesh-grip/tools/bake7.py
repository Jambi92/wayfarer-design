# bake7.py (bpy python) -- RIGDIR OUT.blend MANIFEST.json SIDE
# Diagnostic rig file for ONE hand with every validated test baked in. The hand crop is split into two objects that
# share the armature and weights: GO_hand_<S>_DIAG (no shape keys) and GO_hand_<S>_DIAG_CORR (the vertices any
# soft-tissue corrective touches, + 3 rings; it carries the corrective shape keys). Both carry an int attribute
# 'orig_id' = vertex index in the full crop, so the full posed mesh can be reassembled for checking. The seam
# vertices are uncorrected and deform identically in both objects.
#   * armature Action TEST_<name> keyed at every solved frame (frame i+1 = solver frame i)
#   * shape keys C_<name>_<k> (rest-space corrective basis chosen by keyverify.py) on the _CORR object and a
#     shape-key Action KEYS_<name> keyed per frame with the verified blend weights
#   * coin / handle fixtures (hidden)
import bpy, bmesh, sys, json, os, math, numpy as np, mathutils
a = sys.argv[sys.argv.index('--') + 1:]; rd, outb, manf, S = a[:4]
M = [t for t in json.load(open(manf)) if t['side'] == S]
bpy.ops.wm.open_mainfile(filepath=os.path.join(rd, 'hand_rig_DIAG.blend'))
bpy.context.preferences.edit.keyframe_new_interpolation_type = 'LINEAR'
O = 'L' if S == 'R' else 'R'
for nm in ('GO_hand_%s_DIAG' % O, 'GO_hand_%s_RIG' % O):
    bpy.data.objects.remove(bpy.data.objects[nm], do_unlink=True)
ob = bpy.data.objects['GO_hand_%s_DIAG' % S]; ao = bpy.data.objects['GO_hand_%s_RIG' % S]; me = ob.data; nV = len(me.vertices)
# corrective support per side
sup = np.zeros(nV, bool); KEYS = {}
for t in M:
    if t.get('keys') and os.path.exists(t['keys']):
        Z = np.load(t['keys']); KEYS[t['name']] = Z
        for k in Z['keys']:
            if len(Z['i%d' % k]): sup[Z['i%d' % k]] = True
Q = np.zeros(len(me.polygons) * 4, int); me.polygons.foreach_get('vertices', Q); Q = Q.reshape(-1, 4)
zone = sup.copy()
for r in range(3): zone[np.unique(Q[zone[Q].any(1)])] = True
fz = zone[Q].all(1)                      # faces of the corrective object
at = me.attributes.new('orig_id', 'INT', 'POINT'); at.data.foreach_set('value', np.arange(nV, dtype=np.int32))
oc = ob.copy(); oc.data = ob.data.copy(); oc.name = 'GO_hand_%s_DIAG_CORR' % S; oc.data.name = oc.name; bpy.context.scene.collection.objects.link(oc)
def keep_faces(o, mask):
    bm = bmesh.new(); bm.from_mesh(o.data); bm.faces.ensure_lookup_table()
    bmesh.ops.delete(bm, geom=[f for f in bm.faces if not mask[f.index]], context='FACES')
    loose = [v for v in bm.verts if not v.link_faces]; bmesh.ops.delete(bm, geom=loose, context='VERTS')
    bm.to_mesh(o.data); bm.free(); o.data.update()
keep_faces(oc, fz); keep_faces(ob, ~fz)
def ids(o):
    v = np.zeros(len(o.data.vertices), np.int32); o.data.attributes['orig_id'].data.foreach_get('value', v); return v
idc = ids(oc); pos = -np.ones(nV, int); pos[idc] = np.arange(len(idc))
print('zone verts', len(idc), 'of', nV, 'support', int(sup.sum()), flush=True)
oc.shape_key_add(name='Basis', from_mix=False)
basis = np.zeros(len(oc.data.vertices) * 3); oc.data.shape_keys.key_blocks['Basis'].data.foreach_get('co', basis); basis = basis.reshape(-1, 3)
key = oc.data.shape_keys; key.animation_data_create()
for t in M:
    d = json.load(open(t['out'])); FR = d['frames']; nF = len(FR)
    act = bpy.data.actions.new('TEST_' + t['name']); act.use_fake_user = True
    ao.animation_data_create(); ao.animation_data.action = act
    for pb in ao.pose.bones: pb.rotation_mode = 'XYZ'
    for i, f in enumerate(FR):
        ang = f['angles']
        for pb in ao.pose.bones:
            v = ang.get(pb.name, [0, 0, 0]); pb.rotation_euler = (math.radians(v[0]), math.radians(v[2]), math.radians(v[1]))
            pb.keyframe_insert('rotation_euler', frame=i + 1)
    ao.animation_data.action = None
    nk = 0
    if t['name'] in KEYS:
        Z = KEYS[t['name']]; Wt = json.load(open(t['kv']))['weights']
        kact = bpy.data.actions.new('KEYS_' + t['name']); kact.use_fake_user = True; key.animation_data.action = kact
        for k in [int(k) for k in Z['keys'] if len(Z['i%d' % k])]:
            vi = Z['i%d' % k]; assert (pos[vi] >= 0).all()
            sk = oc.shape_key_add(name='C_%s_%03d' % (t['name'], k), from_mix=False); co = basis.copy(); co[pos[vi]] += Z['o%d' % k]
            sk.data.foreach_set('co', co.astype(np.float32).ravel()); sk.slider_max = 10.0
            for i in range(nF):
                sk.value = float(Wt[str(i)].get(str(k), 0.0)); sk.keyframe_insert('value', frame=i + 1)
            sk.value = 0.0; nk += 1
        key.animation_data.action = None
    print(t['name'], 'frames', nF, 'corrective keys', nk, flush=True)
    for fxn in ('coin', 'handle'):
        if t.get(fxn):
            fx = json.load(open(t[fxn])); c = np.array(fx['c']) / 100; ax = np.array(fx['ax'], float); ax /= np.linalg.norm(ax)
            bpy.ops.mesh.primitive_cylinder_add(radius=fx['r'] / 100, depth=2 * fx['hl'] / 100, location=c, vertices=64)
            o = bpy.context.object; o.name = 'FIXTURE_%s_%s' % (fxn, S); o.rotation_mode = 'QUATERNION'; o.rotation_quaternion = mathutils.Vector((0, 0, 1)).rotation_difference(mathutils.Vector(ax)); o.hide_set(True)
bpy.context.scene['status'] = ('DIAGNOSTIC %s-hand rig + validated test sequences. Per test: armature Action TEST_<name> on GO_hand_%s_RIG and shape-key '
                               'Action KEYS_<name> on GO_hand_%s_DIAG_CORR (soft-tissue correctives). Not a game rig, not frozen.' % (S, S, S))
bpy.ops.wm.save_as_mainfile(filepath=outb, compress=True)
print('saved', outb, os.path.getsize(outb))
