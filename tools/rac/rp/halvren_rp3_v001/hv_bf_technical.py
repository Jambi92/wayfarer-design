# hv_bf_technical.py WORK OUT.json : Halvren body / face source order §18 -- technical regression of every propagated candidate (run_hveval.sh) on frozen
# MPFB v005: exact topology (faces / UV / map identical to the v005 family, V = M @ hm08), integrity, validator D1 + D3 + D4 + D5 + D6, T-1 / T-2 / T-3 / T-7,
# density, contact class, face rings, regeneration identity, Standard v1 deformation vs the frozen Marchfolk v005 realization of the same configuration
# (and the native source, for classification of contact excess).
import sys, os, glob, json, numpy as np, scipy.sparse as sp
W, OUT = sys.argv[1:3]; jl = lambda p: json.load(open(p)); REPO = '/home/claude/wayfarer-design'; B5 = '/mnt/user-data/outputs/rp5'
csr = lambda z: sp.csr_matrix((z['M_data'], z['M_indices'], z['M_indptr']), shape=tuple(z['M_shape'])); Mf = csr(np.load(B5 + '/MF_M_REF_RP3_retopo_v005_hm08_map.npz')); fam0 = np.load('/tmp/claude-0/rt/v5/cand/MF-M-R_v005.npz')
MFN = {c: jl(REPO + '/reviews/rac-rp3-evidence/marchfolk_baseline_v001/deformation/deform_%s_native.json' % c) for c in ('MF-M-R', 'MF-F-R')}
res = {}
for v in sorted(glob.glob(W + '/val/*_fam_validator_v2_D1-D6.json')):
    i = os.path.basename(v).split('_fam_')[0]; mf = 'MF-M-R' if i.startswith('HVC1') else 'MF-F-R'
    va = jl(v); au = jl('%s/audit/%s_fam_audit.json' % (W, i)); an = jl('%s/anat/%s_fam_anatomy.json' % (W, i)); fr = jl('%s/audit/%s_fam_face.json' % (W, i)); ct = jl('%s/contact/%s_contact.json' % (W, i))
    rc = jl('%s/src/%s_regen_check.json' % (W, i)); cz = np.load('%s/fam/%s_fam.npz' % (W, i)); nz = np.load('%s/src/%s_native.npz' % (W, i))
    df = jl('%s/def/deform_%s_fam.json' % (W, i)); dn = jl('%s/def/deform_%s_native.json' % (W, i)); dm = jl(REPO + '/reviews/rac-rp3-evidence/mpfb_family_base_final_toe2/deformation/deform_%s_v005.json' % mf)
    P = {p: dict(flips=df['poses'][p]['flipped_faces'], flips_mf=dm['poses'][p]['flipped_faces'], selfx=df['poses'][p]['new_selfx_pairs'], selfx_mf=dm['poses'][p]['new_selfx_pairs'], native_selfx=dn['poses'][p]['new_selfx_pairs'],
                 native_selfx_mf=MFN[mf]['poses'].get(p, {}).get('new_selfx_pairs'), folds=df['poses'][p]['new_folds'], folds_mf=dm['poses'][p]['new_folds']) for p in df['poses']}
    res[i] = dict(validator=va['summary']['firm_pass_count'], stations=va['summary']['stations'], margin_zero=va['summary']['margin_zero'],
                  topology=dict(faces_equal_v005=bool(np.array_equal(cz['Q'], fam0['Q'])), uv_equal=bool(np.array_equal(cz['UV'], fam0['UV'])), map_equal=bool(abs(csr(cz) - Mf).max() == 0),
                                V_eq_M_hm08_max_cm=float(np.abs(Mf @ nz['V'].astype(float) - cz['V'].astype(float)).max()), quads_pct=au['quads_pct']),
                  integrity=dict(components=au['components'], boundary=au['boundary_edges'], nonmanifold=au['nonmanifold_edges'], nonmanifold_vertices=au['nonmanifold_vertices'], degenerate=au['degenerate_faces'],
                                 coincident=au['coincident_vertex_pairs'], outward=au['normals_outward'], winding=au['winding_consistent']),
                  regen=dict(identical=rc['geometry_identical'], max_abs_dV_cm=rc['max_abs_dV_cm']),
                  anatomy=dict(T1_T2=an['T1_T2_pass'], T3=an['T3_pass'], T7=an['T7_pass'], iou_min=min(an['silhouette_iou'].values())),
                  density_all_pass=all(z['pass_mean'] for z in au['density_pct_of_stature'].values()), density_max_over_limit=round(max(z['mean'] / z['limit'] for z in au['density_pct_of_stature'].values()), 3),
                  face=dict(mouth_rings=fr['mouth_rings']['count'], orbit_rings=[fr['orbit_rings_l']['count'], fr['orbit_rings_r']['count']], poles_at_mouth_corners=fr['poles_at_mouth_corners'], mouth_pass=fr['mouth_pass'], orbit_pass=fr['orbit_pass']),
                  contact=ct['classes'], new_contact_class=ct['classes']['new'], worst_flip_excess=max(x['flips'] - x['flips_mf'] for x in P.values()), poses_flip_excess_gt5=[p for p, x in P.items() if x['flips'] - x['flips_mf'] > 5],
                  worst_selfx_excess=max(x['selfx'] - x['selfx_mf'] for x in P.values()),
                  selfx_excess_gt10={p: dict(family=x['selfx'], mf=x['selfx_mf'], native=x['native_selfx'], native_mf=x['native_selfx_mf']) for p, x in P.items() if x['selfx'] - x['selfx_mf'] > 10}, poses=P)
    r = res[i]; r['technical_pass'] = bool(r['validator'] == 69 and all(v_ for k_, v_ in r['topology'].items() if isinstance(v_, bool)) and r['topology']['V_eq_M_hm08_max_cm'] == 0 and r['integrity']['components'] == 1
                                          and r['integrity']['boundary'] == 0 and r['integrity']['nonmanifold'] == 0 and r['integrity']['degenerate'] == 0 and r['integrity']['outward'] and r['regen']['identical']
                                          and r['anatomy']['T1_T2'] and r['anatomy']['T3'] and r['anatomy']['T7'] and r['density_all_pass'] and r['new_contact_class'] == 0 and not r['poses_flip_excess_gt5'] and r['face']['mouth_pass'] and r['face']['orbit_pass'])
    print(i, r['technical_pass'], r['validator'], r['density_max_over_limit'], r['worst_flip_excess'], r['worst_selfx_excess'], r['new_contact_class'], {p: (x['family'], x['mf'], x['native'], x['native_mf']) for p, x in r['selfx_excess_gt10'].items()})
json.dump(res, open(OUT, 'w'), indent=1)
