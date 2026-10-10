# RAC W3A RM-OT-03: source-passing statistics on REAL-BUILD deterministic Halvren tail samples (NON-CANON diagnostics).
# Why real builds: the linear response emulator (w3a_emul.py) FAILED its own validation - joint-breadth / thoracic-depth / neck readings respond
# non-linearly to the hidden expression coordinates (rms error 3.7-6.9 % on wrist / knee / ankle / thoracic depth against a 1 % separation
# threshold), and it under-called Marchfolk duplication on 3 of 8 lower-tail validation bodies. Its rates are therefore NOT reported as results.
# Samples: w3a_sample.draw (coverage design, fixed seeds) built on the real generator (tail_build.py 'rs': L-MF 60, U-SK 36, U-AE 36, U-SA 28) +
# the 20 emulator-validation builds (w3a_sample.val_set, seeds SEED['VAL'] + k), all at reference frame / composition (frame and composition do
# not change the separations materially at the endpoints: F / M rows).
# Readings: the 17 body-only readings needing no skeletal grid (13 skin + 4 exact-plane joints): CONSERVATIVE vs the 24-reading protocol.
# Sources: matched height = linear interpolation between the real accepted / W3A source bodies of that family inside its valid range; outside it
# the nearest valid adult (ENDPOINT, labelled; Aelari above 221 = W2G D1). Classes per source: NEAR-DUPLICATE < 2 readings separate by >= 1 %;
# AMBIGUOUS 2-3 (diagnostic band); DISTINCT >= 4. Rejections: DUPLICATE of a matched-height source; ADULT-READ (lower tail: head share above
# matched Marchfolk by >= 1 %).   Usage: python3 w3a_rs.py VALUES.json OUT.json
import sys, json, numpy as np
sys.path.insert(0, '/home/claude/wayfarer-design/tools/rac/w1/w3a_drivers'); import w3a_sample as SM
V = json.load(open(sys.argv[1]))["values"]; OUT = sys.argv[2]
JP = lambda j: "%s breadth / adjacent segment (exact-plane section)" % j
K = ["torso_share", "leg_share", "arm_share", "span_der", "forearm_over_arm", "shin_over_leg", "neck_share", "hand_share", "finger_over_hand", "palm_breadth_over_hand",
     "foot_share", "thorax_breadth_share", "thorax_depth_share", JP("elbow"), JP("wrist"), JP("knee"), JP("ankle")]
KK = K + ["HH_share"]
def vec(b): return np.array([V[b][k] for k in KK], float)
def st(b): return V[b]["stature (cm)"]
FAM = {"MF": (147.0, 203.0, ["MF147", "MF147p2", "MF147p5", "MF148", "MF149", "MF150", "MF152", "MF163", "MF173", "MF178", "MF181", "MF190", "MF203"]),
       "SK": (183.0, 229.0, ["SK183", "SK190", "SK203", "SK208", "SK217", "SK219", "SK220p8", "SK221", "SK225", "SK228p8", "SK229"]),
       "AE": (168.0, 221.0, ["AE168", "AE173", "AE178", "AE181", "AE190", "AE203", "AE211", "AE217", "AE219", "AE220p8", "AE221"]),
       "FN": (157.0, 211.0, ["FN157", "FN163", "FN173", "FN178", "FN181", "FN190", "FN203", "FN211"]),
       "VA": (157.0, 203.0, ["VA157", "VA163", "VA173", "VA178", "VA181", "VA190", "VA203"]),
       "SG": (152.0, 208.0, ["SG152", "SG163", "SG173", "SG178", "SG181", "SG190", "SG203", "SG208"])}
def src(s, h):
    lo, hi, names = FAM[s]; P = sorted((st(b), vec(b)) for b in names if b in V); hs = np.array([p[0] for p in P]); M = np.array([p[1] for p in P])
    hc = min(max(h, lo), hi); return np.array([np.interp(hc, hs, M[:, j]) for j in range(M.shape[1])]), lo - 1e-6 <= h <= hi + 1e-6
def nsep(a, b): return int((np.abs(a[:len(K)] / b[:len(K)] - 1) >= 0.01).sum())
def wilson(k, n, z=1.96):
    if n == 0: return [None, None]
    p = k / n; d = 1 + z * z / n; c = (p + z * z / (2 * n)) / d; hw = z * np.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d; return [max(0.0, c - hw), min(1.0, c + hw)]
SUP = {"L-MF": ("MF",), "U-SK": ("SK",), "U-AE": ("AE",), "U-SA": ("SK", "AE")}
samples = []
for stt, n in (("L-MF", 60), ("U-SK", 36), ("U-AE", 36), ("U-SA", 28)):
    d = SM.draw(stt, n, frames=False)
    for i in range(n): samples.append(("R%s%02d" % (stt.replace("-", ""), i), stt, {s: float(round(d["E"][i, j], 4)) for j, s in enumerate(SM.SRC) if d["E"][i, j] > 1e-4}, "rs"))
for nid, stt, h, e in SM.val_set(): samples.append((nid, stt, e, "val"))
rows = []
for nid, stt, e, batch in samples:
    if nid not in V: continue
    r = vec(nid); h = st(nid); rec = {"id": nid, "stratum": stt, "batch": batch, "h": h, "e": e, "e_support": sum(e.get(s, 0) for s in SUP[stt]), "per_source": {}}
    for s in SM.SRC:
        rs, m = src(s, h); n_ = nsep(r, rs); rec["per_source"][s] = {"nsep": n_, "matched": m, "class": "NEAR-DUPLICATE" if n_ < 2 else ("AMBIGUOUS" if n_ <= 3 else "DISTINCT")}
    mf, _ = src("MF", h)
    rec["adult_read_fail"] = bool(stt == "L-MF" and r[-1] / mf[-1] - 1 >= 0.01)
    rec["dup_matched"] = [s for s in SM.SRC if rec["per_source"][s]["matched"] and rec["per_source"][s]["nsep"] < 2]
    rec["dup_endpoint"] = [s for s in SM.SRC if not rec["per_source"][s]["matched"] and rec["per_source"][s]["nsep"] < 2]
    rec["accepted"] = not rec["dup_matched"] and not rec["adult_read_fail"]
    rec["ambiguous"] = rec["accepted"] and min(v["nsep"] for v in rec["per_source"].values()) <= 3
    rows.append(rec)
OUTJ = {"readings": K, "design": "coverage sampling (w3a_sample.py); NOT a prevalence model", "samples": rows, "strata": {}}
for stt in SUP:
    R = [x for x in rows if x["stratum"] == stt]; n = len(R)
    if not n: continue
    acc = sum(x["accepted"] for x in R); dup = sum(bool(x["dup_matched"]) for x in R); amb = sum(x["ambiguous"] for x in R); adb = sum(x["adult_read_fail"] for x in R)
    S_ = {"n": n, "accepted": acc, "accept_ci95": wilson(acc, n), "rejected_duplicate_matched": dup, "dup_ci95": wilson(dup, n), "rejected_adult_read": adb, "accepted_ambiguous": amb, "amb_ci95": wilson(amb, n), "per_source": {}, "convergence": {}, "frontier": {}}
    for s in SM.SRC:
        ns = [x["per_source"][s]["nsep"] for x in R]; mt = [x["per_source"][s]["matched"] for x in R]
        S_["per_source"][s] = {"comparison": "matched height" if all(mt) else ("ENDPOINT (nearest valid adult)" if not any(mt) else "mixed"), "near_duplicate": sum(v < 2 for v in ns),
                               "near_duplicate_ci95": wilson(sum(v < 2 for v in ns), n), "ambiguous_2_3": sum(2 <= v <= 3 for v in ns), "distinct": sum(v >= 4 for v in ns), "nsep_quantiles": np.percentile(ns, [0, 25, 50, 75, 100]).tolist()}
    for c in sorted(set([10, 20, 30, 40, 60, n])):
        if c > n: continue
        RR = R[:c]; S_["convergence"][c] = {"accept": sum(x["accepted"] for x in RR) / c, "dup_matched": sum(bool(x["dup_matched"]) for x in RR) / c, "ambiguous": sum(x["ambiguous"] for x in RR) / c,
                                             "dup_ci95": wilson(sum(bool(x["dup_matched"]) for x in RR), c)}
    for lo in (0.0, 0.2, 0.4, 0.6, 0.7, 0.8, 0.9):
        hi = {0.0: 0.2, 0.2: 0.4, 0.4: 0.6, 0.6: 0.7, 0.7: 0.8, 0.8: 0.9, 0.9: 1.01}[lo]; RR = [x for x in R if lo <= x["e_support"] < hi]
        if RR: S_["frontier"]["%.1f-%.1f" % (lo, min(hi, 1.0))] = {"n": len(RR), "dup_matched": sum(bool(x["dup_matched"]) for x in RR), "ambiguous": sum(x["ambiguous"] for x in RR), "accepted": sum(x["accepted"] for x in RR)}
    # logistic P(dup | e_support) by Newton iterations (2 parameters); bootstrap 95 % interval of the 50 % point
    xs = np.array([x["e_support"] for x in R]); ys = np.array([1.0 if x["dup_matched"] else 0.0 for x in R])
    def fit(x, y):
        if y.sum() in (0, len(y)): return None
        b = np.zeros(2); X = np.c_[np.ones_like(x), x]
        for _ in range(50):
            p = 1 / (1 + np.exp(-X @ b)); W_ = p * (1 - p) + 1e-9; H_ = X.T @ (X * W_[:, None]) + 1e-6 * np.eye(2); b = b + np.linalg.solve(H_, X.T @ (y - p))
            if abs(b[1]) > 200: return None      # separable data: no finite estimate
        return b
    b = fit(xs, ys); S_["logistic"] = None
    if b is not None:
        rng = np.random.RandomState(SM.SEED[stt] + 7); mids = []
        for _ in range(1000):
            ii = rng.randint(0, n, n); bb = fit(xs[ii], ys[ii])
            if bb is not None and bb[1] > 0: mids.append(-bb[0] / bb[1])
        S_["logistic"] = {"b0": float(b[0]), "b1": float(b[1]), "e50": float(-b[0] / b[1]) if b[1] else None, "e50_boot95": np.percentile(mids, [2.5, 97.5]).tolist() if len(mids) > 50 else None, "boot_ok": len(mids)}
    dups = sorted(x["e_support"] for x in R if x["dup_matched"]); nd = sorted(x["e_support"] for x in R if not x["dup_matched"])
    S_["duplication_bracket"] = {"lowest_e_support_duplicate": dups[0] if dups else None, "highest_e_support_non_duplicate": nd[-1] if nd else None}
    OUTJ["strata"][stt] = S_
    print(stt, "n", n, "accepted", acc, "dup", dup, "adult", adb, "amb", amb, "bracket", S_["duplication_bracket"], "logit", S_["logistic"] and round(S_["logistic"]["e50"], 3), S_["logistic"] and S_["logistic"]["e50_boot95"])
json.dump(OUTJ, open(OUT, "w"), indent=1, default=lambda o: o.tolist() if hasattr(o, "tolist") else (bool(o) if isinstance(o, np.bool_) else float(o)))
