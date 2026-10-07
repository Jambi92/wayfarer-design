# RAC W1r (Cogling W1 acceptance gate): CG (CG-NAT route) rows against the current comparators: accepted MF-M-R / SK / SG / elves /
# Gorrund / Grask / Pipkin (PK-NAT); Durrim (DU-NAT) as built = UNACCEPTED dependency. Existing directional and skin rows involving CG,
# plus canon-derived rows not run before (COGLING L100-102, L116-121, L142, L163-167, L217-232, L558-575, L593, L619-632, L685-687;
# SRR L41-48; order item 5), and an optional human-child proxy comparison (report).
# Usage: python3 cg_eval.py CG_meas.json TAG [CHILD_meas.json]; env JBW/JBKEY joint-breadth file/key; env MFMEAS/PKMEAS swap the MF-M-R/PK slots
# (same-composition low check)  -> reviews/rac-w1r-cg-evidence/central_<TAG>.json
import sys, os, json, shutil
sys.path.insert(0, '/home/claude/wayfarer-design/tools/rac/w1')
import directional_checks as DC, w1e_checks as WC
R = '/home/claude/wayfarer-design'; S = '/tmp/claude-0/-home-claude-wayfarer-design/19af7d50-3b61-5fda-9fe0-7a30770fb334/scratchpad'
EV = os.environ.get('EVDIR', R + '/reviews/rac-w1r-cg-evidence'); os.makedirs(EV, exist_ok=True); G = S + '/w1g'
CGM, TAG = sys.argv[1], sys.argv[2]; CHM = sys.argv[3] if len(sys.argv) > 3 else None
def cls(op, va, vb, tol=0.010):
    if op in ('~', '≈'): return "PASS" if abs(va - vb) <= tol else "FAIL"
    rel = abs(va - vb) / abs(vb); holds = {">": va > vb, "<": va < vb, ">=": va >= vb, "<=": va <= vb}[op]
    if op in (">", "<"): return ("PASS" if rel >= 0.01 else "NOT DEMONSTRATED") if holds else "FAIL"
    return "PASS" if holds else ("MARGINAL" if rel < 0.01 else "FAIL")
tmp = S + '/w1r/cand_' + TAG
if os.path.exists(tmp): shutil.rmtree(tmp)
shutil.copytree(G + '/cand', tmp)
for slot, src in (("GO", R + '/reviews/rac-w1i-evidence/candidates/GO_meas.json'), ("GR", S + '/w1l/probe/GRL925_1200_meas.json'), ("AE", S + '/w1m/legs/AEL1_meas.json'),
                  ("VA", S + '/w1n/cand/VAL4_meas.json'), ("FN", S + '/w1p/cand/FNL4_meas.json'), ("CG", CGM), ("CG-NAT", CGM)) + tuple(
                  (sl, os.environ[e]) for sl, e in (("MF-M-R", "MFMEAS"), ("PK", "PKMEAS"), ("PK-NAT", "PKMEAS")) if os.environ.get(e)):
    shutil.copy(src, tmp + '/%s_meas.json' % slot)
inv = lambda r: 'CG' in (r.get('cand'), r.get('b'), r.get('a'))
out = {"cg_meas": CGM, "directional": [], "skin": [r for r in WC.run(tmp) if inv(r)], "added": []}
for r in DC.run(tmp):
    if inv(r): r['result_ADG10'] = cls(r['op'], r['va'], r['vb']) if r['op'] in ('>', '<') else ('PASS' if r['pass'] else 'FAIL'); out["directional"].append(r)
L = lambda p: json.load(open(p))["combined"]
M = {i: L(tmp + '/%s_meas.json' % i) for i in ("CG", "MF-M-R", "PK", "DU", "FN", "GR", "SG")}
if CHM: M["CHILD"] = L(CHM)
rt = lambda i, k: M[i]["ratio"][k]; mn = lambda i, k: M[i]["mean"][k]
F = {"torso / stature": lambda i: rt(i, "torso_share"), "leg / stature": lambda i: rt(i, "leg_share"), "arm / stature": lambda i: rt(i, "arm_share"),
     "thoracic breadth / stature": lambda i: rt(i, "thorax_breadth_share"), "thoracic depth / stature": lambda i: rt(i, "thorax_depth_share"),
     "upper arm / arm": lambda i: rt(i, "upperarm_over_arm"), "forearm / arm": lambda i: rt(i, "forearm_over_arm"), "hand / arm": lambda i: rt(i, "hand_over_arm"),
     "femur / leg": lambda i: rt(i, "femur_over_leg"), "lower leg / leg": lambda i: rt(i, "shin_over_leg"), "hand / stature": lambda i: rt(i, "hand_share"),
     "finger / hand": lambda i: rt(i, "finger_over_hand"), "finger / palm": lambda i: rt(i, "finger_over_palm"), "foot / stature": lambda i: rt(i, "foot_share"),
     "elbow / humerus": lambda i: rt(i, "elbow_over_humerus"), "wrist / forearm": lambda i: rt(i, "wrist_over_forearm"), "knee / femur": lambda i: rt(i, "knee_over_femur"),
     "ankle / lower leg": lambda i: rt(i, "ankle_over_shin"), "crest / thoracic breadth": lambda i: rt(i, "pelvis_over_thorax_breadth"),
     "pelvic vertical / thoracic vertical": lambda i: rt(i, "pelvic_vertical_over_thoracic_vertical"), "AP pelvic depth / thoracic depth": lambda i: rt(i, "pelvic_depth_over_thorax_depth"),
     "waist interval / torso": lambda i: rt(i, "waist_interval_over_torso"), "head height / stature": lambda i: rt(i, "HH_share"), "FVB": lambda i: M[i]["cranio"]["FVB"]}
def add(chk, src, k, op, b, note="", report=False):
    va, vb = F[k]("CG"), F[k](b)
    out["added"].append({"cand": "CG", "check": chk + (" — REPORT ONLY" if report else ""), "canon": src, "reading": k, "va": va, "op": op, "b": b, "vb": vb,
                         "result": "REPORT" if report else cls(op, va, vb), "note": note, "dependency": b in ("DU", "CHILD")})
# narrow stable core
add("torso contribution broadly near MF", "CG L100; RAC-04 L32", "torso / stature", "~", "MF-M-R")
add("narrow-to-moderate thorax: thoracic breadth / stature < MF", "CG L100-102, L649-661", "thoracic breadth / stature", "<", "MF-M-R")
add("thorax never flattened / Durrim-deep: thoracic depth / stature vs MF", "CG L102, L663-669; RA J-5", "thoracic depth / stature", "~", "MF-M-R", report=True)
# near-human total limb contribution
add("arm total broadly within MF envelope", "CG L558-560; RAC-04 L32", "arm / stature", "~", "MF-M-R")
add("leg total broadly within MF envelope ('not longer legs overall')", "CG L558-560, L619-624; RAC-04 L32", "leg / stature", "~", "MF-M-R")
# within-limb distal redistribution
add("reduced proximal upper-arm share vs MF", "CG L571-575", "upper arm / arm", "<", "MF-M-R")
add("increased forearm share vs MF", "CG L571-575", "forearm / arm", ">", "MF-M-R")
add("increased hand share of arm vs MF", "CG L571-575", "hand / arm", ">", "MF-M-R")
add("reduced femoral share vs MF", "CG L619-624", "femur / leg", "<", "MF-M-R")
add("increased lower-leg share vs MF", "CG L619-624", "lower leg / leg", ">", "MF-M-R")
# hands and feet
add("hands proportionally noticeable: hand / stature > MF", "CG L163-167", "hand / stature", ">", "MF-M-R")
add("fingers proportionally long relative to palm (finger / palm) > MF", "CG L142, L593", "finger / palm", ">", "MF-M-R")
add("feet moderate, not unusually small or large: foot / stature ~ MF", "CG L217-232, L630-632", "foot / stature", "~", "MF-M-R")
# fine skeletal shafts / structural-mass axis. COGLING L116-121 asks for lower structural mass than a HEIGHT-NORMALIZED MF, so the primary
# reading is joint breadth / stature. arm_measure takes each joint breadth inside a fixed +/-1 cm slab, which at 91 cm samples ~1.9x more of the
# body (relative) than at MF stature; the primary rows therefore use the slab scaled with stature (1 cm x stature / 173.14; MF unchanged), from
# joint_breadths.json (w1r_drivers/jbw.py). The as-measured fixed-slab readings and the per-segment ratios (elbow / humerus etc., which
# Cogling's within-limb redistribution inflates by design: shorter humerus, longer forearm) are reported, not scored.
JB = json.load(open(os.environ.get('JBW', EV + '/joint_breadths.json'))); JK = os.environ.get('JBKEY', 'CG-NAT')
jb = lambda i, mode, j: JB[{"CG": JK, "MF-M-R": "MF-M-R", "PK": "PK-NAT", "DU": "DU-NAT"}[i]][mode][j]
def addj(chk, src, j, op, b, mode, report=False, note=""):
    va, vb = jb("CG", mode, j), jb(b, mode, j)
    out["added"].append({"cand": "CG", "check": chk + (" — REPORT ONLY" if report else ""), "canon": src, "reading": "%s breadth / stature (%s slab)" % (j, mode), "va": va, "op": op,
                         "b": b, "vb": vb, "result": "REPORT" if report else cls(op, va, vb), "note": note, "dependency": b == "DU"})
for j in (("elbow", "wrist", "knee", "ankle") if JK != 'NONE' else ()):   # JBKEY=NONE: no joint-breadth measurement for this body
    addj("fine construction: %s breadth / stature < height-normalized MF" % j, "CG L116-121, L236", j, "<", "MF-M-R", "scaled")
    addj("structural-mass axis CG < PK (%s breadth / stature)" % j, "SRR L41-48; RAC-05 L32-34; order L32", j, "<", "PK", "scaled")
    addj("structural-mass axis CG < DU (%s breadth / stature)" % j, "SRR L41-48; RAC-05 L32", j, "<", "DU", "scaled")
    addj("%s breadth / stature vs MF, fixed 1 cm slab (as measured)" % j, "method comparison", j, "<", "MF-M-R", "abs", True)
    addj("%s breadth / stature vs PK, fixed 1 cm slab (as measured)" % j, "method comparison", j, "<", "PK", "abs", True)
for k, n in (("elbow / humerus", "elbow"), ("wrist / forearm", "wrist"), ("knee / femur", "knee"), ("ankle / lower leg", "ankle")):
    add("per-segment %s ratio vs MF (confounded by within-limb redistribution)" % n, "method comparison", k, "<", "MF-M-R", report=True)
# pelvis / trunk: mature, integrated, not Pipkin's pelvis-led mechanism
add("less pelvis-led than Pipkin: crest / thoracic breadth < PK", "CG L102, L258-262, L685-687; order L32", "crest / thoracic breadth", "<", "PK")
add("less pelvis-led than Pipkin: pelvic vertical / thoracic vertical < PK", "CG L258-262, L685-687; order L32", "pelvic vertical / thoracic vertical", "<", "PK")
add("less pelvis-led than Pipkin: AP pelvic depth / thoracic depth < PK", "CG L258-262; order L32", "AP pelvic depth / thoracic depth", "<", "PK")
add("pelvis / thorax breadth ~ MF (W1d packet L700 default; not authored canon)", "W1d pelvic packet L700, L707", "crest / thoracic breadth", "~", "MF-M-R", report=True)
add("no narrow-waist stereotype: waist interval / torso ~ MF", "CG L675-677; packet L707", "waist interval / torso", "~", "MF-M-R", report=True)
add("head share: allometry only, never deliberate enlargement (vs MF)", "CG L280, L727-734; RAC-04 L44", "head height / stature", "~", "MF-M-R", report=True)
# separation from Fenn / Grask (distal is within-limb, not global reach)
add("not a miniature Fenn: arm total < Fenn", "CG L935-951; order L35", "arm / stature", "<", "FN")
add("not a miniature Grask: arm total < Grask", "CG L953-969; order L35", "arm / stature", "<", "GR")
add("not a miniature Grask: leg total < Grask", "CG L953-969; order L35", "leg / stature", "<", "GR")
if CHM:
    for k in ("head height / stature", "FVB", "hand / stature", "finger / palm", "foot / stature", "torso / stature", "leg / stature", "arm / stature", "waist interval / torso", "crest / thoracic breadth", "forearm / arm", "lower leg / leg"):
        add("adult vs human-child proxy (91 cm, generator age ~3 y): %s" % k, "CG L84-92, L1005-1015; SR-COMP-11", k, "vs", "CHILD", report=True)
keys = ["HH_share", "neck_share", "torso_share", "leg_share", "arm_share", "upperarm_over_arm", "forearm_over_arm", "hand_over_arm", "femur_over_leg", "shin_over_leg",
        "hand_share", "finger_over_palm", "foot_share", "thorax_depth_share", "thorax_breadth_share", "pelvis_over_thorax_breadth", "pelvic_vertical_over_thoracic_vertical", "waist_interval_over_torso"]
out["distribution"] = {i: {**{k: M[i]["ratio"][k] for k in keys}, "stature": M[i]["stature"]} for i in M}
json.dump(out, open(EV + '/central_%s.json' % TAG, 'w'), indent=1, default=float)
bad = [(r['cand'], r.get('b'), r['check'][:64], r.get('result', r.get('result_ADG10'))) for k in ('skin', 'directional', 'added') for r in out[k] if r.get('result', r.get('result_ADG10')) not in ('PASS', 'REPORT')]
print(TAG, {k: len(out[k]) for k in ('skin', 'directional', 'added')}, 'stature %.2f' % M["CG"]["stature"], 'non-PASS:', bad)
