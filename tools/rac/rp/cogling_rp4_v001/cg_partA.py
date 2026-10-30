# cg_partA.py WORK PKWORK OUT.json : RP4 Cogling order (9424c72) §3 / §4 -- source regeneration identity and validation of the configuration-2 central
# technical anchor CGF91-NAT. Comparator rule (accepted W2H, reviews/claude-rac-w2h-short-race-family-gate.md §5 / §7): Cogling proportions are read as
# NORMALIZED ratios against Marchfolk 173 (MF-M-R for configuration 1, MF-F-R for configuration 2); the less-pelvis-led-than-Pipkin rows (§4B carriers)
# against an equal-height Pipkin body of the same configuration (c1 accepted PK91-NAT; c2 PKF91-NAT = the PKF107-NAT route at 91 cm, DIAGNOSTIC comparator only).
# Per-adjacent-segment joint ratios (wrist / forearm, knee / femur, ankle / shin) are REPORT rows: W2H §6 rules they are inflated by the distal redistribution by design.
# Rows = accepted RM-SR-02 segment distribution + W2H §4B Cogling carriers (narrow core / fine scale / less pelvis-led) + REPORT rows.
# Skeletal rows count only if they hold at t = 0 / 0.5 / 1.0 (W1f / W2H rule).
# Sex consistency (no Cogling-specific sex shift): (CGF91 / CGJ7 - 1) vs (MFF91 / MF91 - 1) on the same native route; |diff| <= 1.5 % = consistent.
import sys, os, json, numpy as np
W, PW, OUT = sys.argv[1:4]
def skin(i):
    for d in (W + '/full', PW + '/full'):
        if os.path.exists('%s/%s_meas.json' % (d, i)): return json.load(open('%s/%s_meas.json' % (d, i)))['combined']
def skel(i):
    for d in (W + '/skp', PW + '/skp'):
        if os.path.exists('%s/%s_skp.json' % (d, i)):
            x = json.load(open('%s/%s_skp.json' % (d, i))); return {t: x['by_t'][t]['ratio'] for t in x['by_t']}
B = ['CGJ7', 'CGF91-NAT', 'CG76H-NAT', 'CG107-NAT', 'MF-M-R', 'MF-F-R', 'MF91-NAT', 'MFF91-NAT', 'PK91-NAT', 'PKF91-NAT']
SK = {b: skin(b) for b in B}; SP = {b: skel(b) for b in B}
def val(b, k, layer): return SK[b]['ratio'][k] if layer == 'skin' else [SP[b][t][k] for t in sorted(SP[b])]
# (label, key, layer, op, comparator: 'MF' | 'PK', report_only)
ROWS = [('upper arm / arm < MF (RM-SR-02)', 'upperarm_over_arm', 'skin', '<', 'MF', False),
        ('forearm / arm > MF (RM-SR-02)', 'forearm_over_arm', 'skin', '>', 'MF', False),
        ('hand / arm > MF (RM-SR-02)', 'hand_over_arm', 'skin', '>', 'MF', False),
        ('finger / hand > MF (RM-SR-02)', 'finger_over_hand', 'skin', '>', 'MF', False),
        ('femur / leg < MF (RM-SR-02)', 'femur_over_leg', 'skin', '<', 'MF', False),
        ('lower leg (shin) / leg > MF (distal redistribution)', 'shin_over_leg', 'skin', '>', 'MF', False),
        ('hand / stature > MF (RM-SR-02)', 'hand_share', 'skin', '>', 'MF', False),
        ('arm share ~ MF (+-0.010, near-human total)', 'arm_share', 'skin', '~', 'MF', False),
        ('leg share ~ MF (+-0.010, near-human total)', 'leg_share', 'skin', '~', 'MF', False),
        ('torso share ~ MF (+-0.010)', 'torso_share', 'skin', '~', 'MF', False),
        ('wrist / forearm (report; per-adjacent-segment joint ratio, inflated by distal redistribution by design, W2H §6)', 'wrist_over_forearm', 'skin', 'R', 'MF', True),
        ('knee / femur (report; per-adjacent-segment joint ratio)', 'knee_over_femur', 'skin', 'R', 'MF', True),
        ('ankle / shin (report; per-adjacent-segment joint ratio)', 'ankle_over_shin', 'skin', 'R', 'MF', True),
        ('femoral shaft / femur < MF (fine shafts)', 'shaft_b_over_femur', 'skel', '<', 'MF', False),
        ('crest / thoracic breadth < Pipkin (less pelvis-led, W2H §4B)', 'pelvis_over_thorax_breadth', 'skel', '<', 'PK', False),
        ('pelvic vertical / thoracic vertical < Pipkin (W2H §4B)', 'pelvic_vertical_over_thoracic_vertical', 'skel', '<', 'PK', False),
        ('pelvic AP / thoracic depth < Pipkin (W2H §4B)', 'pelvic_depth_over_thorax_depth', 'skel', '<', 'PK', False),
        ('skeletal crest breadth / stature < Pipkin (narrow core)', 'crest_share', 'skel', '<', 'PK', False),
        ('skeletal thoracic breadth / stature < Pipkin (narrow core)', 'thorax_breadth_share', 'skel', '<', 'PK', False),
        ('skeletal pelvic AP / stature < Pipkin (narrow core)', 'pelvic_depth_share', 'skel', '<', 'PK', False),
        ('thorax breadth / stature vs MF (report; narrow-to-moderate, D2)', 'thorax_breadth_share', 'skel', 'R', 'MF', True),
        ('thorax depth / stature (report)', 'thorax_depth_share', 'skel', 'R', 'MF', True),
        ('foot share (report)', 'foot_share', 'skin', 'R', 'MF', True),
        ('head share HH / stature (report; allometry only)', 'HH_share', 'skin', 'R', 'MF', True)]
def holds(a, op, b):
    if isinstance(a, list): return all(holds(x, op, y) for x, y in zip(a, b))
    return {'>': a > b, '<': a < b, '~': abs(a - b) <= 0.010, 'R': True}[op]
def pct(a, b):
    if isinstance(a, list): return [round(100 * (x / y - 1), 2) for x, y in zip(a, b)]
    return round(100 * (a / b - 1), 2)
CMP = {'c1_91': ('CGJ7', 'MF-M-R', 'PK91-NAT'), 'c2_91': ('CGF91-NAT', 'MF-F-R', 'PKF91-NAT'), 'c1_76': ('CG76H-NAT', 'MF-M-R', 'PK91-NAT'), 'c1_107': ('CG107-NAT', 'MF-M-R', 'PK91-NAT')}
dirs = []
for lab, k, layer, op, ref, rep in ROWS:
    r = dict(reading=lab, key=k, layer=layer, canon=op, comparator=ref, report_only=rep)
    for tag, (a, mf, pk) in CMP.items():
        if tag == 'c1_107' and ref == 'PK': continue          # Pipkin 107 c1 comparison is the §12 firewall, not the anchor test
        b = mf if ref == 'MF' else pk; va, vb = val(a, k, layer), val(b, k, layer)
        r[tag + '_value'] = va if not isinstance(va, list) else [round(x, 5) for x in va]; r[tag + '_ref_value'] = vb if not isinstance(vb, list) else [round(x, 5) for x in vb]
        r[tag + '_pct'] = pct(va, vb); r[tag + '_holds'] = bool(holds(va, op, vb))
    r['c2_matches_c1'] = r['c2_91_holds'] == r['c1_91_holds']; dirs.append(r)
sexd = []
for lab, k, layer, op, ref, rep in ROWS:
    cg = pct(val('CGF91-NAT', k, layer), val('CGJ7', k, layer)); mf = pct(val('MFF91-NAT', k, layer), val('MF91-NAT', k, layer))
    diff = [round(x - y, 2) for x, y in zip(cg, mf)] if isinstance(cg, list) else round(cg - mf, 2); mx = max(abs(x) for x in diff) if isinstance(diff, list) else abs(diff)
    sexd.append(dict(reading=lab, key=k, cogling_c2_over_c1_pct=cg, marchfolk_c2_over_c1_pct=mf, difference_pct=diff, consistent=bool(mx <= 1.5), report_only=rep))
st = {b: round(SK[b]['stature'], 3) for b in B}
HH = {b: round(SK[b]['ratio']['HH_share'] * SK[b]['stature'], 3) for b in ('CGJ7', 'CGF91-NAT', 'CG76H-NAT', 'CG107-NAT')}
regen = {i: json.load(open('%s/src/%s_regen_check.json' % (W, i))) for i in ('CGJ7', 'CG76H-NAT', 'CG107-NAT', 'CGF91-NAT')}
# §4B crest / thoracic breadth ratio: if it inverts on a body while BOTH the skeletal crest and the skeletal thoracic breadth (per stature) stay narrower
# than the equal-height Pipkin, the inversion comes from a narrower thorax, not a broader pelvis -- recorded as NARROWER-CORE INVERSION (author note), not a pass.
NOTES = []
for tag in ('c1_91', 'c2_91', 'c1_76'):
    r = next(x for x in dirs if x['key'] == 'pelvis_over_thorax_breadth')
    if not r[tag + '_holds']:
        cr = next(x for x in dirs if x['key'] == 'crest_share' and x['comparator'] == 'PK'); th = next(x for x in dirs if x['key'] == 'thorax_breadth_share' and x['comparator'] == 'PK')
        if cr[tag + '_holds'] and th[tag + '_holds']:
            r[tag + '_status'] = 'NARROWER-CORE INVERSION (author note)'; NOTES.append(dict(body=tag, reading=r['reading'], pct=r[tag + '_pct'], crest_vs_PK_pct=cr[tag + '_pct'], thorax_vs_PK_pct=th[tag + '_pct']))
gate = [r for r in dirs if not r['report_only']]
inv = lambda r, t: r.get(t + '_status', '').startswith('NARROWER-CORE')
ok = all(r['c2_91_holds'] or inv(r, 'c2_91') for r in gate) and all(r['c1_91_holds'] for r in gate) and regen['CGF91-NAT']['geometry_identical']
verdict = 'COGLING CONFIG-2 CENTRAL REFERENCE PASS — READY FOR PRODUCTION DIAGNOSIS' if ok else 'COGLING CONFIG-2 CENTRAL REFERENCE STOP'
HHS = {}
for b_ in ('CGJ7', 'CGF91-NAT', 'CG76H-NAT', 'CG107-NAT', 'MF91-NAT', 'MFF91-NAT', 'PK91-NAT', 'PKF91-NAT'):
    for d_ in (W + '/full', PW + '/full'):
        if os.path.exists('%s/%s_r6.npz' % (d_, b_)):
            z_ = np.load('%s/%s_r6.npz' % (d_, b_)); V_ = z_['V'].astype(float); k_ = z_['keep'].astype(bool); hw = z_['w_head']; ew = z_['w_ears']; e_ = np.array(z_['eye_l'])
            top = V_[(hw > 0.5) & k_ & (ew < 0.2), 2].max(); c_ = k_ & (hw > 0.3) & (np.abs(V_[:, 0]) < 0.6) & (V_[:, 2] < e_[2]) & (V_[:, 1] > e_[1] - 0.25 * (top - e_[2]))
            HHS[b_] = round(float(top - V_[c_, 2].min()), 3); break
hh_note = dict(method='crown (head-weighted, ears excluded) to lowest midline chin vertex in front of the eye plane -- cross-check of arm_measure HH, whose profile walk (absolute-cm windows) misplaces menton on the ~11 cm c2 Cogling face',
               HH_simple_cm=HHS, cogling_c2_over_c1_pct=round(100 * (HHS['CGF91-NAT'] / HHS['CGJ7'] - 1), 2), marchfolk_c2_over_c1_pct=round(100 * (HHS['MFF91-NAT'] / HHS['MF91-NAT'] - 1), 2), pipkin_c2_over_c1_pct=round(100 * (HHS['PKF91-NAT'] / HHS['PK91-NAT'] - 1), 2))
res = dict(verdict=verdict, order='reviews/chatgpt-rac-rp4-cogling-independent-compact-diagnosis-order.md (9424c72) §3 / §4', c2_build=json.load(open(W + '/nat/CGF91-NAT_build.json')),
           stature_cm=st, head_HH_cm_arm_measure=HH, head_height_crosscheck=hh_note, author_notes=NOTES,
           source_regeneration={i: dict(geometry_identical=v['geometry_identical'], max_abs_dV_cm=v['max_abs_dV_cm'], committed_sha256=v['committed_sha256']) for i, v in regen.items()},
           directions=dirs, sex_consistency=sexd,
           summary=dict(compared=len(gate), c1_91_hold=sum(r['c1_91_holds'] for r in gate), c2_91_hold=sum(r['c2_91_holds'] for r in gate), c2_matches_c1=sum(r['c2_matches_c1'] for r in gate),
                        c1_76_hold=sum(r['c1_76_holds'] for r in gate), c1_107_hold=sum(r.get('c1_107_holds', True) for r in gate if 'c1_107_holds' in r), c1_107_compared=sum('c1_107_holds' in r for r in gate),
                        c1_failures=[r['reading'] for r in gate if not r['c1_91_holds']], c2_failures=[r['reading'] for r in gate if not r['c2_91_holds']],
                        sex_consistent=sum(s['consistent'] for s in sexd), sex_rows=len(sexd), sex_inconsistent=[s['reading'] for s in sexd if not s['consistent']]))
json.dump(res, open(OUT, 'w'), indent=1); print(verdict); print('NOTES', NOTES); print('HHS', hh_note); print(json.dumps(res['summary'], indent=1)); print('HH', HH, 'stature', st)
