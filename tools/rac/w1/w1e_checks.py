"""RAC W1e: accepted pelvic / girdle / ALPC relational architecture (W1d author decisions) checked on the rebuilt candidates.
SKIN-SURFACE DIAGNOSTICS ONLY: PV-D16 / AD-G10 require skeletal (bony-landmark) validation, which these readings are not.
Result rule (AD-G10 1 % marginal threshold; PV-D10):
  strict > / <      PASS if it holds by >= 1 %; NOT DEMONSTRATED if it holds by < 1 %; FAIL otherwise.
  non-strict >= / <= PASS if it holds; MARGINAL (not a failure, PV-D10) if it misses by < 1 %; FAIL otherwise.
  '~'               the W1c absolute +/-0.010 method tolerance (on shares ~0.13-0.17 this is a +/-6-8 % band: wide; disclosed).
Items that need geometry not available on the skin route are listed with result NOT RUN.
Usage: python3 w1e_checks.py meas_dir out.json"""
import sys, os, json
APPROX = 0.010
def run(d):
    L = lambda i: json.load(open(os.path.join(d, i + "_meas.json")))["combined"]
    M = {i: L(i) for i in ("MF-M-R", "SK", "FN", "AE", "VA", "DU", "GR", "GO", "PK")}
    r = lambda i, k: M[i]["ratio"][k]
    C = []
    def add(c, chk, src, va, op, vb, b):
        rel = abs(va - vb) / max(abs(vb), 1e-9)
        holds = {">": va > vb, "<": va < vb, ">=": va >= vb, "<=": va <= vb, "~": abs(va - vb) <= APPROX}[op]
        if op in (">", "<"): res = ("PASS" if rel >= 0.01 else "NOT DEMONSTRATED") if holds else "FAIL"
        elif op in (">=", "<="): res = "PASS" if holds else ("MARGINAL" if rel < 0.01 else "FAIL")
        else: res = "PASS" if holds else "FAIL"
        C.append({"cand": c, "check": chk, "canon": src, "va": va, "op": op, "vb": vb, "b": b, "result": res,
                  "pass": res != "FAIL", "marginal": res in ("NOT DEMONSTRATED", "MARGINAL")})
    def notrun(c, chk, src, why):
        C.append({"cand": c, "check": chk, "canon": src, "va": None, "op": "n/a", "vb": None, "b": why, "result": "NOT RUN", "pass": None, "marginal": False})
    MF = "MF-M-R"
    # shared elven (E-A2): hip-joint height / stature > MF; bitrochanteric / crest not lower than MF
    for e in ("FN", "AE", "VA"):
        add(e, "hip-joint height / stature > MF (E-A2)", "spec pelvic architecture E-A2", r(e, "leg_share"), ">", r(MF, "leg_share"), "MF")
        add(e, "bitrochanteric / iliac-crest breadth >= MF (E-A2)", "E-A2", r(e, "bitroch_over_crest"), ">=", r(MF, "bitroch_over_crest"), "MF")
    for e in ("FN", "AE"):
        add(e, "AP pelvic depth / stature ~ MF (PV-D3 a)", "FN-P4 / AE-P4", r(e, "pelvic_depth_share"), "~", r(MF, "pelvic_depth_share"), "MF")
    add("FN", "iliac-crest breadth / stature ~ MF (PV-D4 a)", "FN-P5", r("FN", "crest_share"), "~", r(MF, "crest_share"), "MF")
    add("FN", "waist interval / torso >= MF (FN-P6)", "FN-P6", r("FN", "waist_interval_over_torso"), ">=", r(MF, "waist_interval_over_torso"), "MF")
    add("FN", "waist interval / torso < AE (FN-P6)", "FN-P6", r("FN", "waist_interval_over_torso"), "<", r("AE", "waist_interval_over_torso"), "AE")
    for o in (MF, "FN"):
        add("AE", "pelvic vertical / crest breadth > %s (PV-D5)" % o, "AE-P3", r("AE", "pelvic_vertical_over_crest"), ">", r(o, "pelvic_vertical_over_crest"), o)
    for o in ("FN", "VA"):
        add("AE", "waist interval / torso > %s (AE-P6)" % o, "AE-P6", r("AE", "waist_interval_over_torso"), ">", r(o, "waist_interval_over_torso"), o)
    add("AE", "waist interval / torso >= MF (AE-P6)", "AE-P6", r("AE", "waist_interval_over_torso"), ">=", r(MF, "waist_interval_over_torso"), "MF")
    for o in ("FN", "AE"):
        add("VA", "AP pelvic depth / stature > %s (PV-D6 a)" % o, "VA-P4", r("VA", "pelvic_depth_share"), ">", r(o, "pelvic_depth_share"), o)
        add("VA", "hip-joint height / stature < %s (VA-P2a)" % o, "VA-P2a", r("VA", "leg_share"), "<", r(o, "leg_share"), o)
    add("VA", "AP pelvic depth / stature >= MF (minimum, PV-D6 a)", "VA-P4", r("VA", "pelvic_depth_share"), ">=", r(MF, "pelvic_depth_share"), "MF")
    add("DU", "AP pelvic depth / stature > MF (PV-D8)", "DU-P4", r("DU", "pelvic_depth_share"), ">", r(MF, "pelvic_depth_share"), "MF")
    add("DU", "crest breadth / thoracic breadth <= MF (PV-D9, thorax-led)", "DU-P6", r("DU", "pelvis_over_thorax_breadth"), "<=", r(MF, "pelvis_over_thorax_breadth"), "MF")
    add("DU", "crest breadth / stature > MF (DU-P5)", "DU-P5", r("DU", "crest_share"), ">", r(MF, "crest_share"), "MF")
    add("DU", "hip-joint spacing / stature > MF (DU-P2b)", "DU-P2b", r("DU", "hip_joint_breadth_share"), ">", r(MF, "hip_joint_breadth_share"), "MF")
    add("DU", "pelvic vertical / crest breadth < MF (DU-P3)", "DU-P3", r("DU", "pelvic_vertical_over_crest"), "<", r(MF, "pelvic_vertical_over_crest"), "MF")
    for o in (MF, "SK"):
        add("GR", "hip-joint height / stature > %s (GR-P2a)" % o, "GR-P2a", r("GR", "leg_share"), ">", r(o, "leg_share"), o)
    add("GR", "bitrochanteric / crest >= MF (GR-P2b)", "GR-P2b", r("GR", "bitroch_over_crest"), ">=", r(MF, "bitroch_over_crest"), "MF")
    add("GR", "AP pelvic depth / stature <= MF (GR-P4)", "GR-P4", r("GR", "pelvic_depth_share"), "<=", r(MF, "pelvic_depth_share"), "MF")
    add("GR", "crest breadth / stature <= MF (GR-P5)", "GR-P5", r("GR", "crest_share"), "<=", r(MF, "crest_share"), "MF")
    add("GR", "pelvis / thorax breadth ~ MF (GR-P6)", "GR-P6", r("GR", "pelvis_over_thorax_breadth"), "~", r(MF, "pelvis_over_thorax_breadth"), "MF")
    add("GR", "shoulder-joint / thoracic breadth <= MF (GR-G1)", "GR-G1", r("GR", "S1_over_S2_b"), "<=", r(MF, "S1_over_S2_b"), "MF")
    for o in (MF, "SK"):
        add("GO", "AP pelvic depth / crest breadth > %s (PV-D14)" % o, "GO-P (PV-D14)", r("GO", "pelvic_depth_over_crest"), ">", r(o, "pelvic_depth_over_crest"), o)
    # GO-P2b / GO-P3 (PV-D14, as canonicalized in GORRUND)
    add("GO", "bitrochanteric / crest ~ MF (GO-P2b, hip joints under the load path)", "GO-P2b (PV-D14)", r("GO", "bitroch_over_crest"), "~", r(MF, "bitroch_over_crest"), "MF")
    add("GO", "leg share < GR (GO-P2b)", "GO-P2b (PV-D14)", r("GO", "leg_share"), "<", r("GR", "leg_share"), "GR")
    add("GO", "pelvic vertical / stature >= GR (GO-P3)", "GO-P3 (PV-D14)", r("GO", "pelvic_vertical_share"), ">=", r("GR", "pelvic_vertical_share"), "GR")
    notrun("GO", "hip-joint scale / crest breadth >= MF and >= SK (GO-P2a)", "GO-P2a (PV-D14)", "needs femoral-head / acetabular geometry (skeletal proxy, AD-G14)")
    # crest bounded by lower-trunk breadth (GO-P3) is the ALPC-2(b) S5/S4 check below
    # ALPC (GO) relative to the MF profile shape
    for k, lab in (("S3_over_S2_b", "ALPC-1 lower-thorax breadth"), ("S4_over_S2_b", "ALPC-1 lumbar breadth"), ("S3_over_S2_d", "ALPC-1 lower-thorax depth"), ("S4_over_S2_d", "ALPC-1 lumbar depth")):
        add("GO", "%s / thorax > MF" % lab, "GO ALPC-1", r("GO", k), ">", r(MF, k), "MF")
    for k, lab in (("S5_over_S2_b", "ALPC-2a crest breadth / thorax"), ("S6_over_S2_b", "ALPC-2a hip-level breadth / thorax"), ("pelvic_depth_over_thorax_depth", "ALPC-2a pelvic AP / thoracic depth")):
        add("GO", "%s >= MF" % lab, "GO ALPC-2(a)", r("GO", k), ">=", r(MF, k), "MF")
    for k, lab in (("S5_over_S4_b", "ALPC-2b crest / lumbar breadth"), ("S6_over_S4_b", "ALPC-2b hip-level / lumbar breadth")):
        add("GO", "%s <= MF" % lab, "GO ALPC-2(b)", r("GO", k), "<=", r(MF, k), "MF")
    add("GO", "ALPC-4 shoulder-joint / thoracic breadth <= MF", "GO ALPC-4 / GO-G1", r("GO", "S1_over_S2_b"), "<=", r(MF, "S1_over_S2_b"), "MF")
    for k in ("S3_over_S2_b", "S4_over_S2_b", "S3_over_S2_d", "S4_over_S2_d", "S5_over_S2_b", "S6_over_S2_b", "pelvic_depth_over_thorax_depth"):
        add("GO", "ALPC-7 %s > Skarn central (beyond 1 %%; equal-height Broad Skarn not built)" % k, "GO ALPC-7", r("GO", k), ">", r("SK", k), "SK")
    # ALPC-0 validity screen on the skin stations (GO and the MF comparator)
    for i in ("GO", MF):
        st = M[i]["alpc_stations"]; b = [st["S%d" % k][0] for k in range(2, 7)]
        ok0 = b[0] >= b[1] >= b[2] and b[2] <= b[3] <= b[4] and b[2] < b[0]
        add(i, "ALPC-0 valid shape: breadth non-increasing S2->S4, non-decreasing S4->S6, S4 < S2 (1 = holds)", "GO ALPC-0", 1.0 if ok0 else 0.0, ">=", 1.0, "-")
    wi = lambda i: M[i]["waist_interval"] / M[i]["stature"]
    C.append({"cand": "GO", "check": "ALPC-1c costal-iliac gap / stature (REPORT ONLY, AD-G9)", "canon": "GO ALPC-1c", "va": wi("GO"), "op": "vs", "vb": wi(MF), "b": "MF", "result": "REPORT", "pass": None, "marginal": False})
    notrun("GO", "ALPC-3 pelvis -> proximal femur (femoral head/neck, subtrochanteric shaft)", "GO ALPC-3", "needs skeletal femur geometry (soft tissue excluded)")
    notrun("GO", "ALPC-5 frame invariance (GOR-BODY-04, -12, -14)", "GO ALPC-5", "frame bodies not built")
    notrun("GO", "ALPC-6 composition invariance (skeletal proxy + GOR-BODY-16)", "GO ALPC-6", "skeletal proxy / low-composition body not built")
    notrun("GO", "ALPC-8 separation from Durrim (matched-display silhouette)", "GO ALPC-8", "silhouette test not run")
    # RM-LR-02 (d): skeletal shoulder breadth / stature SK > GR, GO > GR (generator shoulder joint used: AD-G10 asks for anatomical landmarks)
    add("SK", "shoulder-joint breadth / stature > GR (RM-LR-02 d; GR L42)", "RM-LR-02 (d)", r("SK", "shoulder_joint_share"), ">", r("GR", "shoulder_joint_share"), "GR")
    add("GO", "shoulder-joint breadth / stature > GR (AD-G6)", "AD-G6", r("GO", "shoulder_joint_share"), ">", r("GR", "shoulder_joint_share"), "GR")
    tv = lambda i: M[i]["thoracic_vertical"] / M[i]["alpc_stations"]["S2"][0]
    add("GO", "ALPC-1b ribcage vertical / breadth >= MF", "GO ALPC-1b", tv("GO"), ">=", tv(MF), "MF")
    for o in ("SK", "GR"):
        add("GO", "thoracic depth / breadth > %s (AD-G7)" % o, "AD-G7", r("GO", "thorax_d_over_b"), ">", r(o, "thorax_d_over_b"), o)
    add("PK", "pelvic vertical / stature >= MF (PV-D10)", "PK-P3", r("PK", "pelvic_vertical_share"), ">=", r(MF, "pelvic_vertical_share"), "MF")
    add("PK", "pelvic vertical / thoracic vertical > MF (PK-P3)", "PK-P3", r("PK", "pelvic_vertical_over_thoracic_vertical"), ">", r(MF, "pelvic_vertical_over_thoracic_vertical"), "MF")
    add("PK", "AP pelvic depth / thoracic depth > MF (PK-P4)", "PK-P4", r("PK", "pelvic_depth_over_thorax_depth"), ">", r(MF, "pelvic_depth_over_thorax_depth"), "MF")
    add("PK", "crest / thoracic breadth > MF (PK-P5)", "PK-P5", r("PK", "pelvis_over_thorax_breadth"), ">", r(MF, "pelvis_over_thorax_breadth"), "MF")
    add("PK", "waist interval / torso < MF (PK-P6)", "PK-P6", r("PK", "waist_interval_over_torso"), "<", r(MF, "waist_interval_over_torso"), "MF")
    add("PK", "hip-joint height / stature > DU (PK-P2a)", "PK-P2a", r("PK", "leg_share"), ">", r("DU", "leg_share"), "DU")
    add("PK", "hip-joint height / stature <= MF (PK-P2a)", "PK-P2a", r("PK", "leg_share"), "<=", r(MF, "leg_share"), "MF")
    return C
if __name__ == "__main__":
    C = run(sys.argv[1]); json.dump(C, open(sys.argv[2], "w"), indent=1, default=float)
    from collections import Counter
    print(len(C), "rows;", dict(Counter(c["result"] for c in C)))
    for c in C:
        if c["result"] != "PASS": print(c["result"], c["cand"], c["check"], c["va"] if c["va"] is None else round(c["va"], 4), c["op"], c["vb"] if c["vb"] is None else round(c["vb"], 4))
