# RAC W2I1 D3 validator closure (closure order §5-§6): Saurin J-2 limb / joint / S7 readings (sa_joints.py) against the accepted W2 MPFB
# comparators, for the previously blocked SAU-BODY-11 (limb portion), -13, -14 (joint portion), -15, -16, and the hip-station /
# "moderate-to-long legs" watch item.
# MPFB readings: arm_measure 'combined' segments and ratios (rig joints); EXACT-PLANE joint sections recomputed here with the w2c1
# joint_section.py rule (same vertex sets / axes; controlled against the committed joint_sections.json values); femoral S7 from the accepted
# skeletal proxy (CIB, by t). Saurin: the same definitions on the J-2 construction joints (sa_joints.py).
# Normalization: joint breadths and S7 per STANDING HEIGHT (w2c1 jbw / W1s hv_skel convention). Per-segment ratios (elbow / humerus etc.)
# are REPORT only, because the Saurin construction femur is short (hip-knee 24 cm at 188) and a per-femur ratio would carry that.
# Surface crotch height (definition-identical on both pipelines: lowest non-tail vertex with |x| < 3 cm between 0.25 H and 0.6 H) is added
# for the leg watch item. Classes AD-G10 (1 % margin). Usage: python3 sa_limbcmp.py JOINTS.json CROTCH.json OUT.json
import sys, os, json, glob, numpy as np
sys.path.insert(0, '/home/claude/wayfarer-design/tools/rac/w1'); from arm_measure import load
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
R = '/home/claude/wayfarer-design/reviews'
REG = {}
for f in ('rac-w2c-gr-evidence/registry.json', 'rac-w2d-go-evidence/registry.json', 'rac-w2e-sg-evidence/registry.json', 'rac-w2g-hv-evidence/registry.json'): REG.update(json.load(open(R + '/' + f)))
CL = json.load(open(R + '/rac-w2h-sr-evidence/closure/registry_closure.json')); REG['DU137C'] = CL['DU137']; REG['CG91'] = CL['CG91']
JT = json.load(open(sys.argv[1]))['bodies']; OUT = sys.argv[-1]
CR = json.load(open(sys.argv[2])) if len(sys.argv) > 3 else {}
for k, v in CR.items():
    if k in JT: JT[k]['crotch_u'] = v
def section(V, F, on, c, ax):
    TF = F[on[F].all(1)]; t = (V - c) @ ax; pts = []
    for i, j in ((0, 1), (1, 2), (2, 0)):
        a, b = TF[:, i], TF[:, j]; m = t[a] * t[b] < 0; u = t[a[m]] / (t[a[m]] - t[b[m]]); pts.append(V[a[m]] + (V[b[m]] - V[a[m]]) * u[:, None])
    P = np.vstack(pts) - c; Q = P - np.outer(P @ ax, ax)
    if len(Q) < 4: return float('nan')
    ev, evec = np.linalg.eigh(np.cov(Q.T)); wd = evec[:, -1]; return float((Q @ wd).max() - (Q @ wd).min())
def crotch(V, H, notail=None):
    m = (np.abs(V[:, 0]) < 3.0) & (V[:, 2] > 0.25 * H) & (V[:, 2] < 0.6 * H)
    if notail is not None: m &= notail
    return float(V[m, 2].min())
def mp_read(key):
    e = REG[key]; m = json.load(open(e['meas'] + '_meas.json'))['combined']; H = m['stature']; mm = m['mean']; r = m['ratio']
    d = load(e['meas'] + '_rest.npz'); V = d['V'].astype(float); F = d['F']; keep = d['keep']; J = d['joints']; w = lambda k: d['w_' + k]; h = lambda n: np.asarray(J[n][0], float)
    u = lambda v: v / np.linalg.norm(v); sec = {k: [] for k in ('elbow', 'wrist', 'knee', 'ankle')}
    for s in ('l', 'r'):
        sh, el, wr, hp, kn, an = h('upperarm_' + s), h('lowerarm_' + s), h('hand_' + s), h('thigh_' + s), h('calf_' + s), h('foot_' + s)
        sec['elbow'].append(section(V, F, keep & ((w('upperarm_' + s) + w('lowerarm_' + s)) > 0.3), el, u(wr - sh)))
        sec['wrist'].append(section(V, F, keep & ((w('lowerarm_' + s) + w('hand_' + s)) > 0.3), wr, u(wr - el)))
        sec['knee'].append(section(V, F, keep & ((w('thigh_' + s) + w('calf_' + s)) > 0.3), kn, u(an - hp)))
        sec['ankle'].append(section(V, F, keep & ((w('calf_' + s) + w('foot_' + s)) > 0.3), an, u(an - kn)))
    sc = {k: float(np.mean(v)) for k, v in sec.items()}
    sk = glob.glob(e['skp'] + '/*_skp.json'); s7 = {}
    if sk:
        bt = json.load(open(sk[0]))['by_t']
        for t, v in bt.items(): s7[t] = dict(b=v['alpc_stations']['S7'][0] / H, d=v['alpc_stations']['S7'][1] / H)
    Vk = V[keep]; Hs = Vk[:, 2].max() - Vk[:, 2].min()
    out = dict(stature=H, leg_share=r['leg_share'], leg_share_station=None, leg_joint_share=mm['leg_joint'] / H, thigh_share=r['thigh_share'], shin_share=r['shin_share'],
               arm_share=r['arm_share'], span_der=r['span_der'], upperarm_share=mm['upperarm'] / H, forearm_share=mm['forearm'] / H, hand_share=r['hand_share'],
               forearm_over_arm=r['forearm_over_arm'], distal_over_arm=r['forearm_over_arm'] + r['hand_over_arm'], hand_over_arm=r['hand_over_arm'],
               forearm_over_upperarm=r['forearm_over_upperarm'], femur_over_leg=r['femur_over_leg'], shin_over_leg=r['shin_over_leg'], finger_over_hand=r['finger_over_hand'],
               elbow_sec_share=sc['elbow'] / H, wrist_sec_share=sc['wrist'] / H, knee_sec_share=sc['knee'] / H, ankle_sec_share=sc['ankle'] / H,
               elbow_sec_over_humerus=sc['elbow'] / mm['upperarm'], wrist_sec_over_forearm=sc['wrist'] / mm['forearm'], knee_sec_over_femur=sc['knee'] / mm['thigh'], ankle_sec_over_shin=sc['ankle'] / mm['shin'],
               ankle_height_share=mm['ankle_height'] / H, S7=s7, joint_sections_cm=sc, joint_stature_norm=H)
    return out
def sa_read(bid):
    b = JT[bid]; m = b['mean']; r = b['ratio']; H = b['stature']
    return dict(stature=H, leg_share=r['leg_share'], leg_share_station=b['axial']['u_hip'] / H, leg_joint_share=r['leg_joint_share'], thigh_share=r['thigh_share'], shin_share=r['shin_share'],
                arm_share=r['arm_share'], span_der=r['span_der'], upperarm_share=r['upperarm_share'], forearm_share=r['forearm_share'], hand_share=r['hand_share'],
                hand_noclaw_share=r['hand_noclaw_share'], forearm_over_arm=r['forearm_over_arm'], distal_over_arm=r['forearm_over_arm'] + r['hand_over_arm'], hand_over_arm=r['hand_over_arm'],
                forearm_over_upperarm=r['forearm_over_upperarm'], femur_over_leg=r['femur_over_leg'], shin_over_leg=r['shin_over_leg'], finger_over_hand=r['finger_over_hand'],
                elbow_sec_share=r['elbow_share'], wrist_sec_share=r['wrist_share'], knee_sec_share=r['knee_share'], ankle_sec_share=r['ankle_share'],
                elbow_sec_over_humerus=r['elbow_over_humerus'], wrist_sec_over_forearm=r['wrist_over_forearm'], knee_sec_over_femur=r['knee_over_femur'], ankle_sec_over_shin=r['ankle_over_shin'],
                ankle_height_share=r['ankle_height_share'], S7={t: dict(b=v['S7_breadth'] / H, d=v['S7_depth'] / H) for t, v in b['S7_CIB'].items()},
                S7_self=dict(b=m['S7_breadth'] / H, d=m['S7_depth'] / H), mid_humerus_share=m['mid_humerus_breadth'] / H, mid_forearm_share=m['mid_forearm_breadth'] / H, mid_shin_share=m['mid_shin_breadth'] / H)
VAL = {}
def cls(op, va, vb):
    rel = abs(va - vb) / abs(vb) if vb else 1.0; holds = {">": va > vb, "<": va < vb}[op]
    return ("PASS" if rel >= 0.01 else "NOT DEMONSTRATED") if holds else "FAIL"
ROWS = []
def row(val, chk, a, op, b, k, note="", report=False, t=None):
    va = VAL[a][k] if t is None else VAL[a]['S7'][t][k]; vb = VAL[b][k] if t is None else VAL[b]['S7'].get(t, {}).get(k)
    if va is None or vb is None or (isinstance(va, float) and np.isnan(va)): ROWS.append(dict(code=val, check=chk, a=a, b=b, reading=k, result="NOT RUN", note="unavailable")); return
    ROWS.append(dict(code=val, check=chk + (" — REPORT" if report else ""), a=a, b=b, reading=k + ('' if t is None else ' (t %s)' % t), va=va, op=op, vb=vb,
                     margin_pct=100 * (va / vb - 1), result="REPORT" if report else cls(op, va, vb), note=note,
                     structural_surface=(t is not None or k.endswith('_sec_share'))))
if __name__ == '__main__':
    for k in JT: VAL[k] = sa_read(k)
    MPK = ["MF168", "MF173", "MF178", "MF181", "MF190", "MF203", "GR208", "GR218", "GO208", "CG91", "DU137C"]
    for k in MPK: VAL[k] = mp_read(k); print(k, {a: round(v, 4) for a, v in VAL[k].items() if isinstance(v, float)}, flush=True)
    # control: recomputed exact-plane sections vs committed evidence (w2h joint_sections.json: 'section' = breadth / R-6 stature)
    ctl = {}
    js = json.load(open(R + '/rac-w2h-sr-evidence/joint_sections.json'))
    for mk, ek in (("CG91", "CGJ7"),):
        if ek in js: ctl[mk] = {j: [VAL[mk]['joint_sections_cm'][j] / js[ek]['stature'], js[ek]['section'][j]] for j in ('elbow', 'wrist', 'knee', 'ankle')}
    print('CONTROL', ctl)
    MATCH = {168: "MF168", 173: "MF173", 178: "MF178", 181: "MF181", 190: "MF190", 203: "MF203"}
    # SAU-BODY-11 limb portion (Marchfolk-normalized skeleton; real matched height)
    for h, mf in MATCH.items():
        for sx in ("M", "F"):
            a = "SA-%s%d" % (sx, h)
            row("SAU-BODY-11", "%d: %s forearm share of arm vs %s (SAURIN §17 'may carry somewhat greater')" % (h, a, mf), a, ">", mf, "forearm_over_arm", "permissive canon wording", True)
            row("SAU-BODY-11", "%d: %s total arm / H vs %s ('moderate total arm contribution')" % (h, a, mf), a, ">", mf, "arm_share", "", True)
            row("SAU-BODY-11", "%d: %s hand / H vs %s ('hands distinctly non-human in proportion')" % (h, a, mf), a, ">", mf, "hand_share", "", True)
            for k in ("elbow_sec_share", "knee_sec_share", "wrist_sec_share", "ankle_sec_share"):
                row("SAU-BODY-11", "%d: %s %s vs %s ('moderate-to-substantial skeletal presence')" % (h, a, k, mf), a, ">", mf, k, "", True)
            for t in ("0.0", "0.5", "1.0"): row("SAU-BODY-11", "%d: %s femoral S7 breadth / H vs %s (CIB proxy)" % (h, a, mf), a, ">", mf, "b", "", True, t=t)
            # leg watch item rows
            for k in ("leg_share", "leg_share_station", "leg_joint_share", "thigh_share", "shin_share", "femur_over_leg", "ankle_height_share"):
                if k == "leg_share_station": row("LEGS", "%d: %s hip height / H (authored axial hip station u91) vs %s rig hip" % (h, a, mf), a, ">", mf, "leg_share", "cross-definition", True); ROWS[-1]['va'] = VAL[a][k]; ROWS[-1]['margin_pct'] = 100 * (VAL[a][k] / VAL[mf]['leg_share'] - 1); ROWS[-1]['reading'] = k; continue
                row("LEGS", "%d: %s %s vs %s" % (h, a, k, mf), a, ">", mf, k, "'moderate-to-long legs' (SAURIN L258, L3599; L970 'rather than by forcing shortened legs')", True)
    # SAU-BODY-13 Grask (not rangy reach specialists; no Grask global limb dominance) - matched 208 + reference-normalized 188 vs GR218
    for a, g, rep in (("SA-M208", "GR208", False), ("SA-F208", "GR208", False), ("SA-M208-B", "GR208", False), ("SA-M188", "GR218", True)):
        for k in ("arm_share", "span_der", "leg_joint_share", "leg_share", "forearm_share", "upperarm_share"):
            row("SAU-BODY-13", "%s %s < %s (no Grask global limb / reach dominance, SAURIN L526)" % (a, k, g), a, "<", g, k, ("matched 208 cm" if not rep else "reference-normalized (218 vs 188)") + ("; segment share, not a global limb reading" if k in ("forearm_share", "upperarm_share") else ""), rep or k in ("forearm_share", "upperarm_share"))
    # SAU-BODY-14 Gorrund structural mass (joint portion): Broad / Broad + high-muscle Saurin vs GO208
    for a in ("SA-M208-B", "SA-M208-B-MUHI", "SA-M208"):
        for k in ("elbow_sec_share", "wrist_sec_share", "knee_sec_share", "ankle_sec_share"):
            row("SAU-BODY-14", "%s %s < GO208 (substantially lower skeletal mass, SAURIN L529)" % (a, k), a, "<", "GO208", k, "matched 208 cm")
        for t in ("0.0", "0.5", "1.0"):
            row("SAU-BODY-14", "%s femoral S7 breadth / H < GO208 (CIB proxy)" % a, a, "<", "GO208", "b", "", False, t=t)
            row("SAU-BODY-14", "%s femoral S7 depth / H < GO208 (CIB proxy)" % a, a, "<", "GO208", "d", "", False, t=t)
    # SAU-BODY-15 Cogling (no Fine-Scale Elongated Articulation: fine shafts / joints + distal redistribution) - reference-normalized
    for a in ("SA-M188", "SA-F188", "SA-M168", "SA-M208"):
        row("SAU-BODY-15", "%s forearm / arm < CG91 (no Cogling distal redistribution, SAURIN L532)" % a, a, "<", "CG91", "forearm_over_arm", "")
        row("SAU-BODY-15", "%s (forearm + hand) / arm < CG91" % a, a, "<", "CG91", "distal_over_arm", "")
        for k in ("elbow_sec_share", "wrist_sec_share"): row("SAU-BODY-15", "%s %s > CG91 (not fine joints)" % (a, k), a, ">", "CG91", k, "")
        for t in ("0.0", "0.5", "1.0"): row("SAU-BODY-15", "%s femoral S7 breadth / H > CG91 (not fine shafts; CIB proxy)" % a, a, ">", "CG91", "b", "", False, t=t)
    # SAU-BODY-16 Durrim (no compact structural concentration, shortened limb contribution or high joint mass) - reference-normalized
    for a in ("SA-M188", "SA-F188", "SA-M168", "SA-M208"):
        for k in ("leg_share", "leg_joint_share", "arm_share"): row("SAU-BODY-16", "%s %s > DU137C (no shortened limb contribution, SAURIN L523)" % (a, k), a, ">", "DU137C", k, "")
        for k in ("elbow_sec_share", "wrist_sec_share", "knee_sec_share", "ankle_sec_share"): row("SAU-BODY-16", "%s %s < DU137C (no high joint mass)" % (a, k), a, "<", "DU137C", k, "")
        for t in ("0.0", "0.5", "1.0"): row("SAU-BODY-16", "%s femoral S7 breadth / H < DU137C (no compact structural concentration; CIB proxy)" % a, a, "<", "DU137C", "b", "", False, t=t)
    BUD = {}
    for a, mf in (("SA-M168", "MF168"), ("SA-M188", "MF190"), ("SA-M203", "MF203")):
        b = JT[a]['axial']; H = JT[a]['stature']; m = json.load(open(REG[mf]['meas'] + '_meas.json'))['combined']; Hm = m['stature']; cost = m['suprasternal_u'] - m['thoracic_vertical']
        BUD[a + ' vs ' + mf] = {"Saurin": {"ground -> hip (J-2 construction hip)": JT[a]['mean']['hip_height'] / H, "ground -> hip station u91": b['u_hip'] / H,
                                           "hip station -> costal (LT1)": b['lower_trunk_costal_hip'] / H, "costal -> vertex": (H - b['u_costal']) / H},
                                mf: {"ground -> hip (rig)": m['mean']['hip_height'] / Hm, "hip -> costal proxy (LT1)": (cost - m['mean']['hip_height']) / Hm, "costal -> vertex": (Hm - cost) / Hm}}
    json.dump({"values": VAL, "control": ctl, "budget": BUD, "rows": ROWS}, open(OUT, 'w'), indent=1, default=float)
    import collections
    print(collections.Counter((r['code'], r['result']) for r in ROWS))
    for r in ROWS:
        if r['result'] not in ('PASS',) and not r['check'].endswith('REPORT'): print(' ', r['code'], r['check'][:100], r.get('reading'), '%.4f vs %.4f' % (r['va'], r['vb']) if 'va' in r else '', r['result'], '%+.1f' % r['margin_pct'] if 'margin_pct' in r else '')
