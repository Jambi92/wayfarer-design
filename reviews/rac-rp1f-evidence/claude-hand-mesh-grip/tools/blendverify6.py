# blendverify6.py (bpy python) -- RIGDIR BAKED.blend MANIFEST.json OUT.json [frame_stride]
# Re-open the saved baked diagnostic file and, for every test and every solved frame, evaluate the mesh through
# Blender itself (armature DQS + corrective shape keys from the test's Actions), then re-run the intersection /
# claw / fixture checks on that Blender geometry; also checks return to rest and posed bone lengths.
import sys, json, numpy as np, os, math
a = sys.argv[sys.argv.index('--') + 1:]; rd, blend, manf, outj = a[:4]; stride = int(a[4]) if len(a) > 4 else 1
M = json.load(open(manf)); res = {}
import bpy
from mathutils.bvhtree import BVHTree
def ids(o):
    v = np.zeros(len(o.data.vertices), np.int32); o.data.attributes['orig_id'].data.foreach_get('value', v); return v
def evfull(side, n):
    P = np.zeros((n, 3)); 
    for nm in ('GO_hand_%s_DIAG' % side, 'GO_hand_%s_DIAG_CORR' % side):
        o = bpy.data.objects.get(nm)
        if o is None: continue
        P[ids(o)] = ev(o)
    return P
def ev(ob):
    dg = bpy.context.evaluated_depsgraph_get(); e = ob.evaluated_get(dg); m = e.to_mesh(); P = np.zeros(len(m.vertices) * 3); m.vertices.foreach_get('co', P); e.to_mesh_clear(); return P.reshape(-1, 3)
for t in M:
    side = t['side']
    src = open('/tmp/claude-0/hand/tools/gripsolve2.py').read(); src = src[:src.index("PH = T['phases']")]
    sys.argv = ['x', '--', rd, side, t['task'], '/tmp/_bv.json']; G = {}
    exec(src, G)
    bpy.ops.wm.open_mainfile(filepath=blend % side if '%s' in blend else blend); nfull = len(G['H'].P0)
    ob = bpy.data.objects['GO_hand_%s_DIAG_CORR' % side]; ao = bpy.data.objects['GO_hand_%s_RIG' % side]
    ao.animation_data_create(); ao.animation_data.action = None
    for pb in ao.pose.bones: pb.rotation_mode = 'XYZ'; pb.rotation_euler = (0, 0, 0)
    bpy.context.view_layer.update(); P0 = evfull(side, nfull); L0 = {pb.name: (pb.tail - pb.head).length for pb in ao.pose.bones}
    ao.animation_data.action = bpy.data.actions['TEST_' + t['name']]
    key = ob.data.shape_keys
    if 'KEYS_' + t['name'] in bpy.data.actions and key is not None:
        key.animation_data_create(); key.animation_data.action = bpy.data.actions['KEYS_' + t['name']]
    d = json.load(open(t['out'])); nF = len(d['frames']); worst = dict(skin_mm=0.0, claw_mm=0.0, fixture_pen_mm=0.0, bad_frames=0, bone_len_mm=0.0)
    for i in list(range(0, nF, stride)) + ([nF - 1] if (nF - 1) % stride else []):
        bpy.context.scene.frame_set(i + 1); P = evfull(side, nfull)
        pr = G['selfx'](P); new = np.array(sorted(set(map(tuple, pr.tolist())) - G['rest']), int).reshape(-1, 2)
        dep = G['depths'](P, new); isc = (G['kerq'][new[:, 0]] | G['kerq'][new[:, 1]]) if len(new) else np.zeros(0, bool)
        sk = float(dep[~isc].max() * 1000) if (~isc).any() else 0.0; cl = float(dep[isc].max() * 1000) if isc.any() else 0.0
        bad = (sk > G['SKIN_TOL'] * 1000 + 1e-6) or (cl > G['CLAW_TOL'] * 1000 + 1e-6)
        if G['T'].get('fixture'):
            sd = G['fixture_sd'](P, G['T']['fixture']); fp = float(max(0.0, -sd.min()) * 1000); worst['fixture_pen_mm'] = max(worst['fixture_pen_mm'], fp); bad = bad or fp > G['FIX_TOL'] * 1000 + 1e-6
        worst['skin_mm'] = max(worst['skin_mm'], sk); worst['claw_mm'] = max(worst['claw_mm'], cl); worst['bad_frames'] += int(bad)
        L1 = {pb.name: (pb.tail - pb.head).length for pb in ao.pose.bones}; worst['bone_len_mm'] = max(worst['bone_len_mm'], max(abs(L1[k] - L0[k]) for k in L0) * 1000)
        if i == nF - 1:
            S = np.load(t['out'].replace('.json', '_posed.npy')).astype(float); worst['final_vs_solver_mm'] = float(np.abs(P - S).max() * 1000)
    ao.animation_data.action = None
    if key is not None and key.animation_data: key.animation_data.action = None
    for kb in (key.key_blocks if key else []): kb.value = 0.0
    for pb in ao.pose.bones: pb.rotation_euler = (0, 0, 0)
    bpy.context.view_layer.update(); Pr = evfull(side, nfull); worst['return_to_rest_mm'] = float(np.abs(Pr - P0).max() * 1000); worst['frames'] = nF
    res[t['name']] = worst; print(t['name'], json.dumps(worst), flush=True)
json.dump(res, open(outj, 'w'), indent=1)
