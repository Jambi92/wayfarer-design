# RAC W3A1 (Halvren tail closure) body builder. Order reviews/chatgpt-rac-w3a1-halvren-tail-closure-order.md. Reuses the W3A machinery
# (w3a_drivers/tail_build.py: HVC1 targets, t_gen hidden diagnostic coordinates, native / macro routes, matched sources) unchanged.
# AD-W3A-1 SOURCE-CONDITIONED LEG-SEGMENT DEVELOPMENT COUPLING (hidden Halvren developmental dependency; replaces the W3A half-strength probe):
#   operates only above the central envelope (h > 213 cm) and only for the source that supplies the tail stature under H-1:
#     Skarn support  -> the accepted Skarn short-femur development (Skarn target measure-upperleg-height-decr 1.0): signed value
#                       (1 - k) * HVC1 (0) + k * Skarn (-1.0)  -> measure-upperleg-height-decr = k
#     Aelari support -> the accepted Aelari W1m thigh / calf development (bone scales thigh x0.9875, calf x1.0523): thigh 1 - 0.0125 k, calf 1 + 0.0523 k
#     Skarn + Aelari -> Skarn is the stature-supporting source through the whole upper tail (Aelari support ends at 221 cm): Skarn coupling
#   strength k_s(h) = min(1, BETA_s * (h - 213))  - continuous, zero at the central ceiling (no junction at 213), monotone in stature.
#   BETA_s = the SMALLEST linear rate that keeps the most demanding supported class (central Halvren anatomy) at or above the Halvren's own accepted
#   lower-leg share at the top of its central envelope (HV213 shin / leg 0.4804; boundary-stature span floor SG208 0.4799), from the W3A k = 0 / 0.5
#   responses (Skarn: -dL/dk 0.0250-0.0260; Aelari: 0.0176). Diagnostic construction parameters, NOT species constants. The coupling never drives
#   a Halvren to the source's own segment proportions (Skarn 228.8 shin / leg 0.4900; the coupled Halvren is held near 0.480).
# Usage: python3 w3a1_build.py JOBSET   (family | onset | ksweep | src | stress | rsup | central)
import sys, os, json
sys.path.insert(0, '/home/claude/wayfarer-design/tools/rac/w1/w3a_drivers'); import tail_build as TB
H = TB.H; S = TB.S; W0 = TB.W; W = S + '/w3a1'
BETA = {"SK": 0.030, "AE": 0.052}; H0 = 213.0
def k_rule(h, s): return min(1.0, BETA[s] * max(0.0, h - H0))
def couple(ov, s, k):
    if k <= 0: return ov
    if s == "SK":   # signed interpolation of the femur-length system toward Skarn (-1.0), from whatever the body already carries (e.g. Aelari expression)
        t = ov["targets"]; v0 = (t.get("measure-upperleg-height-incr") or 0) - (t.get("measure-upperleg-height-decr") or 0); v = round((1 - k) * v0 - k, 4)
        t["measure-upperleg-height-incr"] = v if v > 0 else None; t["measure-upperleg-height-decr"] = -v if v < 0 else None
    else: ov["bone_scales"] = {"LR:thigh": [1, round(1 - 0.0125 * k, 5), 1], "LR:calf": [1, round(1 + 0.0523 * k, 5), 1]}
    return ov
def full(t): f = {k: None for k in TB.hv_t() if k not in t}; f.update(t); return f
def upc(h, t, s, nid, d='up', k=None):
    ov = couple({"targets": full(t), "resolve_stature": True, "stature": float(h)}, s, k_rule(h, s) if k is None else k)
    return (H.variant, (TB.HVB, ov, W + '/' + d, nid))
TU = {"C": TB.hv_t, "S": lambda: TB.t_src("SK"), "A": lambda: TB.t_src("AE"), "SA": lambda: TB.t_mix("SK", "AE")}
def tg(h): return TB.tag(h)
AE221B = S + '/w2f/st/AE221_build.json'
def jobs(which):
    J = []
    if which == 'family':   # coupled upper-tail family (suffix c = coupled; Cc = central anatomy Skarn-supported, Ca = central anatomy Aelari-supported)
        J += [upc(h, TU["S"](), "SK", "HU%sSc" % tg(h)) for h in (215, 217, 219, 221, 223, 225, 227, 228.8)]
        J += [upc(h, TU["C"](), "SK", "HU%sCc" % tg(h)) for h in (217, 221, 225, 228.8)]
        J += [upc(h, TU["A"](), "AE", "HU%sAc" % tg(h)) for h in (215, 217, 219, 220.8, 221)]
        J += [upc(221, TU["C"](), "AE", "HU221Ca")]
        J += [upc(h, TU["SA"](), "SK", "HU%sSAc" % tg(h)) for h in (221, 225, 228.8)]
    if which == 'onset':    # coupling onset: uncoupled 213 cm Skarn- / Aelari-expressed bodies (k = 0 by the rule) + 215 cm central coupled
        J += [upc(213, TU["S"](), "SK", "HU213S"), upc(213, TU["A"](), "AE", "HU213A"), upc(215, TU["C"](), "SK", "HU215Cc")]
    if which == 'ksweep':   # continuity in the coupling strength itself at fixed stature (228.8 cm Skarn-expressed): k = 0.25, 0.75, 1.0 (k = 0, 0.5 from W3A)
        J += [upc(228.8, TU["S"](), "SK", "HU228p8Sk%02d" % round(100 * k), 'ks', k) for k in (0.25, 0.75, 1.0)]
    if which == 'src':      # matched sources at the new family statures + Marchfolk 157 (native, W2A configuration) for the central confirmation
        J += [TB.src(TB.SKB, "SK", h, d='../w3a1/src') for h in (215, 223, 227)] + [TB.src(TB.AEB, "AE", 215, d='../w3a1/src')]
        c = dict(json.load(open(TB.MFC))); c.update(stature=157.0, id="MF157"); J.append((H.native, (c, W + '/src', "MF157")))
    if which == 'stress':   # frames + composition at the final coupled endpoints; Aelari 221 composition partners
        EP = [(W + '/up/%s_build.json' % n, n) for n in ('HU228p8Sc', 'HU221Ac', 'HU228p8SAc')]
        CS = (("LOWMUS", 0.0, 0.5), ("HIMUS", 1.0, 0.5), ("LOWFAT", 0.5, 0.0), ("HIFAT", 0.5, 1.0))
        for b, n in EP:
            J += [(H.variant, (b, H.frame(b, H.NARROWB), W + '/fr', n + '-N')), (H.variant, (b, H.frame(b, H.BROADB), W + '/fr', n + '-B'))]
            J += [(H.variant, (b, {"muscle": m, "weight": w_}, W + '/comp', '%s-%s' % (n, c))) for c, m, w_ in CS]
        J += [(H.variant, (AE221B, {"muscle": m, "weight": w_}, W + '/comp', 'AE221-%s' % c)) for c, m, w_ in CS]
        J += [(H.variant, (AE221B, H.frame(AE221B, H.NARROWB), W + '/fr', 'AEN221'))]
    if which == 'rsup':     # W3A RM-OT-03 upper samples with the strongest supporting-source coordinate, rebuilt under the coupling (source-protection recheck)
        import w3a_sample as SM, numpy as np
        for st, n, top, sup in (("U-SK", 36, 8, "SK"), ("U-AE", 36, 4, "AE"), ("U-SA", 28, 4, "SK")):
            d = SM.draw(st, n, frames=False); es = d["E"][:, [SM.SRC.index(s) for s in (("SK",) if st == "U-SK" else ("AE",) if st == "U-AE" else ("SK", "AE"))]].sum(1)
            for i in np.argsort(-es)[:top]:
                h = float(round(d["h"][i], 2)); e = {s_: float(round(d["E"][i, j], 4)) for j, s_ in enumerate(SM.SRC) if d["E"][i, j] > 1e-4}
                J.append(upc(h, TB.t_gen(e), sup, "R%s%02dc" % (st.replace("-", ""), i), 'rsup'))
    if which == 'central':  # AD-W3A-4 focused native-range confirmation: strong Marchfolk expression at 152 / 157 / 163 cm (native route, below the junction)
        for h in (152, 157, 163):
            for x in (0.6, 0.8, 0.9, 1.0):
                cfg = dict(json.load(open(TB.HVB))["cfg"]); nid = "HC%sM%02d" % (tg(h), round(100 * x))
                cfg.update(stature=float(h), id=nid, base_height_macro=json.load(open(TB.HVB))["height_macro"], targets=TB.t_gen({"MF": x}))
                J.append((H.native, (cfg, W + '/cen', nid)))
    return J
def built(j):
    out, nid = j[1][-2], j[1][-1]
    if j[0] is H.native: nid += '-NAT'
    return os.path.exists('%s/%s_meas.json' % (out, nid))
if __name__ == '__main__':
    from concurrent.futures import ThreadPoolExecutor
    H.W = W; os.makedirs(W + '/logs', exist_ok=True)
    J = [j for j in jobs(sys.argv[1]) if not built(j)]; print('TO BUILD', len(J), flush=True)
    with ThreadPoolExecutor(2) as ex: list(ex.map(lambda j: j[0](*j[1]), J))
    print('DONE', sys.argv[1], flush=True)
