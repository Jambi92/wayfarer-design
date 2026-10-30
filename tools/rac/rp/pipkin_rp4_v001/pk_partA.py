# pk_partA.py WORK OUT.json : RP4 Pipkin order (25f7ba0) §4 -- validation of the configuration-2 central technical anchor PKF107-NAT.
# Comparator rule (accepted W2H, reviews/claude-rac-w2h-short-race-family-gate.md §5): Pipkin proportions are read as NORMALIZED ratios against
# Marchfolk 173 (MF-M-R for configuration 1, MF-F-R for configuration 2) -- never a same-height human (none is a valid adult at 91-122 cm).
# Rows = the accepted RM-SR-01 Pipkin trunk / pelvis relations (PK-P2a / P3 / P4 / P5, PV-D15, T-2) + REPORT rows (limbs, joints, hands, feet, head).
# Skeletal rows count only if they hold at t = 0 / 0.5 / 1.0 (W1f / W2H rule).
# Sex consistency (no Pipkin-specific sex shift): (PKF107 / PK107 - 1) vs (MFF107 / MF107 - 1) on the same native route; |diff| <= 1.5 % = consistent.
# Envelope: PKF107 against the accepted c1 PK91 / PK122 values (context only; different configuration).
import sys, os, json, numpy as np
W, OUT = sys.argv[1:3]
def skin(i): return json.load(open('%s/full/%s_meas.json' % (W, i)))['combined']
def skel(i):
    d = json.load(open('%s/skp/%s_skp.json' % (W, i))); return {t: d['by_t'][t]['ratio'] for t in d['by_t']}
B = ['PK-NAT', 'PKF107-NAT', 'PK91-NAT', 'PK122-NAT', 'MF-M-R', 'MF-F-R', 'MF107-NAT', 'MFF107-NAT']
SK = {b: skin(b) for b in B}; SP = {b: skel(b) for b in B}
def val(b, k, layer): return SK[b]['ratio'][k] if layer == 'skin' else [SP[b][t][k] for t in sorted(SP[b])]
ROWS = [('central trunk (torso) share < MF (T-2)', 'torso_share', 'skin', '<', False),
        ('skeletal pelvic vertical / stature >= MF (PK-P3, PV-D10)', 'pelvic_vertical_share', 'skel', '>=', False),
        ('pelvic vertical / thoracic vertical > MF (PK-P3)', 'pelvic_vertical_over_thoracic_vertical', 'skel', '>', False),
        ('crest / thoracic breadth > MF (PK-P5)', 'pelvis_over_thorax_breadth', 'skel', '>', False),
        ('pelvic AP / thoracic depth > MF (PK-P4)', 'pelvic_depth_over_thorax_depth', 'skel', '>', False),
        ('waist interval / torso < MF (PV-D15)', 'waist_interval_over_torso', 'skin', '<', False),
        ('leg share <= MF (PK-P2a; 122 cm MARGINAL accepted AD-G10)', 'leg_share', 'skin', '<=', False),
        ('arm share (report)', 'arm_share', 'skin', 'R', True), ('thorax breadth / stature (report)', 'thorax_breadth_share', 'skel', 'R', True),
        ('thorax depth / stature (report)', 'thorax_depth_share', 'skel', 'R', True), ('femoral shaft / femur (report)', 'shaft_b_over_femur', 'skel', 'R', True),
        ('wrist / forearm (report)', 'wrist_over_forearm', 'skin', 'R', True), ('knee / femur (report)', 'knee_over_femur', 'skin', 'R', True),
        ('ankle / shin (report)', 'ankle_over_shin', 'skin', 'R', True), ('hand share (report)', 'hand_share', 'skin', 'R', True),
        ('foot share (report)', 'foot_share', 'skin', 'R', True), ('head share HH / stature (report; allometry only)', 'HH_share', 'skin', 'R', True)]
def holds(a, op, b):
    if isinstance(a, list): return all(holds(x, op, y) for x, y in zip(a, b))
    return {'>': a > b, '<': a < b, '<=': a <= b * 1.0005, '>=': a >= b * 0.9995, 'R': True}[op]
def pct(a, b):
    if isinstance(a, list): return [round(100 * (x / y - 1), 2) for x, y in zip(a, b)]
    return round(100 * (a / b - 1), 2)
dirs = []
for lab, k, layer, op, rep in ROWS:
    r = dict(reading=lab, key=k, layer=layer, canon=op, report_only=rep)
    for tag, a, b in (('c1_107', 'PK-NAT', 'MF-M-R'), ('c2_107', 'PKF107-NAT', 'MF-F-R'), ('c1_91', 'PK91-NAT', 'MF-M-R'), ('c1_122', 'PK122-NAT', 'MF-M-R')):
        va, vb = val(a, k, layer), val(b, k, layer); r[tag + '_vs_MF_pct'] = pct(va, vb); r[tag + '_holds'] = bool(holds(va, op, vb))
    r['c2_matches_c1'] = r['c2_107_holds'] == r['c1_107_holds']; dirs.append(r)
sexd = []
for lab, k, layer, op, rep in ROWS:
    pk = pct(val('PKF107-NAT', k, layer), val('PK-NAT', k, layer)); mf = pct(val('MFF107-NAT', k, layer), val('MF107-NAT', k, layer))
    diff = [round(x - y, 2) for x, y in zip(pk, mf)] if isinstance(pk, list) else round(pk - mf, 2); mx = max(abs(x) for x in diff) if isinstance(diff, list) else abs(diff)
    sexd.append(dict(reading=lab, key=k, pipkin_c2_over_c1_pct=pk, marchfolk_c2_over_c1_pct=mf, difference_pct=diff, consistent=bool(mx <= 1.5), report_only=rep))
env = []
for lab, k, layer, op, rep in ROWS:
    f = lambda b: val(b, k, layer) if layer == 'skin' else val(b, k, layer)[0]
    lo, hi = min(f('PK91-NAT'), f('PK122-NAT')), max(f('PK91-NAT'), f('PK122-NAT'))
    env.append(dict(reading=lab, PK91=round(f('PK91-NAT'), 5), PK107=round(f('PK-NAT'), 5), PK122=round(f('PK122-NAT'), 5), PKF107=round(f('PKF107-NAT'), 5),
                    PKF107_within_c1_bounds=bool(lo * 0.99 <= f('PKF107-NAT') <= hi * 1.01)))
st = {b: round(SK[b]['stature'], 3) for b in B}
det = json.load(open(W + '/src/PKF107-NAT_regen_check.json'))
gate = [r for r in dirs if not r['report_only']]
ok = all(r['c2_107_holds'] for r in gate) and all(r['c2_matches_c1'] for r in gate)
verdict = 'PIPKIN CONFIG-2 CENTRAL REFERENCE PASS — READY FOR PRODUCTION DIAGNOSIS' if ok else 'PIPKIN CONFIG-2 CENTRAL REFERENCE REQUIRES AUTHOR DECISION'
res = dict(verdict=verdict, order='reviews/chatgpt-rac-rp4-pipkin-independent-compact-diagnosis-order.md (25f7ba0) §4', c2_build=json.load(open(W + '/nat/PKF107-NAT_build.json')), stature_cm=st,
           determinism=dict(second_rebuild_geometry_identical=det['geometry_identical'], max_abs_dV_cm=det['max_abs_dV_cm']), directions=dirs, sex_consistency=sexd, envelope_context=env,
           summary=dict(compared=len(gate), c1_107_hold=sum(r['c1_107_holds'] for r in gate), c2_107_hold=sum(r['c2_107_holds'] for r in gate), c2_matches_c1=sum(r['c2_matches_c1'] for r in gate),
                        c1_91_hold=sum(r['c1_91_holds'] for r in gate), c1_122_hold=sum(r['c1_122_holds'] for r in gate),
                        c1_failures=[r['reading'] for r in gate if not r['c1_107_holds']], c2_failures=[r['reading'] for r in gate if not r['c2_107_holds']],
                        f91=[r['reading'] for r in gate if not r['c1_91_holds']], f122=[r['reading'] for r in gate if not r['c1_122_holds']],
                        sex_consistent=sum(r['consistent'] for r in sexd), sex_compared=len(sexd), sex_inconsistent=[r['reading'] for r in sexd if not r['consistent']],
                        c2_within_c1_bounds=sum(r['PKF107_within_c1_bounds'] for r in env)),
           comparators='normalized MF-M-R / MF-F-R (W2H rule); route-matched MF107 / MFF107 (native_short.py, no targets) for sex consistency only; diagnostic, not reference assets')
json.dump(res, open(OUT, 'w'), indent=1, default=lambda o: o.item() if hasattr(o, 'item') else str(o))
print(res['verdict']); print(json.dumps(res['summary'], indent=1)); print(st, res['determinism'])
for r in dirs: print('%-58s c1 %-5s %-24s c2 %-5s %-24s 91 %-5s 122 %s' % (r['reading'][:58], r['c1_107_holds'], r['c1_107_vs_MF_pct'], r['c2_107_holds'], r['c2_107_vs_MF_pct'], r['c1_91_holds'], r['c1_122_holds']))
for r in sexd: print('  sex %-50s PK %s MF %s diff %s %s' % (r['reading'][:50], r['pipkin_c2_over_c1_pct'], r['marchfolk_c2_over_c1_pct'], r['difference_pct'], r['consistent']))
