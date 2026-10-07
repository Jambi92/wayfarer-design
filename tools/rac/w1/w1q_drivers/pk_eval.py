# RAC W1q (Pipkin W1 acceptance gate): PK (PK-NAT route) rows against the current comparators: accepted MF-M-R / SK / SG / elves /
# Gorrund / Grask; Durrim (DU-NAT) and Cogling (CG-NAT) as built (W1g) - UNACCEPTED dependencies. Existing directional and skin rows
# involving PK, plus canon-derived rows not run before (PIPKIN L42, L68, L149, L161-167, L183-189; SRR SR-COMP-01..03; order rows),
# a convergent-femora stance reading at the R-6 stance, and an optional human-child proxy comparison (report).
# Usage: python3 pk_eval.py PK_meas.json PK_r6.npz TAG [CHILD_meas.json]  -> reviews/rac-w1q-pk-evidence/central_<TAG>.json
import sys, os, json, shutil, numpy as np
sys.path.insert(0, '/home/claude/wayfarer-design/tools/rac/w1')
import directional_checks as DC, w1e_checks as WC
R = '/home/claude/wayfarer-design'; S = '/tmp/claude-0/-home-claude-wayfarer-design/19af7d50-3b61-5fda-9fe0-7a30770fb334/scratchpad'
EV = os.environ.get('EVDIR', R + '/reviews/rac-w1q-pk-evidence'); os.makedirs(EV, exist_ok=True); G = S + '/w1g'
PKM, PKR6, TAG = sys.argv[1], sys.argv[2], sys.argv[3]; CHM = sys.argv[4] if len(sys.argv) > 4 else None
def cls(op, va, vb, tol=0.010):
    if op in ('~', '≈'): return "PASS" if abs(va - vb) <= tol else "FAIL"
    rel = abs(va - vb) / abs(vb); holds = {">": va > vb, "<": va < vb, ">=": va >= vb, "<=": va <= vb}[op]
    if op in (">", "<"): return ("PASS" if rel >= 0.01 else "NOT DEMONSTRATED") if holds else "FAIL"
    return "PASS" if holds else ("MARGINAL" if rel < 0.01 else "FAIL")
tmp = S + '/w1q/cand_' + TAG
if os.path.exists(tmp): shutil.rmtree(tmp)
shutil.copytree(G + '/cand', tmp)
for slot, src in (("GO", R + '/reviews/rac-w1i-evidence/candidates/GO_meas.json'), ("GR", S + '/w1l/probe/GRL925_1200_meas.json'), ("AE", S + '/w1m/legs/AEL1_meas.json'),
                  ("VA", S + '/w1n/cand/VAL4_meas.json'), ("FN", S + '/w1p/cand/FNL4_meas.json'), ("PK", PKM), ("PK-NAT", PKM)):
    shutil.copy(src, tmp + '/%s_meas.json' % slot)
if os.environ.get('DUMEAS'):   # diagnostic: replace the Durrim comparator (e.g. a Narrow Durrim for the Broad-PK-vs-Narrow-DU check)
    for slot in ('DU', 'DU-NAT'): shutil.copy(os.environ['DUMEAS'], tmp + '/%s_meas.json' % slot)
inv = lambda r: 'PK' in (r.get('cand'), r.get('b'), r.get('a'))
out = {"pk_meas": PKM, "directional": [], "skin": [r for r in WC.run(tmp) if inv(r)], "added": []}
for r in DC.run(tmp):
    if inv(r): r['result_ADG10'] = cls(r['op'], r['va'], r['vb']) if r['op'] in ('>', '<') else ('PASS' if r['pass'] else 'FAIL'); out["directional"].append(r)
L = lambda p: json.load(open(p))["combined"]
M = {i: L(tmp + '/%s_meas.json' % i) for i in ("PK", "MF-M-R", "DU", "CG", "SG", "SK")}
if CHM: M["CHILD"] = L(CHM)
rt = lambda i, k: M[i]["ratio"][k]; mn = lambda i, k: M[i]["mean"][k]
F = {"torso / stature": lambda i: rt(i, "torso_share"), "leg / stature": lambda i: rt(i, "leg_share"), "arm / stature": lambda i: rt(i, "arm_share"),
     "thoracic depth / stature": lambda i: rt(i, "thorax_depth_share"), "thoracic breadth / stature": lambda i: rt(i, "thorax_breadth_share"),
     "pelvic vertical / thoracic vertical": lambda i: rt(i, "pelvic_vertical_over_thoracic_vertical"), "crest / thoracic breadth": lambda i: rt(i, "pelvis_over_thorax_breadth"),
     "waist interval / torso": lambda i: rt(i, "waist_interval_over_torso"), "AP pelvic depth / thoracic depth": lambda i: rt(i, "pelvic_depth_over_thorax_depth"),
     "elbow / humerus": lambda i: rt(i, "elbow_over_humerus"), "wrist / forearm": lambda i: rt(i, "wrist_over_forearm"), "knee / femur": lambda i: rt(i, "knee_over_femur"),
     "ankle / lower leg": lambda i: rt(i, "ankle_over_shin"), "hand / stature": lambda i: rt(i, "hand_share"), "palm breadth / hand": lambda i: rt(i, "palm_breadth_over_hand"),
     "foot / stature": lambda i: rt(i, "foot_share"), "palm breadth / stature": lambda i: mn(i, "palm_breadth") / M[i]["stature"],
     "palm depth / stature": lambda i: mn(i, "palm_depth") / M[i]["stature"], "head height / stature": lambda i: rt(i, "HH_share"), "finger / hand": lambda i: rt(i, "finger_over_hand")}
def add(chk, src, k, op, b, note="", report=False):
    va, vb = F[k]("PK"), F[k](b)
    out["added"].append({"cand": "PK", "check": chk + (" — REPORT ONLY" if report else ""), "canon": src, "reading": k, "va": va, "op": op, "b": b, "vb": vb,
                         "result": "REPORT" if report else cls(op, va, vb), "note": note, "dependency": b in ("DU", "CG", "CHILD")})
# Pipkin vs Durrim (unaccepted dependency): lighter, less thorax-led, smaller joints, greater limb contribution, moderate hands/feet
add("greater proportional leg contribution than Durrim", "PK L54-56, L177; order L132", "leg / stature", ">", "DU")
add("greater proportional arm contribution than Durrim", "PK L54-56; order L132", "arm / stature", ">", "DU")
add("torso vertical contribution never compressed to Durrim levels (torso share > DU? no: DU torso is larger) — report", "PK L42", "torso / stature", "<", "DU", report=True)
add("less thorax-led than Durrim: thoracic depth / stature", "PK L149, L167; SRR SR-COMP-03", "thoracic depth / stature", "<", "DU")
add("lighter than Durrim: thoracic breadth / stature", "PK L21, L149", "thoracic breadth / stature", "<", "DU")
add("pelvis-led vs thorax-led Durrim: pelvic vertical / thoracic vertical", "PK L167", "pelvic vertical / thoracic vertical", ">", "DU")
add("pelvis-led vs thorax-led Durrim: crest / thoracic breadth", "PK L167", "crest / thoracic breadth", ">", "DU")
for k, n in (("elbow / humerus", "elbow"), ("wrist / forearm", "wrist"), ("knee / femur", "knee"), ("ankle / lower leg", "ankle")):
    add("smaller %s than Durrim" % n, "PK L68, L183-189; RAC-05 L28", k, "<", "DU")
add("moderate hands: hand / stature below Durrim-substantial", "PK L183-185", "hand / stature", "<", "DU", report=True)
add("lighter palm than Durrim at matched stature: palm breadth / stature", "PK L183 ('at matched stature ... lighter wrist and palm dimensions')", "palm breadth / stature", "<", "DU")
add("lighter palm than Durrim at matched stature: palm depth / stature", "PK L183", "palm depth / stature", "<", "DU")
add("palm shape: palm breadth / hand length vs Durrim (shape, not 'at matched stature'; first-pass row, superseded)", "PK L183", "palm breadth / hand", "<", "DU", report=True)
# Pipkin vs normalized Marchfolk
add("thorax moderate, never paper-thin: thoracic depth / stature vs MF", "PK L149", "thoracic depth / stature", "~", "MF-M-R", report=True)
add("modestly elevated foot contribution vs MF", "PK L187-189", "foot / stature", ">=", "MF-M-R", report=True)
# Pipkin vs Cogling (unaccepted dependency; W1d pelvic packet L707; SRR SR-COMP-01/02)
add("modestly reduced trunk share vs near-MF Cogling", "SRR SR-COMP-01/02; W1d packet L707", "torso / stature", "<", "CG")
add("pelvis-led: crest / thoracic breadth > Cogling (CG ~ MF)", "W1d packet L707", "crest / thoracic breadth", ">", "CG")
add("compact waist: waist interval / torso < Cogling (CG ~ MF)", "W1d packet L707", "waist interval / torso", "<", "CG")
add("pelvic vertical / thoracic vertical > Cogling", "PK-P3 vs CG ~ MF", "pelvic vertical / thoracic vertical", ">", "CG")
if CHM:
    for k in ("head height / stature", "hand / stature", "foot / stature", "torso / stature", "leg / stature", "crest / thoracic breadth", "pelvic vertical / thoracic vertical", "waist interval / torso", "finger / hand"):
        add("adult vs human-child proxy (107 cm, generator age ~6 y): %s" % k, "PK L31-33, L89, L204; SR-COMP-11", k, "vs", "CHILD", report=True)
# convergent femora / adult narrow base at the R-6 stance (common pose): centroid separation of the left and right leg sections at knee and
# ankle joint height (mesh, leg-weighted vertices) relative to hip-joint separation. The rig joint table holds straight-leg bind positions,
# so the mesh is read instead.
def stance(p):
    from arm_measure import load
    d = load(p); V = d["V"].astype(float); J = d["joints"]; z = lambda n: float(np.asarray(J[n][0], float)[2]); x = lambda n: float(np.asarray(J[n][0], float)[0])
    def cx(side, zz, bones):
        w = sum(d["w_%s_%s" % (b, side)] for b in bones); m = (w > 0.5) & (np.abs(V[:, 2] - zz) < 1.5)
        return float(V[m, 0].mean())
    hip = abs(x("thigh_l") - x("thigh_r")); zk = (z("calf_l") + z("calf_r")) / 2; za = (z("foot_l") + z("foot_r")) / 2 + 3.0
    knee = abs(cx("l", zk, ("thigh", "calf")) - cx("r", zk, ("thigh", "calf"))); ank = abs(cx("l", za, ("calf",)) - cx("r", za, ("calf",)))
    return {"hip_sep": hip, "knee_sep": knee, "ankle_sep": ank, "knee_over_hip_sep": knee / hip, "ankle_over_hip_sep": ank / hip}
out["stance"] = {"PK": stance(PKR6), "MF-M-R": stance(S + '/w1f/final/MF-M-R_r6.npz'), "DU": stance(S + '/w1f/final/DU-NAT_r6.npz'), "CG": stance(S + '/w1f/final/CG-NAT_r6.npz')}
if CHM: out["stance"]["CHILD"] = stance(CHM.replace('_meas.json', '_r6.npz'))
for k in ("knee_over_hip_sep", "ankle_over_hip_sep"):
    va, vb = out["stance"]["PK"][k], out["stance"]["MF-M-R"][k]
    out["added"].append({"cand": "PK", "check": "convergent femora / adult narrow base: %s vs MF (R-6 stance, mesh) — REPORT ONLY" % k, "canon": "PK-P2b (PK L162); L735, L759", "reading": k,
                         "va": va, "op": "<=", "b": "MF-M-R", "vb": vb, "result": "REPORT",
                         "note": "REPORT ONLY: the R-6 measurement stance places each hip joint above its knee and ankle by definition (arm_lib.pose_r6), so femoral convergence cannot appear in joint readings; this mesh centroid reading is soft-tissue-influenced. PK-P2b convergence = NOT DEMONSTRATED (method)", "dependency": False})
keys = ["HH_share", "neck_share", "torso_share", "leg_share", "arm_share", "hand_share", "foot_share", "thorax_depth_share", "thorax_breadth_share", "pelvic_vertical_share",
        "pelvic_vertical_over_thoracic_vertical", "pelvis_over_thorax_breadth", "pelvic_depth_over_thorax_depth", "waist_interval_over_torso"]
out["distribution"] = {i: {**{k: M[i]["ratio"][k] for k in keys}, "stature": M[i]["stature"]} for i in M}
json.dump(out, open(EV + '/central_%s.json' % TAG, 'w'), indent=1, default=float)
bad = [(r['cand'], r.get('b'), r['check'][:60], r.get('result', r.get('result_ADG10'))) for k in ('skin', 'directional', 'added') for r in out[k] if r.get('result', r.get('result_ADG10')) not in ('PASS', 'REPORT')]
print(TAG, {k: len(out[k]) for k in ('skin', 'directional', 'added')}, 'stature %.2f' % M["PK"]["stature"], 'non-PASS:', bad)
