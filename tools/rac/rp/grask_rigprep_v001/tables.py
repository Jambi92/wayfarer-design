# tables.py PROPOSAL.json OUTDIR : readable tables (markdown + csv) for the rig-prep landmark/axis proposal
import sys, os, json, csv
D = json.load(open(sys.argv[1])); O = sys.argv[2]; os.makedirs(O, exist_ok=True); J = D['joints']
r2 = lambda v, n=2: '—' if v is None else ('%.*f' % (n, v))
vec = lambda v, n=2: '(' + ', '.join('%.*f' % (n, x) for x in v) + ')'
L = ['# GR_U_REF_RP2_rigprep_landmarks_v001 — readable tables', '',
     'Generated from `GR_U_REF_RP2_rigprep_landmarks_v001.json` by `tools/rac/rp/grask_rigprep_v001/tables.py`. **Proposal only.** It does not replace the frozen landmark package.', '',
     'Frames:', '',
     '- **production cm**: x = subject left, f = forward, u = up; origin = frozen pelvis_root projected to the ground.',
     '- **Blender m**: (x, −f, u)/100.', '- **source** = production − (−0.11180, 5.72272, 0).', '']
# 1 provenance audit
L += ['## 1. Frozen landmark package: provenance audit (74 records)', '', '| provenance class | records |', '|---|---|']
for k, v in D['provenance_audit']['counts'].items(): L.append('| %s | %d |' % (k, v))
L += ['', '| id | frozen method | frozen "evidence" field | audited provenance | counts as independent measurement | T-6 drift mm |', '|---|---|---|---|---|---|']
for a in D['provenance_audit']['records']:
    L.append('| %s | %s | %s | %s | %s | %s |' % (a['id'], a['method'], a['frozen_evidence'], a['provenance'], 'yes' if a['counts_as_independent_measurement'] else 'no', a['t6_drift_mm']))
# 2 proposal joints (non-digit)
dig = lambda k: any(t in k for t in ('_mcp_', '_pip_', '_dip_', '_tip_', '_ip_', '_mtp_', 'thumb_cmc'))
L += ['', '## 2. Proposed joint centres and markers (body, girdle, axial, face)', '',
      '| id | status | provenance | production cm | Blender m | uncertainty cm | depth in v005 cm | v003 Δ cm | parent | length cm |', '|---|---|---|---|---|---|---|---|---|---|']
for k, j in J.items():
    if dig(k): continue
    L.append('| %s | %s | %s | %s | %s | %s | %s | %s | %s | %s |' % (k, j['status'], j['provenance_class'].split(' (')[0], vec(j['position_production_cm']), vec(j['position_blender_m'], 4),
             r2(j['uncertainty_cm']), r2(j['depth_to_v005_surface_cm']), r2(j['v003_crosscheck_delta_cm'], 3), j['parent'] or '—', r2(j['segment_from_parent_cm'])))
L += ['', '## 3. Alternatives behind each fitted centre (production cm; distance to the proposal)', '', '| id | alternative | position | distance cm |', '|---|---|---|---|']
for k, j in J.items():
    for an, ap in j['alternatives_production_cm'].items():
        L.append('| %s | %s | %s | %.2f |' % (k, an, vec(ap), j['alternative_distance_cm'][an]))
L += ['', '## 4. Local axes (right-handed in Blender; X = flexion axis toward subject-left, Y = toward child, Z = X × Y)', '',
      '| id | X (Blender) | Y (Blender) | Z (Blender) | det Blender / analysis | flexion sign |', '|---|---|---|---|---|---|']
for k, j in J.items():
    fr = j.get('frame')
    if not fr or 'blender_columns_XYZ' not in fr: continue
    c = fr['blender_columns_XYZ']
    L.append('| %s | %s | %s | %s | %+.0f / %+.0f | %s |' % (k, vec(c[0], 3), vec(c[1], 3), vec(c[2], 3), fr['blender_det'], fr['analysis_det'], fr.get('flexion', '')))
L += ['', '## 5. Hand / foot construction joints: surface validation on v005', '',
      '| id | production cm | inside v005 | depth cm | digit-section offset / note | v003 Δ |', '|---|---|---|---|---|---|']
for k, j in J.items():
    if not dig(k): continue
    L.append('| %s | %s | %s | %.2f | %s | 0 (construction; not evidence) |' % (k, vec(j['position_production_cm']), 'yes' if j['inside_v005'] else '**NO**', j['depth_to_v005_surface_cm'], j['note']))
L += ['', '## 6. Segment lengths (parent → child, cm)', '', '| parent | child | length | mirrored partner | L − R |', '|---|---|---|---|---|']
seg = {(s['parent'], s['child']): s['length_cm'] for s in D['segments']}
for (p, c), Ls in seg.items():
    if c.endswith('_r') and not (c.startswith('ball') or True): continue
    pr = (p[:-2] + '_r' if p.endswith('_l') else p, c[:-2] + '_r' if c.endswith('_l') else c)
    if c.endswith('_r'): continue
    other = seg.get(pr) if c.endswith('_l') else None
    L.append('| %s | %s | %.2f | %s | %s |' % (p, c, Ls, '%.2f' % other if other is not None else '—', '%+.2f' % (Ls - other) if other is not None else '—'))
L += ['', '## 7. Left / mirrored-right asymmetry of proposals (cm; x_sum = x_l + x_r, 0 = symmetric)', '', '| joint | x_sum | Δf | Δu |', '|---|---|---|---|']
for a in D['asymmetry_l_minus_mirrored_r_cm']:
    if dig(a['joint'] + '_l'): continue
    L.append('| %s | %+.2f | %+.2f | %+.2f |' % (a['joint'], a['x_sum'], a['df'], a['du']))
open(os.path.join(O, 'GR_U_REF_RP2_rigprep_landmarks_v001_tables.md'), 'w').write('\n'.join(L) + '\n')
with open(os.path.join(O, 'GR_U_REF_RP2_rigprep_landmarks_v001.csv'), 'w', newline='') as fh:
    w = csv.writer(fh); w.writerow(['id', 'side', 'status', 'provenance', 'x_cm', 'f_cm', 'u_cm', 'X_m', 'Y_m', 'Z_m', 'uncertainty_cm', 'depth_cm', 'v003_delta_cm', 'parent', 'length_cm'])
    for k, j in J.items():
        w.writerow([k, j['side'], j['status'], j['provenance_class'], *j['position_production_cm'], *j['position_blender_m'], j['uncertainty_cm'], j['depth_to_v005_surface_cm'],
                    j['v003_crosscheck_delta_cm'], j['parent'], j['segment_from_parent_cm']])
print('tables written')
