# RAC W1k (Grask W1 acceptance gate) builder. Same AD-G14 route as the W1h Grask build (w1h_drivers/grfin.sh -> w1g_drivers/gn3.build).
# Usage: python3 gr_build.py STAGE   (stages: s01 | frames | comp)
#  s01   : diagnostic rebuild of the central GR with spine_01 removed (the W1g/W1h records state it was removed, AD-W1G-1;
#          the delivered W1h geometry still carries base spine_01 [0.96,1,1]); pelvis 0.985 and clavicle as built.
#  frames: GR-BODY-04 Narrow / GR-BODY-05 Broad on the candidate skeleton (CAND env: 'asbuilt' or 's01').
#          Broad = the accepted Broad Skarn frame write (+8 % skeletal breadth, +4 % thoracic depth, +5 % long-bone robusticity)
#          multiplied onto the candidate's bone scales; Narrow = its mirror (x0.92 / x0.96 / x0.95). DIAGNOSTIC construction only.
#  comp  : GR-BODY-06 low muscle (0.0/0.5), -07 high muscle (1.0/0.5), -08 higher fat (0.5/1.0), -09 high muscle + fat (1.0/1.0),
#          plus low composition 0.25/0.25 (as the Gorrund W1j comparisons): candidate skeleton + generator tissue at that composition.
import sys, os, json, subprocess
sys.path.insert(0, '/home/claude/wayfarer-design/tools/rac/w1/w1g_drivers'); sys.path.insert(0, '/home/claude/wayfarer-design/tools/rac/w1')
import gn3, skeleton_envelope as SE
S = gn3.S; F, G = gn3.F, gn3.G; K = S + '/w1k' if os.environ.get('CAND') != 'w1l' else S + '/w1l'; T = gn3.T
BASE = F + '/base/GR_build.json'
CAND = {"asbuilt": {"spine_01": [0.96, 1.0, 1.0], "LR:clavicle": [1.0, 0.98, 1.0], "pelvis": [0.985, 1.0, 1.0]},
        "s01":     {"spine_01": None, "LR:clavicle": [1.0, 0.98, 1.0], "pelvis": [0.985, 1.0, 1.0]},
        # W1l (Issue #1, option b): lumbar narrowing removed; GR-P2b recovered through proximal-femur robusticity (LR:thigh X/Z, length unchanged)
        "w1l":     {"spine_01": None, "LR:clavicle": [1.0, 0.98, 1.0], "pelvis": [0.925, 1.0, 1.0], "LR:thigh": [1.20, 1.0, 1.20]}}
BROAD = {"LR:clavicle": [1, 1.08, 1], "spine_01": [1.08, 1, 1], "spine_02": [1.08, 1, 1.04], "spine_03": [1.08, 1, 1.04], "pelvis": [1.08, 1, 1],
         "LR:thigh": [1.05, 1, 1.05], "LR:calf": [1.05, 1, 1.05], "LR:upperarm": [1.05, 1, 1.05], "LR:lowerarm": [1.05, 1, 1.05]}
NARROW = {k: [{1.08: 0.92, 1.04: 0.96, 1.05: 0.95}.get(c, c) for c in v] for k, v in BROAD.items()}

def apply(B, W):
    out = dict(B)
    for k, v in W.items():
        base = out.get(k) or [1.0, 1.0, 1.0]
        out[k] = [round(a * b, 6) for a, b in zip(base, v)]
    return out

def build(name, B, wd):
    r, C = gn3.build('GR', name, B, wd=wd); print(name, round(r['r6']['stature'], 3), flush=True)
    rc = subprocess.run(['python3', T + '/run_candidate.py', wd, name, F + '/final/MF-M-R_rest.npz'], capture_output=True, text=True, cwd=T)
    open(wd + '/%s.rc.log' % name, 'w').write(rc.stdout + rc.stderr)
    return r

if __name__ == '__main__':
    st = sys.argv[1]; os.makedirs(K, exist_ok=True)
    if st == 's01':
        build('GRS01', CAND['s01'], K + '/s01')
    elif st == 'frames':
        c = os.environ.get('CAND', 's01'); B = CAND[c]
        for nm, W in (('GR-BODY-04', NARROW), ('GR-BODY-05', BROAD)):
            build(nm, apply(B, W), K + '/frames_' + c)
    elif st == 'comp':
        c = os.environ.get('CAND', 's01'); wd = K + '/comp_' + c; os.makedirs(wd, exist_ok=True)
        lean = {'asbuilt': G + '/final/GR-LEAN', 's01': K + '/s01/GRS01-LEAN', 'w1l': S + '/w1l/probe/GRL925_1200-LEAN'}[c]
        for nm, (m, w) in (('GR-BODY-06', (0.0, 0.5)), ('GR-BODY-07', (1.0, 0.5)), ('GR-BODY-08', (0.5, 1.0)), ('GR-BODY-09', (1.0, 1.0)), ('GR-LOW', (0.25, 0.25))):
            did = 'GR0-C%03d%03d' % (round(m * 100), round(w * 100)); dd = K + '/donor'; os.makedirs(dd, exist_ok=True)
            if not os.path.exists(dd + '/' + did + '_rest.npz'):
                json.dump({"muscle": m, "weight": w}, open(dd + '/%s.ov.json' % did, 'w'))
                subprocess.run(['python3', T + '/build_variant.py', F + '/gr/GR0_build.json', dd + '/%s.ov.json' % did, dd, did], check=True, capture_output=True)
            SE.make(lean, dd + '/' + did, F + '/gr/GR0-LEAN', wd + '/' + nm, tag=nm)
            rc = subprocess.run(['python3', T + '/run_candidate.py', wd, nm, F + '/final/MF-M-R_rest.npz'], capture_output=True, text=True, cwd=T)
            open(wd + '/%s.rc.log' % nm, 'w').write(rc.stdout + rc.stderr); print(nm, m, w, flush=True)
    print('STAGE_DONE', st, flush=True)
