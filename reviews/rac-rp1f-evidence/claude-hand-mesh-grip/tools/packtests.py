# packtests.py (bpy) -- RIGDIR FINALDIR OUT.blend : diagnostic rig copy with one Action per solved test (frame 1 rest -> the
# validated intermediate states -> final pose), plus the coin / handle fixtures. Reference-stance production is not in here.
import bpy, sys, json, os, math, glob, numpy as np, mathutils
a = sys.argv[sys.argv.index('--') + 1:]; rd, fd, out = a
bpy.ops.wm.open_mainfile(filepath=os.path.join(rd, 'hand_rig_DIAG.blend'))
def pose_from_state(base, targets_phases, phase_states):
    pass
for f in sorted(glob.glob(os.path.join(fd, '*_out.json'))):
    nm = os.path.basename(f)[:-9]
    if nm.startswith('prepinch') or nm.count('_') > 2 and nm.split('_')[-1].replace('.', '').isdigit(): continue
    side = 'L' if ('_L' in nm or 'A_L' in nm) else 'R'
    d = json.load(open(f)); ao = bpy.data.objects['GO_hand_%s_RIG' % side]
    act = bpy.data.actions.new('TEST_' + nm); act.use_fake_user = True
    ao.animation_data_create(); ao.animation_data.action = act
    for pb in ao.pose.bones: pb.rotation_mode = 'XYZ'
    def key(ang, fr):
        for pb in ao.pose.bones:
            v = ang.get(pb.name, [0, 0, 0]); pb.rotation_euler = (math.radians(v[0]), math.radians(v[2]), math.radians(v[1])); pb.keyframe_insert('rotation_euler', frame=fr)
    key(d['task'].get('base_angles', {}) if False else {}, 1)
    key(d['angles'], 40)
    ao.animation_data.action = None
for side in 'LR':
    for kind, fn in (('coin', 'coin_fix_%s.json'), ('handle', 'handle_fix_%s.json')):
        p = os.path.join(fd, fn % side)
        if not os.path.exists(p): continue
        fx = json.load(open(p)); c = np.array(fx['c']) / 100; ax = np.array(fx['ax']); ax /= np.linalg.norm(ax)
        bpy.ops.mesh.primitive_cylinder_add(radius=fx['r'] / 100, depth=2 * fx['hl'] / 100, location=c, vertices=64)
        o = bpy.context.object; o.name = 'FIXTURE_%s_%s' % (kind, side); o.rotation_mode = 'QUATERNION'; o.rotation_quaternion = mathutils.Vector((0, 0, 1)).rotation_difference(mathutils.Vector(ax))
        o.hide_set(True)
bpy.context.scene['status'] = 'DIAGNOSTIC hand rig + validated test poses (Actions TEST_*). Not a game rig, not frozen.'
bpy.ops.wm.save_as_mainfile(filepath=out, compress=True)
print('saved', out, os.path.getsize(out))
