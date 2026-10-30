# du_density.py MESH.npz LOOPS.npz LANDMARKS.json FACE.json VALIDATOR.json OUT.json : RP4 order 609c557 §8 compact-density diagnosis of one realization.
# Zones = audit.py zones (dominant source weight channel, carried through the family map; face = head zone forward of the ear plane).
# Sub-zones by nearest rig / production landmark inside the zone (landmarks.py package):
#   face  : orbit (eye_l / eye_r), mouth (mouth corners + centre), jaw hinge (jaw_hinge_l / r), other face;
#   hand  : wrist transition (wrist), palm (nearest = wrist / thumb_cmc and proximal of the MCP line), MCP (finger mcp + thumb_mcp), IP (pip / dip / thumb_ip), tips;
#   foot  : ankle transition (ankle), heel (behind the ankle), forefoot (between ankle and the toe j1 line), ball (toe j1), toe joints (toe j2..j4), toe tips.
# Per sub-zone: edge mean / median / p95 as % of stature (contract §8 ceilings: face 0.25, hands / feet 0.3) and in mm; local scale context:
#   mean edge / (digit length) for fingers and toes, mean edge / (palm length) for the palm. Loops: validator D1 station loop counts and margins (contract §7:
#   3 per knuckle, 2 per IP joint, 2 per toe joint, wrist 3, ankle 3), face rings (orbit / mouth ring loops, poles near eyes / mouth) from face_rings.py.
import sys, json, numpy as np
from collections import defaultdict
MP, LP, LM, FJ, VJ, OUT = sys.argv[1:7]
z = np.load(MP); V = z['V'].astype(float); Q = np.asarray(z['Q']).astype(int); L = np.load(LP, allow_pickle=True); zone = L['zone'].astype(str)
lm = {k: np.array(v['production_p_cm'] if 'production_p_cm' in v else v['p_cm'], float) for k, v in json.load(open(LM))['landmarks'].items()}
H = V[:, 2].max() - V[:, 2].min()
E = np.sort(np.stack([Q, np.roll(Q, -1, 1)], 2).reshape(-1, 2), 1); E = np.unique(E, axis=0); el = np.linalg.norm(V[E[:, 0]] - V[E[:, 1]], axis=1)
lab = np.full(len(V), '', object)
def nearest(idx, names):
    P = np.stack([lm[n] for n in names]); d = np.linalg.norm(V[idx][:, None] - P[None], axis=2); return np.array(names)[d.argmin(1)], d.min(1)
# face
fi = np.where(zone == 'face')[0]
if len(fi):
    names = ['eye_l', 'eye_r', 'mouth_corner_l', 'mouth_corner_r', 'jaw_hinge_l', 'jaw_hinge_r']
    mc = (lm['mouth_corner_l'] + lm['mouth_corner_r']) / 2; lm['mouth_centre'] = mc; names.append('mouth_centre')
    n, d = nearest(fi, names); eyer = 0.11 * (lm['crown'][2] - mc[2]) * 1.9          # orbit radius ~ 0.21 x crown-to-mouth distance
    for i, nn, dd in zip(fi, n, d):
        if nn.startswith('eye') and dd < eyer: lab[i] = 'face:orbit'
        elif nn.startswith('mouth') and dd < 0.6 * np.linalg.norm(lm['mouth_corner_l'] - lm['mouth_corner_r']) + 1.0: lab[i] = 'face:mouth'
        elif nn.startswith('jaw') and dd < 2.5 * H / 173: lab[i] = 'face:jaw_hinge'
        else: lab[i] = 'face:other'
for s in ('l', 'r'):
    hi = np.where((zone == 'hand') & ((V[:, 0] > 0) == (s == 'l')))[0]
    if len(hi):
        F = ['index', 'middle', 'ring', 'pinky']
        names = ['wrist_' + s, 'thumb_cmc_' + s, 'thumb_mcp_' + s, 'thumb_ip_' + s, 'thumb_tip_' + s] + ['%s_%s_%s' % (f, j, s) for f in F for j in ('mcp', 'pip', 'dip', 'tip')]
        n, d = nearest(hi, names)
        for i, nn in zip(hi, n):
            k = nn.split('_')[1] if not nn.startswith('wrist') else 'wrist'
            lab[i] = {'wrist': 'hand:wrist_transition', 'cmc': 'hand:palm', 'mcp': 'hand:mcp', 'pip': 'hand:ip', 'dip': 'hand:ip', 'ip': 'hand:ip', 'tip': 'hand:tip'}[k]
        # palm = hand vertices whose nearest is the MCP landmark but lie proximal of the MCP line (towards the wrist)
        mcpc = np.mean([lm['%s_mcp_%s' % (f, s)] for f in F], 0); ax = mcpc - lm['wrist_' + s]; ax /= np.linalg.norm(ax)
        for i in hi:
            if lab[i] == 'hand:mcp' and np.dot(V[i] - mcpc, ax) < -0.35 * np.linalg.norm(mcpc - lm['wrist_' + s]) * 0.25: lab[i] = 'hand:palm'
    fo = np.where((zone == 'foot') & ((V[:, 0] > 0) == (s == 'l')))[0]
    if len(fo):
        T = ['toe%d' % t for t in range(1, 6)]
        names = ['ankle_' + s] + ['%s_%s_%s' % (t, j, s) for t in T for j in ('j1', 'j2', 'j3', 'j4', 'tip') if '%s_%s_%s' % (t, j, s) in lm]
        n, d = nearest(fo, names); fwd = lm['toe2_j1_' + s] - lm['ankle_' + s]; fwd[2] = 0; fwd /= np.linalg.norm(fwd)
        j1 = np.mean([lm['%s_j1_%s' % (t, s)] for t in T], 0); lj1 = np.dot(j1 - lm['ankle_' + s], fwd)
        for i, nn in zip(fo, n):
            a = np.dot(V[i] - lm['ankle_' + s], fwd)
            if nn.startswith('ankle'):
                lab[i] = 'foot:heel' if a < -0.25 * lj1 else ('foot:ankle_transition' if V[i, 2] > lm['ankle_' + s][2] - 0.35 * (lm['ankle_' + s][2]) else 'foot:forefoot')
            else:
                k = nn.split('_')[1]
                if k == 'j1': lab[i] = 'foot:ball' if a > 0.8 * lj1 else 'foot:forefoot'
                elif k == 'tip': lab[i] = 'foot:toe_tip'
                else: lab[i] = 'foot:toe_joints'
el_lab = np.where(lab[E[:, 0]] == lab[E[:, 1]], lab[E[:, 0]], '')
LIM = {'face': 0.25, 'hand': 0.3, 'foot': 0.3}
res = dict(mesh=MP, stature_cm=round(float(H), 3), verts=len(V), subzones={})
for k in sorted(set(el_lab) - {''}):
    e = el[el_lab == k]; z0 = k.split(':')[0]
    res['subzones'][k] = dict(edges=int(len(e)), verts=int((lab == k).sum()), mean_pct=round(float(e.mean() / H * 100), 4), median_pct=round(float(np.median(e) / H * 100), 4),
                              p95_pct=round(float(np.percentile(e, 95) / H * 100), 4), max_pct=round(float(e.max() / H * 100), 4), mean_mm=round(float(e.mean() * 10), 3), p95_mm=round(float(np.percentile(e, 95) * 10), 3),
                              ceiling_pct=LIM[z0], mean_within_ceiling=bool(e.mean() / H * 100 <= LIM[z0]), p95_within_ceiling=bool(np.percentile(e, 95) / H * 100 <= LIM[z0]))
for z0 in LIM:
    e = el[(zone[E[:, 0]] == z0) & (zone[E[:, 1]] == z0)]
    res.setdefault('zones', {})[z0] = dict(mean_pct=round(float(e.mean() / H * 100), 4), p95_pct=round(float(np.percentile(e, 95) / H * 100), 4), mean_mm=round(float(e.mean() * 10), 3), ceiling_pct=LIM[z0],
                                          mean_within=bool(e.mean() / H * 100 <= LIM[z0]), p95_within=bool(np.percentile(e, 95) / H * 100 <= LIM[z0]))
# local scale: digit edges per digit length
def seglen(names): return float(sum(np.linalg.norm(lm[b] - lm[a]) for a, b in zip(names[:-1], names[1:])))
loc = {}
for s in ('l', 'r'):
    fl = np.mean([seglen(['%s_%s_%s' % (f, j, s) for j in ('mcp', 'pip', 'dip', 'tip')]) for f in ('index', 'middle', 'ring', 'pinky')])
    tl = np.mean([seglen([n for n in ['%s_%s_%s' % (t, j, s) for j in ('j1', 'j2', 'j3', 'j4', 'tip')] if n in lm]) for t in ('toe1', 'toe2', 'toe3', 'toe4', 'toe5')])
    loc[s] = dict(finger_len_cm=round(fl, 3), toe_len_cm=round(tl, 3))
for k in ('hand:ip', 'hand:tip', 'hand:mcp'):
    if k in res['subzones']: res['subzones'][k]['mean_edge_over_finger_len'] = round(res['subzones'][k]['mean_mm'] / 10 / np.mean([loc[s]['finger_len_cm'] for s in loc]), 4)
for k in ('foot:toe_joints', 'foot:toe_tip', 'foot:ball'):
    if k in res['subzones']: res['subzones'][k]['mean_edge_over_toe_len'] = round(res['subzones'][k]['mean_mm'] / 10 / np.mean([loc[s]['toe_len_cm'] for s in loc]), 4)
res['digit_lengths'] = loc
# loops (validator) and face rings
Vd = json.load(open(VJ)); rows = {}
for k, v in Vd['stations'].items():
    if any(t in k for t in ('mcp', 'pip', 'dip', 'thumb', 'toe', 'wrist', 'ankle', 'ball', 'cmc')):
        rows[k] = dict(required=v.get('required'), loops=v.get('loops_v2'), margin=v.get('margin'), status=v.get('status_D1_D3'), firm=v.get('firm_D1_D3'))
res['validator_digit_stations'] = rows
sm = Vd['summary']; res['validator_summary'] = dict(firm_pass=sm.get('firm_pass_count'), stations=sm.get('stations'), firm_fail=sm.get('D1_D3_firm_fail'), margin_zero=sm.get('margin_zero'), non_plain=sm.get('D1_D3_non_plain'))
fj = json.load(open(FJ)); res['face_rings'] = {k: fj.get(k) for k in ('orbit_rings', 'mouth_rings', 'poles_at_mouth_corners', 'poles_within_2cm_of_mouth', 'poles_within_2cm_of_eyes', 'mouth_pass', 'orbit_pass', 'face_density_pct')}
if isinstance(res['face_rings'].get('mouth_rings'), dict): res['face_rings']['mouth_rings'] = res['face_rings']['mouth_rings'].get('count')
if isinstance(res['face_rings'].get('orbit_rings'), dict): res['face_rings']['orbit_rings'] = {k: (v.get('count') if isinstance(v, dict) else v) for k, v in res['face_rings']['orbit_rings'].items()}
json.dump(res, open(OUT, 'w'), indent=1, default=lambda o: o.item() if hasattr(o, 'item') else str(o))
print(json.dumps({k: (v['mean_pct'], v['p95_pct'], v['mean_mm']) for k, v in res['subzones'].items()}))
