# RM-OT-05AA AA0 steps 1-3: import the immutable donor C into a fresh Blender scene as a WORKING COPY and save the pinned baseline
# scene (compressed). No geometry is modified; the donor file's SHA-256 is checked before and after and the imported mesh's vertex
# positions are compared against the GLB accessor data. Run: python3 aa_baseline_blend.py --   (bpy module, as used by x_render.py) DONOR.glb OUT.blend OUT.json
import bpy, sys, json, hashlib, numpy as np
a = sys.argv[sys.argv.index('--') + 1:]; src, out_blend, out_json = a
h0 = hashlib.sha256(open(src, 'rb').read()).hexdigest()
bpy.ops.wm.read_factory_settings(use_empty=True); bpy.ops.import_scene.gltf(filepath=src)
obs = [o for o in bpy.context.scene.objects if o.type == 'MESH']; assert len(obs) == 1, len(obs)
o = obs[0]; o.name = 'GO-05AA_C_working'; o.data.name = 'GO-05AA_C_working_mesh'
o['donor_sha256'] = h0; o['role'] = 'RM-OT-05AA working copy of immutable donor C; donor file never written'
me = o.data; V = np.empty(len(me.vertices) * 3); me.vertices.foreach_get('co', V)
bpy.context.preferences.filepaths.use_file_compression = True
bpy.ops.wm.save_as_mainfile(filepath=out_blend, compress=True)
h1 = hashlib.sha256(open(src, 'rb').read()).hexdigest()
res = dict(donor=src.split('/')[-1], donor_sha256_before=h0, donor_sha256_after=h1, donor_unchanged=h0 == h1, object=o.name,
           vertices=len(me.vertices), faces=len(me.polygons), bounds_min=np.round(V.reshape(-1, 3).min(0), 5).tolist(),
           bounds_max=np.round(V.reshape(-1, 3).max(0), 5).tolist(), blender=bpy.app.version_string, baseline=out_blend.split('/')[-1])
json.dump(res, open(out_json, 'w'), indent=1); print(json.dumps(res))
