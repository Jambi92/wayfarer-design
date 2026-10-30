# cg_gates_sum.py VDIR DEF.json OUT.json : RP4 Cogling per-body gate summary on MPFB_COGLING_COMPACT_BRANCH_v001 (order 9424c72 §10-§11 / §17) from run_cg_v1.sh
# outputs: authoritative firm count / failures, thumb MCP stations, T-4 on the branch faces (angle 45-135 / aspect > 4:1 / max aspect) and on the v005 faces they
# replace, T-1 / T-2 / T-3 / T-7 (anatomy.py), T-6 landmark drift (cg_landmarks.py), contact (new pairs vs the v005 realization), integrity, and the
# determinism record (identical face list and S on every body; a second build of the definition and a second apply are bit-identical).
import sys, json, hashlib, subprocess, numpy as np
sys.path.insert(0, '/home/claude/wayfarer-design/tools/rac/rp/cogling_rp4_v001')
VD, DEF, OUT = sys.argv[1:4]; W = '/tmp/claude-0/rt/cg'
H = lambda a: hashlib.sha256(np.ascontiguousarray(a).tobytes()).hexdigest()
def t4(V, Q, F):
    Q = Q[F]; ang = []
    for k in range(4):
        p0, p1, p2 = V[Q[:, (k - 1) % 4]], V[Q[:, k]], V[Q[:, (k + 1) % 4]]; u1 = p0 - p1; u2 = p2 - p1
        ang.append(np.degrees(np.arccos(np.clip((u1 * u2).sum(1) / np.linalg.norm(u1, axis=1) / np.linalg.norm(u2, axis=1), -1, 1))))
    ang = np.stack(ang, 1); sides = np.stack([np.linalg.norm(V[Q[:, (k + 1) % 4]] - V[Q[:, k]], axis=1) for k in range(4)], 1); asp = sides.max(1) / np.maximum(sides.min(1), 1e-9)
    return dict(faces=int(len(F)), angle_flags=int(((ang.min(1) < 45) | (ang.max(1) > 135)).sum()), aspect_gt4=int((asp > 4).sum()), aspect_max=round(float(asp.max()), 2))
res = dict(branch_definition=DEF, branch_definition_sha256=hashlib.sha256(open(DEF, 'rb').read()).hexdigest(), bodies={})
for i in ('CG76H-NAT', 'CGJ7', 'CGF91-NAT', 'CG107-NAT'):
    z = np.load('%s/cb/%s_cgb.npz' % (VD, i), allow_pickle=True); f = np.load('%s/fam/%s_fam.npz' % (W, i), allow_pickle=True)
    V = z['V'].astype(float); Q = np.asarray(z['Q']); Vf = f['V'].astype(float); Qf = np.asarray(f['Q'])
    v = json.load(open('%s/val/%s_cgb_validator_v2_D1-D6.json' % (VD, i))); a = json.load(open('%s/anat/%s_cgb_anatomy.json' % (VD, i))); au = json.load(open('%s/audit/%s_cgb_audit.json' % (VD, i)))
    af = json.load(open('%s/audit/%s_fam_audit.json' % (W, i))); lm = json.load(open('%s/lm/%s_cgb_landmarks.json' % (VD, i))); c = json.load(open('%s/contact/%s_cgb_contact.json' % (VD, i)))
    tf = np.asarray(z['branch_thumb_faces'])
    # v005 faces replaced = the removed parent slots, read from a fresh realization of the definition on the same v005 body
    import cg_branch_v001 as CB
    r = CB.realize(dict(np.load('%s/fam/%s_fam.npz' % (W, i), allow_pickle=True)), json.load(open(DEF)))
    S = r['S'].tocsr()
    st = v['stations']
    res['bodies'][i] = dict(
        firm=v['summary']['firm_pass_count'], stations=v['summary']['stations'], fails=v['summary']['D1_D3_firm_fail'],
        fail_detail={k: dict(status=st[k]['status_D1_D3'], loops=st[k]['loops_v2'], loop_mode=st[k]['loop_mode'], crease_poles=st[k]['crease_poles']) for k in v['summary']['D1_D3_firm_fail']},
        thumb={k: dict(status=st[k]['status_D1_D3'], loops=st[k]['loops_v2'], crease_poles=st[k]['crease_poles'], margin=st[k]['margin']) for k in ('thumb_mcp_l', 'thumb_mcp_r')},
        neck=dict(status=st['neck']['status_D1_D3'], loops=st['neck']['loops_v2']), hip={k: st[k]['status_D1_D3'] for k in ('hip_l', 'hip_r')},
        T4_branch=t4(V, Q, tf), T4_replaced_v005=t4(Vf, Qf, np.asarray(r['removed'])),
        T4_body=dict(angle=au['angle_45_135_violations'], aspect=au['aspect_gt4_violations'], v005_angle=af['angle_45_135_violations'], v005_aspect=af['aspect_gt4_violations']),
        T1_T2=a['T1_T2_pass'], T3=a['T3_pass'], T3_stature_diff_mm=a['stature_diff_mm'], T7=a['T7_pass'], deviation_body_mm=a['deviation_prod_to_source']['body'],
        T6_max_drift_mm=lm['max_surface_fit_drift_mm'], contact=dict(new=c['classes']['new'], new_hand_foot_groin=c['new_hand_foot_groin_defects'], passed=c['pass']),
        integrity={k: au[k] for k in ('components', 'boundary_edges', 'nonmanifold_edges', 'nonmanifold_vertices', 'degenerate_faces', 'normals_outward')},
        rest_selfx=dict(branch=au['self_intersection_face_pairs'], v005=af['self_intersection_face_pairs']),
        determinism=dict(face_hash=H(Q.astype(np.int64)), S_structure=H(np.r_[S.indptr.astype(np.int64), S.indices.astype(np.int64)]), S_weights=H(S.data.astype(np.float64)),
                         rebuild_identical=bool(np.array_equal(r['V'].astype(z['V'].dtype), z['V']) and np.array_equal(r['Q'], Q))),
        verts=int(len(V)), quads=int(len(Q)))
    b = res['bodies'][i]; print(i, b['firm'], b['fails'], 'thumb', [(x['status'], x['loops'], len(x['crease_poles'])) for x in b['thumb'].values()], 'T4br', b['T4_branch'], 'repl', b['T4_replaced_v005']['angle_flags'],
                                 'T1/2', b['T1_T2'], 'T3', b['T3'], b['T3_stature_diff_mm'], 'T7', b['T7'], 'T6', b['T6_max_drift_mm'], 'contact new', b['contact']['new'], 'selfx', b['rest_selfx'])
B = res['bodies']; res['identical_face_list_all_bodies'] = len({b['determinism']['face_hash'] for b in B.values()}) == 1
res['identical_S_all_bodies'] = len({(b['determinism']['S_structure'], b['determinism']['S_weights']) for b in B.values()}) == 1
# second build of the definition from the same inputs
p2 = W + '/br/_rebuild_def.json'; subprocess.run(['python3', '/home/claude/wayfarer-design/tools/rac/rp/cogling_rp4_v001/cg_branch_v001.py', 'build', W + '/br/thumb_def.json', W + '/br/cg_thumb_relax1.json', p2], cwd=W + '/br', check=True, capture_output=True)
res['definition_rebuild_identical'] = hashlib.sha256(open(p2, 'rb').read()).hexdigest() == res['branch_definition_sha256']
print('face list identical', res['identical_face_list_all_bodies'], 'S identical', res['identical_S_all_bodies'], 'def rebuild identical', res['definition_rebuild_identical'])
json.dump(res, open(OUT, 'w'), indent=1)
