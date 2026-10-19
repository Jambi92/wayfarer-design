"""RAC RP1: rig-facing landmark package (contract §12) on a Gorrund mesh in the analysis frame (cm; x subject left, f forward, u up).
Source mode (labels available): joint planes come from the boundaries between the sculpt's segment labels; each landmark is the
centroid of the mesh cross-section in that plane. Re-measure mode: the SAME planes (from the source landmark file) are re-sectioned on
another mesh (production), so drift = production section centroid - source section centroid (T-6).
Usage: source:  python3 rp1_landmarks.py source weld.npz OUT.json
        measure: python3 rp1_landmarks.py measure mesh.npz SOURCE_LANDMARKS.json OUT.json"""
import sys, json, numpy as np
from scipy.sparse import coo_matrix
from scipy.sparse.csgraph import dijkstra

def section_centroid(V, F, p, n, near, R):
    """centroid (by edge-plane intersection points) of the plane section of the mesh within radius R of `near`"""
    d = (V - p) @ n; E = np.concatenate([F[:, [0, 1]], F[:, [1, 2]], F[:, [2, 0]]]); E = np.unique(np.sort(E, 1), axis=0)
    s = d[E[:, 0]] * d[E[:, 1]] < 0; E = E[s]; t = d[E[:, 0]] / (d[E[:, 0]] - d[E[:, 1]])
    X = V[E[:, 0]] + (V[E[:, 1]] - V[E[:, 0]]) * t[:, None]; X = X[np.linalg.norm(X - near, axis=1) < R]
    if len(X) < 8: return None, 0
    # the section loop closest to `near` (largest connected cluster by proximity is enough for limb / neck / tail sections)
    return X.mean(0), len(X)

def load(p):
    z = np.load(p); V = z['V'].astype(float) if 'V' in z.files else z['v'].astype(float); F = (z['F'] if 'F' in z.files else z['f']).astype(np.int64)
    return z, V, F

def source(path, out):
    z, V, F = load(path); V = V * np.array([1, -1, 1])                  # Blender (front -y) -> analysis frame (f forward)
    W = {k[2:]: z[k] > 0.5 for k in z.files if k.startswith('w_')}; H = V[:, 2].max()
    E = np.unique(np.sort(np.concatenate([F[:, [0, 1]], F[:, [1, 2]], F[:, [2, 0]]]), 1), axis=0)
    L = {}
    pairs = {'shoulder': ('trunk', 'upperarm'), 'elbow': ('upperarm', 'forearm'), 'wrist': ('forearm', 'hand'),
             'hip': ('trunk', 'thigh'), 'knee': ('thigh', 'shin'), 'ankle': ('shin', 'foot')}
    for j, (a, b) in pairs.items():
        for s in ('L', 'R'):
            ga = W[a] if a == 'trunk' else W[a + '_' + s]; gb = W[b + '_' + s]
            m = (ga[E[:, 0]] & gb[E[:, 1]]) | (gb[E[:, 0]] & ga[E[:, 1]]); P = (V[E[m, 0]] + V[E[m, 1]]) / 2
            c = P.mean(0); u, sv, vt = np.linalg.svd(P - c); n = vt[2]
            R = 1.6 * np.sqrt(((P - c) ** 2).sum(1)).max()
            cc, k = section_centroid(V, F, c, n, c, R)
            L['%s_%s' % (j, s)] = {'kind': 'joint section (segment-label boundary plane)', 'plane_point': c.tolist(), 'plane_normal': n.tolist(),
                                   'radius_cm': float(R), 'centroid': (cc if cc is not None else c).tolist(), 'n_points': int(k)}
    L['pelvis_root'] = {'kind': 'derived: midpoint of hip section centroids', 'centroid': ((np.array(L['hip_L']['centroid']) + np.array(L['hip_R']['centroid'])) / 2).tolist()}
    # neck: horizontal sections at the narrowest trunk level between shoulders and head
    sh = max(L['shoulder_L']['centroid'][2], L['shoulder_R']['centroid'][2]); best = None
    for zz in np.arange(sh, 0.95 * H, 0.5):
        cc, k = section_centroid(V, F, np.array([0, 0, zz]), np.array([0, 0, 1.0]), np.array([0, np.median(V[W['trunk'], 1]), zz]), 25)
        if cc is None: continue
        sel = W['trunk'] & (np.abs(V[:, 2] - zz) < 0.3); w = np.ptp(V[sel, 0]) if sel.sum() > 10 else 1e9
        if best is None or w < best[0]: best = (w, zz, cc)
    L['neck_min'] = {'kind': 'horizontal section at minimum neck breadth', 'plane_point': [0, 0, float(best[1])], 'plane_normal': [0, 0, 1], 'radius_cm': 25.0, 'centroid': best[2].tolist(), 'breadth_cm': float(best[0])}
    mid = np.abs(V[:, 0] - L['neck_min']['centroid'][0]) < 3.0
    L['crown'] = {'kind': 'highest vertex within 3 cm of the neck-section midline (ears excluded)', 'centroid': V[mid][np.argmax(V[mid, 2])].tolist()}
    L['highest_point'] = {'kind': 'highest vertex overall (ear tip)', 'centroid': V[np.argmax(V[:, 2])].tolist()}
    # tail chain: geodesic path root -> tip, 12 equal arc-length stations, sectioned perpendicular to the path
    band = W['trunk'] & (np.abs(V[:, 2] - 0.5296 * H) < 4) & (np.abs(V[:, 0] - 1.4) < 8); r = int(np.argmin(np.where(band, V[:, 1], 1e9)))
    tip = int(np.argmin(V[:, 1]))
    w = np.linalg.norm(V[E[:, 0]] - V[E[:, 1]], axis=1); G = coo_matrix((np.r_[w, w], (np.r_[E[:, 0], E[:, 1]], np.r_[E[:, 1], E[:, 0]])), shape=(len(V), len(V))).tocsr()
    dist, pred = dijkstra(G, indices=tip, return_predecessors=True)
    path = [r]
    while path[-1] != tip: path.append(pred[path[-1]])
    P = V[path]; seg = np.r_[0, np.cumsum(np.linalg.norm(np.diff(P, axis=0), axis=1))]
    chain = []
    for i, a in enumerate(np.linspace(0, seg[-1], 13)):
        k = min(np.searchsorted(seg, a), len(P) - 1); k0, k1 = max(k - 15, 0), min(k + 15, len(P) - 1); t = P[k1] - P[k0]; t /= np.linalg.norm(t)
        cc, n = section_centroid(V, F, P[k], t, P[k], 7.0)
        chain.append({'station': i, 'arc_cm': float(a), 'plane_point': P[k].tolist(), 'plane_normal': t.tolist(), 'radius_cm': 7.0,
                      'centroid': (cc if cc is not None else P[k]).tolist(), 'n_points': int(n)})
    L['tail_chain'] = {'kind': 'surface geodesic root->tip, 12 equal arc-length segments, perpendicular sections', 'root_surface_point': V[r].tolist(),
                       'tip_vertex': V[tip].tolist(), 'surface_path_length_cm': float(seg[-1]), 'stations': chain}
    # toe tips: in each foot's own frame (ankle -> foremost foot point); candidates in the front 6 cm, below 5 cm height,
    # clustered on the lateral coordinate; each tip = the foremost point of its cluster. Finger tips are left to manual placement
    # (the sculpt hands are partly flexed, so an extreme-point rule is not anatomical).
    from scipy.cluster.vq import kmeans2
    for s_ in ('L', 'R'):
        m = W['foot_' + s_]; X = V[m]; a = np.array(L['ankle_' + s_]['centroid']); fp = X[np.argmax(((X - a) * [1, 1, 0]) @ np.array([0, 1, 0]))]
        ax = (fp - a) * [1, 1, 0]; ax /= np.linalg.norm(ax); lat = np.cross([0, 0, 1], ax)
        pr = (X - a) @ ax; cand = X[(pr > pr.max() - 6) & (X[:, 2] < 5)]
        cen, lab = kmeans2(((cand - a) @ lat)[:, None], 5, seed=1, minit='++')
        pts = [cand[lab == i][np.argmax(((cand[lab == i] - a) @ ax))].tolist() for i in range(5) if (lab == i).any()]
        pts.sort(key=lambda q: (np.array(q) - a) @ lat)
        L['toe_tips_' + s_] = {'kind': 'foot-frame foremost point per lateral cluster (k=5)', 'foot_axis': ax.tolist(), 'points': pts}
    L['_manual_pending'] = ['eye_L', 'eye_R', 'jaw_hinge_L', 'jaw_hinge_R', 'chin', 'mouth_corners', 'ear_root/tip L/R',
                            'sternoclavicular L/R', 'acromion L/R', 'scapular proxy L/R', 'finger tips L/R', 'finger roots (MCP)', 'ball (MTP) line L/R', 'head pivot']
    L['_frame'] = 'analysis frame, cm: x = subject left, f = forward, u = up; z = 0 ground'
    json.dump(L, open(out, 'w'), indent=1); print('LANDMARKS', len(L))

def measure(path, srcp, out):
    z, V, F = load(path); S = json.load(open(srcp)); R = {}
    for k, v in S.items():
        if isinstance(v, dict) and 'plane_point' in v:
            cc, n = section_centroid(V, F, np.array(v['plane_point']), np.array(v['plane_normal']), np.array(v['plane_point']), v['radius_cm'])
            R[k] = {'drift_mm': float(np.linalg.norm(cc - np.array(v['centroid'])) * 10) if cc is not None else None}
        if k == 'tail_chain':
            for st in v['stations']:
                cc, n = section_centroid(V, F, np.array(st['plane_point']), np.array(st['plane_normal']), np.array(st['plane_point']), st['radius_cm'])
                R['tail_%02d' % st['station']] = {'drift_mm': float(np.linalg.norm(cc - np.array(st['centroid'])) * 10) if cc is not None else None}
    json.dump(R, open(out, 'w'), indent=1); print(json.dumps(R)[:2000])

if __name__ == '__main__':
    if sys.argv[1] == 'source': source(sys.argv[2], sys.argv[3])
    else: measure(sys.argv[2], sys.argv[3], sys.argv[4])
