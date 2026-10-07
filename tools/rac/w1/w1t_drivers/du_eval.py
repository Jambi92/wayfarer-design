# RAC W1t (Durrim W1 acceptance gate): DU rows against the accepted comparators (MF-M-R, SK, SG, Aelari AEL1, Vael VAL4, Fenn FNL4,
# Gorrund, Grask W1l, Pipkin PK-NAT, Cogling CGJ7, Halvren HVC1). Existing directional and skin (pelvic) rows involving DU, plus canon-derived
# rows not run before (DURRIM L11, L19-21, L25-46, L93-133; DU-P2a..P6 skin diagnostics; order items 2-5). Joint rows per stature use the
# stature-scaled slab (Cogling ruling); per-segment joint rows are kept where they are the authored relation ("relative to limb length").
# Usage: python3 du_eval.py DU_meas.json TAG [JBW_json JBKEY]  -> reviews/rac-w1t-du-evidence/central_<TAG>.json
import sys, os, json, shutil
sys.path.insert(0, '/home/claude/wayfarer-design/tools/rac/w1')
import directional_checks as DC, w1e_checks as WC
R = '/home/claude/wayfarer-design'; S = '/tmp/claude-0/-home-claude-wayfarer-design/19af7d50-3b61-5fda-9fe0-7a30770fb334/scratchpad'
EV = os.environ.get('EVDIR', R + '/reviews/rac-w1t-du-evidence'); os.makedirs(EV, exist_ok=True)
DUM, TAG = sys.argv[1], sys.argv[2]
JBF = sys.argv[3] if len(sys.argv) > 3 else EV + '/joint_breadths.json'; JK = sys.argv[4] if len(sys.argv) > 4 else 'DU-NAT'
def cls(op, va, vb, tol=0.010):
    if op in ('~', '≈'): return "PASS" if abs(va - vb) <= tol else "FAIL"
    rel = abs(va - vb) / abs(vb); holds = {">": va > vb, "<": va < vb, ">=": va >= vb, "<=": va <= vb}[op]
    if op in (">", "<"): return ("PASS" if rel >= 0.01 else "NOT DEMONSTRATED") if holds else "FAIL"
    return "PASS" if holds else ("MARGINAL" if rel < 0.01 else "FAIL")
SLOTS = (("GO", R + '/reviews/rac-w1i-evidence/candidates/GO_meas.json'), ("GR", S + '/w1l/probe/GRL925_1200_meas.json'), ("AE", S + '/w1m/legs/AEL1_meas.json'),
         ("VA", S + '/w1n/cand/VAL4_meas.json'), ("FN", S + '/w1p/cand/FNL4_meas.json'), ("PK", S + '/w1g/cand/PK-NAT_meas.json'), ("PK-NAT", S + '/w1g/cand/PK-NAT_meas.json'),
         ("CG", S + '/w1r/probe/CGJ7_meas.json'), ("CG-NAT", S + '/w1r/probe/CGJ7_meas.json'), ("HV", S + '/w1s/probe/HVC1_meas.json'), ("DU", DUM), ("DU-NAT", DUM))
tmp = S + '/w1t/cand_' + TAG
if os.path.exists(tmp): shutil.rmtree(tmp)
shutil.copytree(S + '/w1g/cand', tmp)
for slot, src in SLOTS + tuple((sl, os.environ[e]) for sl, e in (("MF-M-R", "MFMEAS"), ("PK", "PKMEAS"), ("PK-NAT", "PKMEAS"), ("SK", "SKMEAS"), ("CG", "CGMEAS"), ("CG-NAT", "CGMEAS")) if os.environ.get(e)):
    shutil.copy(src, tmp + '/%s_meas.json' % slot)
inv = lambda r: 'DU' in (r.get('cand'), r.get('b'), r.get('a'))
out = {"du_meas": DUM, "directional": [], "skin": [r for r in WC.run(tmp) if inv(r)], "added": []}
for r in DC.run(tmp):
    if inv(r): r['result_ADG10'] = cls(r['op'], r['va'], r['vb']) if r['op'] in ('>', '<') else ('PASS' if r['pass'] else 'FAIL'); out["directional"].append(r)
L = lambda p: json.load(open(p))["combined"]
M = {i: L(tmp + '/%s_meas.json' % i) for i in ("DU", "MF-M-R", "PK", "CG", "SK", "SG", "GR", "GO")}
rt = lambda i, k: M[i]["ratio"][k]; mn = lambda i, k: M[i]["mean"][k]; st = lambda i: M[i]["stature"]
F = {"torso / stature": lambda i: rt(i, "torso_share"), "leg / stature": lambda i: rt(i, "leg_share"), "arm / stature": lambda i: rt(i, "arm_share"),
     "neck / stature": lambda i: rt(i, "neck_share"), "head height / stature": lambda i: rt(i, "HH_share"),
     "thoracic breadth / stature": lambda i: rt(i, "thorax_breadth_share"), "thoracic depth / stature": lambda i: rt(i, "thorax_depth_share"),
     "shoulder breadth / stature": lambda i: rt(i, "shoulder_breadth_share"), "shoulder-joint breadth / stature": lambda i: rt(i, "shoulder_joint_share"),
     "upper arm / arm": lambda i: rt(i, "upperarm_over_arm"), "forearm / arm": lambda i: rt(i, "forearm_over_arm"), "femur / leg": lambda i: rt(i, "femur_over_leg"),
     "lower leg / leg": lambda i: rt(i, "shin_over_leg"), "hand / stature": lambda i: rt(i, "hand_share"), "foot / stature": lambda i: rt(i, "foot_share"),
     "palm breadth / stature": lambda i: mn(i, "palm_breadth") / st(i), "palm depth / stature": lambda i: mn(i, "palm_depth") / st(i),
     "palm / hand length": lambda i: mn(i, "palm") / mn(i, "hand"), "palm breadth / hand": lambda i: rt(i, "palm_breadth_over_hand"), "foot breadth / stature": lambda i: mn(i, "foot_breadth") / st(i),
     "ankle / lower leg": lambda i: rt(i, "ankle_over_shin"), "waist interval / torso": lambda i: rt(i, "waist_interval_over_torso"),
     "hip-joint height / stature": lambda i: mn(i, "hip_height") / st(i), "thoracic depth / breadth": lambda i: rt(i, "thorax_d_over_b"),
     "pelvic depth / thoracic depth": lambda i: rt(i, "pelvic_depth_over_thorax_depth"), "crest / thoracic breadth": lambda i: rt(i, "pelvis_over_thorax_breadth"), "FVB": lambda i: M[i]["cranio"]["FVB"]}
def add(chk, src, k, op, b, note="", report=False):
    va, vb = F[k]("DU"), F[k](b)
    out["added"].append({"cand": "DU", "check": chk + (" — REPORT ONLY" if report else ""), "canon": src, "reading": k, "va": va, "op": op, "b": b, "vb": vb,
                         "result": "REPORT" if report else cls(op, va, vb), "note": note})
# stature, torso, limbs, neck, head
add("hip-joint height / stature < MF (DU-P2a: shorter femur and lower leg)", "DU L113, L130", "hip-joint height / stature", "<", "MF-M-R")
add("femur / leg vs MF (both segments shorten; neither alone)", "DU L38, L130", "femur / leg", "~", "MF-M-R", report=True)
add("arm segments: upper arm / arm vs MF (not uniformly shortened; report)", "DU L38, L124", "upper arm / arm", "~", "MF-M-R", report=True)
add("compact torso, not a near-square block: thoracic depth / breadth vs MF", "DU L97", "thoracic depth / breadth", "~", "MF-M-R", report=True)
add("head integrated, never an oversized fantasy-dwarf head: head share vs PK (accepted)", "DU L21; order item 14", "head height / stature", "<", "PK")
add("head integrated: head share vs MF (allometry; somewhat greater allowed)", "DU L21", "head height / stature", ">", "MF-M-R", report=True)
# thorax and shoulders
add("shoulder breadth / stature > MF (skeletal clavicle / joint presence)", "DU L31, L105-106", "shoulder-joint breadth / stature", ">", "MF-M-R")
add("thoracic breadth / stature > SK (accepted human with greatest structural presence) — report", "DU L29-30", "thoracic breadth / stature", ">", "SK", report=True)
add("thoracic depth / stature > SK — report", "DU L29", "thoracic depth / stature", ">", "SK", report=True)
# hands and feet
add("palm breadth / stature > MF (substantial palm)", "DU L44, L126", "palm breadth / stature", ">", "MF-M-R")
add("palm depth / stature > MF (substantial palm)", "DU L44, L126", "palm depth / stature", ">", "MF-M-R")
add("palm share of hand length >= MF (provisional tendency)", "DU L126", "palm / hand length", ">=", "MF-M-R", note="provisional population tendency")
add("foot breadth / stature > MF (broad skeletal base)", "DU L46, L132", "foot breadth / stature", ">", "MF-M-R")
add("foot length / stature: moderate relative length (vs MF)", "DU L46, L132", "foot / stature", ">=", "MF-M-R")
add("ankle presence: ankle / lower leg > MF", "DU L130", "ankle / lower leg", ">", "MF-M-R")
# pelvis / trunk (skin diagnostics; skeletal rows in skeletal_<TAG>.json)
add("pelvis continuous with deep thorax: pelvic depth / thoracic depth vs MF", "DU-P4 (no abrupt shallow step)", "pelvic depth / thoracic depth", ">=", "MF-M-R", report=True)
add("compact waist interval present: waist interval / torso vs MF", "DU-P6, L104", "waist interval / torso", "~", "MF-M-R", report=True)
# joints per stature (stature-scaled slab) and structural-mass axis CG < PK < DU
JB = json.load(open(JBF)) if JK != 'NONE' else {}; JS = json.load(open(os.environ.get('JBSRC', EV + '/joint_breadths.json')))  # JBKEY=NONE: no joint rows
jb = lambda i, j: (JB[JK] if i == "DU" else JS[{"MF-M-R": "MF-M-R", "PK": "PK-NAT", "CG": "CGJ7", "SK": "SK"}[i]])["scaled"][j]
for j in (("elbow", "wrist", "knee", "ankle") if JK != 'NONE' else ()):
    for b, chk, src in (("MF-M-R", "substantial %s breadth / stature > MF" % j, "DU L40, L124, L130"), ("PK", "structural-mass axis PK < DU (%s breadth / stature)" % j, "SRR L41-48; RAC-05 L32; order item 5"),
                        ("CG", "structural-mass axis CG < DU (%s breadth / stature)" % j, "SRR L41-48; order item 5")):
        va, vb = jb("DU", j), jb(b, j)
        out["added"].append({"cand": "DU", "check": chk, "canon": src, "reading": "%s breadth / stature (scaled slab)" % j, "va": va, "op": ">", "b": b, "vb": vb, "result": cls(">", va, vb), "note": ""})
    va, vb = jb("PK", j), jb("CG", j)
    out["added"].append({"cand": "PK", "check": "structural-mass axis CG < PK (%s breadth / stature; accepted bodies)" % j, "canon": "SRR L41-48", "reading": "%s scaled" % j, "va": va, "op": ">", "b": "CG", "vb": vb, "result": cls(">", va, vb), "note": "accepted-body control"})
# separation rows vs Pipkin / Cogling (order items 3, 6, 7): positive Durrim anatomy against the accepted short races
for k, op in (("thoracic depth / stature", ">"), ("thoracic breadth / stature", ">"), ("leg / stature", "<"), ("arm / stature", "<"), ("hand / stature", ">"), ("palm breadth / stature", ">"),
              ("palm depth / stature", ">"), ("foot breadth / stature", ">"), ("neck / stature", "<")):
    add("Durrim vs Pipkin: %s" % k, "SR-COMP-03; SRR L66, L78; DU L64-66", k, op, "PK")
# vs Cogling the hand distinction is structural (SRR L78 vs L82: substantial hands vs fine construction with emphasized fingers);
# Cogling's hand LENGTH share is canonically emphasized, so hand / stature is reported, not scored
for k, op in (("thoracic depth / stature", ">"), ("thoracic breadth / stature", ">"), ("leg / stature", "<"), ("arm / stature", "<"), ("palm depth / stature", ">"),
              ("palm breadth / hand", ">"), ("foot breadth / stature", ">"), ("neck / stature", "<")):
    add("Durrim vs Cogling: %s" % k, "COG-BODY-10; SRR L66, L78, L82; DU L64-66", k, op, "CG")
add("Durrim vs Cogling: hand length / stature (Cogling hands proportionally emphasized by canon)", "SRR L82", "hand / stature", "vs", "CG", report=True)
add("Durrim thorax-led vs Pipkin pelvis-led: crest / thoracic breadth DU < PK", "DU-P6 (opposite direction to PIPKIN L150, L173)", "crest / thoracic breadth", "<", "PK")
json.dump(out, open(EV + '/central_%s.json' % TAG, 'w'), indent=1, default=float)
bad = [(r['cand'], r.get('b'), r['check'][:70], r.get('result', r.get('result_ADG10'))) for k in ('skin', 'directional', 'added') for r in out[k] if r.get('result', r.get('result_ADG10')) not in ('PASS', 'REPORT')]
print(TAG, {k: len(out[k]) for k in ('skin', 'directional', 'added')}, 'stature %.2f' % st("DU"), 'non-PASS:', bad)
