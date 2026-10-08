# RAC W2H (synchronized short-race family: Durrim / Pipkin / Cogling) body builder. NON-CANON diagnostics.
# References (accepted W1, unchanged): Durrim DU-NAT 137 cm, Pipkin PK-NAT 107 cm, Cogling CGJ7 91 cm. Every short-race stature is far below the
# re-solved-macro ~0.40 line, so every body is on the accepted native short-adult route (native_short.py: regional length / girth / hand / foot /
# head factors solved at the target stature; no uniform scale), with each race's own accepted cfg (Durrim generator allometry; Pipkin and Cogling
# girth_beta 1.0 as accepted in W1q / W1r).
# Cogling head: the canon fixes head HEIGHT (menton-vertex) at roughly 11-13 cm (COGLING L1589, W1-A1). CGJ7 = 12 cm at 91 cm. At 76 / 107 cm the
# generator head allometry (beta 0.688, native_short_allometry.json) from 12 cm @ 91 gives 10.6 / 13.4 cm; clamped to the canon range: 11 / 13 cm.
# Frames: accepted W1 breadth-only rules - Durrim (W1t): clavicle Y, spine_01-03 X, pelvis X +/-8 % with Broad pelvis x1.08; Pipkin / Cogling
# (W1q / W1r): same breadth write with Broad pelvis x1.12 (Narrow x0.92). Composition: generator muscle / weight on the same skeleton.
# Usage: python3 sr_build.py JOBSET   (stature | frames | comp | named | child | p4)
import sys, os, json, subprocess
from concurrent.futures import ThreadPoolExecutor
T = '/home/claude/wayfarer-design/tools/rac/w1'; S = '/tmp/claude-0/-home-claude-wayfarer-design/19af7d50-3b61-5fda-9fe0-7a30770fb334/scratchpad'
W = S + '/w2h'; REF = S + '/w1f/final/MF-M-R_rest.npz'
REFB = {"DU": S + '/w1f/final/DU-NAT_build.json', "PK": S + '/w1f/final/PK-NAT_build.json', "CG": S + '/w1r/probe/CGJ7_build.json'}
REFH = {"DU": 137, "PK": 107, "CG": 91}
FAM = {"DU": (122, 137, 152), "PK": (91, 107, 122), "CG": (76, 91, 107)}
CG_HH = {76: 11.0, 91: 12.0, 107: 13.0}
BROADB = {"LR:clavicle": [1, 1.08, 1], "spine_01": [1.08, 1, 1], "spine_02": [1.08, 1, 1], "spine_03": [1.08, 1, 1]}
NARROWB = {k: [0.92 if c == 1.08 else c for c in v] for k, v in BROADB.items()}
FR = {"DU": {"N": {**NARROWB, "pelvis": [0.92, 1, 1]}, "B": {**BROADB, "pelvis": [1.08, 1, 1]}},
      "PK": {"N": {**NARROWB, "pelvis": [0.92, 1, 1]}, "B": {**BROADB, "pelvis": [1.12, 1, 1]}}}
FR["CG"] = FR["PK"]
COMP = (("LOWMUS", 0, 0.5), ("HIMUS", 1, 0.5), ("HIFAT", 0.5, 1), ("HIBOTH", 1, 1), ("LOW", 0.25, 0.25), ("MIN", 0, 0))
def native_cfg(race, h, nid, extra_targets=None):
    b = json.load(open(REFB[race])); c = dict(b["cfg"])
    for k in ("height_macro", "proxy_scale"): c.pop(k, None)
    c.update(stature=float(h), id=nid)
    if race == "CG":   # CGJ7 = CG-NAT targets + CGJ7 override (ankle 1.0); bone scales already in the CGJ7 cfg
        c["targets"] = dict(json.load(open(S + '/w1f/final/CG-NAT_build.json'))["cfg"]["targets"]); c["targets"]["measure-ankle-circ-decr"] = 1.0
        c["head_HH_cm"] = CG_HH.get(h, 12.0); c["girth_beta"] = 1.0
    if extra_targets: c["targets"] = {**c["targets"], **extra_targets}
    return c
def body(race, h):
    """build json of the family body at stature h (reference = accepted W1 body)"""
    return REFB[race] if h == REFH[race] else W + '/st/%s%d-NAT_build.json' % (race, h)
def sh(cmd, log):
    with open(W + '/logs/%s.log' % log, 'w') as f: return subprocess.run(cmd, cwd=T, stdout=f, stderr=subprocess.STDOUT).returncode
def variant(base, ov, out, nid):
    os.makedirs(out, exist_ok=True); json.dump(ov, open(out + '/%s.ov.json' % nid, 'w'))
    rc = sh(['python3', 'build_variant.py', base, out + '/%s.ov.json' % nid, out, nid], nid)
    if rc == 0: sh(['python3', 'run_candidate.py', out, nid, REF], nid + '.rc')
    print('BUILT' if rc == 0 else 'FAILED', nid, flush=True)
def native(c, out):
    os.makedirs(out, exist_ok=True); p = out + '/%s.cfg.json' % c["id"]; json.dump(c, open(p, 'w'))
    rc = sh(['python3', 'native_short.py', p, out], c["id"])
    if rc == 0: sh(['python3', 'run_candidate.py', out, c["id"] + '-NAT', REF], c["id"] + '.rc')
    print('BUILT' if rc == 0 else 'FAILED', c["id"], flush=True)
def frame(src_build, fr):
    b = json.load(open(src_build))["cfg"].get("bone_scales", {}); out = dict(b)
    for k, v in fr.items(): out[k] = [round(x * y, 6) for x, y in zip(b.get(k, [1, 1, 1]), v)]
    return {"bone_scales": out}
def jobs(which):
    J = []
    if which == 'stature':
        for race, hs in FAM.items():
            for h in hs:
                if h != REFH[race]: J.append((native, (native_cfg(race, h, '%s%d' % (race, h)), W + '/st')))
            # route check: the reference re-built from scratch on the same family route must reproduce the accepted W1 body
            J.append((native, (native_cfg(race, REFH[race], '%s%dR' % (race, REFH[race])), W + '/st')))
    if which == 'frames':
        for race, hs in FAM.items():
            for h in hs:
                for tag in ("N", "B"): J.append((variant, (body(race, h), frame(body(race, h), FR[race][tag]), W + '/fr', '%s%s%d' % (race, tag, h))))
    if which == 'comp':     # at each reference stature
        for race in FAM:
            for nm, m, w in COMP: J.append((variant, (REFB[race], {"muscle": m, "weight": w}, W + '/comp', '%s%d-%s' % (race, REFH[race], nm))))
    if which == 'named':
        # COG-BODY-04 Narrow low-muscle; COG-BODY-05 Broad high-muscle (also COG-BODY-10 normalized vs Narrow Durrim); PIP / DU low structural visibility
        J.append((variant, (W + '/fr/CGN91_build.json', {"muscle": 0.0, "weight": 0.5}, W + '/nm', 'COG04')))
        J.append((variant, (W + '/fr/CGB91_build.json', {"muscle": 1.0, "weight": 0.5}, W + '/nm', 'COG05')))
        J.append((variant, (W + '/fr/PKB107_build.json', {"muscle": 1.0, "weight": 0.5}, W + '/nm', 'PKBHM')))
        J.append((variant, (W + '/fr/DUN137_build.json', {"muscle": 0.25, "weight": 0.25}, W + '/nm', 'DUNLOW')))
        # COG-BODY-12 long-finger high end (own finger target x1.5); COG-BODY-13 distal-emphasis low end (own distal targets x0.5) - native at 91 cm
        g = json.load(open(S + '/w1f/final/CG-NAT_build.json'))["cfg"]["targets"]
        J.append((native, (native_cfg("CG", 91, 'COG12', {"LR:hand-fingers-length-incr": round(g["LR:hand-fingers-length-incr"] * 1.5, 4)}), W + '/nm')))
        J.append((native, (native_cfg("CG", 91, 'COG13', {k: round(g[k] * 0.5, 4) for k in ("measure-upperarm-length-decr", "measure-lowerarm-length-incr", "LR:hand-fingers-length-incr", "measure-lowerleg-height-incr", "LR:hand-scale-incr")}), W + '/nm')))
    if which == 'p4':       # DU-P4 composition independence at 152 cm (Durrim and Marchfolk 152, low / minimum / high composition)
        for nm, m, w in (("LOW", 0.25, 0.25), ("MIN", 0, 0), ("HIBOTH", 1, 1)):
            J.append((variant, (W + '/st/DU152-NAT_build.json', {"muscle": m, "weight": w}, W + '/p4', 'DU152-' + nm)))
            J.append((variant, (S + '/w1t/bnd/MF152-NAT_build.json', {"muscle": m, "weight": w}, W + '/p4', 'MF152-' + nm)))
    if which == 'child':    # generator human-child proxy (diagnostic only, COG-BODY-11): ~1.5 y toddler at 76 cm (age macro = (y - 1) x 0.01875, as CHILD3 / 6 / 9 / 11)
        J.append((variant, (S + '/w1f/final/MF-M-R_build.json', {"age_years": 1.5, "age": 0.009375, "stature": 76.0, "resolve_stature": True, "targets": {}, "bone_scales": {}}, W + '/child', 'CHILD1')))
    return J
if __name__ == '__main__':
    os.makedirs(W + '/logs', exist_ok=True)
    J = jobs(sys.argv[1])
    with ThreadPoolExecutor(2) as ex: list(ex.map(lambda j: j[0](*j[1]), J))
    print('DONE', sys.argv[1], len(J))
