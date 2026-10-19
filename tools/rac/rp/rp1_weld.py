"""RAC RP1-A: derived welded working copy of the frozen Gorrund source (contract §1.4, RP1 D-4).
Opens the source read-only, merges coincident positions (UV-seam split duplicates; distance 1e-6 m), and saves a NEW file.
Positions are not moved (merge keeps one of identical positions). The source file is never written.
Usage: blender -b --python rp1_weld.py -- SRC.blend OUT.blend   (or bpy module: python3 rp1_weld.py SRC OUT)"""
import bpy, bmesh, sys, numpy as np, json
a = sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else sys.argv[-2:]
src, out = a[0], a[1]
bpy.ops.wm.open_mainfile(filepath=src)
o = [x for x in bpy.data.objects if x.type == 'MESH'][0]; me = o.data
V0 = np.zeros(len(me.vertices) * 3); me.vertices.foreach_get('co', V0); V0 = V0.reshape(-1, 3)
bm = bmesh.new(); bm.from_mesh(me)
r = bmesh.ops.remove_doubles(bm, verts=bm.verts, dist=1e-6)
bm.to_mesh(me); bm.free(); me.update()
V1 = np.zeros(len(me.vertices) * 3); me.vertices.foreach_get('co', V1); V1 = V1.reshape(-1, 3)
from scipy.spatial import cKDTree
d, _ = cKDTree(V0).query(V1)
o.name = 'GO_U_REF_RP1_weldsrc'; me.name = 'GO_U_REF_RP1_weldsrc'
bpy.ops.wm.save_as_mainfile(filepath=out, compress=True, copy=True)
print('WELD', json.dumps({'verts_in': len(V0), 'verts_out': len(V1), 'max_position_change_m': float(d.max()), 'polys': len(me.polygons)}))
