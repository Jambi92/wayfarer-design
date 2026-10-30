# du2_gates.py WORK OUT.json : RP4 v002 gate summary (order 8080f9f §7, §8, §10-§12, §16) per body, each against the same body's unbranched v005
# realization (and the rejected v001 prototype where it exists): integrity, T-1..T-7, validator D1+D3+D4+D5+D6 (69 stations), thumb / neck stations,
# contact classes, density (zones + thumb MCP / hand sub-zones), branch-zone quad quality, deformation (when present).
import sys, json, os, numpy as np
sys.path.insert(0, '/home/claude/wayfarer-design/tools/rac/rp/marchfolk_rp3_v001')
from core3lib import quality
W, OUT = sys.argv[1:3]; V2 = W + '/v2'; IDS = ['DU122C-NAT', 'DU137C-NAT', 'DU152C-NAT', 'DUF137C-NAT', 'MF152-NAT']
J = lambda p: json.load(open(p)) if os.path.exists(p) else None
def val(p):
    v = J(p); s = v['summary']; st = v['stations']
    return dict(firm=s['firm_pass_count'], of=s['stations'], fails=s['D1_D3_firm_fail'], non_plain=s['D1_D3_non_plain'], margin_zero=s['margin_zero'],
                thumb={k: dict(status=st[k]['status_D1_D3'], loops=st[k]['loops_v2'], margin=st[k]['margin'], crease=st[k]['crease_poles'], h=st[k]['local_loop_cm']) for k in ('thumb_mcp_l', 'thumb_mcp_r')},
                neck=dict(status=st['neck']['status_D1_D3'], loops=st['neck']['loops_v2'], margin=st['neck']['margin'], crease=st['neck']['crease_poles'], within2=st['neck']['within2_poles'], h=st['neck']['local_loop_cm']))
def aud(p):
    a = J(p); return {k: a[k] for k in ('components', 'boundary_edges', 'nonmanifold_edges', 'nonmanifold_vertices', 'coincident_vertex_pairs', 'degenerate_faces', 'winding_consistent',
                                        'normals_outward', 'self_intersection_face_pairs', 'aspect_gt4_violations', 'angle_45_135_violations')} | dict(poles3=a['poles']['valence_3'], poles5=a['poles']['valence_5plus'],
                                        aspect_by_zone=a['aspect_violations_by_zone'], quads=a.get('quads'), verts=a.get('verts'))
def dens(p):
    d = J(p); z = {k: round(v['mean_pct'], 4) for k, v in d['zones'].items()}; sz = {k: (round(v['mean_pct'], 4), round(v['p95_pct'], 4)) for k, v in d['subzones'].items()}
    return dict(zones=z, subzones=sz)
res = {}
for i in IDS:
    r = dict(); f = W; c = V2
    r['v005'] = dict(audit=aud('%s/audit/%s_fam_audit.json' % (f, i)), validator=val('%s/val/%s_fam_validator_v2_D1-D6.json' % (f, i)), density=dens('%s/dens/%s_fam_density.json' % (c, i)))
    r['v002'] = dict(audit=aud('%s/audit/%s_cb2_audit.json' % (c, i)), validator=val('%s/val/%s_cb2_validator_v2_D1-D6.json' % (c, i)), density=dens('%s/dens/%s_cb2_density.json' % (c, i)))
    if os.path.exists('%s/v1/%s_cb1_validator.json' % (c, i)):
        r['v001'] = dict(audit=aud('%s/v1/%s_cb1_audit.json' % (c, i)), validator=val('%s/v1/%s_cb1_validator.json' % (c, i)), density=dens('%s/v1/%s_cb1_density.json' % (c, i)))
    an = J('%s/anat/%s_cb2_anatomy.json' % (c, i)); r['anatomy_v002'] = {k: an[k] for k in ('stature_source_cm', 'stature_prod_cm', 'stature_diff_mm', 'deviation_prod_to_source', 'deviation_source_to_prod', 'T1_T2_pass', 'T3_pass', 'silhouette_iou', 'T7_pass')}
    an0 = J('%s/anat/%s_fam_anatomy.json' % (f, i)); r['anatomy_v005'] = {k: an0[k] for k in ('stature_diff_mm', 'T1_T2_pass', 'T3_pass', 'T7_pass')} if an0 else None
    lm = J('%s/lm/%s_cb2_landmarks.json' % (c, i)); r['T6_max_landmark_drift_mm'] = lm['max_surface_fit_drift_mm']
    ct = J('%s/contact/%s_cb2_contact.json' % (c, i)); r['contact_vs_v005'] = {k: ct[k] for k in ('family_pairs', 'classes', 'new_pairs')}
    z0 = np.load('%s/fam/%s_fam.npz' % (f, i)); z2 = np.load('%s/cb2/%s_cb2.npz' % (c, i)); V0 = z0['V'].astype(float); Q0 = np.asarray(z0['Q']); V = z2['V'].astype(float); Q = np.asarray(z2['Q'])
    def q(VV, QQ, fl):
        ang, asp, ba, bs = quality(VV, QQ[fl]); return dict(faces=int(len(fl)), angle_viol=int(ba.sum()), aspect_gt4=int(bs.sum()), union=int((ba | bs).sum()), aspect_max=round(float(asp.max()), 3),
                                                               angle_min=round(float(ang.min()), 1), angle_max=round(float(ang.max()), 1))
    tf = z2['branch_thumb_faces']; rem = tf[tf < len(Q0)]; nf = z2['branch_neck_faces']
    r['branch_quality'] = dict(thumb_v002=q(V, Q, tf), thumb_v005_replaced=q(V0, Q0, rem), neck_v002=q(V, Q, nf), neck_v005_same_slots=q(V0, Q0, nf[nf < len(Q0)]))
    r['counts'] = dict(v005=dict(verts=int(len(V0)), quads=int(len(Q0))), v002=dict(verts=int(len(V)), quads=int(len(Q))))
    dj = J('%s/def/deform_%s_cb2.json' % (c, i)); dj0 = J('%s/def/deform_%s_fam.json' % (f, i)); djn = J('%s/def/deform_%s_native.json' % (f, i))
    if dj and dj0:
        P2 = dj.get('poses', dj); P0 = dj0.get('poses', dj0); PN = (djn.get('poses', djn) if djn else {})
        r['deformation'] = {p: dict(native=[PN[p][k] for k in ('new_selfx_pairs', 'new_folds', 'flipped_faces')] if p in PN else None,
                                    v005=[P0[p][k] for k in ('new_selfx_pairs', 'new_folds', 'flipped_faces')], v002=[P2[p][k] for k in ('new_selfx_pairs', 'new_folds', 'flipped_faces')],
                                    v002_in_zone=[P2[p].get(k) for k in ('new_selfx_in_zone', 'new_folds_in_zone', 'flipped_in_zone')], v005_in_zone=[P0[p].get(k) for k in ('new_selfx_in_zone', 'new_folds_in_zone', 'flipped_in_zone')])
                            for p in P2 if p in P0}
    res[i] = r
json.dump(res, open(OUT, 'w'), indent=1)
for i, r in res.items():
    a0, a2 = r['v005']['audit'], r['v002']['audit']; v0, v2 = r['v005']['validator'], r['v002']['validator']; b = r['branch_quality']
    print('%-12s val v005 %d -> v002 %d/%d %s | thumb %s | neck %s | integ comp %d bnd %d nm %d deg %d selfx %d->%d | T4 aspect %d->%d angle %d->%d | T1T2 %s T3 %s T7 %s T6 %.4f mm | contact new %d' % (
        i, v0['firm'], v2['firm'], v2['of'], v2['fails'], [(k[-1], s['status'][:12], s['loops'], s['crease']) for k, s in v2['thumb'].items()], (v2['neck']['status'], v2['neck']['loops'], v2['neck']['crease']),
        a2['components'], a2['boundary_edges'], a2['nonmanifold_edges'], a2['degenerate_faces'], a0['self_intersection_face_pairs'], a2['self_intersection_face_pairs'],
        a0['aspect_gt4_violations'], a2['aspect_gt4_violations'], a0['angle_45_135_violations'], a2['angle_45_135_violations'],
        r['anatomy_v002']['T1_T2_pass'], r['anatomy_v002']['T3_pass'], r['anatomy_v002']['T7_pass'], r['T6_max_landmark_drift_mm'], len(r['contact_vs_v005']['new_pairs'])))
    print('    branch quality: thumb v002 %s | v005 replaced %s | neck v002 %s | v005 %s' % (b['thumb_v002'], b['thumb_v005_replaced'], b['neck_v002'], b['neck_v005_same_slots']))
