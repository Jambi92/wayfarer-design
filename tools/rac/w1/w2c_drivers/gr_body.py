# RAC W2C (Grask boundary foundation): build one Grask body on the accepted W1 route (AD-G14 skeleton + unscaled Grask tissue, as
# w1g_drivers/gn3.build), at any stature and with any extra skeletal / target writes:
#   1. tissue donor = the Grask generator inputs WITHOUT skeletal bone scales (GR0), height macro re-solved to the target stature
#      (generator allometry; never a uniform scale), plus its minimum-composition body and composition grid;
#   2. skeleton = the same inputs at minimum composition with the accepted W1l bone scales (pelvis X 0.925, femur cross-section 1.20,
#      clavicle Y 0.98, no lumbar narrowing) and any extra writes, height macro = the donor's;
#   3. envelope = skeleton + (donor_ref - donor_lean) (skeleton_envelope.make); composition grid; CIB (exact-plane S7); skeletal proxy;
#      skin measurement (run_candidate).
# Usage: python3 gr_body.py NAME STATURE|ref '{extra bone scales}' '{extra targets}' [OUTDIR]
import sys, os, json, subprocess, shutil
T = '/home/claude/wayfarer-design/tools/rac/w1'; sys.path.insert(0, T); sys.path.insert(0, T + '/w1g_drivers')
import skeleton_envelope as SE, bony_envelope as BE, skeletal_proxy as SP
S = '/tmp/claude-0/-home-claude-wayfarer-design/19af7d50-3b61-5fda-9fe0-7a30770fb334/scratchpad'; F = S + '/w1f'; W = S + '/w2c'
W1L = {"spine_01": None, "LR:clavicle": [1.0, 0.98, 1.0], "pelvis": [0.925, 1.0, 1.0], "LR:thigh": [1.20, 1.0, 1.20]}
def bv(base, ov, out, nid):
    os.makedirs(out, exist_ok=True); p = out + '/%s.ov.json' % nid; json.dump(ov, open(p, 'w'))
    r = subprocess.run(['python3', T + '/build_variant.py', base, p, out, nid], capture_output=True, text=True)
    if r.returncode: raise RuntimeError(r.stderr[-2000:])
    return json.load(open(out + '/%s_build.json' % nid))
def donor(H, targets, grid=True):
    """GR0 donor at stature H (re-solved height macro) with extra generator targets; returns (prefix, did, donor_dir, macro)"""
    tag = 'H%s' % H if H != 'ref' else 'H218'
    tg = ''.join('_%s%s' % (k.replace('measure-', '').replace('LR:', '')[:10], v) for k, v in sorted(targets.items())) if targets else ''
    did = ('GR0%s%s' % (tag, tg)).replace('.', 'p').replace(' ', ''); dd = W + '/donor'
    if not os.path.exists(dd + '/%s_rest.npz' % did):
        ov = {"targets": targets} if targets else {}
        if H != 'ref': ov.update({"stature": float(H), "resolve_stature": True})
        bv(F + '/gr/GR0_build.json', ov, dd, did)
    b = json.load(open(dd + '/%s_build.json' % did))
    if not os.path.exists(dd + '/%s-LEAN_rest.npz' % did): bv(dd + '/%s_build.json' % did, {"muscle": 0.0, "weight": 0.0}, dd, did + '-LEAN')
    for m, w in (BE.GRID if grid else []):
        if (m, w) in ((0.0, 0.0),): continue
        cid = '%s-%s' % (did, BE.tag(m, w))
        if (m, w) == (0.5, 0.5):
            for st in ('rest', 'r6'):
                q = dd + '/%s_%s.npz' % (cid, st)
                if not os.path.lexists(q): os.symlink(dd + '/%s_%s.npz' % (did, st), q)
        elif not os.path.exists(dd + '/%s_rest.npz' % cid): bv(dd + '/%s_build.json' % did, {"muscle": m, "weight": w}, dd, cid)
    return dd + '/' + did, did, dd, b["height_macro"]
def build(name, H, extra_bones=None, targets=None, out=None):
    out = out or W + '/b/' + name; os.makedirs(out, exist_ok=True)
    dp, did, dd, hm = donor(H, targets or {})
    B = dict(W1L); B.update(extra_bones or {})
    base = json.load(open(dp + '_build.json')); base_p = out + '/%s_base.json' % name; json.dump(base, open(base_p, 'w'))
    bv(base_p, {"muscle": 0.0, "weight": 0.0, "bone_scales": B}, out, name + '-LEAN')       # height macro held = donor's
    r = SE.make(out + '/' + name + '-LEAN', dp, dp + '-LEAN', out + '/' + name, tag=name)
    gd = out + '/grid_' + name
    if os.path.exists(gd): shutil.rmtree(gd)
    os.makedirs(gd)
    comps = BE.assemble_grid(out + '/' + name + '-LEAN', dd, did, dp + '-LEAN', gd, name) + [out + '/' + name + '_rest.npz']
    C = BE.cib(out + '/' + name + '_rest.npz', comps); cj = out + '/%s_cib.json' % name; json.dump(C, open(cj, 'w'), indent=1, default=float)
    SP.main(out, out, name, out + '/skp_' + name, cj)
    subprocess.run(['python3', T + '/run_candidate.py', out, name, F + '/final/MF-M-R_rest.npz'], capture_output=True, text=True, cwd=T)
    rec = {"name": name, "stature_target": H, "height_macro": hm, "donor": did, "bone_scales": B, "extra_targets": targets or {}, "stature_r6": r['r6']['stature'] if isinstance(r, dict) and 'r6' in r else None}
    json.dump(rec, open(out + '/%s_w2c.json' % name, 'w'), indent=1, default=float); print('BUILT', name, H, 'macro', hm, rec["stature_r6"], flush=True)
    return rec
def quick(name, H, extra_bones=None, targets=None, out=None):
    """proportion probe: donor (no composition grid) + skeleton + envelope + skin measurement only (no CIB / skeletal proxy)"""
    out = out or W + '/q/' + name; os.makedirs(out, exist_ok=True)
    dp, did, dd, hm = donor(H, targets or {}, grid=False)
    B = dict(W1L); B.update(extra_bones or {})
    base = json.load(open(dp + '_build.json')); base_p = out + '/%s_base.json' % name; json.dump(base, open(base_p, 'w'))
    bv(base_p, {"muscle": 0.0, "weight": 0.0, "bone_scales": B}, out, name + '-LEAN')
    SE.make(out + '/' + name + '-LEAN', dp, dp + '-LEAN', out + '/' + name, tag=name)
    subprocess.run(['python3', T + '/run_candidate.py', out, name, F + '/final/MF-M-R_rest.npz'], capture_output=True, text=True, cwd=T)
    return json.load(open(out + '/%s_meas.json' % name))["combined"]
if __name__ == '__main__':
    a = sys.argv[1:]
    build(a[0], a[1], json.loads(a[2]) if len(a) > 2 and a[2] != '-' else None, json.loads(a[3]) if len(a) > 3 and a[3] != '-' else None, a[4] if len(a) > 4 else None)
