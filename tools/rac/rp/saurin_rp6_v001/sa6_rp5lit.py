# sa6_rp5lit.py WORKDIR : historical RP5-literal pose diagnostics vs RP6 production gate poses (closure order 58aa486c §3).
#   For every RP5 pose that RP6 re-targets, records both interpretations side by side: the RP5-literal definition (original name, axis, sign, amplitude,
#   pivot as archived in sa_deform4 / the RP5 evidence) and the RP6 production gate definition (anatomical sign in the RP6 frame +Y anterior, rotation
#   about the applicable RP6 joint), the reason for each difference, and the measured results of both (sa6_eval outputs, c1 and c2, fractions 0.25-1.0).
#   The four retained diagnostics (jaw_open_20_rp5lit; tail_root_lateral_30 / tail_root_vertical_25 / tail_twist_30 _rp5lit) also get the measured pivot
#   offset and the rigid translation the off-joint pivot introduces (|(I - R) o|, o = literal pivot - tail_01 joint).
import sys, os, json, numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sa6_common as C, sa6_pose as SP, sa6_fit as FT
WD = sys.argv[1]
def rot(ax, deg):
    ax = np.asarray(ax, float); ax = ax / np.linalg.norm(ax); th = np.radians(deg); K = np.array([[0, -ax[2], ax[1]], [ax[2], 0, -ax[0]], [-ax[1], ax[0], 0]])
    return np.eye(3) + np.sin(th) * K + (1 - np.cos(th)) * K @ K
def ent(v): return [dict(bone=b, pivot_cm=np.round(np.asarray(p, float), 4).tolist(), axis=np.round(np.asarray(a, float) / np.linalg.norm(a), 6).tolist(), deg=round(float(dg), 4)) for b, p, a, dg in v]
def summ(r):
    fx = r['fractions'].values()
    return dict(classification=r['classification'], lbs_flips=max(v['lbs_flips'] for v in fx), corrected_flips=max(v['corrected_flips'] for v in fx),
                corrected_new_penetration=max(v['corrected_new_penetration_vertices'] for v in fx), corrected_tear_edges=max(v['corrected_tear_edges'] for v in fx),
                body_volume_change_cm3=r['body_volume_change_cm3']['corrected'])
REASON = {
    'sagittal_sign': 'RP5 sa_deform4 sagittal definitions assume +Y posterior; in the frozen frame +Y is anterior (rostrum at +Y), so the literal sign extends instead '
                     'of flexing (neck_flex, lower_axial_flex, shoulder_flex, hip_flex), hyper-extends (elbow_*, knee_90), plantar-flexes (ankle_dorsi20) and CLOSES the '
                     'jaw (jaw_open_20).  Production gate = same axis and amplitude with the anatomical sign.',
    'tail_pivot': 'RP5 tail-root poses rotate about a pivot ~10 cm off the RP6 tail_01 joint (archived sa_deform4 pivot); a bone rotation cannot reproduce an '
                  'off-joint pivot (same driver angle, different shape).  Production gate = same axis and angle about the tail_01 joint.'}
out = dict(status='RP6 RIG PILOT / NOT FROZEN', name='SA_RP6_rp5_literal_diagnostics_v001', frame='+X subject left, +Y anterior, +Z up (cm)', reasons=REASON, configurations={})
for c in 'MF':
    R = SP.Rig(c, WD + '/W_%s.npz' % c); PS = FT.pose_set(R); PS['jaw_open_20_rp5lit'] = R.suite('rp5')['jaw_open_20']
    ev = json.load(open(WD + '/ev_%s.json' % c))['poses']; rows = {}
    for k in sorted(p for p in PS if p.endswith('_rp5lit')):
        prod = k[:-len('_rp5lit')]; lit, pr = PS[k], PS[prod]
        why = 'tail_pivot' if prod.startswith('tail_') else 'sagittal_sign'
        row = dict(rp5_literal=ent(lit), rp6_production=ent(pr), difference=why, reason=REASON[why],
                   rp5_literal_result=summ(ev[k]) if k in ev else None, rp6_production_result=summ(ev[prod]) if prod in ev else None,
                   role='DIAGNOSTIC (not gated)' if (k in FT.NONREAL or k == 'jaw_open_20_rp5lit') else 'evaluated + gated with the production variant')
        if why == 'tail_pivot':
            o = np.asarray(lit[0][1], float) - np.asarray(pr[0][1], float); Rm = rot(lit[0][2], lit[0][3])
            row.update(pivot_offset_cm=round(float(np.linalg.norm(o)), 3), pivot_offset_vector_cm=np.round(o, 3).tolist(),
                       induced_translation_cm=round(float(np.linalg.norm((np.eye(3) - Rm) @ o)), 3),
                       same_axis_and_angle=bool(np.allclose(np.asarray(lit[0][2], float) / np.linalg.norm(lit[0][2]), np.asarray(pr[0][2], float) / np.linalg.norm(pr[0][2])) and abs(lit[0][3] - pr[0][3]) < 1e-9))
        rows[k] = row
    out['configurations']['c1' if c == 'M' else 'c2'] = rows
json.dump(out, open(C.EV6 + '/SA_RP6_rp5_literal_diagnostics_v001.json', 'w'), indent=1)
for cc, rows in out['configurations'].items():
    for k, r in rows.items():
        print(cc, k, r['role'], r.get('pivot_offset_cm', ''), r.get('induced_translation_cm', ''), (r['rp5_literal_result'] or {}).get('classification', '')[:40])
