# partA_reference.py WORK OUT.json : order c6c7940 Part A -- Sagekin configuration-2 central reference (SGF178) validation.
# Source integrity on the native hm08 body (helpers removed) for SGF178 and the accepted comparators (SG, MF-F-R native), stature,
# anatomical continuity against SG / SGF152-NAT / SGF208 (committed meas records), sex-configuration consistency against Marchfolk at 178 cm
# (diagnostic matched comparators MFF178 / MFM178, same build route, stature re-solved) and race identity (Sagekin - Marchfolk at matched stature).
import sys, os, json, hashlib, numpy as np
from collections import Counter
W, OUT = sys.argv[1:3]
RA = '/home/claude/wayfarer-design/reviews/reference-assets'
def meas(p): return json.load(open(p))['combined']
def integrity(npz):
    z = np.load(npz); V = z['V'].astype(float); Q = np.asarray(z['Q']).astype(int); nV = len(V)
    E = np.sort(np.stack([Q, np.roll(Q, -1, 1)], 2).reshape(-1, 2), 1); ec = Counter(map(tuple, E.tolist()))
    bnd = sum(1 for c in ec.values() if c == 1); nm = sum(1 for c in ec.values() if c > 2)
    # directed-edge orientation consistency: each interior edge must appear once in each direction
    D = Counter(map(tuple, np.stack([Q, np.roll(Q, -1, 1)], 2).reshape(-1, 2).tolist())); inconsistent = sum(1 for e, c in D.items() if c > 1)
    # components (union-find over quads)
    par = np.arange(nV)
    def f(x):
        while par[x] != x: par[x] = par[par[x]]; x = par[x]
        return x
    for q in Q:
        r0 = f(q[0])
        for v in q[1:]:
            r = f(v)
            if r != r0: par[r] = r0
    used = np.unique(Q); comps = len({f(v) for v in used})
    # degenerate faces: repeated vertex or area < 1e-6 cm^2
    P = V[Q]; a = 0.5 * np.linalg.norm(np.cross(P[:, 1] - P[:, 0], P[:, 2] - P[:, 0]), axis=1) + 0.5 * np.linalg.norm(np.cross(P[:, 2] - P[:, 0], P[:, 3] - P[:, 0]), axis=1)
    deg = int(((np.array([len(set(q)) for q in Q.tolist()]) < 4) | (a < 1e-6)).sum())
    # coincident vertices (distinct used vertices closer than 1e-5 cm)
    from scipy.spatial import cKDTree
    pairs = cKDTree(V[used]).query_pairs(1e-5)
    # orientation: signed volume of the triangulated closed surface (outward if > 0 in a right-handed frame; analysis frame is left-handed)
    tri = np.r_[Q[:, [0, 1, 2]], Q[:, [0, 2, 3]]]; vol = float(np.einsum('ij,ij->i', V[tri[:, 0]], np.cross(V[tri[:, 1]], V[tri[:, 2]])).sum() / 6.0)
    return dict(verts=int(nV), unused_verts=int(nV - len(used)), quads=int(len(Q)), components=comps, boundary_edges=bnd, nonmanifold_edges=nm, orientation_inconsistent_edges=inconsistent,
                degenerate_faces=deg, coincident_vertex_pairs=len(pairs), signed_volume_L=round(vol / 1000.0, 3), bbox_cm=[round(float(x), 3) for x in (V.max(0) - V.min(0))])
res = {'integrity': {}, 'stature': {}}
for nm, p in (('SGF178', W + '/src/SGF178_native.npz'), ('SG', W + '/src/SG_native.npz'), ('MF-F-R (accepted, comparator)', '/tmp/claude-0/rt/v5/src/MF-F-R_native.npz')):
    res['integrity'][nm] = integrity(p)
M = {n: meas('%s/builds/%s_meas.json' % (RA, n)) for n in ('SG', 'SG152-NAT', 'SG208', 'SGF152-NAT', 'SGF178', 'SGF208', 'MF-F-R', 'MF-M-R')}
for n in ('MFF178', 'MFM178'): M[n] = meas('%s/partA/cmp/%s_meas.json' % (W, n))
M['SGF178_full_resolve'] = meas('%s/partA/resolve/SGF178_meas.json' % W)
res['stature'] = {n: round(m['stature'], 4) for n, m in M.items()}
res['measurement_reproduction'] = dict(note='run_candidate.py on the independent full re-solve rebuild reproduces the committed SGF178_meas.json ratios', max_abs_ratio_diff=max(abs(M['SGF178_full_resolve']['ratio'][k] - M['SGF178']['ratio'][k]) for k in M['SGF178']['ratio']))
KEYS = [('head height', 'HH_share'), ('head length', 'HL_share'), ('bideltoid shoulder', 'shoulder_breadth_share'), ('shoulder joint breadth', 'shoulder_joint_share'), ('thorax breadth', 'thorax_breadth_share'),
        ('ribcage (thorax) depth', 'thorax_depth_share'), ('thorax depth / breadth', 'thorax_d_over_b'), ('torso length', 'torso_share'), ('iliac crest (pelvis)', 'crest_share'), ('bitrochanteric (pelvis)', 'bitroch_share'),
        ('pelvic depth', 'pelvic_depth_share'), ('arm', 'arm_share'), ('forearm / arm', 'forearm_over_arm'), ('hand', 'hand_share'), ('finger / hand', 'finger_over_hand'), ('palm breadth / hand', 'palm_breadth_over_hand'),
        ('leg (hip height)', 'leg_share'), ('shin / leg', 'shin_over_leg'), ('foot', 'foot_share'), ('span', 'span_der')]
cont = []; TOL = 0.0025
for lab, k in KEYS:
    a, b, c = M['SGF152-NAT']['ratio'][k], M['SGF178']['ratio'][k], M['SGF208']['ratio'][k]
    lo, hi = min(a, c), max(a, c); inside = lo - TOL * abs(b) <= b <= hi + TOL * abs(b)
    a1, b1, c1 = M['SG152-NAT']['ratio'][k], M['SG']['ratio'][k], M['SG208']['ratio'][k]
    side = lambda x, l, h: 0 if l - TOL * abs(x) <= x <= h + TOL * abs(x) else (1 if x > h else -1)
    s2 = side(b, lo, hi); s1 = side(b1, min(a1, c1), max(a1, c1))
    cont.append(dict(c1_SG_within_SG152_SG208=s1 == 0, outside_side_c2=s2, outside_side_c1=s1, same_pattern_as_accepted_c1=(s2 == s1), excess_outside_pct=round(100 * (b - hi) / hi if s2 > 0 else (100 * (b - lo) / lo if s2 < 0 else 0.0), 2), measure=lab, key=k, SGF152_NAT=round(a, 5), SGF178=round(b, 5), SGF208=round(c, 5), SG_c1=round(M['SG']['ratio'][k], 5), within_bounds=bool(inside),
                     position_in_envelope=round((b - a) / (c - a), 3) if abs(c - a) > 1e-9 else None,
                     sex_delta_SG_pct=round(100 * (b / M['SG']['ratio'][k] - 1), 2), sex_delta_MF178_pct=round(100 * (M['MFF178']['ratio'][k] / M['MFM178']['ratio'][k] - 1), 2)))
res['continuity'] = cont
res['continuity_summary'] = dict(within_bounds=sum(c['within_bounds'] for c in cont), measures=len(cont), tolerance_rel=TOL, outside_but_same_pattern_as_accepted_c1=[c['key'] for c in cont if not c['within_bounds'] and c['same_pattern_as_accepted_c1']], outside_new_pattern=[(c['key'], c['excess_outside_pct']) for c in cont if not c['within_bounds'] and not c['same_pattern_as_accepted_c1']], route_note='SGF152-NAT is the native short-adult route (different allometry from the macro route of SGF178 / SGF208), so shares need not be monotone in stature; the accepted c1 triple SG152-NAT / SG / SG208 shows the same structure',
                                 sex_delta_max_abs_disagreement_pct=round(max(abs(c['sex_delta_SG_pct'] - c['sex_delta_MF178_pct']) for c in cont), 2),
                                 sex_delta_sign_agreement=sum((np.sign(c['sex_delta_SG_pct']) == np.sign(c['sex_delta_MF178_pct'])) or abs(c['sex_delta_MF178_pct']) < 0.3 for c in cont))
ID = [('torso', 'torso_share'), ('leg', 'leg_share'), ('arm', 'arm_share'), ('head', 'HH_share'), ('hand', 'hand_share'), ('thorax depth', 'thorax_depth_share'), ('shoulder', 'shoulder_breadth_share'), ('span', 'span_der'),
      ('forearm / arm', 'forearm_over_arm'), ('foot', 'foot_share')]
CLOSURE = {'c2_152': [-2.37, 1.85, 2.99, -0.64, 5.74, -3.31, -1.20, 2.14], 'c2_208': [-1.95, 1.53, 2.44, -1.20, 4.61, -3.53, -1.18, 1.76], 'c1_152': [-2.32, 1.74, 2.65, -0.66, 5.0, -3.20, -1.28, 1.80], 'c1_208': [-1.94, 1.47, 2.21, -1.20, 4.07, -3.45, -1.25, 1.52]}
idt = []
for i, (lab, k) in enumerate(ID):
    d2 = 100 * (M['SGF178']['ratio'][k] / M['MFF178']['ratio'][k] - 1); d1 = 100 * (M['SG']['ratio'][k] / M['MFM178']['ratio'][k] - 1)
    row = dict(measure=lab, key=k, c2_SGF178_vs_MFF178_pct=round(d2, 2), c1_SG_vs_MFM178_pct=round(d1, 2))
    if i < 8:
        row.update(closure_c2_152=CLOSURE['c2_152'][i], closure_c2_208=CLOSURE['c2_208'][i], c2_sign_matches_closure=bool(np.sign(d2) == np.sign(CLOSURE['c2_152'][i])))
    idt.append(row)
res['identity_vs_marchfolk_178'] = idt
res['identity_summary'] = dict(c2_sign_matches_closure=sum(r.get('c2_sign_matches_closure', False) for r in idt), compared=8,
                               c2_abs_max_pct=round(max(abs(r['c2_SGF178_vs_MFF178_pct']) for r in idt), 2),
                               note='closure-gate rows (RM-OT-05 §4) were measured at 152 / 208; 178 is the first matched central comparison')
res['comparators'] = dict(MFF178='diagnostic only: MF-F-R build + {stature 178, resolve_stature} (build_variant.py), not a reference asset', MFM178='diagnostic only: MF-M-R build + {stature 178, resolve_stature}')
json.dump(res, open(OUT, "w"), indent=1, default=lambda o: o.item() if hasattr(o, "item") else str(o)); print(json.dumps(dict(integrity=res["integrity"], stature=res["stature"], cs=res["continuity_summary"], ids=res["identity_summary"]), indent=1, default=lambda o: o.item()))
for c in cont: print(c)
for r in idt: print(r)
