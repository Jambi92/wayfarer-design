# ear_export.py WORK EVIDENCE_DIR : order bdcd6a6 §20 items 2-5 -- the shared Fenn ear-branch topology definition, the active-v005 -> branch
# mapping, and the per-realization branch geometry (root-frame coordinates of every branch vertex + frame + bounded transition ring).
import sys, os, json, hashlib, shutil, glob, numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ear_branch_lib as E
W_, EV = sys.argv[1], sys.argv[2]
for d in ('topology', 'mapping', 'geometry'): os.makedirs(os.path.join(EV, d), exist_ok=True)
sha = lambda p: hashlib.sha256(open(p, 'rb').read()).hexdigest()
Lo = E.canonical_layout(); canon = json.load(open(os.path.join(W_, 'canon_branch_topology.json')))
z = np.load(os.path.join(W_, 'build/FNL4-CF2_E2_branch.npz')); rec = json.load(open(os.path.join(W_, 'build/FNL4-CF2_E2_branch.json')))
# ---- topology (per side patch; identical for every head / candidate)
tp = os.path.join(EV, 'topology/FENN_EAR_BRANCH_TOPOLOGY_v001.npz')
side = z['side']; part = z['part']; Q = z['Q']; firsts = {s: int(np.nonzero(side == s)[0][0]) for s in ('l', 'r')}; npatch = int((side == 'l').sum())
loc = {}
for s in ('l', 'r'):
    f0 = firsts[s]; inpatch = (Q >= f0) & (Q < f0 + npatch); fs = np.nonzero(inpatch.any(1) & ((side[Q] == s) | (part[Q] == 'v005') | (part[Q] == 'transition')).all(1) & (side[Q] == s).any(1))[0]
    loc[s] = fs
np.savez_compressed(tp, sheet_st=Lo['st'], sheet_part=Lo['part'], sheet_faces=Lo['F'], junction_ring=Lo['J'], junction_segments=np.array(Lo['Jseg']), rim_rows=np.array(Lo['rim']),
                    patch_part=part[firsts['l']:firsts['l'] + npatch], patch_faces_left_global=Q[loc['l']], patch_faces_right_global=Q[loc['r']])
T = dict(order='bdcd6a6', name='Fenn ear branch topology v001 (shared by c1 / c2 and E1 / E2 / E3)', base='MPFB Family Base v005 (frozen; unchanged)',
         per_side=dict(patch_vertices=npatch, patch_faces=int(len(loc['l'])), removed_v005_vertices=int(len(z['removed_v005']) // 2), removed_v005_faces=int(len(z['removed_faces_v005']) // 2),
                       root_loop_vertices=52, transition_ring_v005_vertices=int((part == 'transition').sum() // 2)),
         whole_mesh=dict(v005_verts=57842, v005_faces=57840, branch_verts=int(len(z['V'])), branch_faces=int(len(Q))),
         integers=dict(E.TOPO2, ka=Lo['topo']['ka'], cuff_ring_sizes=list(E.CUFF_SIZES) + [len(Lo['J'])], junction_ring=len(Lo['J']), rim_path_edges=Lo['info']['path_edges']),
         blocks=dict(bridge='front only: attachment line A (c0 -> c1) | notch curve U (c0f -> c1f), sides D_att / B_att (j_f edges); attached concha floor / tragus region',
                     F1='front + back: crescent behind the concha (U lower part | posterior rim P_lo -> P_up; lobe front D\' | cut Y -> P_up)',
                     F2='front + back: upper extension kite (U upper part | posterior upper rim P_up -> tip; anterior helix c1f -> tip | cut)',
                     rim='K_r rows of quads round the free outline c0f -> lobe -> posterior rim -> tip -> anterior helix -> c1f (helix roll)',
                     cuff='root band (v005 root valence kept at 4) + 5 rings 52 / 56 / 60 / 64 / 68 to the junction ring (70); count changes by DP-matched +/-2 transition quads (canonical per side)',
                     transition='one bounded ring of v005 vertices outside the root loop, repositioned by the fairing (topology unchanged)'),
         corners={k: int(v) for k, v in Lo['info']['corners'].items()}, cuff_canonical=canon,
         parameterisation='every sheet vertex carries fixed W1e ear parameters (s along the ear, t across: -1 anterior edge .. +1 posterior rim; rim rows interpolate front -> back); '
                          'candidates and heads differ only in the parameter -> geometry map (outline, relief, orientation, head scale), never in topology',
         files=dict(npz=os.path.basename(tp)))
json.dump(T, open(os.path.join(EV, 'topology/FENN_EAR_BRANCH_TOPOLOGY_v001.json'), 'w'), indent=1, default=lambda o: o.tolist() if hasattr(o, 'tolist') else str(o))
# ---- mapping (identical for every realization)
mp = os.path.join(EV, 'mapping/FENN_EAR_BRANCH_MAP_v005_v001.npz'); _tv = np.nonzero(z['v005_to_branch'] >= 0)[0]; _tv = _tv[part[z['v005_to_branch'][_tv]] == 'transition']
np.savez_compressed(mp, v005_to_branch=z['v005_to_branch'], removed_v005=z['removed_v005'], removed_faces_v005=z['removed_faces_v005'], branch_Q=Q, branch_part=part, branch_side=side,
                    transition_v005=_tv)
Mj = dict(order='bdcd6a6', rule='kept v005 vertices keep their v005 order (compacted) and their v005 family-map row; production V = M_v005 @ (race hm08) outside the branch. '
          'Removed: the v005 ear-zone interior (hm08 w_ears > 0.5 faces, interior vertices). Added per side: the patch (sheet + cuff rings), positions from the root-frame construction '
          '(geometry/*.npz). Root loop: v005 vertices, positions and rows unchanged. Transition ring: v005 vertices, topology unchanged, positions from the fairing (recorded per realization).',
          root_loops_v005={s: rec['sides'][s]['root_loop_v005'] for s in ('l', 'r')}, patch_first_index=firsts, patch_vertices_per_side=npatch, sha256_npz=sha(mp),
          identical_for=sorted(os.path.basename(f).replace('_branch.npz', '') for f in glob.glob(os.path.join(W_, 'build/*_branch.npz'))))
json.dump(Mj, open(os.path.join(EV, 'mapping/FENN_EAR_BRANCH_MAP_v005_v001.json'), 'w'), indent=1)
# ---- per-realization geometry: root-frame coordinates (b posterior, u up, n lateral) of each branch vertex
G = {}
for f in sorted(glob.glob(os.path.join(W_, 'build/*_branch.npz'))):
    zz = np.load(f); rr = json.load(open(f.replace('.npz', '.json'))); nm = os.path.basename(f).replace('_branch.npz', ''); out = {}
    for s in ('l', 'r'):
        fr = rr['sides'][s]['frame']; O, n, b, u = [np.array(fr[k]) for k in ('O', 'n', 'b', 'u')]; X = zz['V'][firsts[s]:firsts[s] + npatch] - O
        out['patch_' + s] = np.c_[X @ b, X @ u, X @ n].astype(np.float64); out['frame_' + s] = np.r_[O, b, u, n]
    tr = np.nonzero(zz['part'] == 'transition')[0]; out['transition_index'] = tr; out['transition_xyz'] = zz['V'][tr]
    gp = os.path.join(EV, 'geometry/%s_branch_geometry.npz' % nm); np.savez_compressed(gp, **out)
    G[nm] = dict(file=os.path.basename(gp), sha256=sha(gp), params=rr['params'], geo=rr['geo'], head_scale=rr['head_scale'], HH_cm=rr['HH_cm'],
                 placement={s: dict(offset_cm=rr['sides'][s]['place_offset_cm'], h0_cm=rr['sides'][s]['h0_cm'], min_margin_cm=rr['sides'][s]['min_margin_cm']) for s in ('l', 'r')},
                 fairing=rr['fairing'], full_mesh_vertex_sha256=hashlib.sha256(zz['V'].astype(np.float64).tobytes()).hexdigest())
json.dump(G, open(os.path.join(EV, 'geometry/FENN_EAR_BRANCH_GEOMETRY_v001.json'), 'w'), indent=1, default=float)
print('exported', list(G))
