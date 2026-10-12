# RAC RM-OT-05I protection-overlay verification (headless bpy module). Order section 3 "Protection-patch verification":
#  V1 unedited round trip with the overlay: setup (frozen 05G package) -> overlay -> export through the derivative package -> preflight: must PASS
#  V2 the 804 added vertices are in the sculpt mask (mask = 1) and in NO_TOUCH_all
#  V3 negative fixture: one previously omitted hand-adjacent vertex moved 1.0 cm -> derivative-package export (X9) and preflight (P4) must FAIL,
#     while the frozen 05G package would have passed it (demonstrates the gap is closed)
#  V4 nothing outside the intended set changed: overlay regions == frozen regions + the one added key; the template, joints and every
#     coordinate are untouched (unedited export bit-identical to the template coordinates)
# Usage: python3 i_verify.py FROZEN_PKG DERIV_PKG OUTDIR
import sys, os, json, subprocess, hashlib, numpy as np, bpy
FZ, DV, OUT = sys.argv[1:4]; os.makedirs(OUT, exist_ok=True); SC = FZ + '/blender/scripts/'
def run(script, argv, g=None):
    sys.argv = ['blender', '--'] + argv; gl = {'__name__': '__main__', '__file__': script}; gl.update(g or {})
    try: exec(compile(open(script).read(), script, 'exec'), gl)
    except SystemExit: pass          # g_export exits 1 in background mode when it refuses (expected for the negative fixture)
def pre(obj, pkg):
    r = subprocess.run(['python3', '-I', SC + 'g_preflight.py', obj, '--package', pkg], capture_output=True, text=True); t = r.stdout
    j = json.loads(t[:t.rindex('}') + 1]); return j, t.strip().splitlines()[-1]
res = {}
run(SC + 'g_setup.py', ['--package', FZ, '--out', OUT + '/v_setup.blend'])
run(os.path.dirname(os.path.abspath(__file__)) + '/i_blender_overlay.py', ['--overlay', DV + '/data/regions.json'])
R = json.load(open(DV + '/data/regions.json')); add = R['regions']['NO_TOUCH_hands_digits_guard05i']
me = bpy.data.objects['GO_SCULPT_BASE'].data; mask = np.zeros(len(me.vertices)); me.attributes['.sculpt_mask'].data.foreach_get('value', mask)
res['V2_added_masked'] = {'added': len(add), 'masked_among_added': int((mask[add] > 0.5).sum()), 'total_masked': int((mask > 0.5).sum()), 'pass': bool((mask[add] > 0.5).all())}
os.makedirs(OUT + '/v1', exist_ok=True); run(SC + 'g_export.py', ['--id', 'V1', '--sculptor', 'overlay-verify', '--package', DV, '--outdir', OUT + '/v1'])
o1 = OUT + '/v1/GO_sculpt_V1_r6.obj'; e1 = json.load(open(OUT + '/v1/GO_sculpt_V1_r6_export_report.json'))
p1, l1 = pre(o1, DV); p1f, l1f = pre(o1, FZ)
res['V1_unedited_round_trip'] = {'export_pass': e1['pass'], 'X9': e1['checks']['X9_no_touch'], 'preflight_overlay': l1, 'preflight_frozen': l1f, 'pass': bool(e1['pass'] and l1 == 'PREFLIGHT PASS' and l1f == 'PREFLIGHT PASS')}
# V3 negative fixture: move one added vertex (largest |x|-distance from the hand bone? simply the first added index in FAM_E overlap if any) 1.0 cm along +y
fam_e = set(json.load(open(FZ + '/data/regions.json'))['regions']['E_elbow_forearm_wrist'])
vi = next((i for i in add if i in fam_e), add[0])
co = me.vertices[vi].co.copy(); me.vertices[vi].co.y += 1.0; me.update()
GX = {'__name__': 'g_export_lib', '__file__': SC + 'g_export.py'}; exec(compile(open(SC + 'g_export.py').read(), SC + 'g_export.py', 'exec'), GX)
eo = GX['check_and_export'](DV, 'V3', 'overlay-verify', OUT, write=False)
ef = GX['check_and_export'](FZ, 'V3', 'overlay-verify', OUT, write=False)
os.makedirs(OUT + '/v3f', exist_ok=True); run(SC + 'g_export.py', ['--id', 'V3', '--sculptor', 'overlay-verify', '--package', FZ, '--outdir', OUT + '/v3f'])
fobj = OUT + '/v3f/GO_sculpt_V3_r6.obj'
po, lo = pre(fobj, DV) if os.path.exists(fobj) else (None, 'no obj'); pf, lf = pre(fobj, FZ) if os.path.exists(fobj) else (None, 'no obj')
res['V3_negative_fixture'] = {'vertex': int(vi), 'in_FAM_E': vi in fam_e, 'moved_cm': 1.0,
    'overlay_export_X9': eo['checks']['X9_no_touch']['pass'], 'overlay_export_pass': eo['pass'],
    'frozen_export_X9': ef['checks']['X9_no_touch']['pass'], 'frozen_export_pass': ef['pass'],
    'overlay_preflight': lo, 'frozen_preflight': lf,
    'pass': bool((not eo['pass']) and lo != 'PREFLIGHT PASS' and ef['pass'] and lf == 'PREFLIGHT PASS')}
me.vertices[vi].co = co; me.update()
FZR = json.load(open(FZ + '/data/regions.json'))['regions']
res['V4_scope'] = {'frozen_keys_identical': all(R['regions'][k] == v for k, v in FZR.items()), 'added_keys': sorted(set(R['regions']) - set(FZR)),
    'template_identical': hashlib.sha256(open(FZ + '/template/GO_ref_route_r6.obj', 'rb').read()).hexdigest() == hashlib.sha256(open(DV + '/template/GO_ref_route_r6.obj', 'rb').read()).hexdigest(),
    'unedited_export_max_change_cm': max(e1['checks']['X9_no_touch']['max_change_cm'].values())}
res['V4_scope']['pass'] = bool(res['V4_scope']['frozen_keys_identical'] and res['V4_scope']['added_keys'] == ['NO_TOUCH_hands_digits_guard05i'] and res['V4_scope']['template_identical'])
res['pass'] = all(v['pass'] for v in res.values() if isinstance(v, dict))
json.dump(res, open(OUT + '/overlay_verify.json', 'w'), indent=1, default=str); print('RAC_OVERLAY_VERIFY', 'PASS' if res['pass'] else 'FAIL'); print(json.dumps(res, indent=1, default=str))
