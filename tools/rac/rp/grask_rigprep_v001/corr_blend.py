# corr_blend.py (bpy module) -- python3(bpy) corr_blend.py -- RIG.blend RIG.json CORR.npz OUT.blend OUTDIR MODE POSES
# Production-mechanism demonstration of the elbow pose-space corrective (order 6c38d75 §5): the rest-space keys become SHAPE KEYS on the derived
# diagnostic body (the frozen rest mesh / Basis is untouched), each driven by the forearm flexion angle through a Blender driver whose simple
# expression is the same C1 smoothstep partition used by the evaluator. MODE:
#   lbs : armature modifier linear blend      dqs : armature modifier preserve volume (dual quaternion)
# For every pose in POSES the driver-evaluated posed mesh is written to OUTDIR/{pose}.npz (source frame) and the driver weights to OUTDIR/drivers.json.
# OUT.blend (optional, '-' = none) is saved as a NEW derived file with the shape keys + drivers (never the frozen parent).
import bpy, sys, os, json, numpy as np, mathutils
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from diag_lib import Rig, build_poses, rotm, bl_to_src
a = sys.argv[sys.argv.index('--') + 1:]; BL, RJ, CF, OUTB, OD, MODE, POSES = a[:7]
os.environ['ELBOW_SET'] = '1'; os.environ['ELBOW_SET_R'] = '1'; os.environ['ELBOW_ARC'] = '1'
bpy.ops.wm.open_mainfile(filepath=BL); os.makedirs(OD, exist_ok=True)
body = [o for o in bpy.data.objects if o.type == 'MESH'][0]; arm = [o for o in bpy.data.objects if o.type == 'ARMATURE'][0]
rig = Rig(RJ, os.environ.get('WEIGHTS', '/tmp/claude-0/rt/rd/rig/weights_v001c.npz')); P = build_poses(rig)
C = np.load(CF); anchors = [float(x) for x in C['anchors']]
for m in body.modifiers:
    if m.type == 'ARMATURE': m.use_deform_preserve_volume = (MODE == 'dqs')
if not body.data.shape_keys: body.shape_key_add(name='Basis', from_mix=False)
nV = len(body.data.vertices); base = np.empty(nV * 3); body.data.vertices.foreach_get('co', base); base = base.reshape(-1, 3)
def ss_expr(a0, a1): return 'smoothstep(%g, %g, t)' % (a0, a1)
ax_sign = {}
for s in ('l', 'r'):
    ax, sg = rig.choose('forearm_' + s, np.array([0, -1.0, 0]), ('X',))                 # flexion axis of the pose builder (FWD in Blender = -Y)
    ax_sign[s] = (ax, sg)
made = []
for k in range(1, len(anchors)):
    for s in ('l', 'r'):
        key = 'K%d_%s' % (int(anchors[k]), s)
        if key not in C.files: continue
        D = C[key]; Db = np.c_[D[:, 0], -D[:, 1], D[:, 2]] / 100.0                    # source cm vector -> Blender m vector
        sk = body.shape_key_add(name='RAC_DIAG_elbow_%s_flex%d' % (s, int(anchors[k])), from_mix=False); sk.data.foreach_set('co', (base + Db).ravel())
        sk.slider_min = 0.0; sk.slider_max = 1.0
        fc = sk.driver_add('value'); dr = fc.driver; dr.type = 'SCRIPTED'
        v = dr.variables.new(); v.name = 'r'; v.type = 'TRANSFORMS'; tg = v.targets[0]; tg.id = arm; tg.bone_target = 'forearm_' + s
        tg.transform_type = 'ROT_' + ax_sign[s][0]; tg.rotation_mode = 'SWING_TWIST_Y'; tg.transform_space = 'LOCAL_SPACE'
        up = ss_expr(anchors[k - 1], anchors[k]); dn = ss_expr(anchors[k], anchors[k + 1]) if k + 1 < len(anchors) else None
        dr.expression = '(lambda t: %s%s)(abs(degrees(r)))' % (up, (' - ' + dn) if dn else '')
        if True:                                                                       # simple-expression form (no lambda) for portability
            texpr = 'abs(degrees(r))'; e_ = up.replace('t)', texpr + ')') + ((' - ' + dn.replace('t)', texpr + ')')) if dn else '')
            dr.expression = e_
        made.append(dict(shape_key=sk.name, expression=dr.expression, simple_expression=bool(dr.is_simple_expression), variable='forearm_%s local %s (swing-twist)' % (s, 'ROT_' + ax_sign[s][0])))
body['rac_corrective'] = 'DIAGNOSTIC pose-space elbow corrective (shape keys %s), driven by forearm flexion; non-production' % [m['shape_key'] for m in made]
out = dict(shape_keys=made, poses={})
for nm in POSES.split(','):
    for pb in arm.pose.bones: pb.rotation_mode = 'QUATERNION'; pb.rotation_quaternion = (1, 0, 0, 0)
    for n, rots in P[nm].items():
        M = np.eye(3)
        for ax, d in rots: M = M @ rotm(ax, d)
        arm.pose.bones[n].rotation_quaternion = mathutils.Matrix(M.tolist()).to_quaternion()
    bpy.context.view_layer.update(); dg = bpy.context.evaluated_depsgraph_get()
    vals = {kb.name: float(kb.value) for kb in body.data.shape_keys.key_blocks if kb.name != 'Basis'}
    ob = body.evaluated_get(dg); me = ob.to_mesh(); co = np.empty(len(me.vertices) * 3); me.vertices.foreach_get('co', co); ob.to_mesh_clear()
    np.savez_compressed('%s/%s.npz' % (OD, nm), V=bl_to_src(co.reshape(-1, 3)).astype(np.float32)); out['poses'][nm] = vals; print('POSE', nm, vals, flush=True)
for pb in arm.pose.bones: pb.rotation_quaternion = (1, 0, 0, 0)
bpy.context.view_layer.update()
json.dump(out, open(OD + '/drivers.json', 'w'), indent=1)
if OUTB != '-':
    for m in body.modifiers:
        if m.type == 'ARMATURE': m.use_deform_preserve_volume = False
    bpy.ops.wm.save_as_mainfile(filepath=OUTB, compress=True, copy=False); print('SAVED', OUTB)
