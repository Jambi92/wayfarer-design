# pk_firewalls.py WORK OUT.json : RP4 Pipkin order (25f7ba0) §9-§13 body firewalls on the accepted Pipkin sources (the production branch only re-samples the
# v005 surface: T-1 / T-2 hold, so source readings are the production readings to within the T-1 tolerance). Readings = run_candidate skin ratios and the
# skeletal proxy (t = 0 / 0.5 / 1.0; a skeletal direction counts only if it holds at all three), the accepted W1 / W2H measurement routes.
#  §10 critical 122 cm boundary  : PK122-NAT vs DU122C-NAT (real matched height) on the accepted W2H §4A carrier directions;
#  §11 adult vs child            : PK107 / PKF107 vs CHILD6 (107 cm, generator age ~6 y) and PK91 vs CHILD3 (91 cm, ~3 y) -- generator human-child proxies,
#                                  DIAGNOSTIC ONLY (never a baseline); 19 body readings, separation = |difference| >= 1 %;
#  §12 Marchfolk normalized      : see pk_partA.py (RM-SR-01 rows vs MF-M-R / MF-F-R); summarized here;
#  §13 Cogling context           : PK91 vs CGJ7 (91 cm) and PK107 vs CG107-NAT (107 cm) on the accepted W2H §4B carriers (Cogling less pelvis-led,
#                                  finer femoral shaft / joints, distal limb redistribution).
import sys, json, numpy as np
W, OUT = sys.argv[1:3]
def skin(i, d='full'): return json.load(open('%s/%s/%s_meas.json' % (W, d, i)))['combined']['ratio']
def skel(i):
    d = json.load(open('%s/skp/%s_skp.json' % (W, i))); return {t: d['by_t'][t]['ratio'] for t in sorted(d['by_t'])}
SKD = {'CHILD6': 'child', 'CHILD3': 'child'}
def absL(i, k): d = json.load(open('%s/%s/%s_meas.json' % (W, SKD.get(i, 'full'), i)))['combined']; return d['L'][k] / d['stature']
def val(i, k, layer):
    if layer == 'abs': return absL(i, k)                                    # W2H 'palm breadth / stature', 'foot breadth / stature' (w2h_eval.py L45)
    return skin(i, SKD.get(i, 'full'))[k] if layer == 'skin' else [v[k] for v in skel(i).values()]
def holds(a, op, b):
    if isinstance(a, list): return all(holds(x, op, y) for x, y in zip(a, b))
    return a > b if op == '>' else a < b
def pct(a, b): return [round(100 * (x / y - 1), 2) for x, y in zip(a, b)] if isinstance(a, list) else round(100 * (a / b - 1), 2)
def table(rows, A, B):
    out = []
    for lab, k, layer, op in rows:
        a, b = val(A, k, layer), val(B, k, layer); out.append(dict(reading=lab, key=k, layer=layer, expected='%s %s %s' % (A, op, B), diff_pct=pct(a, b), holds=bool(holds(a, op, b))))
    return out
# §10: Durrim (A) vs Pipkin (B) at 122 cm, W2H §4A carriers (Durrim side of each relation)
DU_ROWS = [('torso share', 'torso_share', 'skin', '>'), ('thoracic breadth / stature', 'thorax_breadth_share', 'skel', '>'), ('thoracic depth / stature', 'thorax_depth_share', 'skel', '>'),
           ('arm share', 'arm_share', 'skin', '<'), ('leg share', 'leg_share', 'skin', '<'), ('crest / thoracic breadth (Durrim thorax-led)', 'pelvis_over_thorax_breadth', 'skel', '<'),
           ('pelvic vertical / thoracic vertical (Pipkin pelvis-led)', 'pelvic_vertical_over_thoracic_vertical', 'skel', '<'), ('neck share', 'neck_share', 'skin', '<'),
           ('femoral shaft breadth / femur', 'shaft_b_over_femur', 'skel', '>'), ('wrist / forearm', 'wrist_over_forearm', 'skin', '>'), ('knee / femur', 'knee_over_femur', 'skin', '>'),
           ('ankle / shin', 'ankle_over_shin', 'skin', '>'), ('elbow / humerus', 'elbow_over_humerus', 'skin', '>'), ('hand share', 'hand_share', 'skin', '>'),
           ('palm breadth / stature (W2H row)', 'palm_breadth', 'abs', '>'), ('foot breadth / stature (W2H row)', 'foot_breadth', 'abs', '>'),
           ('palm breadth / hand (report)', 'palm_breadth_over_hand', 'skin', '>'), ('foot share (report)', 'foot_share', 'skin', '>')]
du122 = table(DU_ROWS, 'DU122C-NAT', 'PK122-NAT')
for r in du122: r['report_only'] = '(report)' in r['reading']
# §11: adult vs child, 19 readings (separation, no direction scored except head share: adult < child)
CH = [('HH_share', 'skin'), ('torso_share', 'skin'), ('leg_share', 'skin'), ('arm_share', 'skin'), ('neck_share', 'skin'), ('waist_interval_over_torso', 'skin'), ('pelvic_vertical_share', 'skin'),
      ('crest_share', 'skin'), ('thorax_breadth_share', 'skin'), ('thorax_depth_share', 'skin'), ('shoulder_breadth_share', 'skin'), ('wrist_over_forearm', 'skin'), ('knee_over_femur', 'skin'),
      ('ankle_over_shin', 'skin'), ('elbow_over_humerus', 'skin'), ('hand_share', 'skin'), ('foot_share', 'skin'), ('palm_breadth_over_hand', 'skin'), ('pelvis_over_thorax_breadth', 'skel')]
child = {}
for a, c in (('PK-NAT', 'CHILD6'), ('PKF107-NAT', 'CHILD6'), ('PK91-NAT', 'CHILD3')):
    rows = []
    for k, layer in CH:
        x, y = val(a, k, layer), val(c, k, layer); d = pct(x, y); m = min(abs(t) for t in d) if isinstance(d, list) else abs(d); rows.append(dict(key=k, diff_pct=d, separates=bool(m >= 1.0)))
    hh = (val(a, 'HH_share', 'skin'), val(c, 'HH_share', 'skin'))
    child['%s_vs_%s' % (a, c)] = dict(separating=sum(r['separates'] for r in rows), of=len(rows), head_share_adult=round(hh[0], 4), head_share_child=round(hh[1], 4),
                                       head_share_adult_below_child=bool(hh[0] < hh[1]), rows=rows)
# §13: Pipkin (A) vs Cogling (B), W2H §4B carriers (Pipkin side)
CG_ROWS = [('crest / thoracic breadth (Pipkin more pelvis-led)', 'pelvis_over_thorax_breadth', 'skel', '>'), ('pelvic vertical / thoracic vertical', 'pelvic_vertical_over_thoracic_vertical', 'skel', '>'),
           ('pelvic AP / thoracic depth', 'pelvic_depth_over_thorax_depth', 'skel', '>'), ('femoral shaft breadth / femur (Cogling finer)', 'shaft_b_over_femur', 'skel', '>'),
           ('wrist / forearm', 'wrist_over_forearm', 'skin', '>'), ('knee / femur', 'knee_over_femur', 'skin', '>'), ('ankle / shin', 'ankle_over_shin', 'skin', '>'),
           ('upper arm / arm (Cogling distal)', 'upperarm_over_arm', 'skin', '>'), ('forearm / arm (Cogling distal)', 'forearm_over_arm', 'skin', '<'),
           ('hand / arm (Cogling distal)', 'hand_over_arm', 'skin', '<'), ('femur / leg (Cogling distal)', 'femur_over_leg', 'skin', '>')]
cg = {'PK91_vs_CGJ7_91': table(CG_ROWS, 'PK91-NAT', 'CGJ7'), 'PK107_vs_CG107': table(CG_ROWS, 'PK-NAT', 'CG107-NAT')}
pa = json.load(open(W + '/rec/PK_partA.json'))['summary']
res = dict(order='reviews/chatgpt-rac-rp4-pipkin-independent-compact-diagnosis-order.md (25f7ba0) §9-§13', note='source readings; production branch preserves the source surface (T-1)',
           pipkin_vs_durrim_122=dict(rows=du122, hold=sum(r['holds'] for r in du122 if not r['report_only']), of=sum(1 for r in du122 if not r['report_only'])),
           adult_vs_child=child, marchfolk_normalized=dict(c1_107=pa['c1_107_hold'], c2_107=pa['c2_107_hold'], c1_91=pa['c1_91_hold'], c1_122=pa['c1_122_hold'], of=pa['compared'], see='PK_partA.json'),
           cogling_context={k: dict(rows=v, hold=sum(r['holds'] for r in v), of=len(v)) for k, v in cg.items()},
           broad_pipkin_vs_narrow_durrim='not rebuilt: the W2H frame bodies (PKB122 / DUN122) are not committed reference assets; accepted W2H result PIP-BODY-14 16 / 16 + 2 REPORT stands (order §10: do not invent frame biology)')
json.dump(res, open(OUT, 'w'), indent=1)
print('PK122 vs DU122: %d / %d scored' % (res['pipkin_vs_durrim_122']['hold'], res['pipkin_vs_durrim_122']['of']))
for r in du122: print('   %-55s %-6s %s' % (r['reading'], r['holds'], r['diff_pct']))
for k, v in child.items(): print(k, 'separating %d / %d' % (v['separating'], v['of']), 'head share %s vs %s' % (v['head_share_adult'], v['head_share_child']))
for k, v in res['cogling_context'].items():
    print(k, '%d / %d' % (v['hold'], v['of']))
    for r in v['rows']: print('   %-50s %-6s %s' % (r['reading'], r['holds'], r['diff_pct']))
