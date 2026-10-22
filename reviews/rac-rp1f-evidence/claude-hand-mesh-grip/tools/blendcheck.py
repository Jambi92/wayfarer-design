# blendcheck.py (bpy) -- RIGDIR OUT.json RESULT1.json [RESULT2.json ...] : re-evaluate each solved final pose through Blender's own
# armature modifier (DQS), compare with the solver geometry, check rest recovery and posed bone lengths.
import bpy, sys, json, numpy as np, math, os
a = sys.argv[sys.argv.index('--') + 1:]; rd, outj = a[0], a[1]; files = a[2:]
bpy.ops.wm.open_mainfile(filepath=os.path.join(rd, 'hand_rig_DIAG.blend'))
def ev(ob):
    dg = bpy.context.evaluated_depsgraph_get(); e = ob.evaluated_get(dg); m = e.to_mesh(); P = np.zeros(len(m.vertices) * 3); m.vertices.foreach_get('co', P); e.to_mesh_clear(); return P.reshape(-1, 3)
def setp(ao, ang):
    for pb in ao.pose.bones: pb.rotation_mode = 'XYZ'; pb.rotation_euler = (0, 0, 0)
    for b, (fx, ab, tw) in ang.items(): ao.pose.bones[b].rotation_euler = (math.radians(fx), math.radians(tw), math.radians(ab))
    bpy.context.view_layer.update()
R = {}
for f in files:
    side = 'L' if '_L' in os.path.basename(f) or 'A_L' in os.path.basename(f) else 'R'
    d = json.load(open(f)); ob = bpy.data.objects['GO_hand_%s_DIAG' % side]; ao = bpy.data.objects['GO_hand_%s_RIG' % side]
    setp(ao, {}); P0 = ev(ob); L0 = {pb.name: (pb.tail - pb.head).length for pb in ao.pose.bones}
    setp(ao, d['angles']); P = ev(ob); L1 = {pb.name: (pb.tail - pb.head).length for pb in ao.pose.bones}
    S = np.load(f.replace('.json', '_posed.npy')).astype(float)
    setp(ao, {}); Pr = ev(ob)
    R[os.path.basename(f)] = dict(blender_vs_solver_max_mm=float(np.abs(P - S).max() * 1000), return_to_rest_max_mm=float(np.abs(Pr - P0).max() * 1000),
                                  posed_bone_length_change_max_mm=float(max(abs(L1[k] - L0[k]) for k in L0) * 1000), max_joint_angle_deg=float(max(abs(x) for v in d['angles'].values() for x in v)))
    np.save(f.replace('.json', '_posed_blender.npy'), P.astype(np.float32))
    print(os.path.basename(f), json.dumps(R[os.path.basename(f)]), flush=True)
json.dump(R, open(outj, 'w'), indent=1)
