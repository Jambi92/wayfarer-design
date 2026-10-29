# hv_ear_domains.py OUT.json LABEL:KIND:PATH[:HEAD] ... : Halvren mixed-ear order §17 / §18 -- generic, mesh-based EAR-DOMAIN coordinates of one external ear
# (both sides, averaged), measured identically on (a) the v005 family human auricle of a family realization (KIND fam: PATH = fam npz, HEAD = record id
# for the R-6 w_ears zone) and (b) any engineering-topology ear branch (KIND branch: PATH = ear_build branch npz). Common frame for both: the 52-vertex
# v005 root loop (centroid O, lateral n, posterior b, up u; ear_branch_lib.root_data) and the hidden-ear skull height field (skull_field), so that a
# Marchfolk ear and an elf / Halvren ear on the same head are measured by one rule. 'free' = ear points > 0.25 cm above the hidden-ear skull.
#   length_over_HH       side-view diameter of the free auricle / head height
#   width_over_length    max side-view extent across the diameter axis / length
#   projection_deg       angle between the best-fit plane of the free auricle and the root (skull) plane
#   upward_ext_over_HH   free-auricle top above the root-loop top / HH
#   backward_angle_deg   side-view inclination of the diameter axis from vertical (posterior +)
#   tip_angle_deg        side-view outline (convex hull) angle at the top, chords 1.0 cm x head scale
#   lobe_fraction        free auricle below the lowest skin-attachment point / length
#   root_line_deg        side-view inclination of the anterior skin-attachment line from vertical (root relation to the skull)
#   concha_depth_over_L  front-surface bowl depth (grey closing of the outer surface height map, disk 0.22 L) / length
#   tragus_height_frac   height fraction of the deepest concha point in the anterior 55 % / lower 60 % of the auricle (cavum) -- the tragus / intertragic level that fronts it
#   helix_fullness       side-view hull area / (length x width) (rounded helix ~ 0.75, tapered leaf lower)
import sys, os, json, numpy as np, scipy.sparse as sp
os.environ.setdefault('EAR_TOPO', 'v002')
sys.path.insert(0, '/home/claude/wayfarer-design/tools/rac/rp/fenn_rp3_v001')
import ear_branch_lib as E
from scipy.spatial import ConvexHull, cKDTree
from scipy import ndimage
RA = '/home/claude/wayfarer-design/reviews/reference-assets/r6'; CF = os.environ.get('EAR_CF', '/tmp/claude-0/rt/hv/hpe')
FLOOR = dict(length_over_HH=0.01, width_over_length=0.03, projection_deg=3.0, upward_ext_over_HH=0.01, backward_angle_deg=3.0, tip_angle_deg=5.0, lobe_fraction=0.03,
             root_line_deg=3.0, concha_depth_over_L=0.02, tragus_height_frac=0.04, helix_fullness=0.03)   # SD floors for normalisation (measurement resolution)
DOM = ['length_over_HH', 'width_over_length', 'projection_deg', 'upward_ext_over_HH', 'backward_angle_deg', 'tip_angle_deg', 'lobe_fraction', 'root_line_deg',
       'concha_depth_over_L', 'tragus_height_frac', 'helix_fullness']
_rd = {}
def frame(head, sd):
    if (head, sd) not in _rd:
        fz = np.load('%s/fam/%s_fam.npz' % (CF, head)); V0 = fz['V'].astype(float); Q0 = np.asarray(fz['Q']); si = fz['src_index']
        M0 = sp.csr_matrix((fz['M_data'], fz['M_indices'], fz['M_indptr']), shape=tuple(fz['M_shape'])); we = M0 @ np.load('%s/%s_r6.npz' % (RA, head))['w_ears'][si].astype(float)
        sg = 1 if sd == 'l' else -1; rd = E.root_data(V0, Q0, we, sg); rd['skull'] = E.skull_field(V0, Q0, rd, sg)[0]; rd['V_loop'] = V0[rd['loop']]; _rd[(head, sd)] = rd
    return _rd[(head, sd)]
def hull_angle(P, top, ch):
    h = ConvexHull(P); H = P[h.vertices]; k = int(np.argmin(np.linalg.norm(H - top, axis=1))); n = len(H)
    def walk(dirn):
        acc = 0.0; i = k
        while True:
            j = (i + dirn) % n; seg = np.linalg.norm(H[j] - H[i])
            if acc + seg >= ch or j == k: return H[i] + (H[j] - H[i]) * min(1.0, (ch - acc) / max(seg, 1e-9))
            acc += seg; i = j
    a = walk(1) - H[k]; b = walk(-1) - H[k]; return float(np.degrees(np.arccos(np.clip(a @ b / np.linalg.norm(a) / np.linalg.norm(b), -1, 1)))), float(h.volume)
def one(X, rd, HH, sc):
    O, n, b, u = rd['O'], rd['n'], rd['b'], rd['u']; d = X - O; B = d @ b; U = d @ u; bu = np.c_[B, U]; hgt = d @ n - rd['skull'](bu)
    fr = hgt > 0.25; F = bu[fr]
    h = ConvexHull(F); Hv = F[h.vertices]; D = np.linalg.norm(Hv[:, None] - Hv[None], axis=2); i, j = np.unravel_index(np.argmax(D), D.shape)
    lo, hi = (Hv[i], Hv[j]) if Hv[i][1] < Hv[j][1] else (Hv[j], Hv[i]); L = float(D[i, j]); ax = (hi - lo) / L; pr = np.array([-ax[1], ax[0]])
    W = float((F @ pr).max() - (F @ pr).min())
    P3 = d[fr] - d[fr].mean(0); nrm = np.linalg.svd(P3, full_matrices=False)[2][2]; proj = float(np.degrees(np.arccos(min(1.0, abs(nrm @ n)))))
    top = F[np.argmax(F @ ax)]; tip, area = hull_angle(F, top, 1.0 * sc)
    Ul = (rd['V_loop'] - O) @ u
    # skin attachment line: attached ear points (< 0.12 cm above skull) within 0.35 cm of a free point
    att = np.nonzero(~fr & (hgt < 0.12))[0]; dd, _ = cKDTree(d[fr]).query(d[att]); att = att[dd < 0.35]
    Bc = F[:, 0].mean(); antA = att[B[att] < Bc]
    lobe = float(max(0.0, U[antA].min() - F[:, 1].min()) / L) if len(antA) else 0.0
    if len(antA) > 3:
        A2 = bu[antA] - bu[antA].mean(0); v = np.linalg.svd(A2, full_matrices=False)[2][0]; v = v if v[1] > 0 else -v; rl = float(np.degrees(np.arctan2(v[0], v[1])))
    else: rl = float('nan')
    # front-surface height map (outermost hgt per 0.1 cm cell) and its grey-closing depth inside the free hull
    g = 0.1; mn = F.min(0) - 0.5; ij = np.floor((bu - mn) / g).astype(int); nx, ny = (F.max(0) - mn + 0.5) / g; nx, ny = int(nx) + 1, int(ny) + 1
    Hm = np.full((nx, ny), -9.0); ok = (ij[:, 0] >= 0) & (ij[:, 1] >= 0) & (ij[:, 0] < nx) & (ij[:, 1] < ny)
    np.maximum.at(Hm, (ij[ok, 0], ij[ok, 1]), hgt[ok]); fill = Hm > -9; Hm = np.where(fill, Hm, ndimage.grey_dilation(np.where(fill, Hm, -9.0), size=3))
    r = max(2, int(round(0.22 * L / g))); yy, xx = np.mgrid[-r:r + 1, -r:r + 1]; fp = (xx ** 2 + yy ** 2) <= r * r
    Cl = ndimage.grey_closing(Hm, footprint=fp); dep = Cl - Hm
    cells = np.c_[np.nonzero(fill)]; cen = cells * g + mn + g / 2; inside = E._inside_dist(Hv, cen) > 0.25 * sc
    conc = float(np.percentile(dep[fill][inside], 99) / L) if inside.any() else 0.0
    Uf = F[:, 1]; ur = Uf.max() - Uf.min(); Bf = F[:, 0]; reg = inside & (cen[:, 0] < Bf.min() + 0.55 * (Bf.max() - Bf.min())) & (cen[:, 1] < Uf.min() + 0.6 * ur); dv = np.where(reg, dep[fill], -1); cav = cen[int(np.argmax(dv))] if reg.any() else None
    trag = float((cav[1] - Uf.min()) / ur) if cav is not None else float('nan')     # the tragus fronts the cavum: deepest concha point height fraction
    return dict(length_over_HH=L / HH, width_over_length=W / L, projection_deg=proj, upward_ext_over_HH=float(F[:, 1].max() - Ul.max()) / HH,
                backward_angle_deg=float(np.degrees(np.arctan2(ax[0], ax[1]))), tip_angle_deg=tip, lobe_fraction=lobe, root_line_deg=rl, concha_depth_over_L=conc,
                tragus_height_frac=trag, helix_fullness=float(area / (L * W)), raw=dict(length_cm=L, width_cm=W, free_points=int(fr.sum()), attach_points=int(len(antA))))
def measure(kind, path, head):
    HH, sc = E.head_scale('%s/%s_r6.npz' % (RA, head)); z = np.load(path); V = z['V'].astype(float); out = {}
    for sd in ('l', 'r'):
        rd = frame(head, sd)
        if kind == 'fam': X = V[rd['interior']]
        else: X = V[(z['side'] == sd) & np.isin(z['part'], ['front', 'back', 'rim', 'cuff'])]
        out[sd] = one(X, rd, HH, sc)
    m = {k: float(np.mean([out[s][k] for s in out])) for k in DOM}; m['sides'] = out; m['HH_cm'] = HH; return m
if __name__ == '__main__':
    res = {}
    for it in sys.argv[2:]:
        lab, kind, path, head = it.split(':'); res[lab] = measure(kind, path, head); print(lab, {k: round(res[lab][k], 3) for k in DOM}, flush=True)
    json.dump(dict(domains=DOM, frame='v005 root loop + hidden-ear skull field of the common head', items=res), open(sys.argv[1], 'w'), indent=1)
