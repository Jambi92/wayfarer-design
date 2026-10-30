# cg_native_c2.py CFG.json OUTDIR : RP4 Cogling c2 technical anchor (order 9424c72 §4) on the accepted native short-adult route (tools/rac/w1/native_short.py)
# with the Cogling HEAD FACTOR copied exactly from CGJ7 (cfg 'head_factor', CGJ7 build native_factors.head) instead of re-solving a head height.
# Reason: native_short's head_HH() quick check uses absolute-cm chin windows that read the configuration-2 head differently from the measured HH
# (a solve to 12 cm gave a measured 12.83 cm c2 head vs 11.81 cm c1 = a Cogling-specific +8.6 % head shift, which §4 forbids). Copying the CGJ7 factor
# keeps the Cogling head intent and leaves any c2 / c1 head difference to the MPFB configuration-2 base itself, as on Marchfolk.
import sys, os, json
sys.path.insert(0, '/home/claude/wayfarer-design/tools/rac/w1')
import native_short as N
A = N.A
cfgp, out = sys.argv[1:3]; cfg = json.load(open(cfgp)); tag = cfg['id'] + '-NAT'; HF = float(cfg['head_factor'])
betas = json.load(open('/home/claude/wayfarer-design/tools/rac/w1/native_short_allometry.json'))['betas']; target = cfg['stature']
def stat(k):
    b, r, f = N.build_native(cfg, betas, k, HF); A.pose_r6(r); A.ground(b, r); return A.stature(b)
k0, k1 = target / 173.0, target / 173.0 * 1.02; h0, h1 = stat(k0), stat(k1)
for it in range(12):
    k2 = k1 + (target - h1) * (k1 - k0) / (h1 - h0); h2 = stat(k2); k0, h0, k1, h1 = k1, h1, k2, h2
    if abs(h2 - target) < 0.02: break
b, r, f = N.build_native(cfg, betas, k1, HF)
meta = {'id': tag, 'inputs': cfg, 'native_factors': f, 'betas': betas, 'state': 'rest (re-proportioned, baked)', 'method': 'regional re-proportioning at target stature (no global uniform scale); head factor = CGJ7'}
A.export(b, r, os.path.join(out, tag + '_rest.npz'), meta)
pose = A.pose_r6(r); A.ground(b, r); meta.update({'state': 'R-6', 'pose': pose}); A.export(b, r, os.path.join(out, tag + '_r6.npz'), meta)
rec = {'id': tag, 'cfg': cfg, 'height_macro': cfg.get('base_height_macro', 0.5), 'native_factors': f, 'betas': betas, 'stature_r6': A.stature(b), 'iters': it + 1, 'pose': pose}
json.dump(rec, open(os.path.join(out, tag + '_build.json'), 'w'), indent=1); print('BUILT', tag, rec['stature_r6'], f)
