# RAC W2D (Gorrund W2): build a Gorrund body on the accepted W1i/W1j route (AD-G14 skeleton + trunk sculpt + unscaled Gorrund tissue,
# w1g_drivers/gn3.build with the accepted W1i parameter vector unpacked by w1i_drivers/gn6.unpack), at any height macro, optionally with a
# frame write (gn6.unpack frame dict: bone-scale multipliers, kb / ka / kp sculpt-node multipliers) and extra generator targets.
# Tissue donor = the W1c Gorrund generator inputs without skeletal scales at the same height macro (as w1i_drivers/true208.py), with its
# minimum-composition body and composition grid in w1g/donor (where gn3.build assembles the grid). Stature follows the macro (generator
# allometry); never a uniform scale. Exact-plane S7 (current bony_envelope).
# Usage: python3 go_body.py NAME HEIGHT_MACRO ['{frame}'|-] ['{targets}'|-] [OUTDIR]
import sys, os, json, subprocess
T = '/home/claude/wayfarer-design/tools/rac/w1'
for p in (T, T + '/w1g_drivers', T + '/w1h_drivers', T + '/w1i_drivers'): sys.path.insert(0, p)
import gn3, gn6, bony_envelope as BE
S = gn3.S; F, G = gn3.F, gn3.G; W = S + '/w2d'
X = json.load(open(S + '/w1i/GO_W1i_x.json'))["x"]
def bv(base, ov, out, nid):
    os.makedirs(out, exist_ok=True); p = out + '/%s.ov.json' % nid; json.dump(ov, open(p, 'w'))
    r = subprocess.run(['python3', T + '/build_variant.py', base, p, out, nid], capture_output=True, text=True)
    if r.returncode: raise RuntimeError(r.stderr[-1500:])
def donor(macro, targets=None, grid=True):
    tg = ''.join('_%s%s' % (k.replace('measure-', '').replace('LR:', '')[:10], v) for k, v in sorted((targets or {}).items()))
    n = ('GO0W%04d%s' % (round(macro * 10000), tg)).replace('.', 'p'); hd = W + '/h'; os.makedirs(hd, exist_ok=True)
    if not os.path.exists(hd + '/%s_build.json' % n):
        gi = json.load(open(F + '/base_w1c/GO_build.json')); d = dict(gi); d["height_macro"] = macro; d["id"] = n + '_src'
        json.dump(d, open(hd + '/%s_src.json' % n, 'w')); bv(hd + '/%s_src.json' % n, {"targets": targets} if targets else {}, hd, n)
    if not os.path.exists(hd + '/%s-LEAN_rest.npz' % n): bv(hd + '/%s_build.json' % n, {"muscle": 0.0, "weight": 0.0}, hd, n + '-LEAN')
    for m, w in (BE.GRID if grid else []):
        if (m, w) == (0.0, 0.0): continue
        cid = '%s-%s' % (n, BE.tag(m, w))
        if (m, w) == (0.5, 0.5):
            for st in ('rest', 'r6'):
                q = G + '/donor/%s_%s.npz' % (cid, st)
                if not os.path.lexists(q): os.symlink(hd + '/%s_%s.npz' % (n, st), q)
        elif not os.path.exists(G + '/donor/%s_rest.npz' % cid): bv(hd + '/%s_build.json' % n, {"muscle": m, "weight": w}, G + '/donor', cid)
    return hd + '/' + n, n
def build(name, macro, frame=None, targets=None, out=None):
    out = out or W + '/b/' + name; os.makedirs(out, exist_ok=True)
    dp, did = donor(macro, targets)
    B, sc = gn6.unpack(X, frame)
    r, C = gn3.build("GO", name, B, sc, wd=out, base=dp + '_build.json', donor=dp, did=did)
    subprocess.run(['python3', T + '/run_candidate.py', out, name, F + '/final/MF-M-R_rest.npz'], capture_output=True, text=True, cwd=T)
    rec = {"name": name, "height_macro": macro, "donor": did, "frame": frame, "extra_targets": targets, "bone_scales": B, "sculpt": sc, "stature_r6": r['r6']['stature']}
    json.dump(rec, open(out + '/%s_w2d.json' % name, 'w'), indent=1, default=float); print('BUILT', name, macro, round(r['r6']['stature'], 2), flush=True)
    return rec
def quick(name, macro, frame=None, targets=None, out=None):
    """proportion probe: donor (no grid) + sculpted skeleton + envelope + skin measurement (no CIB / skeletal proxy)"""
    import skeleton_envelope as SE
    out = out or W + '/q/' + name; os.makedirs(out, exist_ok=True)
    dp, did = donor(macro, targets, grid=False); B, sc = gn6.unpack(X, frame)
    bv(dp + '_build.json', {"muscle": 0.0, "weight": 0.0, "bone_scales": B}, out, name + '-LEAN')
    SE.make(out + '/' + name + '-LEAN', dp, dp + '-LEAN', out + '/' + name, tag=name, sculpt=sc)
    subprocess.run(['python3', T + '/run_candidate.py', out, name, F + '/final/MF-M-R_rest.npz'], capture_output=True, text=True, cwd=T)
    return json.load(open(out + '/%s_meas.json' % name))["combined"]
if __name__ == '__main__':
    a = sys.argv[1:]
    build(a[0], float(a[1]), json.loads(a[2]) if len(a) > 2 and a[2] != '-' else None, json.loads(a[3]) if len(a) > 3 and a[3] != '-' else None, a[4] if len(a) > 4 else None)
