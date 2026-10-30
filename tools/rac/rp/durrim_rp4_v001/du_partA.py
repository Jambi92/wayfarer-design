# du_partA.py WORK OUT.json : RP4 order 609c557 Part A (§4 / §5) -- Durrim configuration-2 central reference (DUF137C-NAT) validation.
# Bodies (all native short-adult route, regional factors, no uniform scale): DU137C-NAT (accepted c1 central), DU122C-NAT / DU152C-NAT (accepted c1 bounds),
# DUF137C-NAT (new c2 technical anchor = MF-F-R base macro + the DU137C targets + D1 pelvis), MF137 / MFF137 / MF152 / MFF152 (diagnostic equal-height Marchfolk
# comparators on the same route; not reference assets).
# Readings: skin layer (run_candidate 'combined' ratios; anatomy on rest, shares to the R-6 stature) and skeletal proxy (skeletal_proxy.py, t = 0 / 0.5 / 1.0;
# a skeletal direction counts only if it holds at all three t, as W1f / W2H).
# Checks:
#   1. stature / integrity / determinism (second independent rebuild of DUF137C-NAT from its record = native_short output);
#   2. Durrim direction vs equal-height Marchfolk, per configuration: sign(DU137 - MF137) and sign(DUF137 - MFF137) must both match the canon direction
#      (DU-P2a ... P6, torso / thorax / neck / limbs / joints / hands / feet / head); magnitudes reported side by side;
#   3. no Durrim-specific sex shift: (DUF137 / DU137 - 1) vs (MFF137 / MF137 - 1) per reading (difference reported; |diff| <= 1.5 % = consistent);
#   4. envelope context: DUF137 against the c1 DU122 / DU137 / DU152 values (reported, c1 bounds are a different configuration).
import sys, os, json, hashlib, numpy as np
W, OUT = sys.argv[1:3]
RA = '/home/claude/wayfarer-design/reviews/reference-assets/builds'
def skin(i):
    p = '%s/full/%s_meas.json' % (W, i); return json.load(open(p))['combined']
def skel(i):
    d = json.load(open('%s/skp/%s_skp.json' % (W, i))); return {t: d['by_t'][t]['ratio'] for t in d['by_t']}, d
B = ['DU137C-NAT', 'DUF137C-NAT', 'DU122C-NAT', 'DU152C-NAT', 'MF137-NAT', 'MFF137-NAT', 'MF152-NAT', 'MFF152-NAT']
SK = {b: skin(b) for b in B}; SP = {b: skel(b) for b in B}
def val(b, key, layer):
    if layer == 'skin': return SK[b]['ratio'][key]
    return [SP[b][0][t][key] for t in sorted(SP[b][0])]           # skeletal at every t
# (label, key, layer, canon direction vs equal-height Marchfolk, canon reference)
ROWS = [('torso share', 'torso_share', 'skin', '>', 'DURRIM greater torso contribution (RM-SR-06)'),
        ('thoracic breadth / stature', 'thorax_breadth_share', 'skel', '>', 'broad thorax'),
        ('thoracic depth / stature', 'thorax_depth_share', 'skel', '>', 'deep thorax (RM-SR-06)'),
        ('shoulder-joint breadth / stature', 'shoulder_joint_share', 'skel', '>', 'shoulder relationship'),
        ('neck share', 'neck_share', 'skin', '<', 'short visible neck'),
        ('arm share', 'arm_share', 'skin', '<', 'lower limb contribution'),
        ('leg share = hip-joint height / stature (DU-P2a)', 'leg_share', 'skin', '<', 'DU-P2a'),
        ('hip-joint spacing / stature (DU-P2b)', 'hip_joint_breadth_share', 'skel', '>', 'DU-P2b'),
        ('pelvic vertical / crest (DU-P3)', 'pelvic_vertical_over_crest', 'skel', '<', 'DU-P3 compact vertical'),
        ('AP pelvic depth / stature (DU-P4, D1-corrected)', 'pelvic_depth_share', 'skel', '>', 'DU-P4'),
        ('crest breadth / stature (DU-P5)', 'crest_share', 'skel', '>', 'DU-P5'),
        ('crest / thoracic breadth (DU-P6 thorax-led)', 'pelvis_over_thorax_breadth', 'skel', '<=', 'DU-P6'),
        ('femoral shaft breadth / femur (long bones)', 'shaft_b_over_femur', 'skel', '>', 'substantial long bones'),
        ('wrist / forearm', 'wrist_over_forearm', 'skin', '>', 'substantial joints'),
        ('knee / femur', 'knee_over_femur', 'skin', '>', 'substantial joints'),
        ('ankle / shin', 'ankle_over_shin', 'skin', '>', 'substantial joints'),
        ('elbow / humerus', 'elbow_over_humerus', 'skin', '>', 'substantial joints'),
        ('hand share', 'hand_share', 'skin', '>', 'relatively large hands'),
        ('palm breadth / hand', 'palm_breadth_over_hand', 'skin', '>', 'broad palm'),
        ('foot share', 'foot_share', 'skin', '>', 'relatively large feet'),
        ('head share (HH / stature)', 'HH_share', 'skin', '>', 'allometry only (no oversized head); reported')]
def holds(a, op, b):
    if isinstance(a, list): return all(holds(x, op, y) for x, y in zip(a, b))
    return {'>': a > b, '<': a < b, '<=': a <= b * 1.0005, '>=': a >= b * 0.9995}[op]
def pct(a, b):
    if isinstance(a, list): return [round(100 * (x / y - 1), 2) for x, y in zip(a, b)]
    return round(100 * (a / b - 1), 2)
dirs = []
for lab, k, layer, op, ref in ROWS:
    r = dict(reading=lab, key=k, layer=layer, canon=op, ref=ref)
    for tag, a, b in (('c1_137', 'DU137C-NAT', 'MF137-NAT'), ('c2_137', 'DUF137C-NAT', 'MFF137-NAT'), ('c1_152', 'DU152C-NAT', 'MF152-NAT')):
        va, vb = val(a, k, layer), val(b, k, layer); r[tag + '_vs_MF_pct'] = pct(va, vb); r[tag + '_holds'] = bool(holds(va, op, vb))
    r['report_only'] = k in ('HH_share', 'palm_breadth_over_hand')   # head share: allometry only; palm share: W1 MARGINAL / provisional (DU-NAT ruling)
    r['c2_matches_c1'] = r['c2_137_holds'] == r['c1_137_holds']
    dirs.append(r)
sexd = []
for lab, k, layer, op, ref in ROWS:
    a = val('DUF137C-NAT', k, layer); b = val('DU137C-NAT', k, layer); c = val('MFF137-NAT', k, layer); d = val('MF137-NAT', k, layer)
    du = pct(a, b); mf = pct(c, d)
    diff = [round(x - y, 2) for x, y in zip(du, mf)] if isinstance(du, list) else round(du - mf, 2)
    mx = max(abs(x) for x in diff) if isinstance(diff, list) else abs(diff)
    dm = np.mean(diff) if isinstance(diff, list) else diff
    toward = 'neutral' if mx <= 1.5 else ('more Durrim' if (dm > 0) == (op in ('>', '>=')) else 'less Durrim')
    sexd.append(dict(reading=lab, key=k, durrim_c2_over_c1_pct=du, marchfolk_c2_over_c1_pct=mf, difference_pct=diff, consistent=bool(mx <= 1.5),
                     residual_direction=toward, report_only=(k in ('HH_share', 'palm_breadth_over_hand'))))
env = []
for lab, k, layer, op, ref in ROWS:
    f = lambda b: val(b, k, layer) if layer == 'skin' else val(b, k, layer)[0]
    env.append(dict(reading=lab, key=k, DU122=round(f('DU122C-NAT'), 5), DU137=round(f('DU137C-NAT'), 5), DU152=round(f('DU152C-NAT'), 5), DUF137=round(f('DUF137C-NAT'), 5),
                    DUF137_within_c1_bounds=bool(min(f('DU122C-NAT'), f('DU152C-NAT')) * 0.99 <= f('DUF137C-NAT') <= max(f('DU122C-NAT'), f('DU152C-NAT')) * 1.01)))
st = {b: round(SK[b]['stature'], 3) for b in B}
det = json.load(open(W + '/src/DUF137C-NAT_regen_check.json')) if os.path.exists(W + '/src/DUF137C-NAT_regen_check.json') else None
gate = [r for r in dirs if not r['report_only']]
verdict = 'DURRIM CONFIG-2 CENTRAL REFERENCE PASS — READY FOR RP4' if all(r['c2_137_holds'] for r in gate) and all(r['c2_matches_c1'] for r in gate) else 'DURRIM CONFIG-2 CENTRAL REFERENCE NEEDS AUTHOR DECISION'
res = dict(verdict=verdict, order='reviews/chatgpt-rac-rp4-durrim-compact-branch-pilot-order.md (609c557) Part A',
           c2_build=json.load(open(W + '/nat/DUF137C-NAT_build.json')), stature_cm=st,
           determinism=dict(second_rebuild_geometry_identical=det['geometry_identical'] if det else None, max_abs_dV_cm=det['max_abs_dV_cm'] if det else None),
           directions=dirs, sex_consistency=sexd, envelope_context=env,
           summary=dict(c1_137_directions_hold=sum(r['c1_137_holds'] for r in gate), c2_137_directions_hold=sum(r['c2_137_holds'] for r in gate), compared=len(gate),
                        c2_matches_c1=sum(r['c2_matches_c1'] for r in gate), c1_152_directions_hold=sum(r['c1_152_holds'] for r in gate),
                        c2_failures=[r['reading'] for r in gate if not r['c2_137_holds']], c1_failures=[r['reading'] for r in gate if not r['c1_137_holds']],
                        sex_consistent=sum(r['consistent'] for r in sexd), sex_compared=len(sexd), sex_residual_more_durrim=[r['reading'] for r in sexd if r['residual_direction'] == 'more Durrim'],
                        sex_residual_less_durrim=[r['reading'] for r in sexd if r['residual_direction'] == 'less Durrim'],
                        c2_within_c1_bounds=sum(r['DUF137_within_c1_bounds'] for r in env)),
           comparators='MF137 / MFF137 / MF152 / MFF152: native_short.py on the MF-M-R / MF-F-R cfg (base macro 0.5 / 0.60596), no targets; diagnostic only')
json.dump(res, open(OUT, 'w'), indent=1, default=lambda o: o.item() if hasattr(o, 'item') else str(o))
print(json.dumps(res['summary'], indent=1)); print(res['stature_cm'], res['determinism'])
for r in dirs: print('%-50s c1 %-6s %-28s c2 %-6s %-28s 152 %s' % (r['reading'][:50], r['c1_137_holds'], r['c1_137_vs_MF_pct'], r['c2_137_holds'], r['c2_137_vs_MF_pct'], r['c1_152_holds']))
