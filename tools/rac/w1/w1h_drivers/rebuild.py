# RAC W1h driver AS RUN. The session scratch area (all W1f / W1g intermediate builds) was lost to an environment cleanup on
# October 6, 2026; this script regenerates every intermediate body DETERMINISTICALLY from the build records committed in the repo
# (reviews/rac-w1c|w1d|w1e|w1g-evidence/*_build.json, tools/rac/w1/cfg/w1f|w1g) in the same scratch layout the W1g drivers use,
# and checks the rebuilt R-6 geometry against the committed evidence geometry.
# Usage: python3 rebuild.py [step ...]   steps: ref lean grids donors meas verify
import sys, os, json, subprocess, shutil, glob
from concurrent.futures import ThreadPoolExecutor
R = '/home/claude/wayfarer-design'; T = R + '/tools/rac/w1'; EV = R + '/reviews'
S = '/tmp/claude-0/-home-claude-wayfarer-design/19af7d50-3b61-5fda-9fe0-7a30770fb334/scratchpad'
F, G = S + '/w1f', S + '/w1g'
for d in ('final', 'final_lean', 'lean', 'low', 'go', 'gr', 'sk', 'base', 'base_w1c'): os.makedirs(F + '/' + d, exist_ok=True)
for d in ('final', 'final_lean', 'donor', 'comp', 'compg', 'h', 'cib', 'skp', 'cand', 'cf'): os.makedirs(G + '/' + d, exist_ok=True)
SRC = {"MF-M-R": EV + '/rac-w1c-evidence/MF-M-R_build.json', "MF-F-R": EV + '/rac-w1c-evidence/MF-F-R_build.json', "SK": EV + '/rac-w1c-evidence/SK_build.json',
       "SG": EV + '/rac-w1c-evidence/SG_build.json', "HV": EV + '/rac-w1c-evidence/HV_build.json', "MF-FACE-PROJ-MAX": EV + '/rac-w1c-evidence/MF-FACE-PROJ-MAX_build.json',
       "DU-NAT": EV + '/rac-w1e-evidence/candidates/DU-NAT_build.json', "PK-NAT": EV + '/rac-w1e-evidence/candidates/PK-NAT_build.json',
       "CG-NAT": EV + '/rac-w1d-evidence/native-short/CG-NAT_build.json',
       "AE": EV + '/rac-w1g-evidence/candidates/AE_build.json', "FN": EV + '/rac-w1g-evidence/candidates/FN_build.json', "VA": EV + '/rac-w1g-evidence/candidates/VA_build.json'}
LEANOV = {"muscle": 0.0, "weight": 0.0}
SKB_OV = {"muscle": 0.0, "weight": 0.0, "bone_scales": {"LR:clavicle": [1.0, 1.08, 1.0], "spine_01": [1.08, 1.0, 1.0], "spine_02": [1.08, 1.0, 1.04],
          "spine_03": [1.08, 1.0, 1.04], "pelvis": [1.08, 1.0, 1.0], "LR:thigh": [1.05, 1.0, 1.05], "LR:calf": [1.05, 1.0, 1.05],
          "LR:upperarm": [1.05, 1.0, 1.05], "LR:lowerarm": [1.05, 1.0, 1.05]}}

def bv(base, ov, out, nid):
    if os.path.exists('%s/%s_r6.npz' % (out, nid)): return nid
    op = '%s/%s.ov.json' % (out, nid); json.dump(ov, open(op, 'w'))
    r = subprocess.run(['python3', T + '/build_variant.py', base, op, out, nid], capture_output=True, text=True)
    if r.returncode: print('BUILD FAIL', nid, r.stderr[-400:], flush=True)
    return nid

def par(jobs, n=2):
    with ThreadPoolExecutor(n) as ex: return list(ex.map(lambda a: bv(*a), jobs))

def base_files():
    for i, p in SRC.items(): shutil.copy(p, F + '/base/%s_build.json' % i)
    gi = json.load(open(T + '/cfg/w1f/GO.json'))
    json.dump({"id": "GO", "cfg": gi["generator_inputs"], "height_macro": gi["height_macro"]}, open(F + '/base_w1c/GO_build.json', 'w'), indent=1)
    json.dump({"id": "GO208", "cfg": gi["generator_inputs"], "height_macro": 0.701904296875}, open(F + '/base_w1c/GO208_build.json', 'w'), indent=1)
    shutil.copy(EV + '/rac-w1e-evidence/candidates/GR_build.json', F + '/base/GR_build.json')

def ref():
    base_files()
    par([(F + '/base/%s_build.json' % i, {}, F + '/final', i) for i in SRC])
    for i in ("AE", "FN", "VA"):
        for st in ("rest", "r6"): shutil.copy(F + '/final/%s_%s.npz' % (i, st), G + '/final/%s_%s.npz' % (i, st))
        shutil.copy(F + '/final/%s_build.json' % i, G + '/final/%s_build.json' % i)

def lean():
    par([(F + '/base/%s_build.json' % i, LEANOV, F + '/final_lean', i + '-LEAN') for i in SRC])
    for i in SRC:
        for st in ("rest", "r6"):
            shutil.copy(F + '/final_lean/%s-LEAN_%s.npz' % (i, st), F + '/lean/%s-LEAN_%s.npz' % (i, st))
            if i in ("AE", "FN", "VA"): shutil.copy(F + '/final_lean/%s-LEAN_%s.npz' % (i, st), G + '/final_lean/%s-LEAN_%s.npz' % (i, st))
    par([(F + '/base/MF-M-R_build.json', {"muscle": 0.25, "weight": 0.25}, F + '/low', 'MF-M-R-LOW'), (F + '/base/SK_build.json', {"muscle": 0.25, "weight": 0.25}, F + '/low', 'SK-LOW')])

def donors():
    import skeleton_envelope as SE
    par([(F + '/base_w1c/GO_build.json', {}, F + '/go', 'GO0'), (F + '/base_w1c/GO_build.json', LEANOV, F + '/go', 'GO0-LEAN'),
         (F + '/base_w1c/GO_build.json', {"muscle": 0.25, "weight": 0.25}, F + '/go', 'GO0-LOW'),
         (F + '/base_w1c/GO208_build.json', {}, F + '/go', 'GO2080'), (F + '/base_w1c/GO208_build.json', LEANOV, F + '/go', 'GO2080-LEAN'),
         (F + '/base/GR_build.json', {"bone_scales": {"spine_01": None, "LR:clavicle": None}}, F + '/gr', 'GR0'),
         (F + '/base/GR_build.json', {"muscle": 0.0, "weight": 0.0, "bone_scales": {"spine_01": None, "LR:clavicle": None}}, F + '/gr', 'GR0-LEAN'),
         (F + '/base/SK_build.json', {"stature": 229.0, "resolve_stature": True}, F + '/sk', 'SK229')])
    par([(F + '/sk/SK229_build.json', LEANOV, F + '/sk', 'SK229-LEAN'), (F + '/sk/SK229_build.json', SKB_OV, F + '/sk', 'SKB229-LEAN'),
         (F + '/base/SK_build.json', SKB_OV, F + '/sk', 'SKB208-LEAN'),
         (F + '/base/GR_build.json', {"muscle": 0.0, "weight": 0.0, "bone_scales": {"pelvis": [1.12, 1.0, 1.0], "spine_01": None}}, G + '/final_lean', 'GR-LEAN')])
    SE.make(F + '/sk/SKB229-LEAN', F + '/sk/SK229', F + '/sk/SK229-LEAN', F + '/sk/SKB229', tag='SKB229')
    SE.make(F + '/sk/SKB208-LEAN', F + '/final/SK', F + '/lean/SK-LEAN', F + '/sk/SKB208', tag='SKB208')
    SE.make(G + '/final_lean/GR-LEAN', F + '/gr/GR0', F + '/gr/GR0-LEAN', G + '/final/GR', tag='GR')
    # height donors for the stature series (macros as W1g) and Skarn heights (stature re-solved)
    gi = json.load(open(F + '/base_w1c/GO_build.json'))
    for n, m in (("GO0M215", 0.7438), ("GO0M222", 0.7911), ("GO0M251", 0.985)):
        d = dict(gi); d["height_macro"] = m; d["id"] = n; json.dump(d, open(G + '/h/%s_src.json' % n, 'w'))
    par([(G + '/h/%s_src.json' % n, {}, G + '/h', n) for n in ("GO0M215", "GO0M222", "GO0M251")] +
        [(F + '/base/SK_build.json', {"stature": float(h), "resolve_stature": True}, G + '/h', 'SKH%d' % h) for h in (215, 222)])
    par([(G + '/h/%s_build.json' % n, LEANOV, G + '/h', n + '-LEAN') for n in ("GO0M215", "GO0M222", "GO0M251", "SKH215", "SKH222")])

GRID = [(m, w) for m in (0.0, 0.25, 0.5) for w in (0.0, 0.25, 0.5) if (m, w) not in ((0.0, 0.0), (0.5, 0.5))]
def tag(m, w): return "C%03d%03d" % (round(m * 100), round(w * 100))
def grids():
    jobs = []
    for i in SRC:
        if i == "MF-FACE-PROJ-MAX": continue
        out = G + '/compg' if i in ("AE", "FN", "VA") else G + '/comp'
        jobs += [(F + '/base/%s_build.json' % i, {"muscle": m, "weight": w}, out, '%s-%s' % (i, tag(m, w))) for m, w in GRID]
    donors_ = {"GO0": F + '/go/GO0_build.json', "GR0": F + '/gr/GR0_build.json', "SK229": F + '/sk/SK229_build.json', "GO2080": F + '/go/GO2080_build.json',
               "GO0M215": G + '/h/GO0M215_build.json', "GO0M222": G + '/h/GO0M222_build.json', "GO0M251": G + '/h/GO0M251_build.json',
               "SKH215": G + '/h/SKH215_build.json', "SKH222": G + '/h/SKH222_build.json', "SK": F + '/base/SK_build.json'}
    for did, b in donors_.items():
        if did == "SK": continue
        jobs += [(b, {"muscle": m, "weight": w}, G + '/donor', '%s-%s' % (did, tag(m, w))) for m, w in GRID if (m, w) != (0.25, 0.25) or did != "GO0"]
    par(jobs)
    # links: (0.5,0.5) = donor ref; GO0 (0.25,0.25) = GO0-LOW; SK donor grid = comp/SK-*
    refs = {"GO0": F + '/go/GO0', "GR0": F + '/gr/GR0', "SK229": F + '/sk/SK229', "GO2080": F + '/go/GO2080', "GO0M215": G + '/h/GO0M215', "GO0M222": G + '/h/GO0M222',
            "GO0M251": G + '/h/GO0M251', "SKH215": G + '/h/SKH215', "SKH222": G + '/h/SKH222', "SK": F + '/final/SK'}
    for did, rp in refs.items():
        for st in ("rest", "r6"):
            p = G + '/donor/%s-C050050_%s.npz' % (did, st)
            if not os.path.lexists(p): os.symlink(rp + '_%s.npz' % st, p)
        if did == "SK":
            for m, w in GRID:
                for st in ("rest", "r6"):
                    p = G + '/donor/SK-%s_%s.npz' % (tag(m, w), st)
                    if not os.path.lexists(p): os.symlink(G + '/comp/SK-%s_%s.npz' % (tag(m, w), st), p)
    for st in ("rest", "r6"):
        p = G + '/donor/GO0-C025025_%s.npz' % st
        if not os.path.lexists(p): os.symlink(F + '/go/GO0-LOW_%s.npz' % st, p)

def meas():
    ids = [i for i in SRC]
    for i in ids:
        if not os.path.exists(F + '/final/%s_meas.json' % i):
            subprocess.run(['python3', T + '/run_candidate.py', F + '/final', i, F + '/final/MF-M-R_rest.npz'], capture_output=True)
    for i in ("MF-M-R-LOW", "SK-LOW"):
        subprocess.run(['python3', T + '/run_candidate.py', F + '/low', i, F + '/final/MF-M-R_rest.npz'], capture_output=True)

def verify():
    import numpy as np
    pairs = {"MF-M-R": EV + '/rac-w1c-evidence/geometry/MF-M-R_r6.npz', "SK": EV + '/rac-w1c-evidence/geometry/SK_r6.npz', "SG": EV + '/rac-w1c-evidence/geometry/SG_r6.npz',
             "HV": EV + '/rac-w1c-evidence/geometry/HV_r6.npz', "MF-F-R": EV + '/rac-w1c-evidence/geometry/MF-F-R_r6.npz', "DU-NAT": EV + '/rac-w1e-evidence/geometry/DU-NAT_r6.npz',
             "PK-NAT": EV + '/rac-w1e-evidence/geometry/PK-NAT_r6.npz', "CG-NAT": EV + '/rac-w1d-evidence/native-short/CG-NAT_r6.npz',
             "AE": EV + '/rac-w1g-evidence/geometry/AE_r6.npz', "FN": EV + '/rac-w1g-evidence/geometry/FN_r6.npz', "VA": EV + '/rac-w1g-evidence/geometry/VA_r6.npz'}
    out = {}
    for i, p in pairs.items():
        a = np.load(F + '/final/%s_r6.npz' % i)["V"]; b = np.load(p)["V"]; out[i] = float(np.abs(a - b).max()) if a.shape == b.shape else "shape differs"
    a = np.load(G + '/final/GR_r6.npz')["V"]; b = np.load(EV + '/rac-w1g-evidence/geometry/GR_r6.npz')["V"]; out["GR"] = float(np.abs(a - b).max())
    print(json.dumps(out, indent=1)); json.dump(out, open(S + '/rebuild_verify.json', 'w'), indent=1)

if __name__ == '__main__':
    sys.path.insert(0, T)
    for step in sys.argv[1:]:
        print('STEP', step, flush=True); globals()[step]()
    print('REBUILD DONE', flush=True)
