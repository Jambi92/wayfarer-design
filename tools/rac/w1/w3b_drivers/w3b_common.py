# RAC W3B (Saurin orbit / structural ridge / scale-field envelopes) common layer. NON-CANON DIAGNOSTICS on COPIES.
# Canonical W2 Saurin reference (RAC W2I6) read-only: scratchpad w2i6/canon (base, surface delta, seeds, region fields; hashes in
# reviews/rac-w2i6-sa-evidence/canon6.json). Nothing here writes into w2i6/canon.
# Frames: world cm (x right, f forward, u up); head-local = the TS6 skull frame of tools/rodin/gate1/wf_saurin_head63.py
#   head_local(P) = (P - AT - PIV) / HS + PIV   (creator-biology vary.py; HS = 1.08 head scale about the roof pivot)
# The skull SDF (w3b_head.py = diagnostic copy of head63 with ridge-amplitude multipliers RM) matches the canonical head surface to
# ~0.1 cm on the face (marching-cubes / polish residual); every diagnostic deformation is applied as a LEVEL-SET TRANSFER:
#   a canonical vertex p keeps its own canonical residual phi_ref(p) and is moved (optionally after a smooth tangential pre-warp) by Newton
#   steps until phi_new(p') = phi_ref(p) on the modified skull. Same topology throughout; region fields / seeds stay attached by index.
import os, sys, json, numpy as np, igl
os.environ.setdefault('BROW_INT', '5')
S = '/tmp/claude-0/-home-claude-wayfarer-design/19af7d50-3b61-5fda-9fe0-7a30770fb334/scratchpad'; CAN = S + '/w2i6/canon'; W = S + '/w3b'
D = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, D)
import w3b_head as HD
AT = np.array([0.0, 3.0, 179.3]); PIV = np.array([0.0, -3.0, 8.6]); HS = 1.08
def head_local(P): return (P - AT - PIV) / HS + PIV
def head_world(Lc): return (Lc - PIV) * HS + PIV + AT
_b = np.load(CAN + '/saurin_w2_final_base.npz'); V0 = _b['v'].astype(np.float64); F0 = _b['f'].astype(np.int64)
RINGS = [(u, 0.0, -3.0, 4.5, 4.5) for u in (-14, -10, -6, -2)]; CUT = -8.0      # neck stand-in (cancels in every difference; face residual ~0.1 cm)
L0 = head_local(V0)
HEADM = (L0[:, 2] > -7.5) & (np.abs(L0[:, 0]) < 12) & (L0[:, 1] > -15)          # head vertices (skull incl. mandible / gular floor) evaluated against the skull SDF
EYE0 = HD.EYE.copy()
def sdf(Lp, rm=None, eye_dx=0.0, eye_scale=1.0):
    """skull SDF in head-local cm with ridge multipliers rm and orbit-complex lateral shift eye_dx (head-local cm, per side, + = outward)"""
    old = dict(HD.RM); oe = dict(HD.EYE)
    try:
        if rm: HD.RM.update(rm)
        X = Lp[:, 0]; Fh = Lp[:, 1]; U = Lp[:, 2]
        if eye_dx:
            X = orbit_unshift(Lp, eye_dx)
        return HD.head_sdf(X, Fh, U, RINGS, CUT)
    finally:
        HD.RM.clear(); HD.RM.update(old); HD.EYE.clear(); HD.EYE.update(oe)
# ---- orbit complex lateral shift (RM-UF-03) as a smooth SPACE WARP of the skull SDF: points inside the orbital-platform influence
# region are pulled back by w(p) * dx toward the midline before evaluation, i.e. the orbit / lid / aperture / supraorbital crest / root /
# shelf and the orbit-adjacent platform are carried outward coherently, the rostrum, interorbital roof midline, cranial vault behind the
# platform, jaw and hinge stay put, and the smooth falloff of w re-fits the brow / canthal / postorbital / temporal support between them.
OC = np.array([EYE0['x'], EYE0['f'], EYE0['u']])
ORB_R0, ORB_R1 = 2.4, 5.2      # head-local cm: full carry inside R0 of the orbit centre, zero beyond R1 (smoothstep)
MIDW = 2.0     # head-local cm: interorbital roof span over which the spacing change is distributed (medial orbital margin at |x| ~ 2.2)
def orbit_weight(Lp):
    Xa = np.abs(Lp[:, 0]); d = np.sqrt((Xa - OC[0]) ** 2 + (Lp[:, 1] - OC[1]) ** 2 + (Lp[:, 2] - OC[2]) ** 2)
    t = np.clip((ORB_R1 - d) / (ORB_R1 - ORB_R0), 0, 1); w = t * t * (3 - 2 * t)
    mid = np.clip(Xa / MIDW, 0, 1); return w * mid * mid * (3 - 2 * mid)       # the midline never moves; the interorbital roof (|x| < MIDW) shares the change
def orbit_unshift(Lp, dx):
    """inverse of the forward warp x' = x + sign(x) dx w(x): fixed-point iteration (w smooth, |dx w'| << 1)"""
    X = Lp[:, 0].copy(); sg = np.where(Lp[:, 0] >= 0, 1.0, -1.0)
    for _ in range(6):
        Q = Lp.copy(); Q[:, 0] = X; X = Lp[:, 0] - sg * dx * orbit_weight(Q)
    return X
def orbit_shift_points(Lp, dx):
    sg = np.where(Lp[:, 0] >= 0, 1.0, -1.0); Q = Lp.copy(); Q[:, 0] = Lp[:, 0] + sg * dx * orbit_weight(Lp); return Q
_phi0 = None
def phi_ref():
    global _phi0
    if _phi0 is None:
        p = W + '/phi_ref.npy'
        if os.path.exists(p): _phi0 = np.load(p)
        else: os.makedirs(W, exist_ok=True); _phi0 = sdf(L0[HEADM]); np.save(p, _phi0)
    return _phi0
def grad(fn, Lp, h=0.02):
    g = np.zeros_like(Lp)
    for k in range(3):
        e = np.zeros(3); e[k] = h; g[:, k] = (fn(Lp + e) - fn(Lp - e)) / (2 * h)
    return g
_N0 = None
def normals0():
    global _N0
    if _N0 is None: _N0 = igl.per_vertex_normals(V0, F0)[HEADM]          # canonical normals (head-local = world directions; uniform scale)
    return _N0
def level_set_transfer(fn, pre=None, iters=4, along_normal=False):
    """canonical head vertices -> modified skull: optional tangential pre-warp, then Newton steps to phi_new = phi_ref (own residual kept).
    along_normal=True: 1-D Newton along the canonical vertex normal only (no tangential sliding; used for the ridge-strength family, where
    gradient projection let crest vertices slide and fold on the base mesh)"""
    tgt = phi_ref(); Lp = L0[HEADM].copy()
    if pre is not None: Lp = pre(Lp)
    if along_normal:
        n = normals0(); t = np.zeros(len(Lp))
        for _ in range(iters + 2):
            Q = Lp + t[:, None] * n; ph = fn(Q); h = 0.02; dd = (fn(Q + h * n) - fn(Q - h * n)) / (2 * h)
            dd = np.where(np.abs(dd) < 0.2, np.sign(dd + 1e-12) * 0.2, dd); t = t - np.clip((ph - tgt) / dd, -0.4, 0.4)
        Lp = Lp + t[:, None] * n
    for _ in range(0 if along_normal else iters):
        ph = fn(Lp); g = grad(fn, Lp); gg = (g * g).sum(1) + 1e-9
        step = np.clip((ph - tgt) / gg, -0.6, 0.6); Lp = Lp - step[:, None] * g
    P = V0.copy(); P[HEADM] = head_world(Lp)
    # feather: head vertices at the evaluation edge (neck) blend back to the canonical position
    u = L0[HEADM, 2]; f = L0[HEADM, 1]; a = np.clip((u + 7.5) / 1.5, 0, 1) * np.clip((f + 15.0) / 2.0, 0, 1)
    P[HEADM] = V0[HEADM] + (P[HEADM] - V0[HEADM]) * a[:, None]
    return P
# ---- surfaced (scale relief) meshes: canonical per-vertex scalar relief carried along the deformed normals (W2I4 convention)
_up = None
def upF():
    global _up
    if _up is None:
        _, Fu = igl.upsample(V0[:3], F0[:1]); z = np.load(S + '/w2i4/surf/fin_up.npz'); _up = z['F'].astype(np.int64)
    return _up
_disp = None
def canon_disp():
    global _disp
    if _disp is None:
        p = W + '/canon_disp.npy'
        if os.path.exists(p): _disp = np.load(p)
        else:
            Vu, Fu = igl.upsample(V0, F0); d = np.load(CAN + '/saurin_w2_final_surface_delta.npz')['d'].astype(np.float64)
            _disp = (d * igl.per_vertex_normals(Vu, Fu)).sum(1); np.save(p, _disp)
    return _disp
def surfaced(P, disp=None):
    Vu, Fu = igl.upsample(P, F0); d = canon_disp() if disp is None else disp
    return Vu + d[:, None] * igl.per_vertex_normals(Vu, Fu), Fu
def quality(Pa, Fa, Pref):
    """flipped faces vs the reference state, degenerate faces, edge-strain percentiles on changed edges"""
    na = np.cross(Pa[Fa[:, 1]] - Pa[Fa[:, 0]], Pa[Fa[:, 2]] - Pa[Fa[:, 0]]); nr = np.cross(Pref[Fa[:, 1]] - Pref[Fa[:, 0]], Pref[Fa[:, 2]] - Pref[Fa[:, 0]])
    area = 0.5 * np.linalg.norm(na, axis=1); flip = int(((na * nr).sum(1) < 0).sum()); deg = int((area < 1e-10).sum())
    flip_ns = int((((na * nr).sum(1) < 0) & (0.5 * np.linalg.norm(nr, axis=1) >= 1e-4)).sum())       # excluding canonical sliver faces (< 1e-4 cm^2)
    E = np.vstack([Fa[:, [0, 1]], Fa[:, [1, 2]], Fa[:, [2, 0]]]); la = np.linalg.norm(Pa[E[:, 0]] - Pa[E[:, 1]], axis=1); lr = np.linalg.norm(Pref[E[:, 0]] - Pref[E[:, 1]], axis=1)
    r = la / np.maximum(lr, 1e-12); ch = np.abs(r - 1) > 1e-6
    return {"flipped": flip, "flipped_nonsliver": flip_ns, "degenerate": deg, "strain_pct": (np.percentile(r[ch], [0.1, 1, 50, 99, 99.9]).round(4).tolist() if ch.any() else [1, 1, 1, 1, 1]),
            "changed_edges": int(ch.sum())}
def save_head_npz(path, P, Fa, box=None):
    """crop to the head (render speed) and save rclose-format npz (P, f)"""
    keep = (P[:, 2] > 166) if box is None else box(P)
    idx = np.where(keep)[0]; m = np.full(len(P), -1); m[idx] = np.arange(len(idx)); ff = Fa[keep[Fa].all(1)]
    np.savez(path, P=P[idx].astype(np.float32), f=m[ff].astype(np.int32))
RC = S + '/w2i/rodin/g1/rclose.py'
HEADV = "hF:0:3:0:10:183:24;hP:90:0:0:8:182:26;hF34:40:12:0:8:183:26;hT:0:89:0:5:184:30"
def render(npz, tag, views=HEADV, res=900):
    import subprocess
    subprocess.run(['python3', RC], env=dict(os.environ, VIEWS=views, NPZ=npz, TAG=tag, RES=str(res)), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
