# va_ear_export.py WORK EVIDIR : Vael ear-prototype order §21 items 2-4 -- Vael ear topology definition (= frozen Fenn v002 engineering connectivity,
# proven equal), the v005 -> branch map for every Vael realization (proven equal to the frozen Fenn map), and the VA-E1 / VA-E2 / VA-E3 branch geometry
# for c1 / c2 (root-frame coordinates, frame, transition ring, parameters, placement, fairing record, full-mesh vertex hash).
import sys, os, json, hashlib, glob, numpy as np
os.environ.setdefault('EAR_TOPO', 'v002')
sys.path.insert(0, '/home/claude/wayfarer-design/tools/rac/rp/fenn_rp3_v001')
import ear_branch_lib as E
W_, EV = sys.argv[1], sys.argv[2]; FE = '/home/claude/wayfarer-design/reviews/rac-rp3-evidence/fenn_ear_v002'
for d in ('topology', 'mapping', 'geometry'): os.makedirs(os.path.join(EV, d), exist_ok=True)
sha = lambda p: hashlib.sha256(open(p, 'rb').read()).hexdigest()
Lo = E.canonical_layout(); assert Lo['version'] == 'v002'
FT = np.load(FE + '/topology/FENN_EAR_BRANCH_TOPOLOGY_v002.npz'); FM = np.load(FE + '/mapping/FENN_EAR_BRANCH_MAP_v005_v002.npz')
canon = json.load(open(os.path.join(W_, 'canon_branch_topology.json')))
builds = sorted(os.path.basename(f).replace('_branch.npz', '') for f in glob.glob(os.path.join(W_, 'build/*_branch.npz')))
# ---- topology: every Vael realization has the frozen Fenn v002 face list, part / side labels and v005 map
chk = {}
for b in builds:
    z = np.load(os.path.join(W_, 'build/%s_branch.npz' % b))
    chk[b] = dict(face_list_equal=bool(np.array_equal(z['Q'], FM['branch_Q'])), part_equal=bool(np.array_equal(z['part'], FM['branch_part'])), side_equal=bool(np.array_equal(z['side'], FM['branch_side'])),
                  v005_to_branch_equal=bool(np.array_equal(z['v005_to_branch'], FM['v005_to_branch'])), removed_v005_equal=bool(np.array_equal(z['removed_v005'], FM['removed_v005'])),
                  removed_faces_v005_equal=bool(np.array_equal(z['removed_faces_v005'], FM['removed_faces_v005'])), verts=int(len(z['V'])), faces=int(len(z['Q'])))
sheet_equal = bool(np.allclose(Lo['st'], FT['sheet_st']) and np.array_equal(np.asarray(Lo['F']), FT['sheet_faces']))
canon_equal = json.load(open(FE + '/topology/FENN_EAR_BRANCH_CUFF_CANON_v002.json')) == canon
T = dict(name='VAEL_EAR_BRANCH_TOPOLOGY_v001', order='chatgpt-rac-rp3-vael-ear-prototype-order',
         definition='the frozen Fenn ear branch topology v002 ENGINEERING connectivity, reused unchanged (order §3-§4): 52-vertex root interface per side (v005 root loop), '
                    'cuff (canon FENN_EAR_BRANCH_CUFF_CANON_v002, read-only), tapered-leaf upper-extension block, sheet layout (s, t) parameterisation, deformation-aware guard. '
                    'No Fenn vertex geometry, projection, taper, tip, base width or orientation is carried; every vertex position is Vael (ear_branch_lib CAND VA-E*). '
                    'Not a universal elf-ear topology.',
         reference_topology=dict(file='reviews/rac-rp3-evidence/fenn_ear_v002/topology/FENN_EAR_BRANCH_TOPOLOGY_v002.npz', sha256=sha(FE + '/topology/FENN_EAR_BRANCH_TOPOLOGY_v002.npz')),
         reference_cuff_canon=dict(file='reviews/rac-rp3-evidence/fenn_ear_v002/topology/FENN_EAR_BRANCH_CUFF_CANON_v002.json', sha256=sha(FE + '/topology/FENN_EAR_BRANCH_CUFF_CANON_v002.json'), equal_to_work_canon=canon_equal),
         sheet_layout_equal_to_reference=sheet_equal, face_topology_sha256=hashlib.sha256(FM['branch_Q'].astype(np.int32).tobytes()).hexdigest(),
         counts=dict(vertices=58944, quads=58942, patch_vertices_per_side=int((FM['branch_side'] == 'l').sum()), root_loop_vertices_per_side=52, sheet_vertices=int(len(Lo['st'])), sheet_faces=int(len(Lo['F']))),
         realizations=chk, all_equal=all(all(v for k, v in c.items() if k.endswith('_equal')) for c in chk.values()))
json.dump(T, open(os.path.join(EV, 'topology/VAEL_EAR_BRANCH_TOPOLOGY_v001.json'), 'w'), indent=1)
# ---- map (identical for every realization; written once from the c1 VA-E2 build)
z = np.load(os.path.join(W_, 'build/VAL4-R1-VD2-VF2_VA-E2_branch.npz')); rec = json.load(open(os.path.join(W_, 'build/VAL4-R1-VD2-VF2_VA-E2_branch.json')))
part = z['part']; _tv = np.nonzero(z['v005_to_branch'] >= 0)[0]; _tv = _tv[part[z['v005_to_branch'][_tv]] == 'transition']
mp = os.path.join(EV, 'mapping/VAEL_EAR_BRANCH_MAP_v005_v001.npz')
np.savez_compressed(mp, v005_to_branch=z['v005_to_branch'], removed_v005=z['removed_v005'], removed_faces_v005=z['removed_faces_v005'], branch_Q=z['Q'], branch_part=part, branch_side=z['side'], transition_v005=_tv)
json.dump(dict(order='chatgpt-rac-rp3-vael-ear-prototype-order', rule='identical to FENN_EAR_BRANCH_MAP_v005_v002 (kept v005 vertices keep their v005 order and family-map rows; '
               'removed: the v005 ear-zone interior; added per side: the v002 patch; root loop: v005 vertices unchanged; transition ring: v005 vertices, positions faired + quality pass)',
               root_loops_v005={s: rec['sides'][s]['root_loop_v005'] for s in ('l', 'r')}, sha256_npz=sha(mp), equal_to_fenn_map_arrays=all(c['v005_to_branch_equal'] and c['face_list_equal'] for c in chk.values()),
               fenn_map_sha256=sha(FE + '/mapping/FENN_EAR_BRANCH_MAP_v005_v002.npz'), identical_for=builds), open(os.path.join(EV, 'mapping/VAEL_EAR_BRANCH_MAP_v005_v001.json'), 'w'), indent=1)
# ---- geometry per realization (root-frame coordinates)
side = z['side']; firsts = {s: int(np.nonzero(side == s)[0][0]) for s in ('l', 'r')}; npatch = int((side == 'l').sum()); G = {}
for b in builds:
    zz = np.load(os.path.join(W_, 'build/%s_branch.npz' % b)); rr = json.load(open(os.path.join(W_, 'build/%s_branch.json' % b))); out = {}
    for s in ('l', 'r'):
        fr = rr['sides'][s]['frame']; O, n, bb, u = [np.array(fr[k]) for k in ('O', 'n', 'b', 'u')]; Xs = zz['V'][firsts[s]:firsts[s] + npatch] - O
        out['patch_' + s] = np.c_[Xs @ bb, Xs @ u, Xs @ n].astype(np.float64); out['frame_' + s] = np.r_[O, bb, u, n]
    tr = np.nonzero(zz['part'] == 'transition')[0]; out['transition_index'] = tr; out['transition_xyz'] = zz['V'][tr]; out['patch_kind'] = FT['patch_kind']; out['patch_provenance'] = FT['patch_provenance']
    gp = os.path.join(EV, 'geometry/%s_branch_geometry_v001.npz' % b); np.savez_compressed(gp, **out)
    gl = os.path.join(W_, 'build/%s_deform_guard.json' % b)
    G[b] = dict(file=os.path.basename(gp), sha256=sha(gp), params=rr['params'], geo=rr['geo'], head_scale=rr['head_scale'], HH_cm=rr['HH_cm'],
                placement={s: dict(offset_cm=rr['sides'][s]['place_offset_cm'], h0_cm=rr['sides'][s]['h0_cm'], min_margin_cm=rr['sides'][s]['min_margin_cm']) for s in ('l', 'r')},
                fairing={k: v for k, v in rr['fairing'].items() if k != 'untangle'}, untangle=rr['fairing']['untangle'], deform_guard_faces=json.load(open(gl)) if os.path.exists(gl) else [],
                engineering_env=dict(EAR_TOPO='v002', EAR_UNT_MODE='contacts'), full_mesh_vertex_sha256=hashlib.sha256(zz['V'].astype(np.float64).tobytes()).hexdigest())
json.dump(G, open(os.path.join(EV, 'geometry/VAEL_EAR_BRANCH_GEOMETRY_v001.json'), 'w'), indent=1, default=float)
print('exported', builds, 'topology all equal', T['all_equal'], 'sheet equal', sheet_equal, 'canon equal', canon_equal)
