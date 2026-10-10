# RAC W3A (Halvren genealogy-conditioned stature tails) body builder. Starts from the accepted W2G Halvren machinery (w2g_drivers/hv_build.py):
# HVC1 (~178 cm diagnostic anchor) targets; native short-adult route below the junction (native_short.py from HVC1's base macro), generator height
# macro re-solved above it; source-influenced expression = signed interpolation of HVC1 targets toward the source's own targets on the systems the
# Halvren canon names for that influence (hv_build.expr_targets; HVXMF = HVC1 targets at half strength).
# GENEALOGY / SOURCE-CONDITION CLASSES are DIAGNOSTIC TEST COORDINATES (order §6): the class names which source supplies the tail-stature support and
# which sources are expressed in the anatomy; the expression fraction is a hidden builder coordinate, never a genealogy percentage, lore or a control.
#   lower tail (native route; H-1: Marchfolk support only)            upper tail (macro route; H-1: Skarn / Aelari support)
#   HL<h>C   central Halvren anatomy, Marchfolk stature support        HU<h>C   central Halvren anatomy, Skarn / Aelari stature support
#   HL<h>M   Marchfolk-expressed anatomy (HVXMF construction)          HU<h>S   Skarn-expressed (expr_targets SK, 0.5)
#   HL<h>X   mixed human / elven: Marchfolk 0.5 + Fenn 0.5             HU<h>A   Aelari-expressed (expr_targets AE, 0.5)
#   HL<h>FN / VA / SG  controls: Fenn / Vael / Sagekin expression,     HU<h>SA  combined Skarn 0.5 + Aelari 0.5 (t_gen: shared systems at the mean
#            no Marchfolk support                                               of the two sources' signed targets)
#                                                                      HU<h>FN / VA / SG / MF  controls without Skarn / Aelari support
# Matched-height sources: Marchfolk native (W2A MFM147 configuration, MF base macro 0.5), Skarn W2B (SK_build re-solved), Aelari W2F (AEL1 re-solved).
# Frames: W2G breadth-only writes (Narrow -8 %; Broad +8 %, pelvis X x1.12). Composition: generator muscle / weight macros on the same skeleton.
# Statures are written <h> with 'p' for the decimal point (147p2 = 147.2 cm).   Usage: python3 tail_build.py JOBSET
import sys, os, json, glob, subprocess
from concurrent.futures import ThreadPoolExecutor
T = '/home/claude/wayfarer-design/tools/rac/w1'; S = '/tmp/claude-0/-home-claude-wayfarer-design/19af7d50-3b61-5fda-9fe0-7a30770fb334/scratchpad'
sys.path.insert(0, T + '/w2g_drivers'); import hv_build as H
W = S + '/w3a'; H.W = W
REF = H.REF; HVB = H.HVB
MFC = S + '/w2a/st/MFM147.cfg.json'; SKB = S + '/w1f/final/SK_build.json'; AEB = S + '/w1m/legs/AEL1_build.json'
def tag(h): return ("%g" % h).replace('.', 'p')
def strip(t): return {k: v for k, v in t.items() if v is not None}
def hv_t(): return dict(json.load(open(HVB))["cfg"]["targets"])
def t_mf(): return t_gen({"MF": 0.5})
def t_src(s, f=0.5): return t_gen({s: f})
def tgt(src):
    """the source's own signed targets and the base systems through which it is expressed (Marchfolk: HVC1's own Halvren-specific targets pulled
    toward the Marchfolk configuration, which has none - the HVXMF construction)"""
    if src == "MF": return {}, {H.signed({}, k)[1] for k in hv_t()}
    return json.load(open(H.SRC[src]))["cfg"]["targets"], {H.signed({}, k)[1] for k in H.SYS[src]}
def t_gen(e):
    """general diagnostic condition: hidden expression coordinates e = {source: fraction}, sum <= 1. On every base system the value is the convex
    combination (1 - sum e_s) * HVC1 + sum e_s * source_s over the sources that name that system (single source at 0.5 = hv_build.expr_targets)"""
    assert sum(e.values()) <= 1 + 1e-3
    hv0 = hv_t(); hv = dict(hv0); T_ = {s: tgt(s) for s in e}
    for base in sorted(set().union(*[T_[s][1] for s in e]) if e else []):
        x, _, neg = H.signed(hv0, base)
        v = round(x + sum(f * (H.signed(T_[s][0], base)[0] - x) for s, f in e.items() if base in T_[s][1]), 4); hv.pop(base, None); hv.pop(neg, None)
        if v > 0: hv[base] = v
        elif v < 0 and neg: hv[neg] = -v
    return hv
def t_mix(a, b, f=0.5): return t_gen({a: f, b: f})
def t_mfx(): return t_gen({"MF": 0.5, "FN": 0.5})
TL = {"C": hv_t, "M": t_mf, "X": t_mfx, "A": lambda: t_src("AE"), "S": lambda: t_src("SK"), "M1": lambda: t_gen({"MF": 1.0}), "FN": lambda: t_src("FN"), "VA": lambda: t_src("VA"), "SG": lambda: t_src("SG")}
TU = {"C": hv_t, "S1": lambda: t_gen({"SK": 1.0}), "S": lambda: t_src("SK"), "A": lambda: t_src("AE"), "SA": lambda: t_mix("SK", "AE"), "FN": lambda: t_src("FN"), "VA": lambda: t_src("VA"),
      "SG": lambda: t_src("SG"), "MF": t_mf}
def low(h, c, d='lo'):
    cfg = dict(json.load(open(HVB))["cfg"]); cfg.update(stature=float(h), id="HL%s%s" % (tag(h), c), base_height_macro=json.load(open(HVB))["height_macro"], targets=TL[c]())
    return (H.native, (cfg, W + '/' + d, cfg["id"]))
def mf(h, d='src'):
    cfg = dict(json.load(open(MFC))); cfg.update(stature=float(h), id="MF%s" % tag(h)); return (H.native, (cfg, W + '/' + d, cfg["id"]))
def up(h, c, d='up'):
    t = TU[c](); full = {k: None for k in hv_t() if k not in t}; full.update(t)
    return (H.variant, (HVB, {"targets": full, "resolve_stature": True, "stature": float(h)}, W + '/' + d, "HU%s%s" % (tag(h), c)))
def src(b, nm, h, d='src'): return (H.variant, (b, {"stature": float(h), "resolve_stature": True}, W + '/' + d, "%s%s" % (nm, tag(h))))
def built(j):
    out, nid = j[1][-2], j[1][-1]
    if j[0] is H.native: nid += '-NAT'
    return os.path.exists('%s/%s_meas.json' % (out, nid))
LO = (150, 149, 148, 147.5, 147.2); UP = (217, 221, 225, 228.8)
def jobs(which):
    J = []
    if which == 'search':
        for h in LO: J += [low(h, "C"), mf(h)]
        for h in (150, 148, 147.2): J.append(low(h, "M"))
        J.append(low(148, "X"))
        for h in UP: J += [up(h, "C"), up(h, "S"), src(SKB, "SK", h)]
        for h in (217, 220.8): J.append(up(h, "A"))
        J += [src(AEB, "AE", 217), src(AEB, "AE", 220.8), up(225, "A")]      # HU225A: beyond the valid Aelari range (source-first probe; never matched-height)
        for h in (221, 225, 228.8): J.append(up(h, "SA"))
    if which == 'controls':
        for c in ("FN", "VA", "SG"): J += [low(148, c, 'ctl'), up(221, c, 'ctl')]
        J.append(up(221, "MF", 'ctl'))
    if which == 'mix':      # rebuild of the combined classes with the additive t_gen construction (the first search pass used a sequential / halved-mean construction)
        J += [low(148, "X")] + [up(h, "SA") for h in (221, 225, 228.8)]
    if which == 'cal':      # emulator calibration: Aelari / Skarn expression in the lower-tail region, full-strength (e = 1) expression probes
        J += [low(148, "A"), low(148, "S"), low(148, "M1"), up(225, "S1")]
    if which == 'val':      # emulator validation: deterministic random diagnostic samples built on the real generator (w3a_sample.val_set)
        import w3a_sample as SM
        for nid, st, h, e in SM.val_set():
            t = t_gen(e)
            if st == "L-MF":
                cfg = dict(json.load(open(HVB))["cfg"]); cfg.update(stature=h, id=nid, base_height_macro=json.load(open(HVB))["height_macro"], targets=t); J.append((H.native, (cfg, W + '/val', nid)))
            else:
                full = {k: None for k in hv_t() if k not in t}; full.update(t); J.append((H.variant, (HVB, {"targets": full, "resolve_stature": True, "stature": h}, W + '/val', nid)))
    if which == 'refine':   # upper-tail bracket refinement at 219 cm (the lower-leg share leaves the scored span between 217 and 221 cm)
        J += [up(219, "C"), up(219, "S"), up(219, "A"), src(SKB, "SK", 219), src(AEB, "AE", 219)]
    if which == 'probe':    # TAIL-DEVELOPMENT PROBE (diagnostic, BUILDER-CHOSEN, NOT canon): the supporting source's own leg-segment development carried
        # into the tail - Skarn: its accepted short-femur target (measure-upperleg-height-decr 1.0) at half strength; Aelari: its accepted W1m leg bone
        # scales (thigh x0.9875, calf x1.0523) at half strength; the combined probe carries both at half strength. The Halvren canon-named Skarn / Aelari systems (HV-13...17) do not include leg segments.
        def dev(h, c, sk, ae):
            t = TU[c](); full = {k: None for k in hv_t() if k not in t}; full.update(t); ov = {"targets": full, "resolve_stature": True, "stature": float(h)}
            if sk: full.pop("measure-upperleg-height-incr", None); full["measure-upperleg-height-decr"] = round(1.0 * sk, 4)
            if ae: ov["bone_scales"] = {"LR:thigh": [1, round(1 - 0.0125 * ae, 5), 1], "LR:calf": [1, round(1 + 0.0523 * ae, 5), 1]}
            return (H.variant, (HVB, ov, W + '/probe', "HU%s%sD" % (tag(h), c)))
        J += [dev(h, "S", 0.5, 0) for h in (221, 225, 228.8)] + [dev(220.8, "A", 0, 0.5), dev(228.8, "SA", 0.5, 0.5)]
    if which == 'rs':       # RM-OT-03 REAL-BUILD samples (the linear emulator failed its own validation): deterministic draws, reference frame / composition
        import w3a_sample as SM
        for st, n in (("L-MF", 60), ("U-SK", 36), ("U-AE", 36), ("U-SA", 28)):
            d = SM.draw(st, n, frames=False)
            for i in range(n):
                nid = "R%s%02d" % (st.replace("-", ""), i); h = float(round(d["h"][i], 2)); e = {s_: float(round(d["E"][i, j], 4)) for j, s_ in enumerate(SM.SRC) if d["E"][i, j] > 1e-4}
                t = t_gen(e)
                if st == "L-MF":
                    cfg = dict(json.load(open(HVB))["cfg"]); cfg.update(stature=h, id=nid, base_height_macro=json.load(open(HVB))["height_macro"], targets=t); J.append((H.native, (cfg, W + '/rs', nid)))
                else:
                    full = {k: None for k in hv_t() if k not in t}; full.update(t); J.append((H.variant, (HVB, {"targets": full, "resolve_stature": True, "stature": h}, W + '/rs', nid)))
    if which == 'stress':   # frames and composition at the proposed endpoints + matched sources at the same composition / frame
        EP = [(W + '/lo/HL147p2C-NAT_build.json', 'HL147p2C')] + [(W + '/up/%s_build.json' % n, n) for n in ('HU228p8S', 'HU220p8A', 'HU228p8SA')]
        CS = (("LOWMUS", 0.0, 0.5), ("HIMUS", 1.0, 0.5), ("LOWFAT", 0.5, 0.0), ("HIFAT", 0.5, 1.0))
        for b, n in EP:
            J += [(H.variant, (b, H.frame(b, H.NARROWB), W + '/fr', n + '-N')), (H.variant, (b, H.frame(b, H.BROADB), W + '/fr', n + '-B'))]
            J += [(H.variant, (b, {"muscle": m, "weight": w}, W + '/comp', '%s-%s' % (n, c))) for c, m, w in CS]
        J.append(src(SKB, "SK", 220.8))
        for b, n in ((W + '/src/MF147p2-NAT_build.json', 'MF147p2'), (W + '/src/SK228p8_build.json', 'SK228p8'), (W + '/src/AE220p8_build.json', 'AE220p8')):
            J += [(H.variant, (b, {"muscle": m, "weight": w}, W + '/comp', '%s-%s' % (n, c))) for c, m, w in CS]
        b = W + '/src/SK228p8_build.json'; J.append((H.variant, (b, H.frame(b, H.BROADB), W + '/fr', 'SKB228p8')))
    return J
def run(J):
    os.makedirs(W + '/logs', exist_ok=True)
    J = [j for j in J if not built(j) or sys.argv[1] == 'mix']; print('TO BUILD', len(J), flush=True)
    with ThreadPoolExecutor(2) as ex: list(ex.map(lambda j: j[0](*j[1]), J))
if __name__ == '__main__':
    run(jobs(sys.argv[1])); print('DONE', sys.argv[1], flush=True)
