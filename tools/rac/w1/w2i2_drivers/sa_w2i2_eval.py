# RAC W2I2 candidate evaluation (order §6, §7, §9, §10): limb / budget criteria and limb-dependent cross-race rows for one candidate body set
# (sa_w2i2_build.py output) against the as-built set (AS) and the accepted comparators. The non-limb W2I rows (lower-trunk floor, matched-height
# directions, passing, never-Gorrund) come from the accepted sa_compare.py run on the same candidate set (COMPARE json, unchanged script).
# Comparator limb readings: W2I1 evidence (rac-w2i-sa-evidence/closure/limbcmp.json: MF168-203, GR208 / GR218, GO208, CG91, DU137C) and the
# elf / Sagekin / Halvren / Skarn meas json (leg share, leg length, arm, forearm share). Classes AD-G10 (1 % margin); no new hard gap invented.
# Usage: python3 sa_w2i2_eval.py CAND_BODIES.json AS_BODIES.json COMPARE.json OUT.json
import sys, json
R = '/home/claude/wayfarer-design/reviews'
CB, AB, CMP, OUT = [json.load(open(f)) for f in sys.argv[1:4]] + [sys.argv[4]]
LC = json.load(open(R + '/rac-w2i-sa-evidence/closure/limbcmp.json'))['values']
REG = {}
for f in ('rac-w2e-sg-evidence/registry.json', 'rac-w2g-hv-evidence/registry.json', 'rac-w2f-elf-evidence/registry.json', 'rac-w2d-go-evidence/registry.json'): REG.update(json.load(open(R + '/' + f)))
def mp(key):
    if key in LC: return LC[key]
    m = json.load(open(REG[key]['meas'] + '_meas.json'))['combined']; r = m['ratio']; mm = m['mean']; H = m['stature']
    return dict(stature=H, leg_share=r['leg_share'], leg_joint_share=mm['leg_joint'] / H, arm_share=r['arm_share'], forearm_over_arm=r['forearm_over_arm'], span_der=r['span_der'],
                distal_over_arm=r['forearm_over_arm'] + r['hand_over_arm'], femur_over_leg=r['femur_over_leg'])
def sa(B, bid):
    M = B[bid]; r = M['limb']['ratio']; lg = M['ledger']['share']
    return dict(stature=M['height'], leg_share=r['leg_share'], B1_hip_share=M['ledger']['B1_axis_hip_share'], leg_joint_share=r['leg_joint_share'], femur_over_leg=r['femur_over_leg'],
                shin_over_leg=r['shin_over_leg'], arm_share=r['arm_share'], span_der=r['span_der'], upperarm_share=r['upperarm_share'], forearm_share=r['forearm_share'],
                arm_to_wrist_share=r['upperarm_share'] + r['forearm_share'], hand_share=r['hand_share'], forearm_over_arm=r['forearm_over_arm'], forearm_over_upperarm=r['forearm_over_upperarm'],
                hand_over_arm=r['hand_over_arm'], distal_over_arm=r['forearm_over_arm'] + r['hand_over_arm'], elbow_u=0.5 * (M['limb']['joints']['EL'][2] + M['limb']['joints']['ER'][2]),
                elbow_sec_share=r['elbow_share'], wrist_sec_share=r['wrist_share'], LT_share=M['lower_trunk_costal_hip_over_H'], TV_share=M['thoracic_vertical_over_H'],
                neck_share=lg['neck'], head_height_share=lg['head_height'], head_len=M['head_len'], dw=M['thorax_d_over_w'], tail_len_pct=M['tail_len_pct'], tail_root_area=M['tail_root_area'],
                tail_RSI_raw=M['tail_RSI_raw'], platform_minus_hip=M['u_platform'] - M['u_hip'], lean=M['lean_scaled_deg'], shoulder_joint_share=r['shoulder_joint_share'], height=M['height'])
ROWS = []
def cls(op, va, vb):
    rel = abs(va - vb) / abs(vb) if vb else 1.0; holds = {">": va > vb, "<": va < vb}[op]
    return ("PASS" if rel >= 0.01 else "NOT DEMONSTRATED") if holds else "FAIL"
def row(code, chk, a, va, op, b, vb, note="", report=False):
    ROWS.append(dict(code=code, check=chk + (" — REPORT" if report else ""), a=a, va=va, op=op, b=b, vb=vb, margin_pct=100 * (va / vb - 1) if vb else None, result="REPORT" if report else cls(op, va, vb), note=note))
MATCH = {168: "MF168", 173: "MF173", 178: "MF178", 181: "MF181", 190: "MF190", 203: "MF203"}
ELF = {168: ["AE168"], 173: ["FN173", "AE173", "VA173"], 178: ["FN178", "AE178", "VA178"], 181: ["FN181", "AE181", "VA181"], 190: ["FN190", "AE190", "VA190"], 203: ["FN203", "AE203", "VA203"]}
if __name__ == '__main__':
    V = {}
    for bid in CB: V[bid] = sa(CB, bid)
    VA = {bid: sa(AB, bid) for bid in AB}
    # budget / invariance vs as-built (same body ids)
    for bid in ("SA-M168", "SA-M188", "SA-M203", "SA-M208", "SA-F188"):
        for k in ("leg_share", "B1_hip_share", "leg_joint_share", "femur_over_leg", "shin_over_leg", "LT_share", "TV_share", "neck_share", "head_height_share", "height", "head_len", "dw",
                  "tail_len_pct", "tail_root_area", "tail_RSI_raw", "platform_minus_hip", "arm_share", "forearm_over_arm", "upperarm_share", "forearm_share", "arm_to_wrist_share", "hand_over_arm",
                  "forearm_over_upperarm", "elbow_u", "elbow_sec_share", "wrist_sec_share", "span_der", "lean"):
            ROWS.append(dict(code="BUD", check="%s %s candidate vs as-built" % (bid, k), a=bid, va=V[bid][k], op="vs", b="as-built", vb=VA[bid][k],
                             margin_pct=100 * (V[bid][k] / VA[bid][k] - 1) if VA[bid][k] else None, result="REPORT"))
    for h, mf in MATCH.items():
        for sx in ("M", "F"):
            a = "SA-%s%d" % (sx, h)
            # §6 legs: not Durrim-like; approach lower Marchfolk; below Grask; not elf distributed elongation
            row("L-DU", "%s hip height / H > Durrim DU137C (no shortened-limb identity, SAURIN L523)" % a, a, V[a]['leg_share'], ">", "DU137C", mp("DU137C")['leg_share'])
            row("L-DU", "%s leg length / H > Durrim DU137C" % a, a, V[a]['leg_joint_share'], ">", "DU137C", mp("DU137C")['leg_joint_share'])
            row("L-MF", "%s hip height / H vs matched %s (approach lower Marchfolk tendency)" % (a, mf), a, V[a]['leg_share'], ">", mf, mp(mf)['leg_share'], "", True)
            row("L-MF", "%s leg length / H vs matched %s" % (a, mf), a, V[a]['leg_joint_share'], ">", mf, mp(mf)['leg_joint_share'], "", True)
            for e in ELF[h]:
                if e in REG: row("L-ELF", "%s hip height / H vs matched %s (single reading; elf identity is distributed elongation of the complete body, W2E rule)" % (a, e), a, V[a]['leg_share'], "<", e, mp(e)['leg_share'], "complete-anatomy separation: sa_compare P / P0 rows", True)
            # §9 forearm: no longer strongly below Marchfolk; below Cogling / Grask; total arm moderate
            row("F-MF", "%s forearm / arm vs matched %s ('modest forearm emphasis')" % (a, mf), a, V[a]['forearm_over_arm'], ">", mf, mp(mf)['forearm_over_arm'], "", True)
            row("F-MF", "%s total arm / H vs matched %s ('moderate total arm')" % (a, mf), a, V[a]['arm_share'], ">", mf, mp(mf)['arm_share'], "", True)
    for a in ("SA-M188", "SA-F188", "SA-M168", "SA-M208"):
        row("F-CG", "%s forearm / arm < CG91 (no Cogling distal redistribution, SAURIN L532)" % a, a, V[a]['forearm_over_arm'], "<", "CG91", mp("CG91")['forearm_over_arm'])
        row("F-CG", "%s (forearm + hand) / arm < CG91" % a, a, V[a]['distal_over_arm'], "<", "CG91", mp("CG91")['distal_over_arm'])
        row("SAU-BODY-16", "%s arm / H > DU137C" % a, a, V[a]['arm_share'], ">", "DU137C", mp("DU137C")['arm_share'], "near-equal in W2I1; report", True)
    for a, g in (("SA-M208", "GR208"), ("SA-F208", "GR208"), ("SA-M208-B", "GR208"), ("SA-M188", "GR218")):
        rep = g == "GR218"
        for k in ("leg_share", "leg_joint_share", "arm_share", "span_der", "forearm_over_arm"):
            row("SAU-BODY-13", "%s %s < %s (no Grask reach specialization, SAURIN L526)" % (a, k, g), a, V[a][k], "<", g, mp(g)[k], "matched 208" if not rep else "reference-normalized", rep)
    cmpc = {}
    for c in CMP['checks']: cmpc.setdefault(c['code'], {}).setdefault(c['result'], 0); cmpc[c['code']][c['result']] += 1
    fails = [dict(code=c['code'], check=c['check'], result=c['result'], va=c.get('va'), vb=c.get('vb'), margin_pct=c.get('margin_pct')) for c in CMP['checks'] if c['result'] not in ('PASS', 'REPORT')]
    import collections
    cnt = collections.Counter((r['code'], r['result']) for r in ROWS)
    json.dump({"values": V, "rows": ROWS, "compare_counts": cmpc, "compare_nonpass": fails, "counts": {"%s|%s" % k: n for k, n in cnt.items()}}, open(OUT, 'w'), indent=1, default=float)
    print(dict(cnt)); print('compare', cmpc); print('compare non-pass', len(fails))
    for f in fails[:20]: print('  ', f['code'], f['check'][:100], f['result'], f.get('margin_pct'))
    for r in ROWS:
        if r['result'] in ('FAIL', 'NOT DEMONSTRATED'): print(' x', r['code'], r['check'][:100], '%.4f vs %.4f' % (r['va'], r['vb']), r['result'], '%+.2f' % r['margin_pct'])
