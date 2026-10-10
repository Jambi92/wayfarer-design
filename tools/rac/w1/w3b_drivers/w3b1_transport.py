# RAC W3B1 section 4: extreme-body folds - biology vs SURFACE TRANSPORT firewall (diagnostic, copies only, not a production rewrite).
# On the accepted composition extremes the W2 convention CARRIES the canonical per-vertex relief along each body's own normals; W3B found
# excess folds there at canonical relief. Routes compared on the same field identity, size / relief multipliers and seed indices:
#   R0 CARRIED      - canonical scalar relief along the body's raw normals (W2 convention)
#   R1 RE-EVALUATED - the W2 generator core re-evaluated on the deformed body surface (same seed indices, same R / H fields scaled by the
#                     stature factor, flow T re-projected onto the body's tangent planes), along the raw normals
#   R2 RE-EVALUATED + SMOOTH NORMALS - R1 displaced along normals of the Laplacian-smoothed body base (20 uniform iterations), so neighbouring
#                     displacements cannot cross inside compressed creases
#   R3 CARRIED + SMOOTH NORMALS - canonical relief along the smoothed normals (the minimal transport fix)
# Folds: surfaced faces whose orientation opposes the body's own unsurfaced base face, non-sliver; EXCESS over the canonical surfaced body's
# own count on the same faces. Base self-folds (body base vs canonical base) are reported separately (a base fold is not a surface issue).
import os, sys, json, numpy as np, igl
from scipy import sparse
D = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, D)
import w3b_common as C, w3b_scale as SC, w3b_regions as RG, w3b_bodies as BD
BODIES = ['SA-M188', 'SA-M188-MUHI', 'SA-M188-FAHI', 'SA-M188-N-FAHI']
FIELDS = ['S_lateral_trunk', 'S_dorsal_hand', 'S_dorsal_tail', 'S_dorsal_trunk', 'S_shin', 'S_upper_posterior_neck', 'A_axilla', 'A_neck_flexion', 'A_lower_trunk_flexion', 'A_tail_articulation']
def smooth_normals(V, F, iters=20):
    A = igl.adjacency_matrix(F).astype(np.float64); deg = np.asarray(A.sum(1)).ravel(); L = sparse.diags(1 / deg) @ A; Vs = V.copy()
    for _ in range(iters): Vs = 0.5 * Vs + 0.5 * (L @ Vs)
    return igl.per_vertex_normals(Vs, F)
def reeval(Vb, Nb, aff, k):
    Z = SC.ref(); T = Z['T'].astype(np.float64); T = T - Nb * (T * Nb).sum(1)[:, None]; T /= np.maximum(np.linalg.norm(T, axis=1), 1e-9)[:, None]
    R = Z['R'].astype(np.float64) * k; H = Z['H'].astype(np.float64)
    core = SC.core_relief(Vb, aff, Z['seeds'], R, H, Z['EL'].astype(np.float64), T, Z['PL'].astype(np.float64), Z['IMB'].astype(np.float64), Z['FAM'])
    if isinstance(core, tuple): core = core[0]
    return core
def run():
    Z = SC.ref(); Fu = Z['Fu']; masks = RG.masks(); out = {}
    Vc = Z['Vu']; Nc = Z['N'].astype(np.float64); Sc = Vc + Z['disp'][:, None] * Nc
    cores = {k: SC.weight(masks[k]) >= 0.9 for k in FIELDS}
    # canonical core relief on each field's vertices (for the re-evaluated route: rel = disp + ATT (core_body - core_canonical))
    for bid in BODIES:
        P = BD.build(bid); h = {b: hh for b, _, hh in BD.bodies()}[bid]; k = h / 188.0
        Vu, _ = igl.upsample(P, C.F0); Nr = igl.per_vertex_normals(Vu, Fu); Ns = smooth_normals(Vu, Fu); res = {}
        for f in FIELDS:
            core = cores[f]; fm = np.where(core[Fu].all(1))[0]
            A0 = 0.5 * np.linalg.norm(np.cross(Vc[Fu[fm, 1]] - Vc[Fu[fm, 0]], Vc[Fu[fm, 2]] - Vc[Fu[fm, 0]]), axis=1); fm = fm[A0 >= 0.25 * np.median(A0)]
            cr = lambda Q: np.cross(Q[Fu[fm, 1]] - Q[Fu[fm, 0]], Q[Fu[fm, 2]] - Q[Fu[fm, 0]])
            nb = cr(Vu); fc = int(((cr(Sc) * cr(Vc)).sum(1) < 0).sum()); base_folds = int(((nb * cr(Vc)).sum(1) < 0).sum())
            aff = np.unique(Fu[fm].ravel())
            cb = reeval(Vu, Nr, aff, k); cc = reeval(Vc, Nc, aff, 1.0)
            rel1 = Z['disp'].copy(); rel1[aff] = Z['disp'][aff] + Z['ATT'][aff] * (cb - cc)
            routes = {'R0_carried': Vu + Z['disp'][:, None] * Nr, 'R1_reevaluated': Vu + rel1[:, None] * Nr,
                      'R2_reevaluated_smoothN': Vu + rel1[:, None] * Ns, 'R3_carried_smoothN': Vu + Z['disp'][:, None] * Ns}
            r = {nm: int(((cr(S_) * nb).sum(1) < 0).sum()) - fc for nm, S_ in routes.items()}
            res[f] = dict(canonical_folds=fc, base_self_folds_vs_canonical=base_folds, excess=r, tol=max(2, 0.10 * fc), faces=int(len(fm)))
            print(bid, f, 'canon', fc, 'base', base_folds, r, flush=True)
        out[bid] = res; json.dump(out, open(C.W + '/w3b1_transport.json', 'w'), indent=1)
    return out
if __name__ == '__main__': run()
