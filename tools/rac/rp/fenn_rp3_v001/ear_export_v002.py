# ear_export_v002.py WORK EVIDENCE_DIR [V001_WORK] : order 0d9c70b §21 items 2-5 -- Fenn ear-branch topology v002 definition, the active
# v005 -> v002 branch map, the v001 -> v002 provenance map, and the final E2 c1 / c2 branch geometry (root-frame coordinates + provenance).
import sys, os, json, hashlib, glob, numpy as np
os.environ.setdefault('EAR_TOPO', 'v002')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ear_branch_lib as E
from scipy.spatial import cKDTree
W_, EV = sys.argv[1], sys.argv[2]; W1 = sys.argv[3] if len(sys.argv) > 3 else '/tmp/claude-0/rt/fn/ear/final2'
EV1 = '/home/claude/wayfarer-design/reviews/rac-rp3-evidence/fenn_ear_branch_v001'
for d in ('topology', 'mapping', 'geometry'): os.makedirs(os.path.join(EV, d), exist_ok=True)
sha = lambda p: hashlib.sha256(open(p, 'rb').read()).hexdigest()
Lo = E.canonical_layout(); assert Lo['version'] == 'v002'
canon = json.load(open(os.path.join(W_, 'canon_branch_topology.json')))
z = np.load(os.path.join(W_, 'build/FNL4-CF2_E2_branch.npz')); rec = json.load(open(os.path.join(W_, 'build/FNL4-CF2_E2_branch.json')))
side = z['side']; part = z['part']; Q = z['Q']; firsts = {s: int(np.nonzero(side == s)[0][0]) for s in ('l', 'r')}; npatch = int((side == 'l').sum())
ns = len(Lo['st']); sizes = canon['l']['cuff']['sizes']
# ---- per-patch-vertex provenance (identical for every realization): sheet / rim vertices carry fixed (s, t); cuff vertices (ring, index)
kind = []; prov = []
for v in range(npatch):
    if v < ns:
        pp = str(Lo['part'][v]); kind.append('sheet_' + pp); prov.append([float(Lo['st'][v, 0]), float(Lo['st'][v, 1])])
    else:
        k = v - ns; r = 0
        while k >= sizes[r]: k -= sizes[r]; r += 1
        kind.append('cuff'); prov.append([float(r + 1), float(k)])
kind = np.array(kind); prov = np.array(prov)
# ---- topology
tp = os.path.join(EV, 'topology/FENN_EAR_BRANCH_TOPOLOGY_v002.npz')
loc = {}
for s in ('l', 'r'):
    f0 = firsts[s]; loc[s] = np.nonzero(((Q >= f0) & (Q < f0 + npatch)).any(1) & ((side[Q] == s) | (part[Q] == 'v005') | (part[Q] == 'transition')).all(1) & (side[Q] == s).any(1))[0]
np.savez_compressed(tp, sheet_st=Lo['st'], sheet_part=Lo['part'], sheet_faces=Lo['F'], sheet_face_block=np.array(Lo['face_block_list']), junction_ring=Lo['J'],
                    junction_segments=np.array(Lo['Jseg']), rim_rows=np.array(Lo['rim']), patch_kind=kind, patch_provenance=prov,
                    patch_part=part[firsts['l']:firsts['l'] + npatch], patch_faces_left_global=Q[loc['l']], patch_faces_right_global=Q[loc['r']])
info = Lo['info']; FB = np.array(Lo['face_block_list'])
T = dict(order='0d9c70b', name='Fenn ear branch topology v002 (selected E2; shared by configuration 1 / configuration 2)', base='MPFB Family Base v005 (frozen; unchanged)',
         supersedes='FENN_EAR_BRANCH_TOPOLOGY_v001 (order bdcd6a6)',
         per_side=dict(patch_vertices=npatch, patch_faces=int(len(loc['l'])), sheet_and_rim_faces=int(len(Lo['F'])), cuff_faces=int(sum(len(b['faces']) for b in canon['l']['cuff']['bands'])),
                       removed_v005_vertices=int(len(z['removed_v005']) // 2), removed_v005_faces=int(len(z['removed_faces_v005']) // 2), root_loop_vertices=52,
                       transition_ring_v005_vertices=int((part == 'transition').sum() // 2)),
         whole_mesh=dict(v005_verts=57842, v005_faces=57840, branch_verts=int(len(z['V'])), branch_faces=int(len(Q))),
         blocks={b: int((FB == b).sum()) for b in sorted(set(FB))},
         changes_from_v001=dict(
             A_upper_extension='v001 12 x 12 kite F2 (corners Y, c1f, tip, P_up) replaced: crescent F1\' (whole notch U c0f -> c1f, 28 rows, kb = 12 columns, to a new cut c1f -> P_up) '
                               '+ tapered leaf above the cut: rows across the ear (anterior helix edge Ant[k] -> posterior rim Pup[k]) marched at square cells; columns 12 -> 2 by 3 -> 1 '
                               'reduction templates (two interior valence-3 / two valence-5 vertices each, never in consecutive bands); one diamond cap quad at the tip',
             A_columns=info['leaf_columns'], A_reductions=info['reductions'], A_params=info['params'],
             B_cuff='transition rule unchanged (v001 DP: ring sizes 52 / 56 / 60 / 64 / 68 -> J 70, pole penalty 0.5, valence guards; canonical band list re-derived once on c1 E2); '
                    'positions: 3-D corner-angle quality pass with an active-set contact guard (ear_quality3d.py, ear_build.py)',
             C_attachment='attachment-line end shape exponent 0.7 -> 1.5 (line A leaves c0 / c1 closer to the plate edge) + 2-D corner-angle energy pass on the sheet',
             D_lobe_front='attached lobe front (Datt, c0f): lobe stand-off x (1 - 0.4 att), thickness x (1 - 0.6 att) (GEO_V2); free lobe unchanged'),
         corners={k: int(v) for k, v in info['corners'].items()}, cut_front=[int(v) for v in info['cut_front']], cuff_canonical=canon,
         parameterisation='every sheet / rim vertex carries fixed W1e ear parameters (s, t) (patch_provenance); cuff vertices are (ring, index); probes change only the parameter -> geometry map',
         sheet_optimisation=dict(opt=info.get('opt'), quality=info.get('quality')), files=dict(npz=os.path.basename(tp), sha256_npz=sha(tp)))
json.dump(T, open(os.path.join(EV, 'topology/FENN_EAR_BRANCH_TOPOLOGY_v002.json'), 'w'), indent=1, default=lambda o: o.tolist() if hasattr(o, 'tolist') else str(o))
json.dump(canon, open(os.path.join(EV, 'topology/FENN_EAR_BRANCH_CUFF_CANON_v002.json'), 'w'), indent=1)
# ---- v005 -> v002 map
mp = os.path.join(EV, 'mapping/FENN_EAR_BRANCH_MAP_v005_v002.npz'); _tv = np.nonzero(z['v005_to_branch'] >= 0)[0]; _tv = _tv[part[z['v005_to_branch'][_tv]] == 'transition']
np.savez_compressed(mp, v005_to_branch=z['v005_to_branch'], removed_v005=z['removed_v005'], removed_faces_v005=z['removed_faces_v005'], branch_Q=Q, branch_part=part, branch_side=side,
                    transition_v005=_tv)
builds = sorted(os.path.basename(f).replace('_branch.npz', '') for f in glob.glob(os.path.join(W_, 'build/*_branch.npz')))
same = all(np.array_equal(np.load(os.path.join(W_, 'build/%s_branch.npz' % b))['Q'], Q) and np.array_equal(np.load(os.path.join(W_, 'build/%s_branch.npz' % b))['v005_to_branch'], z['v005_to_branch'])
           for b in builds)
Mj = dict(order='0d9c70b', rule='kept v005 vertices keep their v005 order (compacted) and their v005 family-map row (unchanged from v001); removed: the v005 ear-zone interior (same set as v001); '
          'added per side: the v002 patch. Root loop: v005 vertices, positions and rows unchanged. Transition ring: v005 vertices, topology unchanged, positions faired + quality pass (recorded).',
          root_loops_v005={s: rec['sides'][s]['root_loop_v005'] for s in ('l', 'r')}, patch_first_index=firsts, patch_vertices_per_side=npatch, sha256_npz=sha(mp), identical_for=builds, identical=bool(same))
json.dump(Mj, open(os.path.join(EV, 'mapping/FENN_EAR_BRANCH_MAP_v005_v002.json'), 'w'), indent=1)
# ---- v001 -> v002 provenance map
t1 = np.load(os.path.join(EV1, 'topology/FENN_EAR_BRANCH_TOPOLOGY_v001.npz')); st1 = t1['sheet_st']; pt1 = t1['sheet_part']; J1 = t1['junction_ring']
z1 = np.load(os.path.join(W1, 'build/FNL4-CF2_E2_branch.npz')); f1 = {s: int(np.nonzero(z1['side'] == s)[0][0]) for s in ('l', 'r')}; np1 = int((z1['side'] == 'l').sum()); ns1 = len(st1)
assert np.array_equal(z1['v005_to_branch'], z['v005_to_branch']), 'kept v005 vertices differ'
ip = E.InPlane(E.CAND['E2']); X1 = ip.flat(st1[:, 0], st1[:, 1]); X2 = ip.flat(Lo['st'][:, 0], Lo['st'][:, 1])
m_local = -np.ones(npatch, int); m_type = np.empty(npatch, dtype='<U20'); m_dist = np.zeros(npatch)
Jmap = {int(b): int(a) for a, b in zip(J1, Lo['J'])}                                           # junction ring: same (s, t), same order
for v in range(ns):
    if v in Jmap: m_local[v] = Jmap[v]; m_type[v] = 'junction_identical'; continue
    same_p = np.nonzero(pt1 == Lo['part'][v])[0]; d = np.linalg.norm(X1[same_p] - X2[v], axis=1); i = int(np.argmin(d))
    m_local[v] = int(same_p[i]); m_dist[v] = float(d[i]); m_type[v] = 'sheet_nearest_st' if Lo['part'][v] != 'rim' else 'rim_nearest_st'
off1 = np.cumsum([0] + list(json.load(open(os.path.join(EV1, 'topology/FENN_EAR_BRANCH_CUFF_CANON_v001.json')))['l']['cuff']['sizes'])); off2 = np.cumsum([0] + list(sizes))
for v in range(ns, npatch):
    r = int(prov[v, 0]) - 1; k = int(prov[v, 1]); m_local[v] = ns1 + off1[r] + k; m_type[v] = 'cuff_ring_index'
v001_to_v002 = dict(kept_v005='identity (both versions keep the same v005 vertices in the same compacted order)')
np.savez_compressed(os.path.join(EV, 'mapping/FENN_EAR_BRANCH_MAP_v001_v002.npz'), v002_patch_to_v001_patch=m_local, type=m_type, inplane_distance_cm=m_dist,
                    v002_patch_first=np.array([firsts['l'], firsts['r']]), v001_patch_first=np.array([f1['l'], f1['r']]))
json.dump(dict(order='0d9c70b', rule='per v002 patch vertex: junction ring -> the identical v001 junction vertex (same (s, t)); sheet / rim -> the nearest v001 vertex of the same part in the '
               'E2 in-plane metric (distance recorded; correspondence, not identity: the sheet topology changed); cuff -> the v001 vertex of the same ring and index (ring sizes unchanged). '
               'Global index = patch_first[side] + local. Kept v005 vertices: identical in both versions.', kept_v005=v001_to_v002['kept_v005'],
               counts={t_: int((m_type == t_).sum()) for t_ in sorted(set(m_type))}, inplane_distance_cm=dict(mean=float(m_dist[m_type == 'sheet_nearest_st'].mean()), max=float(m_dist.max())),
               v001_patch_vertices=np1, v002_patch_vertices=npatch), open(os.path.join(EV, 'mapping/FENN_EAR_BRANCH_MAP_v001_v002.json'), 'w'), indent=1)
# ---- final geometry (root-frame coordinates) per realization
G = {}
for b in builds:
    zz = np.load(os.path.join(W_, 'build/%s_branch.npz' % b)); rr = json.load(open(os.path.join(W_, 'build/%s_branch.json' % b))); out = {}
    for s in ('l', 'r'):
        fr = rr['sides'][s]['frame']; O, n, bb, u = [np.array(fr[k]) for k in ('O', 'n', 'b', 'u')]; Xs = zz['V'][firsts[s]:firsts[s] + npatch] - O
        out['patch_' + s] = np.c_[Xs @ bb, Xs @ u, Xs @ n].astype(np.float64); out['frame_' + s] = np.r_[O, bb, u, n]
    tr = np.nonzero(zz['part'] == 'transition')[0]; out['transition_index'] = tr; out['transition_xyz'] = zz['V'][tr]; out['patch_kind'] = kind; out['patch_provenance'] = prov
    gp = os.path.join(EV, 'geometry/%s_branch_geometry_v002.npz' % b); np.savez_compressed(gp, **out)
    G[b] = dict(file=os.path.basename(gp), sha256=sha(gp), params=rr['params'], geo=rr['geo'], head_scale=rr['head_scale'], HH_cm=rr['HH_cm'],
                placement={s: dict(offset_cm=rr['sides'][s]['place_offset_cm'], h0_cm=rr['sides'][s]['h0_cm'], min_margin_cm=rr['sides'][s]['min_margin_cm']) for s in ('l', 'r')},
                fairing={k: v for k, v in rr['fairing'].items() if k != 'untangle'}, untangle_rounds=rr['fairing']['untangle']['rounds'],
                full_mesh_vertex_sha256=hashlib.sha256(zz['V'].astype(np.float64).tobytes()).hexdigest())
json.dump(G, open(os.path.join(EV, 'geometry/FENN_EAR_BRANCH_GEOMETRY_v002.json'), 'w'), indent=1, default=float)
print('exported v002', builds, 'identical topology/map', same)
