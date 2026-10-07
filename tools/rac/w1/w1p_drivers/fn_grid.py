# RAC W1p: CIB grid (reference, minimum composition, composition grid) for a Fenn candidate (copy of w1n_drivers/va_grid.py) build record, generator route,
# height macro held; files named FN* in their own folder; then cib_all.py FN. Optional frame write (diagnostic, as Grask / Aelari).
# Usage: python3 va_grid.py BUILD_JSON OUTDIR [NARROW|BROAD]
import sys, os, json, subprocess
S = '/tmp/claude-0/-home-claude-wayfarer-design/19af7d50-3b61-5fda-9fe0-7a30770fb334/scratchpad'; T = '/home/claude/wayfarer-design/tools/rac/w1'
BROAD = {"LR:clavicle": [1, 1.08, 1], "spine_01": [1.08, 1, 1], "spine_02": [1.08, 1, 1.04], "spine_03": [1.08, 1, 1.04], "pelvis": [1.08, 1, 1],
         "LR:thigh": [1.05, 1, 1.05], "LR:calf": [1.05, 1, 1.05], "LR:upperarm": [1.05, 1, 1.05], "LR:lowerarm": [1.05, 1, 1.05]}
NARROW = {k: [{1.08: 0.92, 1.04: 0.96, 1.05: 0.95}.get(c, c) for c in v] for k, v in BROAD.items()}
# Vael-faithful breadth-only write (VAEL L114: depth survives Narrow; frame = skeletal breadth): +/-8 % skeletal breadth only,
# thoracic depth and long-bone robusticity unchanged. Diagnostic construction; not authored magnitudes.
BROADB = {"LR:clavicle": [1, 1.08, 1], "spine_01": [1.08, 1, 1], "spine_02": [1.08, 1, 1], "spine_03": [1.08, 1, 1], "pelvis": [1.08, 1, 1]}
NARROWB = {k: [0.92 if c == 1.08 else c for c in v] for k, v in BROADB.items()}
# W1o (Vael W1n ruling, bounded): Broad breadth-only write with the hip apparatus carried with the crest - the pelvis (which carries
# the hip joints, i.e. hip-joint spacing) widened beyond the +8 % frame breadth; limb lengths, thoracic depth, joint robusticity,
# head and tissue unchanged. BROADB_P<nnn> = pelvis X factor nnn/100.
for _p in (110, 112, 114, 116, 120):
    globals()['BROADB_P%d' % _p] = {**BROADB, "pelvis": [_p / 100, 1, 1]}
GRID = [(0.0, 0.25), (0.0, 0.5), (0.25, 0.0), (0.25, 0.25), (0.25, 0.5), (0.5, 0.0), (0.5, 0.25)]
src, D = sys.argv[1], sys.argv[2]; fr = sys.argv[3] if len(sys.argv) > 3 else None
def bv(base, ov, out, nid):
    os.makedirs(out, exist_ok=True); json.dump(ov, open(out + '/%s.ov.json' % nid, 'w'))
    subprocess.run(['python3', T + '/build_variant.py', base, out + '/%s.ov.json' % nid, out, nid], check=True, capture_output=True, cwd=T); print('BUILT', nid, flush=True)
b = json.load(open(src)); os.makedirs(D + '/final', exist_ok=True)
if fr:
    Bs = b["cfg"]["bone_scales"]; W = {'BROAD': BROAD, 'NARROW': NARROW, 'BROADB': BROADB, 'NARROWB': NARROWB}.get(fr) or globals()[fr]
    sc = dict(Bs); sc.update({k: [round(x * y, 6) for x, y in zip(Bs.get(k, [1, 1, 1]), v)] for k, v in W.items()})
    tmpb = D + '/src_build.json'; json.dump(b, open(tmpb, 'w')); bv(tmpb, {"bone_scales": sc}, D + '/final', 'FN')
else:
    b["id"] = "VA"; b["cfg"]["id"] = "VA"; json.dump(b, open(D + '/final/FN_build.json', 'w'))
    stem = src[:-len('_build.json')]
    for st in ('rest', 'r6'): subprocess.run(['cp', stem + '_%s.npz' % st, D + '/final/FN_%s.npz' % st], check=True)
bv(D + '/final/FN_build.json', {"muscle": 0.0, "weight": 0.0}, D + '/lean', 'FN-LEAN')
for m, w in GRID: bv(D + '/final/FN_build.json', {"muscle": m, "weight": w}, D + '/comp', 'FN-C%03d%03d' % (round(m * 100), round(w * 100)))
subprocess.run(['python3', T + '/run_candidate.py', D + '/final', 'FN', S + '/w1f/final/MF-M-R_rest.npz'], capture_output=True, cwd=T)
env = dict(os.environ, REF=D + '/final', LEAN=D + '/lean', COMP=D + '/comp', OUT=D + '/skp', CIBD=D + '/cib')
r = subprocess.run(['python3', T + '/w1g_drivers/cib_all.py', 'FN'], env=env, capture_output=True, text=True, cwd=T); print(r.stdout[-300:], 'GRID_DONE', flush=True)
