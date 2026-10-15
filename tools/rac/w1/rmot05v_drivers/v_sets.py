# RM-OT-05V: frozen per-step SET builders. Each builder reads the CURRENT checkpoint state and writes the point sets the step's
# region / transplant / primitives reference (Voronoi A = vertices to rebuild, B = everything kept). All selections are
# deterministic geometric / connectivity rules recorded here; numbers are builder-chosen construction values (R-14).
# Usage: python3 v_sets.py STEP_NAME STATE.npz OUTDIR   -> writes OUTDIR/<files> and prints a JSON summary
import sys, json, hashlib, numpy as np, trimesh
sys.path.insert(0, __import__('os').path.dirname(__import__('os').path.abspath(__file__)))
from v_engine import components
from scipy.spatial import cKDTree
X0 = -0.5   # bilateral plane (median mirror fit of the trunk, readiness/symmetry_fit.json)

def load(p):
    d = np.load(p); return d['V'].astype(np.float64), d['F'], d['vid']

def arm_component(V, F, seed, zmax=150.0):
    keep = (V[F][:, :, 2].max(1) < zmax); lab = components(F[keep], len(V)); i = int(np.argmin(np.linalg.norm(V - np.asarray(seed, float), axis=1)))
    return lab == lab[i]

def save(out, name, P):
    import os; p = os.path.join(out, name); np.save(p, P); return dict(file=name, points=int(len(P)), sha256=hashlib.sha256(open(p, 'rb').read()).hexdigest())

def B1(V, F, vid, out):
    arm = arm_component(V, F, [41, 11, 120]); A = arm & (V[:, 2] >= 102.8) & (V[:, 2] <= 146.0)
    return dict(A=save(out, 'B1_A.npy', V[A]), B=save(out, 'B1_B.npy', V[~A]), rule='+X forearm: the +X arm connected component below z 150 with 102.8 <= z <= 146 (wrist above the fist to above the bracer top)')

def B2(V, F, vid, out):
    arm = arm_component(V, F, [41, 11, 120])
    up = (V[:, 2] >= 148) & (V[:, 2] <= 176.5) & (V[:, 0] >= 23.5)
    a = np.array([36.5, 1, 148.]); b = np.array([29.5, -1, 175.]); ab = b - a; t = np.clip(((V - a) @ ab) / (ab @ ab), 0, 1)
    dax = np.linalg.norm(V - (a + t[:, None] * ab), axis=1)
    Ap = arm | (up & (dax < 13))
    M = V[Ap].copy(); M[:, 0] = 2 * X0 - M[:, 0]; env = cKDTree(M).query(V)[0]
    wreck = (V[:, 0] <= -24) & (V[:, 2] <= 177) & (env < 4.0)
    keep = (V[F][:, :, 2].max(1) < 150); lab = components(F[keep], len(V))
    for c in np.unique(lab[(V[:, 0] < -27) & (V[:, 2] < 150) & (V[:, 2] > 84)]):
        m = lab == c
        if V[m][:, 0].mean() < -27 and m.sum() < 20000: wreck |= m
    return dict(A=save(out, 'B2_A.npy', V[wreck]), B=save(out, 'B2_B.npy', V[~wreck]), selA=save(out, 'B2_selA.npy', V[Ap]), selB=save(out, 'B2_selB.npy', V[~Ap]),
                rule='-X arm wreck (open 05N slab-seam remains + detached hand fragments) = vertices x <= -24, z <= 177 within 4 cm of the mirrored +X arm, '
                     'plus -X components below z 150 with mean x < -27; transplant source = +X arm component below z 150 + upper arm (z 148-176.5, x >= 23.5, '
                     'within 13 cm of the upper-arm axis), mirrored across x = %.2f' % X0)

def D(V, F, vid, out):
    arms = arm_component(V, F, [41, 11, 120]) | arm_component(V, F, [-42, 11, 120])
    A = (V[:, 2] >= 66) & (V[:, 2] <= 147) & ~arms
    return dict(A=save(out, 'D_A.npy', V[A]), B=save(out, 'D_B.npy', V[~A]), rule='pelvis slab 66 <= z <= 147 minus both arm components (forearms / hands stay outside; boundary mid-way in the hand-hip gaps)')

def E(V, F, vid, out):
    """whole head / neck / upper-back-mane cap above a clean skin band (z 168) is rebuilt; the face and throat are re-extracted from
    the source inside a facial mask, so the region boundary lies only on clean shoulder / chest / back skin."""
    X = V[:, 0] - X0; Y = V[:, 1]; Z = V[:, 2]; ax = np.abs(X)
    cap = (Z >= 168) & ((ax < 26) | ((Y < 2) & (ax < 33))) & ~((ax > 20) & (Z < 175.5))
    A = cap
    # ears: the -X pinna (lateral flare above z 226) is the intact source ear; the +X side carries only a hair spike, so the +X ear is the
    # bilateral counterpart (R-5) of the -X ear
    ear = (Z >= 226) & (X > -25) & (X < -11) & (Y > 3) & (Y < 19)
    fs = ear[F].all(1); u = np.unique(F[fs]); mp = -np.ones(len(V), int); mp[u] = np.arange(len(u)); Ve = V[u]; Fe = mp[F[fs]]
    Vm = Ve.copy(); Vm[:, 0] = 2 * X0 - Vm[:, 0]
    import os; ep = os.path.join(out, 'E_ears.obj'); trimesh.Trimesh(np.vstack([Ve, Vm]), np.vstack([Fe, Fe[:, ::-1] + len(Ve)]), process=False).export(ep)
    return dict(A=save(out, 'E_A.npy', V[A]), B=save(out, 'E_B.npy', V[~A]), ears=dict(file='E_ears.obj', faces=int(fs.sum()), sha256=hashlib.sha256(open(ep, 'rb').read()).hexdigest()),
                rule='head / neck / mane cap: z >= 168 with |x| < 26, or back (y < 2) with |x| < 33; nothing lateral of |x| 20 below z 175.5 (clear of the '
                     'protected U6-U8 posterior-axilla repair, z <= 172.9). Inside, the facial mask and throat are re-extracted from the source; ears '
                     '(the two lateral pinnae above z 226) are re-attached from the source as identity anatomy; everything else is INFERRED.')

BUILD = dict(B1=B1, B2=B2, D=D, E=E)
if __name__ == '__main__':
    name, st, out = sys.argv[1:4]; V, F, vid = load(st); r = BUILD[name](V, F, vid, out); print(json.dumps(r))
