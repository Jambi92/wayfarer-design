# RM-OT-05AB1: armpit-web weight cleanup for the cp2 rig (weights only; order 05AB1 s3).
# In each armpit web the inner upper arm lies against the latissimus; the cp2 geodesic labels gave the two touching surfaces
# different trunk/upper-arm weights, so arm shortening pushed one surface through the other. Here, inside a bounded web region
# around each contact zone, the upper-arm weight is replaced by its EUCLIDEAN Gaussian average (touching surfaces then receive
# matching weights and move together), faded back to the cp2 weights at the region edge. Only trunk / upperarm_L / upperarm_R
# weights of vertices whose other groups are zero are changed; trunk = 1 - upper-arm weight there. Bones, pose, topology and every
# other group are untouched. Exact-position duplicates receive identical weights.
# Usage: python3 ab1_web_weights.py RIG_cp2.npz OUT.npz SIGMA_CM CORE_CM FADE_CM [CONTACT_CM=1.5]
import sys, json, numpy as np
from scipy.spatial import cKDTree
rp, out, SIG, CORE, FADE = sys.argv[1], sys.argv[2], float(sys.argv[3]), float(sys.argv[4]), float(sys.argv[5]); CON = float(sys.argv[6]) if len(sys.argv) > 6 else 1.5
d = np.load(rp); V = d['V'] * 100; W = d['W'].astype(np.float64); W /= W.sum(1, keepdims=True); names = [str(x) for x in d['names']]
it = names.index('trunk'); rep = {}
for s in 'LR':
    iu = names.index('upperarm_' + s); others = [i for i in range(len(names)) if i not in (it, iu)]
    elig = W[:, others].sum(1) < 1e-6                                  # vertices weighted only to trunk / this upper arm
    arm = elig & (W[:, iu] > 0.5); tr = elig & (W[:, it] > 0.5)
    # contact zone: arm-dominant vertices within CON cm of trunk-dominant vertices (and vice versa); the geodesic label seam itself is excluded below
    da, _ = cKDTree(V[tr]).query(V[arm]); dt, _ = cKDTree(V[arm]).query(V[tr])
    ca = np.where(arm)[0][da < CON]; ct = np.where(tr)[0][dt < CON]; contact = np.r_[ca, ct]
    # keep only contact points that are not merely the cp2 label seam: seam vertices have a 0.05 < w < 0.95 blend
    blend = (W[contact, iu] > 0.05) & (W[contact, iu] < 0.95); contact = contact[~blend]
    if len(contact) == 0: rep[s] = dict(contact=0); continue
    # region: every vertex carrying trunk/upper-arm mass near the contact zone. Other groups (e.g. a small forearm share near the
    # elbow) keep their weights exactly; only the trunk : upper-arm split of the remaining mass is smoothed (no jumps at the region edge)
    mass = W[:, iu] + W[:, it]; dc, _ = cKDTree(V[contact]).query(V); reg = (mass > 1e-6) & (dc < CORE + FADE)
    idx = np.where(reg)[0]; P = V[idx]; tree = cKDTree(P); m = mass[idx]; wu = W[idx, iu] / m; new = np.empty_like(wu)
    for k, nb in enumerate(tree.query_ball_point(P, 3 * SIG)):
        g = np.exp(-np.sum((P[nb] - P[k]) ** 2, 1) / (2 * SIG ** 2)); new[k] = (g * wu[nb]).sum() / g.sum()
    a = np.clip((CORE + FADE - dc[idx]) / FADE, 0, 1); a = a * a * (3 - 2 * a)            # smoothstep fade to cp2 weights
    wn = a * new + (1 - a) * wu; old = W[idx, iu].copy()
    W[idx, iu] = m * wn; W[idx, it] = m * (1 - wn); wn = W[idx, iu]; wu = old
    rep[s] = dict(contact_vertices=int(len(contact)), region_vertices=int(len(idx)), changed_vertices=int((np.abs(wn - wu) > 1e-4).sum()),
                  max_weight_change=round(float(np.abs(wn - wu).max()), 4), contact_centre_cm=np.round(V[contact].mean(0), 1).tolist())
# optional sliver equalisation: near-degenerate source triangles whose three vertices carry different trunk : upper-arm splits can
# flip under linear-blend skinning; giving the three vertices (and their exact-position duplicates) the same split makes the
# triangle's map a single affine blend of positive-determinant bone transforms, which cannot invert it. Weights only.
if len(sys.argv) > 7:
    F = d['F']; key0, inv0 = np.unique(np.round(V, 5), axis=0, return_inverse=True); inv0 = inv0.ravel(); eq = []
    for f in json.load(open(sys.argv[7])):
        vs = F[f]; vs = np.where(np.isin(inv0, inv0[vs]))[0]                      # the face's vertices + seam duplicates
        for s in 'LR':
            iu = names.index('upperarm_' + s); ms_ = W[vs, iu] + W[vs, it]
            if W[vs, iu].max() > 0:
                u = (W[vs, iu] / ms_).mean(); W[vs, iu] = ms_ * u; W[vs, it] = ms_ * (1 - u); eq.append(dict(face=int(f), side=s, vertices=int(len(vs)), split=round(float(u), 4)))
    rep['sliver_equalised'] = eq
# exact-position duplicates must carry identical weights (they already do in cp2; smoothing is position-based so it is preserved)
key, inv = np.unique(np.round(V, 5), axis=0, return_inverse=True); inv = inv.ravel()
spread = np.zeros(len(key)); np.maximum.at(spread, inv, W[:, names.index('upperarm_L')]); lo = np.full(len(key), 9.0); np.minimum.at(lo, inv, W[:, names.index('upperarm_L')])
rep['duplicate_weight_mismatch_max'] = round(float((spread - lo).max()), 6)
rep['params'] = dict(sigma_cm=SIG, core_cm=CORE, fade_cm=FADE, contact_cm=CON)
np.savez(out, W=W.astype(np.float32), names=np.array(names)); print(json.dumps(rep, indent=1))
