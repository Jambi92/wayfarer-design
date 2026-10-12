"""RAC RM-OT-05D: TRUE SKELETAL ENVELOPE (protected bony floor) for the race base-surface stage, and the verified outward-normal convention.

WHY (RM-OT-05D §3). In the AD-G14 route the skeleton surface (-LEAN) is the MPFB body at muscle 0 / weight 0. It is not bone: it still carries
a human gluteal mass, pectoral contour, deltoid cap, calf / biceps bellies, abdominal wall and erector mass. 05C protected that whole surface
as if it were bone, which froze the human soft organization exactly where the race anatomy has to differ.

DEFINITION. The protected floor is the -LEAN surface moved inward along its OUTWARD normal by a documented soft-tissue depth d(v) >= 0:
        floor(v) = lean(v) - d(v) * n_out(v)
  - d is ~0.3-0.8 cm where bone is subcutaneous: joint condyles / epicondyles, patella, malleoli, olecranon, wrist, hands and feet,
    clavicle, acromion, sternum, spinous line, sacrum, iliac crest, ASIS, anteromedial tibia. These are the joint extents and bony
    landmarks the W2 relations read.
  - d is the minimum-composition muscle / fat depth over bone elsewhere:
      - gluteal mass;
      - pectoral;
      - deltoid cap;
      - trapezius;
      - erector / paraspinal;
      - scapular cover;
      - abdominal wall (the abdominal CAVITY is kept: only the wall depth);
      - lateral flank;
      - limb shafts down to a bone-radius model around the accepted long-bone axis.
  - limb shafts: the floor never comes closer to the bone axis than r_bone = k_seg x the segment's narrowest lean section radius
    (humerus 0.35, radius + ulna 0.50, femur 0.32, tibia + fibula 0.45). Joint zones are held at subcutaneous depth.
The map is authored in each body's own anatomical coordinates (trunk: r = (u - hip) / (sst - hip), angle about the section centre; limbs:
t along the bone, angle about the bone axis) and blended by skin weights, then mesh-smoothed. So it transports across stature, frame and pose.
It never moves joints, bone axes, bone lengths or bone scales. Where the separation cannot be made from this skeleton data it is recorded in
DEPENDENCIES (RM-OT-05D §3.1).

NORMALS. race_surface._normals returns inward normals on this mesh (negative signed volume). outward_normals() orients by the signed volume
of the kept mesh and test_outward() checks it on anatomical probes (chest front +y, back -y, crown +z, sole -z, lateral thigh +/-x)."""
import json, numpy as np

ARMK = ("upperarm_l", "upperarm_r", "lowerarm_l", "lowerarm_r", "hand_l", "hand_r", "fingers_l", "fingers_r")
DEPENDENCIES = [
    "Posterior hip-level section depth (ALPC S6 depth, 'pelvic AP'): on the -LEAN the posterior extreme at the hip-joint level is the "
    "gluteal mass over the ischium, not bone. The accepted W2 pelvic-depth relations were read on that surface. The true floor at that "
    "point is ~4-5 cm deeper. The relation is therefore reported on the unorganized skeleton proxy (unchanged by construction) and the "
    "organized / floor depths are reported beside it; the separation of 'bony pelvic AP' from gluteal tissue cannot be made from the "
    "skeleton data alone (no bone mesh exists in the route).",
    "Thorax-maximum breadth (ALPC S2 b) lateral extreme lies on latissimus / serratus cover over the ribs; the floor keeps 1.2 cm there, so "
    "the reading is close to but not exactly the rib cage.",
]

def _ss(x): x = np.clip(x, 0, 1); return x * x * (3 - 2 * x)

def _smooth(D, F, iters):
    n = len(D); E = np.r_[F[:, [0, 1]], F[:, [1, 2]], F[:, [2, 0]]]; E = np.r_[E, E[:, ::-1]]
    deg = np.bincount(E[:, 0], minlength=n).astype(float); deg[deg == 0] = 1
    for _ in range(iters):
        nb = np.zeros_like(D); np.add.at(nb, E[:, 0], D[E[:, 1]]); D = 0.5 * D + 0.5 * nb / deg[:, None]
    return D

def signed_volume(V, F, keep):
    Fk = F[keep[F].all(1)]
    return float(np.einsum('ij,ij->i', V[Fk[:, 0]], np.cross(V[Fk[:, 1]], V[Fk[:, 2]])).sum() / 6.0)

def outward_normals(V, F, keep):
    """area-weighted vertex normals oriented OUTWARD (by the sign of the kept mesh's signed volume)"""
    n = np.zeros_like(V); fn = np.cross(V[F[:, 1]] - V[F[:, 0]], V[F[:, 2]] - V[F[:, 0]])
    for k in range(3): np.add.at(n, F[:, k], fn)
    n /= np.maximum(np.linalg.norm(n, axis=1), 1e-9)[:, None]
    return n if signed_volume(V, F, keep.astype(bool)) > 0 else -n

def test_outward(V, F, L):
    """anatomical probes for the outward convention; returns (pass, details)"""
    keep = L["keep"].astype(bool); n = outward_normals(V, F, keep); J = json.loads(str(L["joints"])) if isinstance(L["joints"], (str, np.ndarray)) else L["joints"]
    armw = np.maximum.reduce([L["w_" + k] for k in ARMK]); out = {}
    def probe(name, mask, pick, axis, sign):
        idx = np.where(mask)[0]
        if not len(idx): out[name] = None; return True
        i = idx[pick(V[idx])]; ok = bool(np.sign(n[i, axis]) == sign and abs(n[i, axis]) > 0.5); out[name] = [round(float(x), 3) for x in n[i]] + [ok]; return ok
    sh = (J["clavicle_l"][0][2] + J["clavicle_r"][0][2]) / 2; hip = (J["thigh_l"][0][2] + J["thigh_r"][0][2]) / 2
    chest = keep & (np.abs(V[:, 0]) < 3) & (V[:, 2] > hip + 0.6 * (sh - hip)) & (V[:, 2] < sh) & (armw < 0.05)
    ok = probe("chest_front(+y)", chest, lambda P: np.argmax(P[:, 1]), 1, 1)
    ok &= probe("back(-y)", chest, lambda P: np.argmin(P[:, 1]), 1, -1)
    ok &= probe("crown(+z)", keep, lambda P: np.argmax(P[:, 2]), 2, 1)
    sole = keep & (np.maximum(L["w_foot_l"], L["w_ball_l"]) > 0.5)
    ok &= probe("sole_l(-z)", sole, lambda P: np.argmin(P[:, 2] + 0.0 * P[:, 0]), 2, -1)
    th = keep & (L["w_thigh_l"] > 0.9); sx = 1 if J["thigh_l"][0][0] > 0 else -1
    ok &= probe("lateral_thigh_l(%sx)" % ('+' if sx > 0 else '-'), th, (lambda P: np.argmax(P[:, 0])) if sx > 0 else (lambda P: np.argmin(P[:, 0])), 0, sx)
    out["signed_volume"] = signed_volume(V, F, keep)
    return bool(ok), out

# ---- anatomical coordinate helpers (same conventions as race_base) ----
def _frame(J, bn, side):
    h = np.array(J["%s_%s" % (bn, side)][0]); tl = np.array(J["%s_%s" % (bn, side)][1]); ax = tl - h; ln = np.linalg.norm(ax); ax = ax / ln
    ea = np.array([0, 1.0, 0]); ea = ea - (ea @ ax) * ax; ea /= np.linalg.norm(ea)
    lat = np.array([1.0 if (J["thigh_l"][0][0] > 0) == (side == "l") else -1.0, 0, 0])
    el = np.cross(ax, ea); el = el * (1 if el @ lat > 0 else -1)
    return h, ax, ln, ea, el

def _band(x, a, b, e=0.07): return _ss((x - a) / e + 0.5) * _ss((b - x) / e + 0.5)
def _sect(phi, c, hw, e=25.0):
    d = np.abs((phi - c + 180.0) % 360.0 - 180.0); return _ss((hw - d) / e + 0.5)

# limb model: (bone, joint-zone t0, t1, bone-radius fraction)
LIMB = {"upperarm": (0.10, 0.86, 0.35), "lowerarm": (0.08, 0.90, 0.50), "thigh": (0.08, 0.90, 0.32), "calf": (0.08, 0.92, 0.45)}
SUBQ = 0.4     # subcutaneous depth over exposed bone (cm)

def depth_map(V, L, J):
    """soft-tissue depth d(v) >= 0 (cm) to remove from the -LEAN to reach the protected floor, plus the limb bone-radius floor"""
    keep = L["keep"].astype(bool); n = len(V); W = {}
    hip = (J["thigh_l"][0][2] + J["thigh_r"][0][2]) / 2; sst = (J["clavicle_l"][0][2] + J["clavicle_r"][0][2]) / 2
    rz = (V[:, 2] - hip) / (sst - hip)
    armw = np.maximum.reduce([L["w_" + k] for k in ARMK])
    # trunk section centre (smoothed) and angle 0 anterior .. 180 posterior
    tm = keep & (armw < 0.05) & (np.maximum(L["w_thigh_l"], L["w_thigh_r"]) < 0.5)
    zs = np.linspace(V[tm, 2].min(), V[tm, 2].max(), 120); cy = []
    for z in zs:
        q = tm & (np.abs(V[:, 2] - z) < 0.8); cy.append(0.5 * (V[q, 1].max() + V[q, 1].min()) if q.sum() > 3 else np.nan)
    cy = np.array(cy); ok = ~np.isnan(cy); cy = np.interp(zs, zs[ok], cy[ok]); k = np.exp(-0.5 * (np.arange(-12, 13) / 4.0) ** 2); k /= k.sum()
    cy = np.convolve(np.pad(cy, 12, mode='edge'), k, 'valid'); c = np.interp(V[:, 2], zs, cy)
    ph = np.degrees(np.arctan2(np.abs(V[:, 0]), V[:, 1] - c)); ax_ = np.abs(V[:, 0])
    # ---- trunk / pelvis / shoulder-top depth (cm) ----
    d = np.full(n, 1.0)
    glute = _sect(ph, 150, 40) * _band(rz, -0.5, 0.14, 0.08)
    d = d + (6.0 - d) * glute
    sacrum = _ss((3.0 - ax_) / 2.0) * _sect(ph, 180, 25) * _band(rz, -0.12, 0.25)
    d = d + (0.8 - d) * sacrum
    troch = _sect(ph, 90, 20) * _band(rz, -0.18, 0.05)
    d = d + (1.5 - d) * troch
    crest = _sect(ph, 95, 35) * _band(rz, 0.15, 0.25, 0.08)
    d = d + (1.2 - d) * crest
    asis = _sect(ph, 45, 25) * _band(rz, 0.03, 0.2)
    d = d + (1.0 - d) * asis
    abdo = _sect(ph, 20, 60) * _band(rz, 0.18, 0.55)
    d = d + (1.5 - d) * abdo
    flank = _sect(ph, 100, 20) * _band(rz, 0.27, 0.5)
    d = d + (2.0 - d) * flank
    lumbar = _sect(ph, 150, 30) * _band(rz, 0.12, 0.55)
    d = d + (3.0 - d) * lumbar
    spine = _ss((2.0 - ax_) / 1.5) * _sect(ph, 180, 20) * _band(rz, 0.1, 1.1)
    d = d + (0.6 - d) * spine
    pec = _sect(ph, 40, 32) * _band(rz, 0.6, 1.0)
    d = d + (2.0 - d) * pec
    stern = _ss((3.0 - ax_) / 2.0) * _sect(ph, 0, 15) * _band(rz, 0.55, 1.05)
    d = d + (0.5 - d) * stern
    ribs = _sect(ph, 95, 20) * _band(rz, 0.55, 0.95)
    d = d + (1.2 - d) * ribs
    scap = _sect(ph, 140, 28) * _band(rz, 0.6, 1.02)
    d = d + (2.0 - d) * scap
    trap = _band(rz, 0.95, 1.3) * (ax_ > 6.0)
    d = d + (2.0 - d) * trap
    clav = _sect(ph, 20, 40) * _band(rz, 0.97, 1.08, 0.03)
    d = d + (0.5 - d) * clav
    dt = d
    # ---- limbs: blended by skin weight; the limb floor is RADIAL toward the accepted bone axis (a normal offset would fold the floor) ----
    Dv = np.zeros((n, 3)); Wt = np.zeros(n)
    for side in ("l", "r"):
        for bn, (j0, j1, kb) in LIMB.items():
            w = L["w_%s_%s" % (bn, side)].astype(float) * keep; m = w > 1e-3
            if not m.any(): continue
            h, ax, ln, ea, el = _frame(J, bn, side); P = V[m]; t = np.clip((P - h) @ ax / ln, 0, 1)
            rv = P - (h + np.outer(t * ln, ax)); r = np.linalg.norm(rv, axis=1); u = rv / np.maximum(r, 1e-6)[:, None]
            phl = np.degrees(np.arctan2(rv @ el, rv @ ea))
            shaft = (t > j0 + 0.05) & (t < j1 - 0.05) & (w[m] > 0.5)
            rmin = np.percentile(r[shaft], 5) if shaft.sum() > 10 else r.min()
            rb = kb * rmin
            dl = np.maximum(r - rb, 0.0)                                           # muscle / fat over the bone-radius model
            zone = 1 - _ss((t - j0) / 0.06) * _ss((j1 - t) / 0.06)              # joint zones: subcutaneous
            dl = dl * (1 - zone) + np.minimum(dl, SUBQ) * zone
            if bn == "calf": dl = np.where(_sect(phl, -30, 50) > 0.5, np.minimum(dl, 0.5), dl)   # anteromedial tibia: subcutaneous
            if bn == "lowerarm": dl = np.where(_sect(phl, 180, 30) > 0.5, np.minimum(dl, 0.8), dl)  # ulnar border
            if bn == "upperarm":                                                # deltoid cap over the humeral head: 2.5 cm
                cap = (t < 0.32) & (_sect(phl, 90, 120) > 0.5); dl = np.where(cap, np.minimum(dl, 2.5), dl)
            we = w[m] * (_ss((t - 0.12) / 0.12) if bn == "thigh" else 1.0)     # proximal thigh / buttock shell is read by the trunk map
            Dv[m] += (we * dl)[:, None] * (-u); Wt[m] += we
    hw = np.clip(L["w_hand_l"] + L["w_hand_r"] + L["w_fingers_l"] + L["w_fingers_r"] + L["w_foot_l"] + L["w_foot_r"] + L["w_ball_l"] + L["w_ball_r"] + L["w_head"] + L["w_neck_01"], 0, 1)
    wl = np.clip(Wt, 0, 1) * (1 - hw); Dl = np.where(Wt[:, None] > 1e-6, Dv / np.maximum(Wt, 1e-6)[:, None], 0.0)
    dt = dt * (1 - hw) + SUBQ * hw
    return dt, Dl, wl

def floor(Vlean, L, J=None):
    """protected bony floor (same vertex order and frame as Vlean). Returns (floor, depth cm, outward normals)"""
    J = J or json.loads(str(L["joints"]))
    n = outward_normals(Vlean, L["F"], L["keep"]); keep = L["keep"].astype(bool)
    dt, Dl, wl = depth_map(Vlean, L, J)
    D = -(dt * (1 - wl))[:, None] * n + Dl * wl[:, None]
    D = _smooth(D * keep[:, None], L["F"], 6)
    return Vlean + D, np.linalg.norm(D, axis=1), n

if __name__ == "__main__":
    import sys
    for p in sys.argv[1:]:
        L = dict(np.load(p, allow_pickle=True)); V = L["V"].astype(float)
        ok, det = test_outward(V, L["F"], L); Fv, d, n = floor(V, L)
        print(p, "outward test", ok, json.dumps(det), "depth cm: median %.2f p90 %.2f max %.2f" % (np.median(d[L['keep'].astype(bool)]), np.percentile(d[L['keep'].astype(bool)], 90), d.max()))
