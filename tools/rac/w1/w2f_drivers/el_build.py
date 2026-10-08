# RAC W2F (Elf family W2: Fenn / Aelari / Vael) body builder. Starting points = the accepted W1 references FNL4 (181 cm), AEL1 (190 cm),
# VAL4 (178 cm) with every accepted W1 bone scale and generator target unchanged.
# Routes = the accepted W2A boundary-route rule (as Sagekin W2E): < 159 cm native short-adult route from the population's accepted base
# macro (base_height_macro), bone scales and targets carried; >= 159 cm generator height macro re-solved from the accepted build.
# Frames = the accepted ELF frame principle (W1n / W1o / W1p rulings): breadth-only +/-8 % (clavicle Y, spine_01-03 X), Broad pelvis X x1.12
# (hip joints carried with the crest); limb lengths, thoracic depth, joint robusticity, head and tissue unchanged (NOT the Skarn / Marchfolk write).
# Composition = generator muscle / weight macros on the same skeleton construction. Named validators = the population's OWN target strengths
# scaled (no new targets), or frame + composition combinations. No uniform scaling.
# Usage: python3 el_build.py JOBSET   (stature | frames | comp | named | fcomp)
import sys, os, json, subprocess
from concurrent.futures import ThreadPoolExecutor
T = '/home/claude/wayfarer-design/tools/rac/w1'; S = '/tmp/claude-0/-home-claude-wayfarer-design/19af7d50-3b61-5fda-9fe0-7a30770fb334/scratchpad'
W = S + '/w2f'; REF = S + '/w1f/final/MF-M-R_rest.npz'
BASE = {"FN": S + '/w1p/cand/FNL4_build.json', "AE": S + '/w1m/legs/AEL1_build.json', "VA": S + '/w1n/cand/VAL4_build.json'}
REFH = {"FN": 181, "AE": 190, "VA": 178}
STAT = {"FN": (157, 163, 173, 178, 190, 203, 211), "AE": (168, 173, 178, 181, 203, 211, 221), "VA": (157, 163, 173, 181, 190, 203)}
MINH = {"FN": 157, "AE": 168, "VA": 157}; MAXH = {"FN": 211, "AE": 221, "VA": 203}
BROADB = {"LR:clavicle": [1, 1.08, 1], "spine_01": [1.08, 1, 1], "spine_02": [1.08, 1, 1], "spine_03": [1.08, 1, 1], "pelvis": [1.12, 1, 1]}
NARROWB = {"LR:clavicle": [1, 0.92, 1], "spine_01": [0.92, 1, 1], "spine_02": [0.92, 1, 1], "spine_03": [0.92, 1, 1], "pelvis": [0.92, 1, 1]}
def cfg(p): return json.load(open(p))["cfg"]
def sh(cmd, log):
    with open(W + '/logs/%s.log' % log, 'w') as f: return subprocess.run(cmd, cwd=T, stdout=f, stderr=subprocess.STDOUT).returncode
def variant(base, ov, out, nid):
    os.makedirs(out, exist_ok=True); json.dump(ov, open(out + '/%s.ov.json' % nid, 'w'))
    rc = sh(['python3', 'build_variant.py', base, out + '/%s.ov.json' % nid, out, nid], nid)
    if rc == 0: sh(['python3', 'run_candidate.py', out, nid, REF], nid + '.rc')
    print('BUILT' if rc == 0 else 'FAILED', nid, flush=True)
def native(c, out, nid):
    os.makedirs(out, exist_ok=True); p = out + '/%s.cfg.json' % nid; json.dump(c, open(p, 'w'))
    rc = sh(['python3', 'native_short.py', p, out], nid)
    if rc == 0: sh(['python3', 'run_candidate.py', out, nid + '-NAT', REF], nid + '.rc')
    print('BUILT' if rc == 0 else 'FAILED', nid, flush=True)
def frame(src_build, fr):
    b = json.load(open(src_build))["cfg"].get("bone_scales", {})
    return {"bone_scales": {k: [round(x * y, 6) for x, y in zip(b.get(k, [1, 1, 1]), v)] for k, v in fr.items()}}
def body_build(r, h):
    """build json of a population body at stature h (reference = the accepted W1 build)"""
    if h == REFH[r]: return BASE[r]
    return W + ('/st/%s%d-NAT_build.json' if h < 159 else '/st/%s%d_build.json') % (r, h)
def scaled(r, keys, f):
    t = cfg(BASE[r])["targets"]; return {k: round(t[k] * f, 4) for k in keys if k in t}
NAMED = {   # population's own targets only (scaled), or one own target removed / mirrored
    "FN15": ("FN", {"fn": lambda: scaled("FN", ("measure-upperarm-length-incr", "measure-lowerarm-length-incr", "LR:hand-fingers-length-incr", "LR:hand-scale-incr"), 1.5)}),
    "FN16": ("FN", {"fn": lambda: scaled("FN", ("measure-upperleg-height-incr", "measure-lowerleg-height-incr", "LR:foot-scale-incr"), 1.5)}),
    "FN09": ("FN", {"fn": lambda: scaled("FN", ("measure-upperarm-length-incr", "measure-lowerarm-length-incr", "measure-upperleg-height-incr", "measure-lowerleg-height-incr"), 0.5)}),
    "FN08": ("FN", {"fn": lambda: {"measure-napetowaist-dist-decr": None}}),
    "AE19": ("AE", {"fn": lambda: scaled("AE", ("LR:hand-scale-incr",), 1.5)}),
    "AE20": ("AE", {"fn": lambda: scaled("AE", ("measure-upperleg-height-incr", "measure-lowerleg-height-incr", "LR:foot-scale-incr"), 1.5)}),
    "AE11": ("AE", {"fn": lambda: scaled("AE", ("measure-napetowaist-dist-incr",), 2.5)}),
    "VA09": ("VA", {"fn": lambda: {"measure-lowerleg-height-decr": None, "measure-lowerleg-height-incr": 0.1}}),
    "VA10": ("VA", {"fn": lambda: dict(scaled("VA", ("measure-lowerleg-height-decr",), 2.0), **scaled("VA", ("torso-scale-depth-incr",), 1.5))}),
}
def jobs(which):
    J = []
    if which == 'stature':
        for r in ("FN", "AE", "VA"):
            for h in STAT[r]:
                if h < 159:
                    c = dict(cfg(BASE[r])); c.update(stature=float(h), id="%s%d" % (r, h), base_height_macro=json.load(open(BASE[r]))["height_macro"])
                    J.append((native, (c, W + '/st', '%s%d' % (r, h))))
                else: J.append((variant, (BASE[r], {"stature": float(h), "resolve_stature": True}, W + '/st', '%s%d' % (r, h))))
    if which == 'frames':
        for r in ("FN", "AE", "VA"):
            for h in (MINH[r], REFH[r], MAXH[r]):
                for tag, fr in (("N", NARROWB), ("B", BROADB)):
                    src = body_build(r, h); J.append((variant, (src, frame(src, fr), W + '/fr', '%s%s%d' % (r, tag, h))))
    if which == 'comp':     # composition at the 173 cm matched point (Marchfolk 173 and Sagekin 173 composition states exist)
        for r in ("FN", "AE", "VA"):
            for nm, m, w in (("LOWMUS", 0, 0.5), ("HIMUS", 1, 0.5), ("HIFAT", 0.5, 1), ("HIBOTH", 1, 1), ("LOW", 0.25, 0.25), ("MIN", 0, 0)):
                J.append((variant, (W + '/st/%s173_build.json' % r, {"muscle": m, "weight": w}, W + '/comp', '%s173-%s' % (r, nm))))
    if which == 'fcomp':    # frame x composition named validators at the reference (FN-04/14, -06/11, -07, -12, -13; AE-13, -06/17, -07/15, -14, -18; VL-16, -06/17, -07/18, -49, -48)
        for r in ("FN", "AE", "VA"):
            for nm, src, m, w in (("NLOW", "N", 0.25, 0.25), ("BHM", "B", 1.0, 0.5), ("HF", None, 0.5, 1.0), ("NHM", "N", 1.0, 0.5), ("BHF", "B", 0.5, 1.0)):
                b = W + '/fr/%s%s%d_build.json' % (r, src, REFH[r]) if src else BASE[r]
                J.append((variant, (b, {"muscle": m, "weight": w}, W + '/fcomp', '%s-%s' % (r, nm))))
    if which == 'named':
        for nid, (r, d) in NAMED.items():
            J.append((variant, (BASE[r], {"targets": d["fn"](), "resolve_stature": True, "stature": float(REFH[r])}, W + '/nm', nid)))
        # max-height combined-proportion stress (AE-24, VL-24): the population's own targets x1.5 at its maximum stature
        for r, nid in (("AE", "AE24"), ("VA", "VA24")):
            J.append((variant, (BASE[r], {"targets": scaled(r, list(cfg(BASE[r])["targets"]), 1.5), "resolve_stature": True, "stature": float(MAXH[r])}, W + '/nm', nid)))
        # VL-23 deep ribcage with Narrow frame: Vael ribcage-depth target x2 on the Narrow reference frame
        J.append((variant, (W + '/fr/VAN178_build.json', {"targets": scaled("VA", ("torso-scale-depth-incr",), 2.0)}, W + '/nm', 'VA23')))
    return J
if __name__ == '__main__':
    os.makedirs(W + '/logs', exist_ok=True)
    J = jobs(sys.argv[1])
    with ThreadPoolExecutor(2) as ex: list(ex.map(lambda j: j[0](*j[1]), J))
    print('DONE', sys.argv[1], len(J))
