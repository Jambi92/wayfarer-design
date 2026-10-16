# RM-OT-05AA AA0: read-only macro-frame comparison between a donor mesh and the accepted W1 Gorrund ARM (GO_r6), height-normalised.
# Horizontal sections at fractions of overall height; the trunk loop is the one enclosing x~0, leg loops are those at x>0 below the
# crotch, arm loops are the outermost loops beside the trunk/legs. Reports widths/depths as % of height, crotch, fingertip and
# shoulder-junction heights as % of height. Nothing is written to either mesh.
# Usage: python3 aa_macro.py OUT.json NAME=PATH[:fmt] ...   fmt: npzrev (V metres glTF, review frame) | gor6 (GO_r6 cm, front +Y)
import sys, json, numpy as np, trimesh
def load(spec):
    name, p = spec.split('=', 1); fmt = 'npzrev'
    if ':' in p and p.rsplit(':', 1)[1] in ('npzrev', 'gor6'): p, fmt = p.rsplit(':', 1)
    d = np.load(p, allow_pickle=True)
    if fmt == 'gor6':
        V = d['V'].astype(float).copy(); V[:, 1] *= -1           # front -> -Y like the review frame
        F = d['F']
        if 'keep' in d.files:                                    # drop helper vertices outside the delivered surface
            k = d['keep']; F = F[k[F].all(1)]
    else:
        P = d['V'].astype(float); V = np.stack([P[:, 0], -P[:, 2], P[:, 1]], 1) * 100; F = d['F']
    u = np.unique(F); mp = -np.ones(len(V), np.int64); mp[u] = np.arange(len(u)); V = V[u]; F = mp[F]   # referenced vertices only
    V[:, 2] -= V[:, 2].min(); m = trimesh.Trimesh(V, F, process=True)
    # centre on the trunk midline (x, y of the trunk section at 0.62 H) so left/right and tail filters are body-relative
    H = V[:, 2].max(); s = m.section(plane_origin=[0, 0, 0.62 * H], plane_normal=[0, 0, 1])
    e = max(s.discrete, key=lambda e: np.ptp(e[:, 0])); c = e.mean(0); m.apply_translation([-c[0], -c[1], 0]); return name, m
def loops(m, z):
    s = m.section(plane_origin=[0, 0, z], plane_normal=[0, 0, 1])
    if s is None: return []
    out = []
    for e in s.discrete:
        out.append(dict(c=e.mean(0), xmin=e[:, 0].min(), xmax=e[:, 0].max(), ymin=e[:, 1].min(), ymax=e[:, 1].max(), n=len(e)))
    return out
def measure(m):
    H = m.bounds[1][2]; r = dict(height_raw=round(H, 1))
    # crotch: lowest height (scanning up) at which a single loop spans x = 0 with trunk-like width
    crotch = None
    for f in np.arange(0.30, 0.70, 0.0025):
        if any(l['xmin'] < -0.02 * H and l['xmax'] > 0.02 * H and l['xmax'] - l['xmin'] > 0.10 * H and abs(l['c'][1]) < 0.07 * H for l in loops(m, f * H)): crotch = f; break
    r['crotch_pct'] = round(100 * crotch, 1) if crotch else None
    # fingertip: lowest height with a hand/arm loop well outside the thigh (|c_x| > 0.14 H, not behind the body)
    tip = None
    for f in np.arange(0.70, 0.20, -0.0025):
        if any(abs(l['c'][0]) > 0.14 * H and abs(l['c'][1]) < 0.10 * H for l in loops(m, f * H)): tip = f
    r['fingertip_pct'] = round(100 * tip, 1) if tip else None
    # trunk sections
    for nm, f in [('chest_72', 0.72), ('upper_abd_66', 0.66), ('waist_60', 0.60), ('hip_53', 0.53)]:
        L = [l for l in loops(m, f * H) if l['xmin'] < 0 < l['xmax'] and abs(l['c'][1]) < 0.07 * H]
        if L:
            l = max(L, key=lambda l: l['xmax'] - l['xmin']); r[nm] = dict(width_pct=round(100 * (l['xmax'] - l['xmin']) / H, 1), depth_pct=round(100 * (l['ymax'] - l['ymin']) / H, 1))
    for nm, f in [('thigh_40', 0.40), ('knee_28', 0.28), ('calf_20', 0.20), ('ankle_05', 0.05)]:
        L = [l for l in loops(m, f * H) if l['c'][0] > 2 and l['xmin'] > -1 and (l['xmax'] - l['xmin']) > 0.02 * H
             and abs(l['c'][1]) < 0.08 * H and abs(l['c'][0]) < 0.14 * H]      # excludes tail loops (behind) and hand loops (lateral)
        if L:
            l = min(L, key=lambda l: abs(l['c'][0] - 0.09 * H)); r[nm] = dict(width_pct=round(100 * (l['xmax'] - l['xmin']) / H, 1), depth_pct=round(100 * (l['ymax'] - l['ymin']) / H, 1))
    # shoulder breadth: max trunk+arm width between 0.74H and 0.86H (outer extent)
    best = 0
    for f in np.arange(0.74, 0.86, 0.005):
        L = loops(m, f * H)
        if L: best = max(best, max(l['xmax'] for l in L) - min(l['xmin'] for l in L))
    r['max_breadth_74_86_pct'] = round(100 * best / H, 1)
    return r
if __name__ == '__main__':
    out = {}
    for spec in sys.argv[2:]:
        n, m = load(spec); out[n] = measure(m); print(n, json.dumps(out[n]))
    json.dump(out, open(sys.argv[1], 'w'), indent=1)
