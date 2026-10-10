# RAC W3B section 19: ridge x facial-scale interaction matrix on the SURFACED head (diagnostic copies).
# Facial class multipliers act on every facial scaly field together (the union of the named facial fields + the cranial structural plates,
# smooth weight); ridge strength m = the hidden normalized structural-ridge strength (w3b_ridge). Surfaced head = upsample(ridge-modified
# base) + facial relief along its own normals. Checks per corner:
#   LEGIBILITY: each ridge family's strength >= 1.0 x the scale-relief amplitude within 1 cm of its core (plane readability not erased);
#   ARMOR / SPIKE: new folds on the surfaced head (vs its own base), facial relief aspect <= 0.30;
#   EXPRESSION: frontal eye visibility on the surfaced head >= 90 % of the canonical surfaced head;
#   visual sheet (front / 3/4 / profile).
import os, sys, json, numpy as np, igl
from scipy.spatial import cKDTree
D = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, D)
import w3b_common as C, w3b_scale as SC, w3b_regions as RG, w3b_ridge as RD, w3b_sheet as SS
W = C.W + '/interact'; os.makedirs(W, exist_ok=True)
FACE = RG.CLASS['face']
def face_weight():
    M = RG.masks(); m = np.zeros(len(SC.ref()['Vu']), bool)
    for k in FACE: m |= M[k]
    m |= (SC.ref()['Vu'][:, 2] > 172) & (SC.ref()['FAM'] == 3)        # all fine-expressive head surface
    return SC.weight(m)
def eye_vis_surf(Sv, Fu, elev):
    Z = SC.ref(); hv = np.where(Sv[:, 2] > 176)[0]; P = Sv[hv]; e = np.radians(elev); d = np.array([0, np.cos(e), np.sin(e)]); up = np.array([0, -np.sin(e), np.cos(e)])
    x = P[:, 0]; y = P @ up; depth = P @ d; cell = 0.04; key = np.floor(x / cell).astype(np.int64) * 100000 + np.floor(y / cell).astype(np.int64)
    o = np.argsort(key); ks = key[o]; uq, st = np.unique(ks, return_index=True); mx = np.maximum.reduceat(depth[o], st); fr = dict(zip(uq.tolist(), mx.tolist()))
    eye = np.where(Z['FAM'][hv] == 7)[0]; return float(np.mean([depth[i] >= fr[key[i]] - 0.05 for i in eye]))
def field_multipliers(which):
    """per-vertex multiplier array: every facial field at its own valid-interval end ('rmin' / 'rmax' / 'smin' / 'smax'), blended by the
    fields' smooth weights (w3b_scale_eval envelope)"""
    env = json.load(open(C.W + '/scale/envelope.json')); M = RG.masks(); n = len(SC.ref()['Vu']); acc = np.zeros(n); wsum = np.zeros(n)
    CAP = {'face_cranial_structural': 1.18}                     # W3B1 'rC1': per-field max relief limited by C-R1 at m = 1 (temporal 1.18; others canthal 2.57 -> 2.5)
    key = {'rmin': ('relief', 'min_valid'), 'rmax': ('relief', 'max_valid'), 'smin': ('size', 'min_valid'), 'smax': ('size', 'max_valid'), 'rC1': ('relief', 'max_valid')}[which]
    for k in FACE:
        e = env[k][key[0]]
        if not e or e.get(key[1]) is None: continue
        v = e[key[1]] if which != 'rC1' else min(e[key[1]], CAP.get(k, 2.5))
        wk = SC.weight(M[k]); acc += wk * (v - 1.0); wsum += wk
    return 1.0 + acc / np.maximum(wsum, 1.0)
def corner(tag, m, r, s=1.0, render=True):
    Z = SC.ref(); w = face_weight()
    if isinstance(r, str): r = field_multipliers(r)
    if isinstance(s, str): s = field_multipliers(s)
    rel, seeds, R, H, aff, pure = SC.variant(w, s, r, reseed=not (np.isscalar(s) and s == 1.0))
    P = C.V0 if m == 1.0 else RD.build({k: m for k in RD.FAMS})
    Vu, Fu = igl.upsample(P, C.F0); Nu = igl.per_vertex_normals(Vu, Fu); Sv = Vu + rel[:, None] * Nu
    # legibility per family: strength(m) / relief amplitude near the core (pure scale relief of this corner)
    Mr, _ = RD.metric(P); hv = np.where(Vu[:, 2] > 165)[0]; tr = cKDTree(Vu[hv]); leg = {}
    for k, (core, flank) in RD.sets().items():
        nb = np.unique(np.concatenate(tr.query_ball_point(C.V0[RD.HV[core]], 1.0))); a = pure[hv[nb]]; a = a[np.isfinite(a)]
        amp = float(np.percentile(a, 95) - np.percentile(a, 5)) if len(a) else float('nan'); leg[k] = Mr[k]['strength_cm'] / amp if amp > 0 else None
    hf = np.where((Vu[Fu[:, 0], 2] > 165))[0]; Fq = Fu[hf]; cr = lambda X: np.cross(X[Fq[:, 1]] - X[Fq[:, 0]], X[Fq[:, 2]] - X[Fq[:, 0]])
    ar = 0.5 * np.linalg.norm(cr(Vu), axis=1); ok = ar >= 0.25 * np.median(ar)
    Sc0 = SC.ref()['Vu'] + SC.ref()['disp'][:, None] * SC.ref()['N']; V0u = SC.ref()['Vu']
    cr0 = lambda X: np.cross(X[Fq[:, 1]] - X[Fq[:, 0]], X[Fq[:, 2]] - X[Fq[:, 0]])
    fa = (cr(Sv) * cr(Vu)).sum(1) < 0; fc = (cr0(Sc0) * cr0(V0u)).sum(1) < 0; folds = int((fa & ~fc & ok).sum())
    excess = int((fa & ok).sum()) - int((fc & ok).sum())                  # W3B1: excess folds over the canonical surfaced head (own-base orientation)
    fm = SC.field_metrics(w >= 0.9, pure, seeds)
    out = dict(tag=tag, m=m, r=r if np.isscalar(r) else 'per-field', s=s if np.isscalar(s) else 'per-field', legibility=leg, min_legibility_required=min(v for k, v in leg.items() if k in ('canthal', 'supraorbital', 'temporal', 'jugal', 'occipital', 'mandibular') and v is not None),
               new_folds=folds, excess_folds=excess, face_relief_cm=fm['relief_cm'], face_size_cm=fm['size_cm'], face_aspect=fm['aspect'], eye_vis_0=eye_vis_surf(Sv, Fu, 0), eye_vis_10=eye_vis_surf(Sv, Fu, 10))
    if render: SS.ensure('ix_' + tag, Sv, Fu, "hF:0:4:0:12:182:22;hF34:35:12:0:9:182:24;hP:90:0:0:6:181.5:26", res=900, box=lambda X: X[:, 2] > 168)
    return out
if __name__ == '__main__':
    cases = [tuple(a.split('@')) for a in sys.argv[1].split(';')]
    rp = W + '/' + os.environ.get('W3B_IX', 'results.json'); res = json.load(open(rp)) if os.path.exists(rp) else {}
    num = lambda v: v if v in ('rmin', 'rmax', 'smin', 'smax', 'rC1') else float(v)
    for tag, m, r, s in cases:
        if tag in res: continue
        res[tag] = corner(tag, float(m), num(r), num(s)); json.dump(res, open(rp, 'w'), indent=1)
        x = res[tag]; print(tag, 'excess %d minleg %.2f folds %d asp %.3f eye %.3f/%.3f' % (x['excess_folds'], x['min_legibility_required'], x['new_folds'], x['face_aspect'], x['eye_vis_0'], x['eye_vis_10']), {k: (round(v, 2) if v else v) for k, v in x['legibility'].items()}, flush=True)
