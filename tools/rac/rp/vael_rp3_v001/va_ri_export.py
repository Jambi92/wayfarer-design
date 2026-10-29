# va_ri_export.py RI_WORK EVIDIR [SEL] : Vael root-integration order §19 items 2-4 -- RI1 / RI2 / RI3 definitions, the local Vael ear branch topology
# derivative (when the selected alternative carries its own cuff canon: VAEL_EAR_BRANCH_TOPOLOGY_v002), its v005 -> branch map, and the selected
# revised VA-E2 c1 / c2 branch geometry (root-frame coordinates, frame, transition ring, parameters, placement, fairing record, full-mesh hash).
import sys, os, json, hashlib, glob, numpy as np
os.environ.setdefault('EAR_TOPO', 'v002')
sys.path.insert(0, '/home/claude/wayfarer-design/tools/rac/rp/fenn_rp3_v001')
import ear_branch_lib as E
W, EV = sys.argv[1], sys.argv[2]; SEL = sys.argv[3] if len(sys.argv) > 3 else 'RI3'; FE = '/home/claude/wayfarer-design/reviews/rac-rp3-evidence/fenn_ear_v002'
for d in ('topology', 'mapping', 'geometry'): os.makedirs(os.path.join(EV, d), exist_ok=True)
sha = lambda p: hashlib.sha256(open(p, 'rb').read()).hexdigest()
FM = np.load(FE + '/mapping/FENN_EAR_BRANCH_MAP_v005_v002.npz'); FT = np.load(FE + '/topology/FENN_EAR_BRANCH_TOPOLOGY_v002.npz')
Lo = E.canonical_layout(); ns = len(Lo['st'])
DEF = {'RI1': 'reduced stand-off: VA-E2 parameters unchanged; concha clearance -0.30 cm (prototype 0.15) -- the concha floor may sink below the hidden-ear skull level '
              '(inside the junction ring, over the head interior), the whole auricle lowers rigidly so the attachment line meets the skin; Fenn v002 cuff canon',
       'RI2': 'RI1 + skin-hugging cuff: cuff target = planar annulus position at the skin height (hidden-ear skull field + root-loop residual) rising to the junction '
              'within a fillet max(0.45 x head scale, 1.4 x junction height) cm; biharmonic fairing + data pull (weight 0.2) on the anterior (front-sheet) attachment, fading '
              'to 0 at the root loop (0.45 cm) and near the rim / back junction (0.6 cm); Fenn v002 cuff canon',
       'RI3': 'RI2 on the local Vael cuff topology derivative: six cuff rings 52 / 56 / 60 / 64 / 66 / 68 (Fenn v002: five, 52 .. 68) -- two extra rows next to the '
              'junction carry the skin fillet; 52-vertex v005 root interface, root band, junction ring (70) and the whole ear sheet unchanged; canon VAEL_EAR_CUFF_CANON_v001'}
D = {}
for ri in ('RI1', 'RI2', 'RI3'):
    b = sorted(glob.glob('%s/%s/build/*_branch.json' % (W, ri)))
    if not b: continue
    r = json.load(open(b[0])); D[ri] = dict(definition=DEF[ri], candidate='VA-E2-' + ri, params=r['params'], geo=r['geo'], cuff_canon_sha256=sha('%s/%s/canon_branch_topology.json' % (W, ri)),
                                       engineering_env=dict(EAR_TOPO='v002', EAR_UNT_MODE='contacts'))
json.dump(D, open(os.path.join(EV, 'VAEL_EAR_RI_definitions.json'), 'w'), indent=1)
builds = sorted(os.path.basename(f).replace('_branch.npz', '') for f in glob.glob('%s/%s/build/*_branch.npz' % (W, SEL)))
z = np.load('%s/%s/build/%s_branch.npz' % (W, SEL, builds[0])); rec = json.load(open('%s/%s/build/%s_branch.json' % (W, SEL, builds[0])))
canon = json.load(open('%s/%s/canon_branch_topology.json' % (W, SEL))); own = canon != json.load(open(FE + '/topology/FENN_EAR_BRANCH_CUFF_CANON_v002.json'))
same = all(np.array_equal(np.load('%s/%s/build/%s_branch.npz' % (W, SEL, b))['Q'], z['Q']) and np.array_equal(np.load('%s/%s/build/%s_branch.npz' % (W, SEL, b))['v005_to_branch'], z['v005_to_branch']) for b in builds)
side = z['side']; firsts = {s: int(np.nonzero(side == s)[0][0]) for s in ('l', 'r')}; npatch = int((side == 'l').sum())
TN = 'VAEL_EAR_BRANCH_TOPOLOGY_v002' if own else 'FENN_EAR_BRANCH_TOPOLOGY_v002 (reused)'
part = z['part']; tv = np.nonzero(z['v005_to_branch'] >= 0)[0]; tv = tv[part[z['v005_to_branch'][tv]] == 'transition']
if own:
    np.savez_compressed(os.path.join(EV, 'topology/VAEL_EAR_BRANCH_TOPOLOGY_v002.npz'), sheet_st=Lo['st'], sheet_part=Lo['part'][:ns], sheet_faces=np.asarray(Lo['F']), junction_ring=np.asarray(Lo['J']),
                        patch_part=part[firsts['l']:firsts['l'] + npatch], branch_faces=z['Q'][(part[z['Q']] != 'v005').any(1)], branch_face_index=np.nonzero((part[z['Q']] != 'v005').any(1))[0])
mp = os.path.join(EV, 'mapping/VAEL_EAR_BRANCH_MAP_v005_v002.npz' if own else 'mapping/VAEL_EAR_BRANCH_MAP_v005_RI.npz')
np.savez_compressed(mp, v005_to_branch=z['v005_to_branch'], removed_v005=z['removed_v005'], removed_faces_v005=z['removed_faces_v005'], branch_Q=z['Q'], branch_part=part, branch_side=side, transition_v005=tv)
T = dict(name=TN, order='chatgpt-rac-rp3-vael-ear-root-integration-order', selected=SEL, local_derivative=bool(own),
         definition=('Vael-specific LOCAL cuff derivative of the frozen Fenn v002 engineering topology: identical sheet layout / faces (front, back, rim), junction ring (70), '
                     '52-vertex v005 root interface and root band; the cuff between them has six rings (52, 56, 60, 64, 66, 68) instead of five -- two extra rows next to the '
                     'junction carry the skin fillet. No Fenn vertex geometry carried; one topology for c1 / c2.') if own else 'frozen Fenn v002 engineering topology reused unchanged',
         cuff_canon=dict(file='reviews/rac-rp3-evidence/vael_rp3_ear_root_integration/topology/VAEL_EAR_CUFF_CANON_v001.json' if own else 'fenn_ear_v002/topology/FENN_EAR_BRANCH_CUFF_CANON_v002.json',
                         sha256=sha('%s/%s/canon_branch_topology.json' % (W, SEL)), sizes=canon['l']['cuff']['sizes']),
         sheet_layout_equal_to_fenn_v002=bool(np.allclose(Lo['st'], FT['sheet_st']) and np.array_equal(np.asarray(Lo['F']), FT['sheet_faces'])),
         root_loop_v005_equal_to_fenn={s: rec['sides'][s]['root_loop_v005'] == json.load(open(FE + '/mapping/FENN_EAR_BRANCH_MAP_v005_v002.json'))['root_loops_v005'][s] for s in ('l', 'r')},
         removed_v005_equal_to_fenn=bool(np.array_equal(z['removed_v005'], FM['removed_v005'])), counts=dict(vertices=int(len(z['V'])), quads=int(len(z['Q'])), patch_vertices_per_side=npatch,
         fenn_v002_vertices=int(len(FM['branch_part'])), fenn_v002_quads=int(len(FM['branch_Q'])), added_vertices=int(len(z['V']) - len(FM['branch_part'])), added_quads=int(len(z['Q']) - len(FM['branch_Q']))),
         face_topology_sha256=hashlib.sha256(np.asarray(z['Q']).astype(np.int32).tobytes()).hexdigest(), identical_for=builds, identical=bool(same), map_file=os.path.basename(mp), map_sha256=sha(mp))
json.dump(T, open(os.path.join(EV, 'topology/VAEL_EAR_BRANCH_TOPOLOGY_v002.json' if own else 'topology/VAEL_EAR_RI_topology.json'), 'w'), indent=1)
G = {}
for b in builds:
    zz = np.load('%s/%s/build/%s_branch.npz' % (W, SEL, b)); rr = json.load(open('%s/%s/build/%s_branch.json' % (W, SEL, b))); out = {}
    for s in ('l', 'r'):
        fr = rr['sides'][s]['frame']; O, n, bb, u = [np.array(fr[k]) for k in ('O', 'n', 'b', 'u')]; Xs = zz['V'][firsts[s]:firsts[s] + npatch] - O
        out['patch_' + s] = np.c_[Xs @ bb, Xs @ u, Xs @ n].astype(np.float64); out['frame_' + s] = np.r_[O, bb, u, n]
    tr = np.nonzero(zz['part'] == 'transition')[0]; out['transition_index'] = tr; out['transition_xyz'] = zz['V'][tr]; out['patch_part'] = zz['part'][firsts['l']:firsts['l'] + npatch]
    gp = os.path.join(EV, 'geometry/%s_branch_geometry_%s.npz' % (b, SEL)); np.savez_compressed(gp, **out); gl = '%s/%s/build/%s_deform_guard.json' % (W, SEL, b)
    G[b] = dict(file=os.path.basename(gp), sha256=sha(gp), params=rr['params'], geo=rr['geo'], head_scale=rr['head_scale'], HH_cm=rr['HH_cm'],
                placement={s: dict(offset_cm=rr['sides'][s]['place_offset_cm'], h0_cm=rr['sides'][s]['h0_cm'], min_margin_cm=rr['sides'][s]['min_margin_cm']) for s in ('l', 'r')},
                fairing={k: v for k, v in rr['fairing'].items() if k != 'untangle'}, untangle=rr['fairing']['untangle'], deform_guard_faces=json.load(open(gl)) if os.path.exists(gl) else [],
                engineering_env=dict(EAR_TOPO='v002', EAR_UNT_MODE='contacts'), full_mesh_vertex_sha256=hashlib.sha256(zz['V'].astype(np.float64).tobytes()).hexdigest())
json.dump(G, open(os.path.join(EV, 'geometry/VAEL_EAR_BRANCH_GEOMETRY_%s.json' % SEL), 'w'), indent=1, default=float)
print('exported', SEL, TN, 'identical', same, T['counts'])
