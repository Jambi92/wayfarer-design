# cg_firewalls.py WORK PKWORK OUT.json : RP4 Cogling order (9424c72) §11-§16 body firewalls on the accepted Cogling sources and the c2 anchor (the production
# branch only re-samples the v005 surface: T-1 / T-2 hold, so source readings are the production readings to within the T-1 tolerance). Readings = run_candidate
# skin ratios and the skeletal proxy (t = 0 / 0.5 / 1.0; a skeletal direction counts only if it holds at all three) -- the accepted W1 / W2H measurement routes.
#  §12 Pipkin overlap (equal real height): CGJ7 vs PK91-NAT (91), CG107-NAT vs PK-NAT (107), c2: CGF91-NAT vs PKF91-NAT (DIAGNOSTIC Pipkin c2 at 91, PKF107 route);
#      W2H §4B carriers (Cogling side) + narrow-core breadths.
#  §13 Durrim context (REAL height, not equal height): CG107-NAT (Cogling max) vs DU122C-NAT (Durrim min): stature gap + structural concentration rows.
#  §14 adult vs child: CG76H-NAT vs CHILD1 (76 cm, ~1.5 y toddler, COG-BODY-11), CGJ7 / CGF91-NAT vs CHILD3 (91 cm, ~3 y) -- generator human-child proxies,
#      DIAGNOSTIC ONLY; the same 19 body readings as the Pipkin gate (separation = |difference| >= 1 %) + head share adult < child.
#  §15 Marchfolk normalized: from cg_partA.py (CG_partA.json); summarized here.
#  §16 hidden identity: the §12 / §15 readings re-counted with hand / finger rows removed (hands hidden) and with head, hand and foot rows removed
#      (head + hands + feet hidden) -- the central body and limb organization alone must still separate Cogling from Pipkin and normalized Marchfolk.
import sys, os, json, numpy as np
W, PW, OUT = sys.argv[1:4]
def _p(i, kind):
    for d in ([W + '/child', PW + '/child'] if i.startswith('CHILD') else [W + '/full', PW + '/full']) if kind == 'meas' else [W + '/skp', PW + '/skp']:
        p = '%s/%s_%s.json' % (d, i, 'meas' if kind == 'meas' else 'skp')
        if os.path.exists(p): return p
    raise FileNotFoundError(i + kind)
def skin(i): return json.load(open(_p(i, 'meas')))['combined']['ratio']
def skel(i): d = json.load(open(_p(i, 'skp'))); return {t: d['by_t'][t]['ratio'] for t in sorted(d['by_t'])}
def absL(i, k): d = json.load(open(_p(i, 'meas')))['combined']; return d['L'][k] / d['stature']
def stature(i): return json.load(open(_p(i, 'meas')))['combined']['stature']
def val(i, k, layer):
    if layer == 'abs': return absL(i, k)
    return skin(i)[k] if layer == 'skin' else [v[k] for v in skel(i).values()]
def holds(a, op, b):
    if isinstance(a, list): return all(holds(x, op, y) for x, y in zip(a, b))
    return a > b if op == '>' else a < b
def pct(a, b): return [round(100 * (x / y - 1), 2) for x, y in zip(a, b)] if isinstance(a, list) else round(100 * (a / b - 1), 2)
def table(rows, A, B):
    out = []
    for lab, k, layer, op, region in rows:
        a, b = val(A, k, layer), val(B, k, layer); out.append(dict(reading=lab, key=k, layer=layer, region=region, expected='%s %s %s' % (A, op, B), diff_pct=pct(a, b), holds=bool(holds(a, op, b))))
    return out
# region tags: core / limb / hand / foot / head
PK_ROWS = [('crest / thoracic breadth (Cogling less pelvis-led)', 'pelvis_over_thorax_breadth', 'skel', '<', 'core'),
           ('pelvic vertical / thoracic vertical (Cogling less pelvis-led)', 'pelvic_vertical_over_thoracic_vertical', 'skel', '<', 'core'),
           ('pelvic AP / thoracic depth (Cogling less pelvis-led)', 'pelvic_depth_over_thorax_depth', 'skel', '<', 'core'),
           ('skeletal crest breadth / stature (narrow core)', 'crest_share', 'skel', '<', 'core'),
           ('skeletal thoracic breadth / stature (narrow core)', 'thorax_breadth_share', 'skel', '<', 'core'),
           ('skeletal pelvic AP / stature (narrow core)', 'pelvic_depth_share', 'skel', '<', 'core'),
           ('femoral shaft breadth / femur (Cogling finer)', 'shaft_b_over_femur', 'skel', '<', 'limb'),
           ('upper arm / arm (Cogling distal)', 'upperarm_over_arm', 'skin', '<', 'limb'), ('forearm / arm (Cogling distal)', 'forearm_over_arm', 'skin', '>', 'limb'),
           ('femur / leg (Cogling distal)', 'femur_over_leg', 'skin', '<', 'limb'), ('lower leg / leg (Cogling distal)', 'shin_over_leg', 'skin', '>', 'limb'),
           ('hand / arm (Cogling distal)', 'hand_over_arm', 'skin', '>', 'hand'), ('finger / hand (Cogling long fingers)', 'finger_over_hand', 'skin', '>', 'hand'),
           ('hand / stature', 'hand_share', 'skin', '>', 'hand')]
pk = {'91_c1_CGJ7_vs_PK91': table(PK_ROWS, 'CGJ7', 'PK91-NAT'), '107_c1_CG107_vs_PK107': table(PK_ROWS, 'CG107-NAT', 'PK-NAT'),
      '91_c2_CGF91_vs_PKF91_diagnostic': table(PK_ROWS, 'CGF91-NAT', 'PKF91-NAT')}
# §13 Durrim context at REAL height (Durrim side of each relation; W2H §4A-type structural-concentration carriers)
DU_ROWS = [('thoracic breadth / stature (Durrim broad)', 'thorax_breadth_share', 'skel', '>', 'core'), ('thoracic depth / stature (Durrim deep)', 'thorax_depth_share', 'skel', '>', 'core'),
           ('torso share (Durrim larger)', 'torso_share', 'skin', '>', 'core'), ('femoral shaft / femur (Durrim heavier)', 'shaft_b_over_femur', 'skel', '>', 'limb'),
           ('knee / femur (Durrim heavier joint)', 'knee_over_femur', 'skin', '>', 'limb'), ('elbow / humerus (Durrim heavier joint)', 'elbow_over_humerus', 'skin', '>', 'limb'),
           ('arm share (Durrim shorter)', 'arm_share', 'skin', '<', 'limb'), ('leg share (Durrim shorter)', 'leg_share', 'skin', '<', 'limb'),
           ('forearm / arm (Cogling distal)', 'forearm_over_arm', 'skin', '<', 'limb'), ('finger / hand (Cogling long fingers)', 'finger_over_hand', 'skin', '<', 'hand'),
           ('palm breadth / stature (Durrim broad palm)', 'palm_breadth', 'abs', '>', 'hand')]
du = table(DU_ROWS, 'DU122C-NAT', 'CG107-NAT')
du_ctx = dict(rows=du, hold=sum(r['holds'] for r in du), of=len(du), stature_cm=dict(CG107=round(stature('CG107-NAT'), 2), DU122C=round(stature('DU122C-NAT'), 2)),
              stature_gap_cm=round(stature('DU122C-NAT') - stature('CG107-NAT'), 2), note='REAL-height context (Cogling maximum vs Durrim minimum), not an equal-height test; ratios are per-stature, NOT normalized displays')
# §14 adult vs child
CH = [('HH_share', 'skin'), ('torso_share', 'skin'), ('leg_share', 'skin'), ('arm_share', 'skin'), ('neck_share', 'skin'), ('waist_interval_over_torso', 'skin'), ('pelvic_vertical_share', 'skin'),
      ('crest_share', 'skin'), ('thorax_breadth_share', 'skin'), ('thorax_depth_share', 'skin'), ('shoulder_breadth_share', 'skin'), ('wrist_over_forearm', 'skin'), ('knee_over_femur', 'skin'),
      ('ankle_over_shin', 'skin'), ('elbow_over_humerus', 'skin'), ('hand_share', 'skin'), ('foot_share', 'skin'), ('palm_breadth_over_hand', 'skin'), ('pelvis_over_thorax_breadth', 'skel')]
def hh_simple(i):
    for d in ([W + '/child', PW + '/child'] if i.startswith('CHILD') else [W + '/full', PW + '/full']):
        p = '%s/%s_r6.npz' % (d, i)
        if os.path.exists(p):
            z = np.load(p); V = z['V'].astype(float); k = z['keep'].astype(bool); hw = z['w_head']; ew = z['w_ears']; e = np.array(z['eye_l'])
            top = V[(hw > 0.5) & k & (ew < 0.2), 2].max(); c = k & (hw > 0.3) & (np.abs(V[:, 0]) < 0.6) & (V[:, 2] < e[2]) & (V[:, 1] > e[1] - 0.25 * (top - e[2]))
            return float(top - V[c, 2].min()), float(V[k, 2].max() - V[k, 2].min())
child = {}
for a, c in (('CG76H-NAT', 'CHILD1'), ('CGJ7', 'CHILD3'), ('CGF91-NAT', 'CHILD3')):
    rows = []
    for k, layer in CH:
        x, y = val(a, k, layer), val(c, k, layer); d = pct(x, y); m = min(abs(t) for t in d) if isinstance(d, list) else abs(d); rows.append(dict(key=k, diff_pct=d, separates=bool(m >= 1.0)))
    ha, sa = hh_simple(a); hc, sc = hh_simple(c)
    child['%s_vs_%s' % (a, c)] = dict(separating=sum(r['separates'] for r in rows), of=len(rows), head_height_cm=dict(adult=round(ha, 2), child=round(hc, 2)),
                                       head_share_adult=round(ha / sa, 4), head_share_child=round(hc / sc, 4), head_share_adult_below_child=bool(ha / sa < hc / sc),
                                       child_stature_cm=round(sc, 2), rows=rows)
# §15 + §16
pa = json.load(open(W + '/CG_partA.json'))
mf_rows = [r for r in pa['directions'] if not r['report_only'] and r['comparator'] == 'MF']
REG = {'upperarm_over_arm': 'limb', 'forearm_over_arm': 'limb', 'hand_over_arm': 'hand', 'finger_over_hand': 'hand', 'femur_over_leg': 'limb', 'shin_over_leg': 'limb', 'hand_share': 'hand',
       'arm_share': 'limb', 'leg_share': 'limb', 'torso_share': 'core', 'shaft_b_over_femur': 'limb'}
mf = {t: dict(hold=sum(r[t + '_holds'] for r in mf_rows), of=len(mf_rows)) for t in ('c1_91', 'c2_91', 'c1_76', 'c1_107')}
# §16: separation counts (a direction that holds = separates) by hidden set; 'near-human total' rows (~) are sameness rows, not separators -> excluded from MF counts
SEP_MF = [r for r in mf_rows if r['canon'] != '~']
def hidden(rows_pk, rows_mf, drop):
    p = [r for r in rows_pk if r['region'] not in drop]; m = [r for r in rows_mf if REG[r['key']] not in drop]
    return p, m
hid = {}
for nm, drop in (('hands_hidden', {'hand'}), ('head_hands_feet_hidden', {'hand', 'head', 'foot'})):
    e = {}
    for tag, key in (('91_c1', '91_c1_CGJ7_vs_PK91'), ('107_c1', '107_c1_CG107_vs_PK107'), ('91_c2', '91_c2_CGF91_vs_PKF91_diagnostic')):
        p, m = hidden(pk[key], SEP_MF, drop); mt = {'91_c1': 'c1_91', '107_c1': 'c1_107', '91_c2': 'c2_91'}[tag]
        e[tag] = dict(vs_pipkin='%d / %d' % (sum(r['holds'] for r in p), len(p)), vs_pipkin_failing=[r['reading'] for r in p if not r['holds']],
                      vs_marchfolk_normalized='%d / %d' % (sum(r[mt + '_holds'] for r in m), len(m)), readings_used=sorted({r['region'] for r in p}))
    hid[nm] = e
res = dict(order='reviews/chatgpt-rac-rp4-cogling-independent-compact-diagnosis-order.md (9424c72) §11-§16', note='source readings; the production branch preserves the source surface (T-1)',
           pipkin_overlap={k: dict(rows=v, hold=sum(r['holds'] for r in v), of=len(v)) for k, v in pk.items()}, durrim_context=du_ctx, adult_vs_child=child,
           marchfolk_normalized=dict(counts=mf, see='CG_partA.json'), hidden_identity=hid)
json.dump(res, open(OUT, 'w'), indent=1)
for k, v in res['pipkin_overlap'].items():
    print(k, '%d / %d' % (v['hold'], v['of']))
    for r in v['rows']: print('   %-58s %-6s %s' % (r['reading'], r['holds'], r['diff_pct']))
print('Durrim context %d / %d' % (du_ctx['hold'], du_ctx['of']), du_ctx['stature_cm'])
for r in du: print('   %-58s %-6s %s' % (r['reading'], r['holds'], r['diff_pct']))
for k, v in child.items(): print(k, 'separating %d / %d' % (v['separating'], v['of']), 'HH', v['head_height_cm'], 'share %s vs %s' % (v['head_share_adult'], v['head_share_child']))
print('MF', mf); print(json.dumps(hid, indent=1))
