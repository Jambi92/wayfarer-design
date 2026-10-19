"""RAC RP1-D: self-intersection count of the production object (bpy BVH overlap, pairs that share no vertex), read-only.
Usage: blender-python rp1_selfx.py -- PRODUCTION.blend OBJECT OUT.json"""
import sys, json, bpy, bmesh
from mathutils.bvhtree import BVHTree
a = sys.argv[sys.argv.index('--') + 1:]; path, name, out = a
bpy.ops.wm.open_mainfile(filepath=path)
o = bpy.data.objects[name]; bm = bmesh.new(); bm.from_mesh(o.data); bm.faces.ensure_lookup_table()
t = BVHTree.FromBMesh(bm, epsilon=0.0)
pairs = t.overlap(t); bad = []
for i, j in pairs:
    if i >= j: continue
    vi = {v.index for v in bm.faces[i].verts}; vj = {v.index for v in bm.faces[j].verts}
    if vi & vj: continue
    bad.append((i, j))
import numpy as np; cent = np.array([list(bm.faces[i].calc_center_median()) for i, _ in bad]) if bad else np.zeros((0, 3)); np.save(out.replace(".json", "_centres.npy"), cent)
json.dump({'self_intersecting_face_pairs': len(bad), 'sample_centres_m': cent[:200].tolist()}, open(out, 'w'), indent=1)
print('SELFX', len(bad))
