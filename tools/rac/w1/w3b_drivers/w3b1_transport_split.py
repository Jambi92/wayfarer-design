# RAC W3B1 section 4 supplement: split the extreme-body surfaced folds by whether the BODY BASE itself is already inverted there.
# A base face whose orientation opposes the canonical base face (the composition deformation has folded the unsurfaced skin) cannot carry
# a clean surface whatever the transport. Excess surfaced folds are counted (a) on faces whose base is clean (not inverted, not within one
# vertex ring of an inverted face) and (b) on / next to inverted base faces, for the carried route (R0) and carried + smoothed normals (R3).
import os, sys, json, numpy as np, igl
D = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, D)
import w3b_common as C, w3b_scale as SC, w3b_regions as RG, w3b_bodies as BD, w3b1_transport as TR
Z = SC.ref(); Fu = Z['Fu']; Vc = Z['Vu']; Sc = Vc + Z['disp'][:, None] * Z['N'].astype(float); masks = RG.masks(); out = {}
for bid in ['SA-M188-MUHI', 'SA-M188-FAHI', 'SA-M188-N-FAHI']:
    P = BD.build(bid); Vu, _ = igl.upsample(P, C.F0); Nr = igl.per_vertex_normals(Vu, Fu); Ns = TR.smooth_normals(Vu, Fu); res = {}
    for f in TR.FIELDS:
        core = SC.weight(masks[f]) >= 0.9; fm = np.where(core[Fu].all(1))[0]
        A0 = 0.5 * np.linalg.norm(np.cross(Vc[Fu[fm, 1]] - Vc[Fu[fm, 0]], Vc[Fu[fm, 2]] - Vc[Fu[fm, 0]]), axis=1); fm = fm[A0 >= 0.25 * np.median(A0)]
        cr = lambda Q: np.cross(Q[Fu[fm, 1]] - Q[Fu[fm, 0]], Q[Fu[fm, 2]] - Q[Fu[fm, 0]])
        nb = cr(Vu); binv = (nb * cr(Vc)).sum(1) < 0; fcan = (cr(Sc) * cr(Vc)).sum(1) < 0
        bad_v = np.zeros(len(Vu), bool); bad_v[Fu[fm[binv]].ravel()] = True; near = bad_v[Fu[fm]].any(1)
        r = {}
        for nm, N_ in (('R0_carried', Nr), ('R3_carried_smoothN', Ns)):
            fl = (cr(Vu + Z['disp'][:, None] * N_) * nb).sum(1) < 0
            r[nm] = dict(clean_base=int((fl & ~near).sum()) - int((fcan & ~near).sum()), at_inverted_base=int((fl & near).sum()) - int((fcan & near).sum()))
        res[f] = dict(base_inverted=int(binv.sum()), faces=int(len(fm)), **r); print(bid, f, res[f], flush=True)
    out[bid] = res; json.dump(out, open(C.W + '/w3b1_transport_split.json', 'w'), indent=1)
