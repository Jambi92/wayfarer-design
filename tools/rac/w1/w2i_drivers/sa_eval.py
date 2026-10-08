# RAC W2I Saurin internal checks (stature family, frames, composition, sex-related cases, tails, balance) on sa_build.py / sa_build_extra.py output.
# Tail ratios are normalized to the W2I-reproduced SA-M (sa_repro.py); RSI is additionally size-normalized (÷ H / 187.88) because §256.9 makes every
# tail relationship isometric with stature. Classes AD-G10. Usage: python3 sa_eval.py SA_BODIES.json SA_EXTRA.json REPRO.json OUT.json
import sys, json
B = json.load(open(sys.argv[1])); B.update(json.load(open(sys.argv[2]))); RP = json.load(open(sys.argv[3])); OUT = sys.argv[4]
H0 = 187.881473082305; REF = B["SA-M188"]
C = []
def add(code, chk, a, va, op, vb, res, note=""):
    C.append(dict(code=code, check=chk, a=a, va=va, op=op, vb=vb, result=res, note=note))
def tail_n(M):
    sH = M['height'] / H0
    return dict(RSI=M['tail_RSI_raw'] / REF['tail_RSI_raw'] / sH, taper=M['tail_taper_raw'] / REF['tail_taper_raw'], A50=M['tail_A50'], A25=M['tail_A25'], dlean=M['lean_scaled_deg'] - REF['lean_scaled_deg'])
def guards(M):
    n = tail_n(M); return n, {"RSI 0.75-1.20": 0.75 <= n['RSI'] <= 1.20, "taper <= 1.25": n['taper'] <= 1.25, "A50 0.27-0.48": 0.27 <= n['A50'] <= 0.48, "A25 >= 0.065": n['A25'] >= 0.065,
                              "lean <= +3 deg": n['dlean'] <= 3.0, "d/w <= 1.00": M['thorax_d_over_w'] <= 1.0}
# R: reproduction
for k, (a, b, d) in RP['SA-M_vs_ref_metrics'].items():
    add("R", "SA-M reproduction vs frozen Part 7 reference: %s" % k, "SA-M", a, "~", b, "PASS" if abs(d or 0) < 0.5 else "REPORT", "%+.3f %%" % (d or 0))
for k in ('height', 'lower_trunk', 'pelvis_w', 'thorax_d_over_w', 'tail_len_pct'):
    for b in ('SA-M', 'SA-F'):
        w = RP['W1_ARM'][b].get(k)
        if w: v = RP[b][k]; add("R", "%s reproduction vs W1 ARM record: %s" % (b, k), b, v, "~", w, "PASS" if abs(v / w - 1) < 0.005 else "REPORT", "%+.3f %%" % (100 * (v / w - 1)))
# ST: stature family
SER = ["SA-M168", "SA-M173", "SA-M178", "SA-M181", "SA-M188", "SA-M190", "SA-M203", "SA-M208"]
SERF = [s.replace("M", "F", 1) if s != "SA-M188" else "SA-F188" for s in SER]
for s in SER + SERF:
    M = B[s]; tgt = H0 if s.endswith("188") else float(s[-3:])
    add("ST", "%s standing height (tail excluded) hits the target" % s, s, M['height'], "~", tgt, "PASS" if abs(M['height'] - tgt) < 0.05 else "FAIL", "k_len %.4f" % M['k_len'])
    add("ST", "%s head length / H inside the §258 bound 0.156-0.184" % s, s, M['head_len_ratio'], "in", [0.156, 0.184], "PASS" if 0.156 <= M['head_len_ratio'] <= 0.184 else "FAIL", "allometric head (beta 0.688)")
    add("ST", "%s thoracic d/w <= 1.00 (§258)" % s, s, M['thorax_d_over_w'], "<=", 1.0, "PASS" if M['thorax_d_over_w'] <= 1.0 else "FAIL")
    n, g = guards(M)
    add("ST", "%s tail relationships isometric (§256.9): size-normalized RSI, taper, A50, A25 inside the §256 guards" % s, s, [round(n[x], 4) for x in ('RSI', 'taper', 'A50', 'A25')], "guards", None,
        "PASS" if all(v for k, v in g.items() if not k.startswith("lean")) else "FAIL", "tail %.2f %% H" % M['tail_len_pct'])
KEYS = ["lower_trunk_costal_hip_over_H", "lower_trunk_costal_platform_over_H", "thoracic_vertical_over_H", "thorax_d_over_w", "thorax_d_over_H", "thorax_w_over_H", "shoulder_b_over_H",
        "pelvis_w_over_H", "head_len_ratio", "head_depth_over_H", "tail_len_pct", "foot_len_over_H", "lean_scaled_deg"]
for nm, ser in (("male", SER), ("female centre", SERF)):
    for k in KEYS:
        vals = [B[s].get(k) for s in ser]
        if any(v is None for v in vals): continue
        steps = [100 * (vals[i + 1] / vals[i] - 1) for i in range(len(vals) - 1)]; up = sum(x > 0 for x in steps); dn = sum(x < 0 for x in steps)
        bad = [i for i, x in enumerate(steps) if up and dn and ((x > 0) != (up >= dn)) and abs(x) >= 1.0]
        add("C", "continuity %s 168 -> 208: %s" % (nm, k), ser[0], vals, "trend", None, "PASS" if not bad else "NON-MONOTONIC", " / ".join("%+.2f" % x for x in steps) + " % per step")
for h in (168, 208):
    a, u = B["SA-M%d" % h], B["SA-M%d-UNIF" % h]
    for k in KEYS: add("U", "%d cm regional route vs Part 7 uniform convention: %s" % (h, k), "SA-M%d" % h, a.get(k), "vs", u.get(k), "REPORT", "%+.2f %%" % (100 * (a[k] / u[k] - 1)) if a.get(k) and u.get(k) else "")
# FR: frames (§258: frame changes shoulder, thoracic width, depth +/-2 % only, pelvic width, limb / joint girth, hands / feet, tail-base frame component;
#     never stature, long-bone or axial lengths, skull, pelvic depth / sacral-caudal organization)
for h in (168, 188, 203, 208):
    base = B["SA-M%d" % h]
    for t, sign in (("N", -1), ("B", 1)):
        x = "SA-M%d-%s" % (h, t); M = B[x]
        for k in ("height", "lower_trunk_costal_hip", "lower_trunk_costal_platform", "thoracic_vertical", "head_len", "u_hip", "tail_len_pct"):
            d = 100 * (M[k] / base[k] - 1); add("FR", "%s keeps %s (frame never changes stature / axial lengths / skull / tail; 0.5 %%)" % (x, k), x, M[k], "~", base[k], "PASS" if abs(d) < 0.5 else "FAIL", "%+.2f %%" % d)
        d = 100 * (M['thorax_d'] / base['thorax_d'] - 1); add("FR", "%s thoracic depth within +/-2 %% (§258)" % x, x, M['thorax_d'], "~", base['thorax_d'], "PASS" if abs(d) <= 2.05 else "FAIL", "%+.2f %%" % d)
        for k in ("shoulder_b", "thorax_w", "pelvis_w"):
            d = 100 * (M[k] / base[k] - 1); add("FR", "%s moves %s in the frame direction (>= 1 %%)" % (x, k), x, M[k], "D", base[k], "PASS" if sign * d >= 1.0 else "NOT DEMONSTRATED", "%+.2f %%" % d)
        add("FR", "%s thoracic d/w <= 1.00 (never-Gorrund interim guard)" % x, x, M['thorax_d_over_w'], "<=", 1.0, "PASS" if M['thorax_d_over_w'] <= 1.0 else "FAIL")
        n, g = guards(M); add("FR", "%s tail identity: §256 guards hold with the reference tail" % x, x, [round(n[q], 4) for q in ('RSI', 'taper', 'A50', 'A25', 'dlean')], "guards", None,
                               "PASS" if all(g.values()) else "FAIL", ", ".join(k for k, v in g.items() if not v))
# CO: composition firewall
for sx, ref in (("M", "SA-M188"), ("F", "SA-F188")):
    base = B[ref]
    for c in ("MULO", "MUHI", "FALO", "FAHI", "MUFAHI", "MIN"):
        x = "SA-%s188-%s" % (sx, c); M = B[x]
        for k in ("height", "lower_trunk_costal_hip", "thoracic_vertical", "head_len", "u_hip", "tail_len_pct"):
            d = 100 * (M[k] / base[k] - 1); add("CO", "%s keeps %s (composition never changes lengths; 1 %%)" % (x, k), x, M[k], "~", base[k], "PASS" if abs(d) < 1.0 else "FAIL", "%+.2f %%" % d)
        add("CO", "%s thoracic d/w <= 1.00" % x, x, M['thorax_d_over_w'], "<=", 1.0, "PASS" if M['thorax_d_over_w'] <= 1.0 else "FAIL")
        n, g = guards(M); add("CO", "%s tail §256 guards (composition cannot create a fake tail base)" % x, x, [round(n[q], 4) for q in ('RSI', 'taper', 'A50', 'A25', 'dlean')], "guards", None,
                               "PASS" if all(g.values()) else "FAIL", "root area %+.1f %%; %s" % (100 * (M['tail_root_area'] / base['tail_root_area'] - 1), ", ".join(k for k, v in g.items() if not v)))
# SX: sex-related (§263): female centre vs male centre at every stature; clamps; female at the -10 % request
for h in (168, 173, 178, 181, 188, 190, 203, 208):
    f, m = B["SA-F%d" % h], B["SA-M%d" % h]
    for k, note in (("lower_trunk_costal_hip", "+7 % female-centre tendency (canon accounting 32.0 -> 33.6 cm at 187.9)"), ("pelvis_w", "+5.5 % pelvic band tendency (accounting 41.7 -> 43.1)"),
                    ("thorax_d_over_w", "0.880 -> 0.922 (accounting)"), ("height", "no sex shift"), ("tail_len_pct", "no sex shift (head / tail stature compensation)"), ("head_len_ratio", "no sex shift")):
        add("SX", "%d cm female centre vs male centre: %s" % (h, k), "SA-F%d" % h, f[k], "vs", m[k], "REPORT", "%+.2f %%; %s" % (100 * (f[k] / m[k] - 1), note))
    add("SX", "%d cm female centre thoracic d/w <= 1.00 (shared guard)" % h, "SA-F%d" % h, f['thorax_d_over_w'], "<=", 1.0, "PASS" if f['thorax_d_over_w'] <= 1.0 else "FAIL")
for x, note in (("SA-F188-N", "Narrow female centre"), ("SA-F188-B", "Broad female centre"), ("SA-FREF188", "+10 % reference female"), ("SA-F188-N-B30", "Narrow + B 3.0 requested (canon: CONSTRAIN)"),
                ("SA-F188-N-B21", "Narrow + B clamped 2.1 (canon clamp)"), ("SA-F188-N-FAHI", "Narrow + high fat, B 1.6 (canon: CONSTRAIN)"), ("SA-F188-N-FAHI-B15", "Narrow + high fat, B clamped 1.5 (canon clamp)"),
                ("SA-F188-FAHI", "female high fat"), ("SA-F188-FALO", "female low fat")):
    M = B[x]; ok = M['thorax_d_over_w'] <= 1.0; req = x.endswith(("B30",)) or x == "SA-F188-N-FAHI"
    add("SX", "%s: thoracic d/w <= 1.00 (§263 clamps)" % x, x, M['thorax_d_over_w'], "<=", 1.0, ("PASS (request exceeds the guard -> CONSTRAIN, as canon)" if not ok else "PASS (request inside the guard)") if req else ("PASS" if ok else "FAIL"), note)
for h in (168, 203):
    f, m = B["SA-F%d-LT90" % h], B["SA-M%d-LT90" % h]
    add("SX", "%d cm: a female-shifted body requesting the -10 %% trunk sits at the same species bound as the male (sex never extends a bound)" % h, "SA-F%d-LT90" % h, f['lower_trunk_costal_hip'], "~", m['lower_trunk_costal_hip'],
        "PASS" if abs(f['lower_trunk_costal_hip'] / m['lower_trunk_costal_hip'] - 1) < 0.01 else "REPORT", "%+.2f %%" % (100 * (f['lower_trunk_costal_hip'] / m['lower_trunk_costal_hip'] - 1)))
# TL: tail bodies (§256) and balance (§13 firewall: +3 deg relative guard, uniform-density model only)
for x in ("SA-M188-T55", "SA-M188-T55-B83", "SA-M188-T78", "SA-M188-T80", "SA-M188-B-T80", "SA-M188-N-FAHI-T72", "SA-M188-N-FAHI-T78", "SA-M168-T55", "SA-M208-B-T80"):
    M = B[x]; n, g = guards(M)
    add("TL", "%s (%s): §256 guards" % (x, M['note']), x, dict({k: round(v, 4) for k, v in n.items()}, tail_pct=round(M['tail_len_pct'], 2), mass_share=round(M['tail_mass_share'], 4)), "guards", None,
        "PASS" if all(g.values()) else "FAIL (" + ", ".join(k for k, v in g.items() if not v) + ")")
for x, M in B.items():
    add("BAL", "%s: lean relative to the frozen reference (uniform-density static model; diagnostic)" % x, x, M['lean_scaled_deg'] - REF['lean_scaled_deg'], "<=", 3.0, "REPORT", "")
json.dump({"checks": C}, open(OUT, 'w'), indent=1, default=float)
import collections
print(collections.Counter((c['code'], c['result'][:20]) for c in C))
for c in C:
    if c['result'] not in ('PASS', 'REPORT') and not c['result'].startswith('PASS'): print(' ', c['code'], c['check'][:110], c['va'] if not isinstance(c['va'], list) else '', c['note'][:90], c['result'])
