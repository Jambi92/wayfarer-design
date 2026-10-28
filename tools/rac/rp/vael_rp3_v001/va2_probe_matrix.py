# va2_probe_matrix.py EVAL.json OUT.json : Vael body / face source order §6 / §9 response matrix -- for every probe (va2_eval.py output, configuration 1,
# VAL4 record with the height macro held) the % change vs VAL4 of the body-canon keys, the human-separation system descriptors, the face descriptors and the
# region RMS vs Marchfolk; this is the evidence used to choose the VB / VC control sets.
import sys, json
E, OUT = sys.argv[1:3]; r = json.load(open(E)); it = r['items']; b = it['VAL4']
BK = ['leg_share', 'waist_interval_over_torso', 'torso_share', 'thorax_depth_share', 'central_vertical_share', 'arm_share', 'extremity_share', 'joint_mean', 'wrist_over_forearm', 'palm_breadth_over_hand',
      'foot_breadth_over_length', 'pelvic_depth_share', 'bitroch_over_crest']
canonv = lambda x: {row['key']: row['VA'] for row in x['canon']}
sysv = lambda x: {d['key']: d['VA'] for s in x['body_systems'].values() for d in s['descriptors']}
M = {}
for tag, x in it.items():
    if tag == 'VAL4': continue
    cb, cx = {**canonv(b), **sysv(b)}, {**canonv(x), **sysv(x)}
    M[tag] = dict(stature_delta_cm=round(x['stature'] - b['stature'], 3),
                  body_pct={k: round(100 * (cx[k] / cb[k] - 1), 2) for k in sorted(set(cb) & set(cx))},
                  face_pct={k: round(100 * (x['face_desc'][k] / b['face_desc'][k] - 1), 2) for k in x['face_desc'] if k != 'head_height_cm'},
                  face_rms_vs_MF_mm={rg: v['VA_vs_MF_mm'] for rg, v in x['face_regions'].items()}, body_rms_vs_MF_mm={rg: v['VA_vs_MF'] for rg, v in x['body_region_rms_mm'].items()},
                  canon_failing=x['canon_failing'], body_systems_material=x['body_systems_material'], face_systems_material=x['face_systems_material'])
json.dump(dict(base='VAL4 (height macro held)', probes=M), open(OUT, 'w'), indent=1)
for t, v in M.items():
    if t.startswith('pB'): print('%-12s st %+.2f' % (t, v['stature_delta_cm']), ' '.join('%s %+.2f' % (k[:12], v['body_pct'][k]) for k in BK if k in v['body_pct']), '| neck', v['body_pct'].get('neck_breadth_share'), '| fing', v['body_pct'].get('finger_over_hand'))
for t, v in M.items():
    if t.startswith('pF'): print('%-30s' % t, ' '.join('%s %+.1f' % (k.split('_over')[0][:10], v['face_pct'][k]) for k in ('cranial_height_over_stature', 'cranial_height_over_face', 'skull_breadth_over_HH', 'face_height_over_bizygomatic', 'lower_face_height_over_HH', 'bizygomatic_over_HH', 'cheekbone_height_over_HH', 'midface_projection_over_HH', 'brow_projection_over_HH', 'jaw_width_over_bizygomatic', 'lower_face_width_over_bizygomatic')),
                                  '| rms', ' '.join('%.1f' % x for x in v['face_rms_vs_MF_mm'].values()))
