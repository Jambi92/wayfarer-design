# RAC W3A RM-OT-03: source-passing statistics on deterministic generated Halvren tail samples via a CALIBRATED RESPONSE EMULATOR of the real
# generator (real builds take ~1 min each; several thousand samples per stratum are only practical through an emulator). NON-CANON diagnostics.
# Readings: the 17 body-only readings of the W2G neutralized source-passing protocol that need no skeletal-proxy grid (13 skin ratios + 4 exact-plane
# joints per adjacent segment). The full protocol has 24 (+7 skeletal); with fewer readings a sample can only separate on fewer readings, so a
# NEAR-DUPLICATE call on 17 is CONSERVATIVE (it over-calls duplication relative to 24) - checked on the real builds.
# Emulator (all terms measured on real builds, linear in the hidden expression coordinates):
#   r(h, e, phi, m, w) = rC(h) + sum_s e_s * D_s(h) / 0.5 + frame(phi) + comp(m, w)
#   rC(h)   central Halvren route: piecewise linear over the real HL / HV / HU central series (native below the junction, macro above)
#   D_s(h)  real e = 0.5 single-source expression body minus rC at its stature (lower region: 148 cm, Marchfolk also 147.2 / 150; upper region: Skarn
#           217 / 221 / 225 / 228.8, Aelari 217 / 220.8, Fenn / Vael / Sagekin / Marchfolk 221), interpolated in h, held constant outside
#   frame   real Narrow / Broad endpoint builds (breadth-only write), linear in |phi|;  comp: real LOWMUS / HIMUS / LOWFAT / HIFAT endpoint builds, linear
# Sources: matched height where the source has a valid adult (interpolated over the real source family: Marchfolk 147-152, Skarn 208-229,
# Aelari 211-221), otherwise its nearest valid adult (ENDPOINT, labelled; Aelari above 221 = W2G D1). Same composition: the source's own real
# composition delta where built (Marchfolk 147.2, Skarn 228.8, Aelari 220.8), else the Halvren delta (same generator operation; approximation).
# Classes per source: NEAR-DUPLICATE (< 2 readings separate by >= 1 %; W2G protocol), AMBIGUOUS (2-3; hard-to-classify band, diagnostic only),
# DISTINCT (>= 4). Sample rejection reasons: DUPLICATE of a matched-height source; ADULT-READ (lower tail head share above matched Marchfolk by >= 1 %).
# Usage: python3 w3a_emul.py VALUES.json OUT.json
import sys, json, numpy as np
sys.path.insert(0, '/home/claude/wayfarer-design/tools/rac/w1/w3a_drivers'); import w3a_sample as SM
V = json.load(open(sys.argv[1]))["values"]; OUT = sys.argv[2]
JP = lambda j: "%s breadth / adjacent segment (exact-plane section)" % j
K = ["torso_share", "leg_share", "arm_share", "span_der", "forearm_over_arm", "shin_over_leg", "neck_share", "hand_share", "finger_over_hand", "palm_breadth_over_hand",
     "foot_share", "thorax_breadth_share", "thorax_depth_share", JP("elbow"), JP("wrist"), JP("knee"), JP("ankle")]
HH = "HH_share"; KK = K + [HH]
def vec(b): return np.array([V[b][k] for k in KK], float)
def st(b): return V[b]["stature (cm)"]
def interp(names):
    P = sorted((st(b), vec(b)) for b in names if b in V); hs = np.array([p[0] for p in P]); M = np.array([p[1] for p in P])
    def f(h):
        h = np.atleast_1d(h); return np.stack([np.interp(h, hs, M[:, j]) for j in range(M.shape[1])], 1)
    return f, (hs.min(), hs.max())
RC, _ = interp(["HL147p2C", "HL147p5C", "HL148C", "HL149C", "HL150C", "HV152", "HV163", "HV173", "HV178", "HV181", "HV190", "HV203", "HV213", "HU217C", "HU221C", "HU225C", "HU228p8C"])
def delta(bodies, e=0.5):
    """D(h) per unit expression: (body - rC at its stature) / e, interpolated over the bodies' statures"""
    P = sorted((st(b), (vec(b) - RC(st(b))[0]) / e) for b in bodies if b in V); hs = np.array([p[0] for p in P]); M = np.array([p[1] for p in P])
    return lambda h: np.stack([np.interp(np.atleast_1d(h), hs, M[:, j]) for j in range(M.shape[1])], 1)
D = {"L": {"MF": delta(["HL147p2M", "HL148M", "HL150M"]), "FN": delta(["HL148FN"]), "VA": delta(["HL148VA"]), "SG": delta(["HL148SG"]), "AE": delta(["HL148A"]), "SK": delta(["HL148S"])},
     "U": {"SK": delta(["HU217S", "HU221S", "HU225S", "HU228p8S"]), "AE": delta(["HU217A", "HU220p8A"]), "FN": delta(["HU221FN"]), "VA": delta(["HU221VA"]),
           "SG": delta(["HU221SG"]), "MF": delta(["HU221MF"])}}
def fd(base, x): return vec(x) - vec(base)
EPS = {"L": ["HL147p2C"], "U": ["HU228p8S", "HU220p8A", "HU228p8SA"]}
FR = {g: {t: np.mean([fd(e, e + "-" + t) for e in EPS[g]], 0) for t in ("N", "B")} for g in EPS}
CO = {g: {c: np.mean([fd(e, e + "-" + c) for e in EPS[g]], 0) for c in ("LOWMUS", "HIMUS", "LOWFAT", "HIFAT")} for g in EPS}
SCO = {"MF": {c: fd("MF147p2", "MF147p2-" + c) for c in CO["L"]}, "SK": {c: fd("SK228p8", "SK228p8-" + c) for c in CO["L"]}, "AE": {c: fd("AE220p8", "AE220p8-" + c) for c in CO["L"]}}
SFR = {"SK": {"B": fd("SK228p8", "SKB228p8")}}
def comp(dc, m, w):
    m = np.asarray(m)[:, None]; w = np.asarray(w)[:, None]
    return (np.where(m < 0.5, (0.5 - m) / 0.5, 0) * dc["LOWMUS"] + np.where(m > 0.5, (m - 0.5) / 0.5, 0) * dc["HIMUS"]
            + np.where(w < 0.5, (0.5 - w) / 0.5, 0) * dc["LOWFAT"] + np.where(w > 0.5, (w - 0.5) / 0.5, 0) * dc["HIFAT"])
def frame(df, phi):
    phi = np.asarray(phi)[:, None]; return np.where(phi < 0, -phi, 0) * df["N"] + np.where(phi > 0, phi, 0) * df["B"]
# source families: valid adult range + interpolator over the real bodies (matched height) or the nearest valid adult (endpoint)
FAM = {"MF": (147.0, 203.0, ["MF147", "MF147p2", "MF147p5", "MF148", "MF149", "MF150", "MF152", "MF163", "MF173", "MF178", "MF181", "MF190", "MF203"]),
       "SK": (183.0, 229.0, ["SK183", "SK190", "SK203", "SK208", "SK217", "SK220p8", "SK221", "SK225", "SK228p8", "SK229"]),
       "AE": (168.0, 221.0, ["AE168", "AE173", "AE178", "AE181", "AE190", "AE203", "AE211", "AE217", "AE220p8", "AE221"]),
       "FN": (157.0, 211.0, ["FN157", "FN163", "FN173", "FN178", "FN181", "FN190", "FN203", "FN211"]),
       "VA": (157.0, 203.0, ["VA157", "VA163", "VA173", "VA178", "VA181", "VA190", "VA203"]),
       "SG": (152.0, 208.0, ["SG152", "SG163", "SG173", "SG178", "SG181", "SG190", "SG203", "SG208"])}
FI = {s: interp(b)[0] for s, (_, _, b) in FAM.items()}
def source(s, h, g, m, w, phi):
    lo, hi, _ = FAM[s]; hc = np.clip(h, lo, hi); matched = (h >= lo - 1e-9) & (h <= hi + 1e-9)
    r = FI[s](hc) + comp(SCO.get(s, CO[g]), m, w)
    sf = dict(FR[g]); sf.update(SFR.get(s, {})); r = r + frame(sf, phi)
    return r, matched
def emulate(d, g):
    h, E = d["h"], d["E"]; r = RC(h)
    for j, s in enumerate(SM.SRC): r = r + E[:, j:j + 1] * D[g][s](h) / 0.5
    return r + frame(FR[g], d["phi"]) + comp(CO[g], d["muscle"], d["weight"])
def nsep(a, b): return (np.abs(a[:, :len(K)] / b[:, :len(K)] - 1) >= 0.01).sum(1)
def classify(d, g, r=None, noise=None, rng=None):
    r = emulate(d, g) if r is None else r
    if noise is not None: r = r * (1 + rng.normal(0, 1, r.shape) * noise[None, :])
    res = {}
    for s in SM.SRC:
        rs, matched = source(s, d["h"], g, d["muscle"], d["weight"], d["phi"]); n = nsep(r, rs)
        res[s] = {"nsep": n, "matched": matched}
    mf, _ = source("MF", d["h"], g, d["muscle"], d["weight"], d["phi"])
    adult_bad = (r[:, -1] / mf[:, -1] - 1 >= 0.01) if g == "L" else np.zeros(len(d["h"]), bool)
    dup_matched = np.zeros(len(d["h"]), bool)
    for s in SM.SRC: dup_matched |= (res[s]["nsep"] < 2) & res[s]["matched"]
    accept = ~dup_matched & ~adult_bad
    amb = accept & (np.min([res[s]["nsep"] for s in SM.SRC], 0) <= 3)
    return res, accept, dup_matched, adult_bad, amb
def wilson(k, n, z=1.96):
    if n == 0: return (None, None)
    p = k / n; d = 1 + z * z / n; c = (p + z * z / (2 * n)) / d; hw = z * np.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d; return (max(0.0, c - hw), min(1.0, c + hw))
OUTJ = {"readings": K, "adult_read": HH, "design": "coverage sampling (w3a_sample.py); NOT a prevalence model", "strata": {}}
# --- emulator validation on the real random builds (w3a_sample.val_set; reference frame / composition)
VAL = []
for nid, stt, h, e in SM.val_set():
    if nid not in V: continue
    g = "L" if stt == "L-MF" else "U"; dd = {"h": np.array([st(nid)]), "E": np.array([[e.get(s, 0.0) for s in SM.SRC]]), "phi": np.zeros(1), "muscle": np.full(1, 0.5), "weight": np.full(1, 0.5)}
    pr = emulate(dd, g)[0]; re = vec(nid); rel = pr / re - 1
    real = {s: int(nsep(re[None], source(s, dd["h"], g, dd["muscle"], dd["weight"], dd["phi"])[0])[0]) for s in SM.SRC}
    emu = {s: int(nsep(pr[None], source(s, dd["h"], g, dd["muscle"], dd["weight"], dd["phi"])[0])[0]) for s in SM.SRC}
    VAL.append({"id": nid, "stratum": stt, "h": st(nid), "e": e, "rel_err": dict(zip(KK, rel.tolist())), "nsep_real": real, "nsep_emul": emu})
# calibration-independent probes (not used to fit): combined classes and full-strength expression
PROBES = []
for nid, g, e in (("HL148X", "L", {"MF": 0.5, "FN": 0.5}), ("HU221SA", "U", {"SK": 0.5, "AE": 0.5}), ("HU225SA", "U", {"SK": 0.5, "AE": 0.5}), ("HU228p8SA", "U", {"SK": 0.5, "AE": 0.5}),
                  ("HL148M1", "L", {"MF": 1.0}), ("HU225S1", "U", {"SK": 1.0})):
    if nid not in V: continue
    dd = {"h": np.array([st(nid)]), "E": np.array([[e.get(s, 0.0) for s in SM.SRC]]), "phi": np.zeros(1), "muscle": np.full(1, 0.5), "weight": np.full(1, 0.5)}
    pr = emulate(dd, g)[0]; re = vec(nid); PROBES.append({"id": nid, "e": e, "rel_err": dict(zip(KK, (pr / re - 1).tolist()))})
ALLV = np.array([list(v["rel_err"].values()) for v in VAL] + [list(p["rel_err"].values()) for p in PROBES]) if VAL else None
SIG = np.sqrt((ALLV ** 2).mean(0)) if ALLV is not None else np.zeros(len(KK))
OUTJ["validation"] = {"bodies": VAL, "probes": PROBES, "rms_rel_err": dict(zip(KK, SIG.tolist())), "max_abs_rel_err": dict(zip(KK, np.abs(ALLV).max(0).tolist())) if ALLV is not None else None,
                      "nsep_agreement": {s: {"exact": int(sum(v["nsep_real"][s] == v["nsep_emul"][s] for v in VAL)), "class_same": int(sum((min(v["nsep_real"][s], 4) >= 4) == (min(v["nsep_emul"][s], 4) >= 4) and (v["nsep_real"][s] < 2) == (v["nsep_emul"][s] < 2) for v in VAL)), "n": len(VAL)} for s in SM.SRC}}
# --- strata
N = 8000; CK = (250, 500, 1000, 2000, 4000, 8000)
SUPPORT = {"L-MF": "MF", "U-SK": "SK", "U-AE": "AE", "U-SA": "SK"}
for stt in SM.STRATA:
    g = "L" if stt.startswith("L") else "U"; d = SM.draw(stt, N)
    res, acc, dup, adb, amb = classify(d, g)
    S_ = {"n": N, "seed": SM.SEED[stt], "accepted": int(acc.sum()), "rejected_duplicate_matched": int(dup.sum()), "rejected_adult_read": int(adb.sum()),
          "accepted_ambiguous": int(amb.sum()), "per_source": {}, "convergence": {}, "frontier": {}, "noise_band": {}}
    for s in SM.SRC:
        n = res[s]["nsep"]; mt = res[s]["matched"]
        S_["per_source"][s] = {"matched_fraction": float(mt.mean()), "near_duplicate": int((n < 2).sum()), "ambiguous_2_3": int(((n >= 2) & (n <= 3)).sum()), "distinct": int((n >= 4).sum()),
                               "near_duplicate_rate": float((n < 2).mean()), "ci95": wilson(int((n < 2).sum()), N), "comparison": "matched height" if mt.all() else ("ENDPOINT (nearest valid adult)" if not mt.any() else "mixed"),
                               "nsep_quantiles": np.percentile(n, [0, 5, 25, 50, 75, 95, 100]).tolist()}
    for c in CK:
        S_["convergence"][c] = {"accept_rate": float(acc[:c].mean()), "accept_ci95": wilson(int(acc[:c].sum()), c), "ambiguous_rate": float(amb[:c].mean()),
                                **{"dup_" + s: float((res[s]["nsep"][:c] < 2).mean()) for s in SM.SRC}}
    sup = SUPPORT[stt]; es = d["E"][:, SM.SRC.index(sup)] + (d["E"][:, SM.SRC.index("AE")] if stt == "U-SA" else 0)
    for lo in np.arange(0, 1.0, 0.1):
        m = (es >= lo) & (es < lo + 0.1 + (1e-9 if lo >= 0.89 else 0))
        if m.sum(): S_["frontier"]["%.1f-%.1f" % (lo, lo + 0.1)] = {"n": int(m.sum()), "dup_rate_matched": float(dup[m].mean()), "ambiguous_rate": float(amb[m].mean()),
                                                                     "accept_rate": float(acc[m].mean()), "adult_read_reject": float(adb[m].mean())}
    hb = np.linspace(*SM.STRATA[stt][0], 6)
    S_["by_stature"] = {"%.1f-%.1f" % (hb[i], hb[i + 1]): {"n": int(((d["h"] >= hb[i]) & (d["h"] < hb[i + 1])).sum()), "accept_rate": float(acc[(d["h"] >= hb[i]) & (d["h"] < hb[i + 1])].mean())} for i in range(5)}
    rng = np.random.RandomState(SM.SEED[stt] + 1); band = []
    for rep in range(20):
        _, a2, d2, b2, m2 = classify(d, g, noise=SIG, rng=rng); band.append((a2.mean(), d2.mean(), b2.mean(), m2.mean()))
    band = np.array(band); S_["noise_band"] = {"replicates": 20, "accept": [float(band[:, 0].min()), float(band[:, 0].max())], "dup_matched": [float(band[:, 1].min()), float(band[:, 1].max())],
                                               "adult_read": [float(band[:, 2].min()), float(band[:, 2].max())], "ambiguous": [float(band[:, 3].min()), float(band[:, 3].max())]}
    OUTJ["strata"][stt] = S_
    print(stt, "accepted %d / %d" % (acc.sum(), N), "dup", dup.sum(), "adult", adb.sum(), "amb", amb.sum(), {s: S_["per_source"][s]["near_duplicate"] for s in SM.SRC})
# controls (H-1): a tail stature attributed to Fenn / Vael / Sagekin (both tails) or Marchfolk (upper) has no supporting source adult at that stature
OUTJ["controls"] = {"L": {s: {"source_range": FAM[s][:2], "reaches_below_152": FAM[s][0] < 152} for s in ("FN", "VA", "SG", "MF", "AE", "SK")},
                    "U": {s: {"source_range": FAM[s][:2], "reaches_above_213": FAM[s][1] > 213} for s in ("FN", "VA", "SG", "MF", "AE", "SK")}}
json.dump(OUTJ, open(OUT, "w"), indent=1, default=lambda o: o.tolist() if hasattr(o, "tolist") else float(o))
print("VALIDATION rms rel err (%):", {k[:14]: round(100 * v, 2) for k, v in zip(KK, SIG)})
for s in SM.SRC: print(" nsep agreement", s, OUTJ["validation"]["nsep_agreement"][s])
