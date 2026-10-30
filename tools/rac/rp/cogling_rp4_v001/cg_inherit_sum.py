# cg_inherit_sum.py W OUT.json : summary of the DIAGNOSTIC Durrim v002 / Pipkin v001 inheritance test on the Cogling v005 realizations (run_cg_inh.sh):
# authoritative firm count / failures, thumb MCP and neck stations (status, counted rings, crease poles), and T-4 on the inherited branch faces only
# (angle 45-135 / aspect > 4:1, longest / shortest side as audit.py), against the unbranched v005 realization of the same body.
import sys, json, numpy as np
W, OUT = sys.argv[1:3]; O = W + '/inh'
def t4(V, Q, F):
    if len(F) == 0: return dict(faces=0, angle=0, aspect=0, asp_max=None, ang=None)
    Q = Q[F]; ang = []
    for k in range(4):
        p0, p1, p2 = V[Q[:, (k - 1) % 4]], V[Q[:, k]], V[Q[:, (k + 1) % 4]]; u1 = p0 - p1; u2 = p2 - p1
        ang.append(np.degrees(np.arccos(np.clip((u1 * u2).sum(1) / np.linalg.norm(u1, axis=1) / np.linalg.norm(u2, axis=1), -1, 1))))
    ang = np.stack(ang, 1); sides = np.stack([np.linalg.norm(V[Q[:, (k + 1) % 4]] - V[Q[:, k]], axis=1) for k in range(4)], 1); asp = sides.max(1) / np.maximum(sides.min(1), 1e-9)
    return dict(faces=int(len(F)), angle=int(((ang.min(1) < 45) | (ang.max(1) > 135)).sum()), aspect=int((asp > 4).sum()), asp_max=round(float(asp.max()), 2), ang=[round(float(ang.min()), 1), round(float(ang.max()), 1)])
def st(v, k):
    s = v['stations'][k]; return dict(status=s['status_D1_D3'], loops=s['loops_v2'], crease_poles=s['crease_poles'], margin=s['margin'])
res = {}
for i in ('CG76H-NAT', 'CGJ7', 'CGF91-NAT', 'CG107-NAT'):
    r = {}
    for b, vp, zp in (('v005', '%s/val/%s_fam_validator_v2_D1-D6.json' % (W, i), '%s/fam/%s_fam.npz' % (W, i)), ('durrim_v002', '%s/%s_du2_validator.json' % (O, i), '%s/%s_du2.npz' % (O, i)),
                      ('pipkin_v001', '%s/%s_pk1_validator.json' % (O, i), '%s/%s_pk1.npz' % (O, i))):
        v = json.load(open(vp)); z = np.load(zp, allow_pickle=True); V = z['V'].astype(float); Q = np.asarray(z['Q'])
        e = dict(firm=v['summary']['firm_pass_count'], stations=v['summary']['stations'], fails=v['summary']['D1_D3_firm_fail'],
                 thumb={k: st(v, k) for k in ('thumb_mcp_l', 'thumb_mcp_r')}, neck=st(v, 'neck'), hip={k: st(v, k) for k in ('hip_l', 'hip_r')})
        if b != 'v005':
            e['thumb_T4'] = t4(V, Q, np.asarray(z['branch_thumb_faces'])); e['neck_T4'] = t4(V, Q, np.asarray(z['branch_neck_faces']))
            a = json.load(open('%s/%s_%s_audit.json' % (O, i, 'du2' if b == 'durrim_v002' else 'pk1')))
            e['integrity'] = {k: a[k] for k in ('components', 'boundary_edges', 'nonmanifold_edges', 'nonmanifold_vertices', 'degenerate_faces', 'self_intersection_face_pairs')}
        r[b] = e
    res[i] = r
    print(i, ' | '.join('%s %d %s thumb %s' % (b, e['firm'], e['fails'], [(x['status'], x['loops'], x['crease_poles']) for x in e['thumb'].values()]) for b, e in r.items()))
json.dump(res, open(OUT, 'w'), indent=1)
