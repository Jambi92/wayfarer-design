# RAC W1p (Fenn W1 acceptance gate): Fenn rows against the CURRENT accepted comparators (Aelari AEL1, Vael VAL4, Gorrund, Grask,
# MF / SK / SG), the previously dependent elf-family rows, and canon-derived rows not run before (FENN L50-52, L109-110, L115, L128,
# L134-137; ECR L312-316 gracility order; RAC-03 E-4 neck), with the conventions accepted for Aelari / Vael.
# Usage: python3 fn_eval.py FN_meas.json TAG  -> reviews/rac-w1p-fn-evidence/central_<TAG>.json
import sys, os, json, shutil
sys.path.insert(0, '/home/claude/wayfarer-design/tools/rac/w1')
import directional_checks as DC, w1e_checks as WC
R = '/home/claude/wayfarer-design'; S = '/tmp/claude-0/-home-claude-wayfarer-design/19af7d50-3b61-5fda-9fe0-7a30770fb334/scratchpad'
EV = os.environ.get('EVDIR', R + '/reviews/rac-w1p-fn-evidence'); os.makedirs(EV, exist_ok=True); G = S + '/w1g'; FNM, TAG = sys.argv[1], sys.argv[2]
def cls(op, va, vb, tol=0.010):
    if op in ('~', '≈'): return "PASS" if abs(va - vb) <= tol else "FAIL"
    rel = abs(va - vb) / abs(vb); holds = {">": va > vb, "<": va < vb, ">=": va >= vb, "<=": va <= vb}[op]
    if op in (">", "<"): return ("PASS" if rel >= 0.01 else "NOT DEMONSTRATED") if holds else "FAIL"
    return "PASS" if holds else ("MARGINAL" if rel < 0.01 else "FAIL")
tmp = S + '/w1p/cand_' + TAG
if os.path.exists(tmp): shutil.rmtree(tmp)
shutil.copytree(G + '/cand', tmp)
for slot, src in (("GO", R + '/reviews/rac-w1i-evidence/candidates/GO_meas.json'), ("GR", S + '/w1l/probe/GRL925_1200_meas.json'),
                  ("AE", S + '/w1m/legs/AEL1_meas.json'), ("VA", S + '/w1n/cand/VAL4_meas.json'), ("FN", FNM)):
    shutil.copy(src, tmp + '/%s_meas.json' % slot)
inv = lambda r: 'FN' in (r.get('cand'), r.get('b'), r.get('a'))
out = {"fn_meas": FNM, "directional": [], "skin": [r for r in WC.run(tmp) if inv(r)], "added": []}
for r in DC.run(tmp):
    if inv(r): r['result_ADG10'] = cls(r['op'], r['va'], r['vb']) if r['op'] in ('>', '<') else ('PASS' if r['pass'] else 'FAIL'); out["directional"].append(r)
L = lambda i: json.load(open(tmp + '/%s_meas.json' % i))["combined"]
M = {i: L(i) for i in ("FN", "MF-M-R", "AE", "VA", "SG", "SK")}
rt = lambda i, k: M[i]["ratio"][k]; mn = lambda i, k: M[i]["mean"][k]
F = {"torso / stature": lambda i: rt(i, "torso_share"), "leg / stature": lambda i: rt(i, "leg_share"), "arm / stature": lambda i: rt(i, "arm_share"),
     "forearm / arm": lambda i: rt(i, "forearm_over_arm"), "lower leg / leg": lambda i: rt(i, "shin_over_leg"), "neck / stature": lambda i: rt(i, "neck_share"),
     "neck / torso": lambda i: rt(i, "neck_share") / rt(i, "torso_share"), "hand / stature": lambda i: rt(i, "hand_share"), "finger / hand": lambda i: rt(i, "finger_over_hand"),
     "palm breadth / hand": lambda i: rt(i, "palm_breadth_over_hand"), "foot / stature": lambda i: rt(i, "foot_share"), "foot breadth / foot length": lambda i: mn(i, "foot_breadth") / mn(i, "foot_len"),
     "thoracic depth / stature": lambda i: rt(i, "thorax_depth_share"), "thoracic breadth / stature": lambda i: rt(i, "thorax_breadth_share"),
     "elbow / humerus": lambda i: rt(i, "elbow_over_humerus"), "wrist / forearm": lambda i: rt(i, "wrist_over_forearm"), "knee / femur": lambda i: rt(i, "knee_over_femur"),
     "ankle / lower leg": lambda i: rt(i, "ankle_over_shin"), "shoulder-joint breadth / stature": lambda i: rt(i, "shoulder_joint_share")}
def add(chk, src, k, op, b, note="", report=False):
    va, vb = F[k]("FN"), F[k](b)
    out["added"].append({"cand": "FN", "check": chk + (" — REPORT ONLY" if report else ""), "canon": src, "reading": k, "va": va, "op": op, "b": b, "vb": vb, "result": "REPORT" if report else cls(op, va, vb), "note": note})
add("slightly smaller torso share than humans", "FENN L50", "torso / stature", "<", "MF-M-R")
add("greater leg share than humans", "FENN L52, L136", "leg / stature", ">", "MF-M-R")
add("more limb-focused than Aelari: leg share", "order L26; ECR L33", "leg / stature", ">", "AE")
add("longer arms than humans", "FENN L51, L134", "arm / stature", ">", "MF-M-R")
add("more limb-focused than Aelari: arm share", "order L26; ECR L33", "arm / stature", ">", "AE")
add("slightly longer lower legs: lower leg / leg > MF", "FENN L52, L136", "lower leg / leg", ">", "MF-M-R")
add("Fenn >= Vael neck (relative to torso)", "RAC-03 E-4; ECR L320", "neck / torso", ">=", "VA")
add("Fenn >= Vael neck (share of stature)", "RAC-03 E-4; ECR L320", "neck / stature", ">=", "VA", "second reading of 'relative contribution'", report=True)
add("longer hands than humans (hand / stature)", "FENN L51, L135", "hand / stature", ">", "MF-M-R")
add("longer fingers (finger / hand) than humans", "FENN L51, L135", "finger / hand", ">", "MF-M-R")
add("somewhat narrower hands (palm breadth / hand) than humans", "FENN L135", "palm breadth / hand", "<", "MF-M-R")
add("somewhat longer feet than humans", "FENN L52, L137", "foot / stature", ">", "MF-M-R")
add("somewhat narrower feet than humans", "FENN L137", "foot breadth / foot length", "<", "MF-M-R")
add("somewhat shallower ribcage than humans", "FENN L50, L110", "thoracic depth / stature", "<", "MF-M-R")
add("moderately narrow ribcage for height vs humans", "FENN L110", "thoracic breadth / stature", "<", "MF-M-R")
for k, n in (("elbow / humerus", "elbow"), ("wrist / forearm", "wrist"), ("knee / femur", "knee"), ("ankle / lower leg", "ankle")):
    add("%s smaller relative to limb than humans" % n, "FENN L128", k, "<", "MF-M-R")
    add("gracility order Fenn > Aelari: %s" % n, "E-A1 (FENN L115); ECR L312-316 (average ordering)", k, "<", "AE")
add("less massive shoulder joints than Vael (spacing proxy)", "FENN L109; VAEL L122", "shoulder-joint breadth / stature", "<", "VA", report=True)
keys = ["HH_share", "neck_share", "torso_share", "leg_share", "thigh_share", "shin_share", "arm_share", "hand_share", "foot_share", "waist_interval_over_torso", "thorax_depth_share", "thorax_breadth_share"]
out["distribution"] = {i: {**{k: M[i]["ratio"][k] for k in keys}, "stature": M[i]["stature"]} for i in M}
json.dump(out, open(EV + '/central_%s.json' % TAG, 'w'), indent=1, default=float)
bad = [(r['cand'], r['b'] if r['cand'] == 'FN' else '', r['check'][:58], r.get('result', r.get('result_ADG10'))) for k in ('skin', 'directional', 'added') for r in out[k] if r.get('result', r.get('result_ADG10')) not in ('PASS', 'REPORT')]
print(TAG, {k: len(out[k]) for k in ('skin', 'directional', 'added')}, 'stature %.2f' % M["FN"]["stature"], 'non-PASS:', bad)
