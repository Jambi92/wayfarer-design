# RAC W1n (Vael W1 acceptance gate): Vael directional and skin rows against the CURRENT comparators (accepted Aelari AEL1, Gorrund,
# Grask; Fenn as built W1g, unaccepted dependency), plus canon-derived rows not run before (VAEL L37, L44-46, L145, L151-154;
# RAC-03 E-4), using the conventions accepted for Aelari (balance rows ~ MF +/-0.010; strict directions under AD-G10, BM-3 for MF < VA < AE).
# Usage: python3 va_eval.py VA_meas.json TAG  -> reviews/rac-w1n-va-evidence/central_<TAG>.json
import sys, os, json, shutil
sys.path.insert(0, '/home/claude/wayfarer-design/tools/rac/w1')
import directional_checks as DC, w1e_checks as WC
R = '/home/claude/wayfarer-design'; S = '/tmp/claude-0/-home-claude-wayfarer-design/19af7d50-3b61-5fda-9fe0-7a30770fb334/scratchpad'
EV = R + '/reviews/rac-w1n-va-evidence'; G = S + '/w1g'; VAM, TAG = sys.argv[1], sys.argv[2]
def cls(op, va, vb, tol=0.010):
    if op in ('~', '≈'): return "PASS" if abs(va - vb) <= tol else "FAIL"
    rel = abs(va - vb) / abs(vb); holds = {">": va > vb, "<": va < vb, ">=": va >= vb, "<=": va <= vb}[op]
    if op in (">", "<"): return ("PASS" if rel >= 0.01 else "NOT DEMONSTRATED") if holds else "FAIL"
    return "PASS" if holds else ("MARGINAL" if rel < 0.01 else "FAIL")
tmp = S + '/w1n/cand_' + TAG
if os.path.exists(tmp): shutil.rmtree(tmp)
shutil.copytree(G + '/cand', tmp)
shutil.copy(R + '/reviews/rac-w1i-evidence/candidates/GO_meas.json', tmp + '/GO_meas.json')
shutil.copy(S + '/w1l/probe/GRL925_1200_meas.json', tmp + '/GR_meas.json')
shutil.copy(S + '/w1m/legs/AEL1_meas.json', tmp + '/AE_meas.json')
shutil.copy(VAM, tmp + '/VA_meas.json')
inv = lambda r: 'VA' in (r.get('cand'), r.get('b'), r.get('a'))
out = {"va_meas": VAM, "directional": [], "skin": [r for r in WC.run(tmp) if inv(r)], "added": []}
for r in DC.run(tmp):
    if inv(r): r['result_ADG10'] = cls(r['op'], r['va'], r['vb']) if r['op'] in ('>', '<') else ('PASS' if r['pass'] else 'FAIL'); out["directional"].append(r)
L = lambda i: json.load(open(tmp + '/%s_meas.json' % i))["combined"]
M = {i: L(i) for i in ("VA", "MF-M-R", "AE", "FN", "SG", "SK")}
rt = lambda i, k: M[i]["ratio"][k]; mn = lambda i, k: M[i]["mean"][k]
F = {"lower leg / thigh": lambda i: rt(i, "shin_share") / rt(i, "thigh_share"), "forearm / upper arm": lambda i: rt(i, "forearm_over_upperarm"),
     "arm / stature": lambda i: rt(i, "arm_share"), "leg / stature": lambda i: rt(i, "leg_share"), "neck / torso": lambda i: rt(i, "neck_share") / rt(i, "torso_share"),
     "elbow / humerus": lambda i: rt(i, "elbow_over_humerus"), "wrist / forearm": lambda i: rt(i, "wrist_over_forearm"), "knee / femur": lambda i: rt(i, "knee_over_femur"),
     "ankle / lower leg": lambda i: rt(i, "ankle_over_shin"), "foot breadth / foot length": lambda i: mn(i, "foot_breadth") / mn(i, "foot_len"),
     "shoulder-joint breadth / stature (presence proxy)": lambda i: rt(i, "shoulder_joint_share"), "hip-joint breadth / stature (VA-P2c proxy)": lambda i: rt(i, "hip_joint_breadth_share")}
def rep(chk, src, k, op, b, note=""):   # spacing readings, not joint size: reported only
    va, vb = F[k]("VA"), F[k](b); out["added"].append({"cand": "VA", "check": chk + " — REPORT ONLY (joint spacing, not joint size)", "canon": src, "reading": k, "va": va, "op": op, "b": b, "vb": vb, "result": "REPORT", "note": note})
def add(chk, src, k, op, b, note=""):
    va, vb = F[k]("VA"), F[k](b); out["added"].append({"cand": "VA", "check": chk, "canon": src, "reading": k, "va": va, "op": op, "b": b, "vb": vb, "result": cls(op, va, vb), "note": note})
add("balanced femur and lower leg: lower leg / thigh ~ MF (+/-0.010)", "VAEL L46; Aelari convention", "lower leg / thigh", "~", "MF-M-R")
add("balanced upper arm and forearm: forearm / upper arm ~ MF (+/-0.010)", "VAEL L44; Aelari / directional arm-row convention", "forearm / upper arm", "~", "MF-M-R")
add("arms long relative to humans", "VAEL L44", "arm / stature", ">", "MF-M-R")
add("arms less elongated than Aelari", "VAEL L44, L151", "arm / stature", "<", "AE", "BM-3: NOT DEMONSTRATED within 1 % accepted for MF < VA < AE")
add("arms less elongated than Fenn", "VAEL L44, L151", "arm / stature", "<", "FN")
add("Aelari leg budget: VA leg x 1.01 <= AE leg (accepted AE)", "W1h §6 / AE accepted", "leg / stature", "<", "AE")
add("Fenn >= Vael neck relative to torso", "RAC-03 E-4", "neck / torso", "<=", "FN")
for k, n in (("elbow / humerus", "elbow"), ("wrist / forearm", "wrist"), ("knee / femur", "knee"), ("ankle / lower leg", "ankle")):
    add("gracile %s vs humans" % n, "VAEL L37, L145", k, "<", "MF-M-R")
add("more ankle presence than Aelari", "VAEL L37, L46, L145", "ankle / lower leg", ">", "AE"); add("more ankle presence than Fenn", "VAEL L37, L46, L145", "ankle / lower leg", ">", "FN")
add("feet broader than Aelari", "VAEL L47, L154", "foot breadth / foot length", ">", "AE"); add("feet broader than Fenn", "VAEL L47, L154", "foot breadth / foot length", ">", "FN")
rep("more shoulder-joint presence than Aelari (breadth proxy)", "VAEL L37, L122", "shoulder-joint breadth / stature (presence proxy)", ">", "AE")
rep("more shoulder-joint presence than Fenn (breadth proxy)", "VAEL L37, L122", "shoulder-joint breadth / stature (presence proxy)", ">", "FN")
rep("hip-joint scale > Aelari (VA-P2c, skin proxy)", "VAEL L132", "hip-joint breadth / stature (VA-P2c proxy)", ">", "AE")
rep("hip-joint scale > Fenn (VA-P2c, skin proxy)", "VAEL L132", "hip-joint breadth / stature (VA-P2c proxy)", ">", "FN")
rep("hip-joint scale gracile vs MF (VA-P2c, skin proxy)", "VAEL L132", "hip-joint breadth / stature (VA-P2c proxy)", "<", "MF-M-R")
def rep(chk, src, k, op, b, note=""):   # spacing readings, not joint size: reported only (not a valid test of "joint presence" / "hip-joint scale")
    va, vb = F[k]("VA"), F[k](b); out["added"].append({"cand": "VA", "check": chk + " — REPORT ONLY (joint spacing, not joint size)", "canon": src, "reading": k, "va": va, "op": op, "b": b, "vb": vb, "result": "REPORT", "note": note})
keys = ["HH_share", "neck_share", "torso_share", "leg_share", "thigh_share", "shin_share", "arm_share", "hand_share", "foot_share", "waist_interval_over_torso", "thorax_depth_share", "thorax_breadth_share"]
out["distribution"] = {i: {**{k: M[i]["ratio"][k] for k in keys}, "stature": M[i]["stature"]} for i in M}
json.dump(out, open(EV + '/central_%s.json' % TAG, 'w'), indent=1, default=float)
bad = [(r['cand'], r['check'][:60], r.get('result', r.get('result_ADG10'))) for k in ('skin', 'directional', 'added') for r in out[k] if r.get('result', r.get('result_ADG10')) not in ('PASS', 'REPORT')]
print(TAG, {k: len(out[k]) for k in ('skin', 'directional', 'added')}, 'stature %.2f' % M["VA"]["stature"], 'non-PASS:', bad)
