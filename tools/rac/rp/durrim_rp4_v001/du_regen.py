# du_regen.py BUILD.json (RP4: regen.py + the native short-adult route for *-NAT records, as native_short.build_native) -- COMMITTED_R6.npz OUTDIR : RP3 (order d18ff2a §4) -- regenerate an accepted MPFB Marchfolk source from its committed build
# record with the recorded route (tools/rac/w1/build_variant.py "height macro held from base", MPFB 2.0.17, Blender 5.2.2), pose R-6, export the R-6 npz
# exactly as arm_lib.export, and prove geometry identity with the committed R-6 asset: sha256(float32 V bytes + int32 F bytes).
# Also saves the regenerated source scene (rig + quad body with helpers, UVs, groups, shape keys) as OUTDIR/<id>_regen_source.blend -- a regenerated
# SOURCE (read-only truth, never edited); production copies are derived from it by make_prod.py.
import sys, os, json, hashlib
sys.path.insert(0, '/home/claude/wayfarer-design/tools/rac/w1')
import numpy as np
import arm_lib as A
import native_short as N
bpy = A.bpy
BJ, CR, O = sys.argv[sys.argv.index('--') + 1:][:3] if '--' in sys.argv else sys.argv[1:4]
os.makedirs(O, exist_ok=True); base = json.load(open(BJ)); cfg = dict(base['cfg']); cid = base['id']
def gh(V, F): return hashlib.sha256(np.ascontiguousarray(V, np.float32).tobytes() + np.ascontiguousarray(F, np.int32).tobytes()).hexdigest()
c = dict(cfg); c['height_macro'] = base['height_macro']
b, r = A.build(c)
if "native_factors" in base:   # recorded regional factors on the base macro, baked into the rest mesh
    N.set_factors(r, base["native_factors"]); A.bake(b, r)
A.ground(b, r)
pose = A.pose_r6(r); A.ground(b, r)
p = os.path.join(O, cid + '_r6_regen.npz'); A.export(b, r, p, {'id': cid, 'state': 'R-6', 'pose': pose, 'regenerated_by': 'rp3 regen.py'})
z0 = np.load(CR); z1 = np.load(p)
rec = dict(id=cid, build=os.path.basename(BJ), build_sha256=hashlib.sha256(open(BJ, 'rb').read()).hexdigest(), committed=os.path.basename(CR),
           committed_sha256=hashlib.sha256(open(CR, 'rb').read()).hexdigest(), committed_geom=gh(z0['V'], z0['F']), regen_geom=gh(z1['V'], z1['F']),
           pose_record=base.get('pose'), pose_regen=pose, stature_record=base.get('stature_r6'), stature_regen=float(A.stature(b)),
           max_abs_dV_cm=float(np.abs(z0['V'].astype(float) - z1['V'].astype(float)).max()), faces_identical=bool((z0['F'] == z1['F']).all()))
rec['geometry_identical'] = rec['committed_geom'] == rec['regen_geom']
bpy.ops.wm.save_as_mainfile(filepath=os.path.join(O, cid + '_regen_source.blend'), compress=True)
rec['regen_source_blend_sha256'] = hashlib.sha256(open(os.path.join(O, cid + '_regen_source.blend'), 'rb').read()).hexdigest()
json.dump(rec, open(os.path.join(O, cid + '_regen_check.json'), 'w'), indent=1); print('REGEN', json.dumps(rec))
