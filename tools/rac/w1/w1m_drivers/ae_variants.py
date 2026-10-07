# RAC W1m: Aelari diagnostic variants on the AEL1 candidate (generator route, height macro held).
#  frames: AE Narrow / Broad = the accepted Broad Skarn frame write (+8 % skeletal breadth, +4 % thoracic depth, +5 % long-bone
#          robusticity) and its mirror (x0.92 / x0.96 / x0.95), multiplied onto AEL1's bone scales - the same diagnostic convention as
#          the Grask gate; Aelari has no authored frame magnitudes. Each frame body gets its own lean + composition grid for CIB rows.
#  comp:   generator composition macros on AEL1: low muscle 0/0.5, high muscle 1/0.5, higher fat 0.5/1, high muscle + fat 1/1, low 0.25/0.25.
# Usage: python3 ae_variants.py frames|comp
import sys, os, json, subprocess
S = '/tmp/claude-0/-home-claude-wayfarer-design/19af7d50-3b61-5fda-9fe0-7a30770fb334/scratchpad'; M = S + '/w1m'; T = '/home/claude/wayfarer-design/tools/rac/w1'
BASE = M + '/ael1/final/AE_build.json'
BROAD = {"LR:clavicle": [1, 1.08, 1], "spine_01": [1.08, 1, 1], "spine_02": [1.08, 1, 1.04], "spine_03": [1.08, 1, 1.04], "pelvis": [1.08, 1, 1],
         "LR:thigh": [1.05, 1, 1.05], "LR:calf": [1.05, 1, 1.05], "LR:upperarm": [1.05, 1, 1.05], "LR:lowerarm": [1.05, 1, 1.05]}
NARROW = {k: [{1.08: 0.92, 1.04: 0.96, 1.05: 0.95}.get(c, c) for c in v] for k, v in BROAD.items()}
GRID = [(0.0, 0.25), (0.0, 0.5), (0.25, 0.0), (0.25, 0.25), (0.25, 0.5), (0.5, 0.0), (0.5, 0.25)]
def bv(base, ov, out, nid):
    os.makedirs(out, exist_ok=True); json.dump(ov, open(out + '/%s.ov.json' % nid, 'w'))
    subprocess.run(['python3', T + '/build_variant.py', base, out + '/%s.ov.json' % nid, out, nid], check=True, capture_output=True, cwd=T); print('BUILT', nid, flush=True)
def scales(W):
    B = json.load(open(BASE))["cfg"]["bone_scales"]; o = dict(B)
    for k, v in W.items(): o[k] = [round(a * b, 6) for a, b in zip(B.get(k, [1, 1, 1]), v)]
    return o
if sys.argv[1] == 'frames':
    for nm, W in (('NARROW', NARROW), ('BROAD', BROAD)):
        D = M + '/frame_' + nm; bv(BASE, {"bone_scales": scales(W)}, D + '/final', 'AE')
        bv(D + '/final/AE_build.json', {"muscle": 0.0, "weight": 0.0}, D + '/lean', 'AE-LEAN')
        for m, w in GRID: bv(D + '/final/AE_build.json', {"muscle": m, "weight": w}, D + '/comp', 'AE-C%03d%03d' % (round(m * 100), round(w * 100)))
        subprocess.run(['python3', T + '/run_candidate.py', D + '/final', 'AE', S + '/w1f/final/MF-M-R_rest.npz'], capture_output=True, cwd=T)
        env = dict(os.environ, REF=D + '/final', LEAN=D + '/lean', COMP=D + '/comp', OUT=D + '/skp', CIBD=D + '/cib')
        subprocess.run(['python3', T + '/w1g_drivers/cib_all.py', 'AE'], env=env, capture_output=True, cwd=T); print('FRAME_DONE', nm, flush=True)
else:
    D = M + '/comp'
    for nm, (m, w) in (('AE-LOWMUS', (0.0, 0.5)), ('AE-HIMUS', (1.0, 0.5)), ('AE-HIFAT', (0.5, 1.0)), ('AE-HIBOTH', (1.0, 1.0)), ('AE-LOW', (0.25, 0.25))):
        bv(BASE, {"muscle": m, "weight": w}, D, nm)
        subprocess.run(['python3', T + '/run_candidate.py', D, nm, S + '/w1f/final/MF-M-R_rest.npz'], capture_output=True, cwd=T)
print('STAGE_DONE', sys.argv[1], flush=True)
