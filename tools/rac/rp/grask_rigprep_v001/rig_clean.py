# rig_clean.py (bpy module) -- python3(bpy) rig_clean.py -- RIGDIAG.blend OUT_weights.npz OUT_log.json
# Minimal, logged diagnostic-weight cleanup IN THE DIAGNOSTIC COPY ONLY: bone-heat leaked side-specific bones across the midline
# (thigh / clavicle / scapula / upper arm onto the opposite groin, sternum and upper back). Rule: a side bone keeps no weight on
# vertices more than 3 cm across the midline (x_analysis * side_sign < -3 cm); remaining weights are left as computed.
import bpy, sys, json, numpy as np
a = sys.argv[sys.argv.index('--') + 1:]
bpy.ops.wm.open_mainfile(filepath=a[0])
body = [o for o in bpy.data.objects if o.type == 'MESH'][0]; arm = [o for o in bpy.data.objects if o.type == 'ARMATURE'][0]
deform = [b.name for b in arm.data.bones if b.use_deform]
co = np.empty(len(body.data.vertices) * 3); body.data.vertices.foreach_get('co', co); X = co.reshape(-1, 3)[:, 0] * 100   # Blender x = analysis x
removed = {}; vids_all = np.arange(len(X))
for n in deform:
    if not (n.endswith('_l') or n.endswith('_r')): continue
    sg = 1 if n.endswith('_l') else -1; vg = body.vertex_groups[n]
    bad = vids_all[(X * sg) < -3.0].tolist(); cnt = 0; mx = 0.0
    for vi in bad:
        try: w = vg.weight(vi)
        except RuntimeError: continue
        mx = max(mx, w); cnt += 1
    if cnt: vg.remove(bad); removed[n] = dict(vertices=cnt, max_weight_removed=mx)
idx = {vg.name: vg.index for vg in body.vertex_groups}; col = {n: i for i, n in enumerate(deform)}; gi = {idx[n]: col[n] for n in deform}
W = np.zeros((len(X), len(deform)), np.float32)
for v in body.data.vertices:
    for g in v.groups:
        if g.group in gi: W[v.index, gi[g.group]] = g.weight
zero = int((W.sum(1) <= 0).sum())
body['rac_diag_weight_cleanup'] = 'side bones zeroed > 3 cm across the midline (see rig manifest)'
bpy.ops.wm.save_as_mainfile(filepath=a[0], compress=True)
np.savez_compressed(a[1], W=W, names=np.array(deform)); json.dump(dict(rule='side bones: weight removed where x*side < -3 cm', removed=removed, zero_weight_vertices_after=zero), open(a[2], 'w'), indent=1)
print('CLEAN bones', len(removed), 'zero_after', zero)
