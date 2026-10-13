# RM-OT-05T recommended export (the ONLY supported export path for the direct-sculpt return).
# Run inside Blender (Scripting tab -> open this file -> Run) or headless:
#   python3 t_export_blend.py --blend GO-05T_sculpt_handoff.blend --out RETURN_PREFIX      (bpy module)
#   blender -b GO-05T_sculpt_handoff.blend --python t_export_blend.py -- --out RETURN_PREFIX   (Blender app)
# Writes RETURN_PREFIX.npz (exact float32 vertex positions as stored by Blender, triangle faces, rac_s3_vid1 identity,
# triangulation flag) and RETURN_PREFIX.obj (%.9g, no axis conversion, for viewing). Quads / n-gons made during the
# edit are triangulated on a temporary copy (beauty) and reported; the scene is not modified.
import sys, os, json, numpy as np, bpy, bmesh
argv = sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else sys.argv[1:]
import argparse
ap = argparse.ArgumentParser(); ap.add_argument('--blend', default=None); ap.add_argument('--out', required=True); ap.add_argument('--object', default='GO-05S-S3_working'); a = ap.parse_args(argv)
if a.blend: bpy.ops.wm.open_mainfile(filepath=os.path.abspath(a.blend))
ob = bpy.data.objects[a.object]
if ob.mode != 'OBJECT': bpy.ops.object.mode_set(mode='OBJECT')
assert ob.data.library is None and len(ob.modifiers) == 0, 'working object must be local and have no modifiers (apply or remove them first)'
mw = np.array(ob.matrix_world); ident = bool(np.allclose(mw, np.eye(4)))
bm = bmesh.new(); bm.from_mesh(ob.data); ngon = sum(1 for f in bm.faces if len(f.verts) != 3)
if ngon: bmesh.ops.triangulate(bm, faces=[f for f in bm.faces if len(f.verts) != 3], quad_method='BEAUTY', ngon_method='BEAUTY')
lay = bm.verts.layers.int.get('rac_s3_vid1'); assert lay is not None, 'rac_s3_vid1 attribute missing'
bm.verts.ensure_lookup_table(); bm.faces.ensure_lookup_table()
V = np.array([v.co[:] for v in bm.verts], np.float32); ids = np.array([v[lay] for v in bm.verts], np.int64)
F = np.array([[v.index for v in f.verts] for f in bm.faces], np.int64); bm.free()
np.savez(a.out + '.npz', V=V, F=F, s3_vid1=ids, matrix_world=mw, identity_transform=ident, triangulated_ngons=ngon, blend=bpy.data.filepath)
with open(a.out + '.obj', 'w') as fh:
    fh.write('# RM-OT-05T return export (float32 positions printed with %.9g; identity in the .npz)\n')
    np.savetxt(fh, V.astype(np.float64), fmt='v %.9g %.9g %.9g'); np.savetxt(fh, F + 1, fmt='f %d %d %d')
print(json.dumps(dict(out=a.out, vertices=int(len(V)), faces=int(len(F)), identity_transform=ident, triangulated_ngons=int(ngon), new_vertices=int((ids == 0).sum()))))
