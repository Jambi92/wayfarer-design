# RAC W2G (Halvren central envelope) body builder. Starting point = the accepted W1 Halvren diagnostic anchor HVC1 (~178 cm, accepted HV body
# with the eye-scale target removed; never a mandatory phenotype). Routes = the accepted rules: generator height macro re-solved; native short-adult
# route from HVC1's base macro wherever the re-solved macro falls below ~0.40 (W2F R2). Frames = accepted W1 Halvren breadth-only writes
# (Narrow -8 %; Broad +8 % with pelvis X x1.12). Composition = generator muscle / weight macros on the same skeleton.
# Source-influenced expression bodies (HV-13...17 body portions; diagnostic, BUILDER-CHOSEN, not ancestry percentages or presets): HVC1 keeps its own
# targets, and on the systems that the Halvren canon names for that influence it moves toward the source population's OWN targets:
# each named measure moves halfway from HVC1's signed value toward the source's signed value (build 1 summed and overshot the 178 cm source span on
# forearm; build 2 took max(HVC1, half source) and under-expressed). No uniform scaling.
# Usage: python3 hv_build.py JOBSET   (stature | frames | expr | comp | stress)
import sys, os, json, subprocess
from concurrent.futures import ThreadPoolExecutor
T = '/home/claude/wayfarer-design/tools/rac/w1'; S = '/tmp/claude-0/-home-claude-wayfarer-design/19af7d50-3b61-5fda-9fe0-7a30770fb334/scratchpad'
W = S + '/w2g'; REF = S + '/w1f/final/MF-M-R_rest.npz'
HVB = S + '/w1s/probe/HVC1_build.json'
SRC = {"FN": S + '/w1p/cand/FNL4_build.json', "AE": S + '/w1m/legs/AEL1_build.json', "VA": S + '/w1n/cand/VAL4_build.json', "SK": S + '/w1f/final/SK_build.json',
       "SG": S + '/w1f/final/SG_build.json'}
BROADB = {"LR:clavicle": [1, 1.08, 1], "spine_01": [1.08, 1, 1], "spine_02": [1.08, 1, 1], "spine_03": [1.08, 1, 1], "pelvis": [1.12, 1, 1]}
NARROWB = {"LR:clavicle": [1, 0.92, 1], "spine_01": [0.92, 1, 1], "spine_02": [0.92, 1, 1], "spine_03": [0.92, 1, 1], "pelvis": [0.92, 1, 1]}
# systems named by the Halvren canon for each influence (spec §20-26 table, HV-13...17; order §7)
SYS = {"FN": ("measure-lowerarm-length-incr", "measure-lowerleg-height-incr", "LR:hand-fingers-length-incr", "LR:hand-scale-incr", "LR:foot-scale-incr",
              "measure-wrist-circ-decr", "measure-ankle-circ-decr", "measure-knee-circ-decr", "torso-scale-depth-decr"),
       "AE": ("measure-neck-height-incr", "measure-napetowaist-dist-incr", "measure-upperarm-length-incr", "measure-lowerarm-length-incr", "measure-upperleg-height-incr",
              "measure-lowerleg-height-incr", "head-scale-vert-incr", "torso-scale-depth-decr", "measure-wrist-circ-decr", "measure-knee-circ-decr", "measure-ankle-circ-decr"),
       "VA": ("torso-scale-depth-incr", "LR:hand-scale-incr", "LR:foot-scale-horiz-incr", "LR:hand-fingers-distance-incr", "measure-lowerleg-height-decr"),
       "SK": ("torso-scale-depth-incr", "measure-shoulder-dist-incr", "measure-wrist-circ-incr", "measure-knee-circ-incr", "measure-ankle-circ-incr", "LR:hand-scale-incr",
              "LR:foot-scale-incr", "measure-neck-circ-incr", "LR:lowerarm-scale-depth-incr", "LR:upperarm-scale-depth-incr", "LR:lowerleg-scale-depth-incr", "measure-napetowaist-dist-incr"),
       "SG": ("measure-upperleg-height-incr", "measure-lowerleg-height-incr", "measure-napetowaist-dist-decr", "torso-scale-depth-decr", "measure-lowerarm-length-incr",
              "LR:hand-fingers-length-incr", "LR:hand-scale-incr", "LR:hand-fingers-diameter-decr")}
def opposite(k): return k[:-5] + ("-decr" if k.endswith("-incr") else "-incr") if k.endswith(("-incr", "-decr")) else None
def signed(t, k):
    """signed value of the measure k ('-incr' positive) in a target dict"""
    o = opposite(k); base = k if k.endswith("-incr") or not o else o
    neg = opposite(base); return t.get(base, 0) - (t.get(neg, 0) if neg else 0), base, neg
def expr_targets(src, f=0.5):
    """HVC1 targets moved a fraction f of the way toward the source's own targets on the systems the Halvren canon names for that influence
    (signed interpolation per measure: never past the source, never stacked; build 1 summed and overshot, build 2 took max and under-expressed)"""
    hv0 = json.load(open(HVB))["cfg"]["targets"]; hv = dict(hv0); st = json.load(open(SRC[src]))["cfg"]["targets"]
    for k in SYS[src]:
        a, base, neg = signed(hv, k); b, _, _ = signed(st, k); v = round(a + f * (b - a), 4)
        hv.pop(base, None); hv.pop(neg, None)
        if v > 0: hv[base] = v
        elif v < 0 and neg: hv[neg] = -v
    out = {k: None for k in hv0 if k not in hv}; out.update(hv); return out
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
def hv_native(h):
    c = dict(json.load(open(HVB))["cfg"]); c.update(stature=float(h), id="HV%dN" % h, base_height_macro=json.load(open(HVB))["height_macro"]); return c
def frame(src_build, fr):
    b = json.load(open(src_build))["cfg"].get("bone_scales", {})
    return {"bone_scales": {k: [round(x * y, 6) for x, y in zip(b.get(k, [1, 1, 1]), v)] for k, v in fr.items()}}
def jobs(which):
    J = []
    if which == 'stature':      # macro builds at every point (route check), native where the accepted rule needs it
        for h in (152, 163, 173, 181, 190, 203, 213): J.append((variant, (HVB, {"stature": float(h), "resolve_stature": True}, W + '/st', 'HV%dM' % h)))
        for h in (152, 163): J.append((native, (hv_native(h), W + '/st', 'HV%dN' % h)))
    if which == 'frames':
        for h, b in ((152, W + '/st/HV152N-NAT_build.json'), (178, HVB), (213, W + '/st/HV213M_build.json')):
            for tag, fr in (("N", NARROWB), ("B", BROADB)): J.append((variant, (b, frame(b, fr), W + '/fr', 'HV%s%d' % (tag, h))))
    if which == 'expr':
        for src in ("FN", "AE", "VA", "SK", "SG"):
            J.append((variant, (HVB, {"targets": expr_targets(src), "resolve_stature": True, "stature": 178.0}, W + '/ex', 'HVX' + src)))
        # Marchfolk-influenced: the Halvren targets at half strength (broad human-family distribution)
        hv = json.load(open(HVB))["cfg"]["targets"]
        J.append((variant, (HVB, {"targets": {k: round(v * 0.5, 4) for k, v in hv.items()}, "resolve_stature": True, "stature": 178.0}, W + '/ex', 'HVXMF')))
    if which == 'comp':      # 173 cm (matched Marchfolk 173 / Sagekin 173 composition states)
        for nm, m, w in (("LOWMUS", 0, 0.5), ("HIMUS", 1, 0.5), ("HIFAT", 0.5, 1), ("HIBOTH", 1, 1), ("LOW", 0.25, 0.25), ("MIN", 0, 0)):
            J.append((variant, (W + '/st/HV173M_build.json', {"muscle": m, "weight": w}, W + '/comp', 'HV173-' + nm)))
    if which == 'stress':    # HV-36...43 and HV-07/08/09 body stress combinations
        for nm, b, m, w in (("HV36", W + '/fr/HVN178_build.json', 1.0, 0.5), ("HV37", W + '/fr/HVN178_build.json', 0.5, 1.0), ("HV38", W + '/fr/HVB178_build.json', 0.25, 0.25),
                            ("HV39", W + '/fr/HVB178_build.json', 1.0, 0.5), ("HV40", W + '/fr/HVB178_build.json', 0.5, 1.0), ("HV41", W + '/st/HV213M_build.json', 0.5, 1.0),
                            ("HV42", W + '/st/HV152N-NAT_build.json', 1.0, 0.5), ("HV43", W + '/ex/HVXFN_build.json', 1.0, 0.5),
                            ("HV08", HVB, 0.5, 1.0), ("HV09", HVB, 1.0, 0.5)):
            J.append((variant, (b, {"muscle": m, "weight": w}, W + '/stress', nm)))
    return J
if __name__ == '__main__':
    os.makedirs(W + '/logs', exist_ok=True)
    J = jobs(sys.argv[1])
    with ThreadPoolExecutor(2) as ex: list(ex.map(lambda j: j[0](*j[1]), J))
    print('DONE', sys.argv[1], len(J))
