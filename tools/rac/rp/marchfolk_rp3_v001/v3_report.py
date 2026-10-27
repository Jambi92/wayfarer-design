# v3_report.py WORK OUT.json : v003 change / quality / density / station report (order 103c832 §5 patch table, §8 full 69-station table, §9 density table)
import sys, json, numpy as np
W = sys.argv[1]; OUT = sys.argv[2]; core = np.load(W + '/v3/core_final.npz'); n2 = int(core['n_v002']); Q3 = core['Q']; lg = json.loads(str(core['log']))
def quality(V, Q):
    ang = []
    for k in range(4):
        p0, p1, p2 = V[Q[:, (k - 1) % 4]], V[Q[:, k]], V[Q[:, (k + 1) % 4]]; u1 = p0 - p1; u2 = p2 - p1
        ang.append(np.degrees(np.arccos(np.clip((u1 * u2).sum(1) / np.linalg.norm(u1, axis=1) / np.linalg.norm(u2, axis=1), -1, 1))))
    ang = np.stack(ang, 1); sd = np.stack([np.linalg.norm(V[Q[:, (k + 1) % 4]] - V[Q[:, k]], axis=1) for k in range(4)], 1); asp = sd.max(1) / np.maximum(sd.min(1), 1e-9)
    return (ang.min(1) < 45) | (ang.max(1) > 135), asp > 4
REP = dict(rings=lg['rings'], pole_moves_accepted=[p for p in lg['poles'] if p['accepted']], pole_moves_rejected=[p for p in lg['poles'] if not p['accepted']], t4_rounds=lg.get('t4'),
           repair=lg.get('repair', {}).get('rounds'), region_restore=lg.get('region_restore'), configs={})
for C in 'MF':
    cid = 'MF-%s-R' % C; v2 = np.load('%s/cand/%s_v002.npz' % (W, cid)); v3 = np.load('%s/cand/%s_v003.npz' % (W, cid)); V2, Q2, V3 = v2['V'], v2['Q'], v3['V']
    z2 = np.load('%s/audit/%s_v002_loops.npz' % (W, cid), allow_pickle=True)['zone']; z3 = np.load('%s/audit/%s_v003_loops.npz' % (W, cid), allow_pickle=True)['zone']
    rel = np.zeros(len(V3)); rel[:n2] = np.linalg.norm(V3[:n2] - V2, axis=1); chg = rel > 1e-5; new = np.arange(len(V3)) >= n2
    a2, b2 = quality(V2, Q2); a3, b3 = quality(V3, Q3); f3z = z3[Q3[:, 0]]; f2z = z2[Q2[:, 0]]
    fch = (chg | new)[Q3].any(1)
    zones = {}
    for zn in sorted(set(z3)):
        m3 = f3z == zn; m2 = f2z == zn
        zones[zn] = dict(changed_vertices=int((chg & (z3 == zn)).sum()), added_vertices=int((new & (z3 == zn)).sum()), changed_faces=int((fch & m3).sum()),
                         relocation_max_mm=round(float(rel[z3 == zn].max() * 10), 3) if (z3 == zn).any() else 0, t4_v002=int((a2 | b2)[m2].sum()), t4_v003=int((a3 | b3)[m3].sum()),
                         angle_v002=int(a2[m2].sum()), angle_v003=int(a3[m3].sum()), aspect_v002=int(b2[m2].sum()), aspect_v003=int(b3[m3].sum()),
                         reason={'hand': 'MCP / thenar / hypothenar junction-pole relocation, pinky root ring, T-4 relaxation', 'foot': 'ankle crease and MTP / toe-IP pole relocation, toe root rings, T-4 relaxation',
                                 'face': 'T-4 relaxation only (rings preserved)', 'head': 'T-4 relaxation only', 'ears': 'T-4 relaxation only'}.get(zn, 'T-4 relaxation (neighbourhood of hand / foot / face patches) or untouched'))
    au2 = json.load(open('%s/audit/%s_v002_audit.json' % (W, cid))); au3 = json.load(open('%s/audit/%s_v003_audit.json' % (W, cid)))
    st = {}
    for k in au3['joint_s7']:
        a, b = au2['joint_s7'][k], au3['joint_s7'][k]; bb = au3['joint_bands'][k]
        st[k] = dict(required=b['required'], loops_v002=a['loops'], loops_v003=b['loops'], crease_v002=a['poles_on_crease_line'], crease_v003=b['poles_on_crease_line'],
                     within2_v002=a['poles_within_2_loops'], within2_v003=b['poles_within_2_loops'], firm_v002=a['pass_firm'], firm_v003=b['pass_firm'], strict_v002=a['pass_strict'], strict_v003=b['pass_strict'],
                     nearest_pole_loops_v003=min(bb['pole_offsets_in_loops']) if bb['pole_offsets_in_loops'] else '>2')
    E3 = np.unique(np.sort(np.concatenate([Q3[:, [0, 1]], Q3[:, [1, 2]], Q3[:, [2, 3]], Q3[:, [3, 0]]]), 1), axis=0); el3 = np.linalg.norm(V3[E3[:, 0]] - V3[E3[:, 1]], axis=1); st3 = V3[:, 2].max() - V3[:, 2].min()
    E2 = np.unique(np.sort(np.concatenate([Q2[:, [0, 1]], Q2[:, [1, 2]], Q2[:, [2, 3]], Q2[:, [3, 0]]]), 1), axis=0); el2 = np.linalg.norm(V2[E2[:, 0]] - V2[E2[:, 1]], axis=1)
    dens = {}
    for zn, lim in (('face', 0.25), ('ears', 0.25), ('hand', 0.3), ('foot', 0.3), ('trunk', 0.6), ('arm', 0.6), ('leg', 0.6), ('neck', 0.6), ('head', 0.6)):
        s3 = (z3[E3[:, 0]] == zn) & (z3[E3[:, 1]] == zn); s2 = (z2[E2[:, 0]] == zn) & (z2[E2[:, 1]] == zn)
        dens[zn] = dict(limit_pct=lim, mean_v002=round(float(el2[s2].mean() / st3 * 100), 4), mean_v003=round(float(el3[s3].mean() / st3 * 100), 4), p95_v002=round(float(np.percentile(el2[s2], 95) / st3 * 100), 4),
                        p95_v003=round(float(np.percentile(el3[s3], 95) / st3 * 100), 4), pass_v003=bool(el3[s3].mean() / st3 * 100 <= lim))
    REP['configs'][C] = dict(verts_v002=int(len(V2)), quads_v002=int(len(Q2)), verts_v003=int(len(V3)), quads_v003=int(len(Q3)), relocated_vertices=int(chg.sum()), added_vertices=int(new.sum()),
                             relocation_max_mm=round(float(rel.max() * 10), 3), relocation_p95_mm=round(float(np.percentile(rel[chg], 95) * 10), 3) if chg.any() else 0,
                             t4_union_v002=int((a2 | b2).sum()), t4_union_v003=int((a3 | b3).sum()), t4_pct_v002=round(float(100 * (a2 | b2).mean()), 3), t4_pct_v003=round(float(100 * (a3 | b3).mean()), 3),
                             angle_v002=int(a2.sum()), angle_v003=int(a3.sum()), aspect_v002=int(b2.sum()), aspect_v003=int(b3.sum()), zones=zones, stations=st, density=dens,
                             firm_fail_v002=au2['s7_failing_firm'], firm_fail_v003=au3['s7_failing_firm'], strict_fail_v002=au2['s7_failing_strict'], strict_fail_v003=au3['s7_failing_strict'],
                             selfx_v002=au2['self_intersection_face_pairs'], selfx_v003=au3['self_intersection_face_pairs'], selfx_zones_v002=au2['self_intersection_zones'], selfx_zones_v003=au3['self_intersection_zones'],
                             poles_v002=au2['poles'], poles_v003=au3['poles'])
json.dump(REP, open(OUT, 'w'), indent=1)
for C, r in REP['configs'].items():
    print(C, 'T-4 %d -> %d (%.2f -> %.2f %%)' % (r['t4_union_v002'], r['t4_union_v003'], r['t4_pct_v002'], r['t4_pct_v003']), 'relocated', r['relocated_vertices'], 'added', r['added_vertices'], 'firm', r['firm_fail_v003'], 'selfx', r['selfx_v002'], '->', r['selfx_v003'])
    for zn, z_ in r['zones'].items(): print('   ', zn, z_['changed_vertices'], z_['added_vertices'], z_['t4_v002'], '->', z_['t4_v003'])
