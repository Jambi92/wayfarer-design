# RAC W2I comparisons. Saurin (rig-less closure mesh, sa_build.py) vs the accepted W2 MPFB families (real matched height where adult ranges overlap).
# COMMON readings (same anatomical intent; definitions differ by construction and are stated; ratios to standing height, tail excluded):
#   hip-joint height        Saurin: authored hip-joint level station (u 91 on the frozen reference)          MPFB: rig hip joint (mean hip_height)
#   LT1 lower axial trunk   Saurin: costal-margin station (u 123) - hip-joint station  (= the canon "lower trunk" 32.0 cm, §263 accounting)
#                           MPFB: costal-margin proxy (spine_03 joint = suprasternal - thoracic vertical) - hip joint
#   LT2 costal -> crest     Saurin: costal station - pelvic-platform station (u 100)                         MPFB: waist interval (spine_03 -> spine_01 crest proxy)
#   TV thoracic vertical    Saurin: thoracic-inlet station (u 152) - costal station                          MPFB: suprasternal - costal proxy
#   thoracic d/w, depth, breadth: Saurin metrics (sagittal depth at u 132; torso breadth 118-140)           MPFB: skin thorax depth / breadth
#   shoulder: Saurin torso breadth 140-156 (arms excluded)   MPFB: shoulder-joint breadth
#   pelvis: Saurin torso breadth 86-100                       MPFB: bitrochanteric breadth
#   head height: Saurin vertex - chin                          MPFB: HH (vertex - menton)
#   foot length: Saurin sole extent (u < 1.5 cm, per side)     MPFB: foot length
#   tail (% H): Saurin §256 / AD-R35 landmark                 MPFB: none (0)
# Classes AD-G10. Usage: python3 sa_compare.py SA_BODIES.json [SA_EXTRA.json ...] OUT.json
import sys, json, os
R = '/home/claude/wayfarer-design/reviews'
REG = {}
for f in ('rac-w2d-go-evidence/registry.json', 'rac-w2e-sg-evidence/registry.json', 'rac-w2g-hv-evidence/registry.json'): REG.update(json.load(open(R + '/' + f)))
SA = {}
for f in sys.argv[1:-1]: SA.update(json.load(open(f)))
OUT = sys.argv[-1]
KEYS = ["hip-joint height / H", "LT1 lower axial trunk (costal - hip joint) / H", "LT2 costal - crest / H", "thoracic vertical / H", "thoracic depth / breadth", "thoracic depth / H",
        "thoracic breadth / H", "shoulder breadth / H", "pelvic breadth / H", "head height / H", "foot length / H", "tail length % H"]
def sa_read(M):
    H = M['height']
    return dict(zip(KEYS, [M['u_hip'] / H, M['lower_trunk_costal_hip'] / H, M['lower_trunk_costal_platform'] / H, M['thoracic_vertical'] / H, M['thorax_d_over_w'], M['thorax_d'] / H,
                           M['thorax_w'] / H, M['shoulder_b'] / H, M['pelvis_w'] / H, M['head_depth'] / H, M.get('foot_len_over_H'), M['tail_len_pct']]), stature=H)
def mp_read(key):
    e = REG[key]; m = json.load(open(e['meas'] + '_meas.json'))['combined']; H = m['stature']; mm = m['mean']; cost = m['suprasternal_u'] - m['thoracic_vertical']
    return dict(zip(KEYS, [mm['hip_height'] / H, (cost - mm['hip_height']) / H, m['waist_interval'] / H, m['thoracic_vertical'] / H, m['thorax_depth'] / m['thorax_breadth'], m['thorax_depth'] / H,
                           m['thorax_breadth'] / H, m['shoulder_joint_breadth'] / H, m['bitrochanteric_breadth'] / H, m['ratio']['HH_share'], mm['foot_len'] / H, 0.0]), stature=H)
V = {k: sa_read(M) for k, M in SA.items()}
for k in REG:
    try: V[k] = mp_read(k)
    except Exception: pass
def cls(op, va, vb):
    rel = abs(va - vb) / abs(vb) if vb else 1.0; holds = {">": va > vb, "<": va < vb, ">=": va >= vb, "<=": va <= vb}[op]
    if op in (">", "<"): return ("PASS" if rel >= 0.01 else "NOT DEMONSTRATED") if holds else "FAIL"
    return "PASS" if holds else ("MARGINAL" if rel < 0.01 else "FAIL")
C = []
def row(code, chk, a, op, b, k, note="", report=False):
    if a not in V or b not in V or V[a].get(k) is None or V[b].get(k) is None: C.append(dict(code=code, check=chk, a=a, b=b, reading=k, result="NOT RUN", note="reading or body unavailable")); return
    va, vb = V[a][k], V[b][k]
    C.append(dict(code=code, check=chk + (" — REPORT ONLY" if report else ""), a=a, b=b, reading=k, va=va, op=op, vb=vb, margin_pct=100 * (va / vb - 1) if vb else None,
                  result="REPORT" if report else cls(op, va, vb), note=note))
def absrow(code, chk, a, op, lim, k, note=""):
    va = V[a][k]; ok = {"<=": va <= lim, ">=": va >= lim}[op]
    C.append(dict(code=code, check=chk, a=a, b="limit", reading=k, va=va, op=op, vb=lim, margin_pct=100 * (va / lim - 1), result="PASS" if ok else ("MARGINAL" if abs(va / lim - 1) < 0.01 else "FAIL"), note=note))
def passing(code, chk, a, b, min_sep=3):
    ks = [k for k in KEYS if V[a].get(k) is not None and V[b].get(k) is not None]
    sep = [(k, 100 * (V[a][k] / V[b][k] - 1) if V[b][k] else 100.0) for k in ks if (V[b][k] == 0 and V[a][k] != 0) or (V[b][k] and abs(V[a][k] / V[b][k] - 1) >= 0.01)]
    C.append(dict(code=code, check=chk, a=a, b=b, reading="%d common readings" % len(ks), va=len(sep), op=">=", vb=min_sep, result="PASS" if len(sep) >= min_sep else "NEAR-DUPLICATE",
                  note="; ".join("%s %+.1f" % (k, d) for k, d in sorted(sep, key=lambda z: -abs(z[1]))[:6])))
LT1, LT2, TV = KEYS[1], KEYS[2], KEYS[3]
# LTF: lower-trunk floor (AD-R36, order §6): the -10 % lower-trunk Saurin at 168 and 203 cm vs matched-stature Marchfolk
for h, mf in ((168, "MF168"), (203, "MF203")):
    for a in ("SA-M%d-LT90" % h, "SA-F%d-LT90" % h, "SA-M%d" % h, "SA-F%d" % h):
        rep = not a.endswith("LT90")
        for k in (LT1, LT2): row("LTF", "%d cm: %s longer lower axial trunk than %s: %s" % (h, a, mf, k), a, ">", mf, k, "AD-R36; SAURIN L56, L4269", rep)
        for k in (TV, KEYS[0], KEYS[4]): row("LTF", "%d cm: %s vs %s (context): %s" % (h, a, mf, k), a, "vs", mf, k, "order §6 context", True)
# M: real matched-height race comparisons (order §14) - scored canon directions + body-only passing; Saurin tail always separates
DIRS = {"MF": [(LT1, ">", "elongated lower axial trunk (SA L56)"), (KEYS[4], ">", "deep thorax (SA L56)"), (KEYS[5], ">", "deep thorax")],
        "SK": [(KEYS[7], "<", "caudal / pelvic-axial, not broad clavicular robustness (order §14)"), (LT1, ">", "lower axial trunk")],
        "SG": [(LT1, ">", "linear human proportions must not mimic the Saurin lower axial system (order §14)")],
        "FN": [(KEYS[5], ">", "not Fenn gracility (order §14)"), (LT1, ">", "lower axial trunk")],
        "AE": [(LT1, ">", "not Aelari distributed vertical elongation (order §14)"), (KEYS[4], ">", "deep thorax")],
        "VA": [(LT1, ">", "not Vael compact deep-bodied continuity (order §14)")],
        "HV": [(LT1, ">", "not a mixed human / elf body plus a tail (order §14)"), (KEYS[4], ">", "deep thorax")],
        "GO": [(KEYS[5], "<", "below Gorrund load-bearing mass (order §8, §14)"), (KEYS[6], "<", "below Gorrund breadth"), (KEYS[7], "<", "below Gorrund shoulder mass")]}
MATCH = {168: ["MF168", "AE168"], 173: ["MF173", "SG173", "FN173", "AE173", "VA173", "HV173"], 178: ["MF178", "SG178", "FN178", "AE178", "VA178", "HV178"],
         181: ["MF181", "SG181", "FN181", "AE181", "VA181", "HV181"], 190: ["MF190", "SG190", "FN190", "AE190", "VA190", "HV190", "SK190"],
         203: ["MF203", "SG203", "FN203", "AE203", "VA203", "HV203", "SK203"], 208: ["SG208", "SK208", "GO208", "SKB208"]}
for h, comps in MATCH.items():
    for sx in ("M", "F"):
        a = "SA-%s%d" % (sx, h)
        if a not in V: continue
        for b in comps:
            if b not in V: continue
            for k, op, note in DIRS.get(b[:2], []): row("M", "%d cm: Saurin %s %s %s: %s" % (h, a, op, b, k), a, op, b, k, note, b[:2] == "GO")
            passing("P", "%d cm: Saurin %s vs %s (body-only; tail counted)" % (h, a, b), a, b)
            ks = [k for k in KEYS[:-1]]; sep = [k for k in ks if V[a].get(k) is not None and V[b].get(k) and abs(V[a][k] / V[b][k] - 1) >= 0.01]
            C.append(dict(code="P0", check="%d cm: Saurin %s vs %s WITHOUT the tail (tail-hidden test)" % (h, a, b), a=a, b=b, reading="%d body readings" % len(ks), va=len(sep), op=">=", vb=3,
                          result="PASS" if len(sep) >= 3 else "NEAR-DUPLICATE", note=", ".join(sep[:8])))
# G: never-Gorrund guard at the 208 cm overlap (Broad, Broad + high muscle, Broad + muscle + fat)
for a in ("SA-M208-B", "SA-M208-B-MUHI", "SA-M208-B-MUFAHI"):
    # Gorrund comparison carriers below are NOT the canon guard (AD-R36: frame-scope ban + d/w <= 1.00; numeric Broad-vs-Gorrund boundary OPEN, SAURIN §265)
    # and the thoracic readings are defined differently on the two meshes (Saurin band maxima vs MPFB level readings): REPORT
    for k, op, note in DIRS["GO"]: row("G", "208 cm Gorrund context: %s %s GO208: %s" % (a, op, k), a, op, "GO208", k, note + "; report (not the canon guard; definitions differ)", True)
    absrow("G", "208 cm never-Gorrund: %s thoracic d/w <= 1.00 (§258 / AD-R36 interim guard)" % a, a, "<=", 1.00, KEYS[4], "SAURIN §258, L4269")
    passing("G", "208 cm: %s vs GO208 (body-only)" % a, a, "GO208")
# feet (order §16): broad stable feet, more forefoot / toe contribution than Marchfolk - foot length / H vs matched Marchfolk (toe split not measurable)
for h, mf in ((168, "MF168"), (173, "MF173"), (178, "MF178"), (181, "MF181"), (190, "MF190"), (203, "MF203")):
    row("L", "%d cm: Saurin foot length / H vs %s (forefoot / toe contribution; whole-foot proxy)" % (h, mf), "SA-M%d" % h, ">", mf, KEYS[10], "SA L? feet broad, increased forefoot / toe (order §16)", True)
# RM-OT-04 face rows (existing accepted values only): Saurin r3 FPI (W1 RM-CF-01) vs Sagekin / Halvren FPI
W1 = json.load(open(R + '/rac-w1-evidence/saurin_w1.json'))
sa_fpi = W1['RM_CF_01']['male_centre_base']['FPI']; sa_fpi_f = W1['RM_CF_01']['female_centre_base']['FPI']
for b in ("SG173", "SG178", "SG181", "SG190", "SG203", "SG208", "HV173", "HV178", "HV181", "HV190", "HV203", "HV213"):
    if b in REG:
        fpi = json.load(open(REG[b]['meas'] + '_meas.json'))['combined']['cranio'].get('FPI')
        C.append(dict(code="OT4F", check="RM-OT-04 face (existing values): Saurin male-centre r3 FPI vs %s FPI" % b, a="SA-M (W1 RM-CF-01)", b=b, reading="FPI (r3)", va=sa_fpi, op="vs", vb=fpi,
                      margin_pct=100 * (sa_fpi / fpi - 1) if fpi else None, result="REPORT", note="W1 accepted RM-CF-01 value; female centre %.4f" % sa_fpi_f))
json.dump({"keys": KEYS, "values": V, "checks": C}, open(OUT, 'w'), indent=1, default=float)
import collections
print(collections.Counter((c['code'], c['result']) for c in C))
for c in C:
    if c['result'] not in ('PASS', 'REPORT'): print(' ', c['code'], c['check'][:110], c.get('note', '')[:80], c['result'], '%+.2f' % c['margin_pct'] if c.get('margin_pct') is not None else '')
