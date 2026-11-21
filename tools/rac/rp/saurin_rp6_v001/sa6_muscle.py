# sa6_muscle.py : Saurin RP6 rig v002 elbow-driven upper-arm muscle layer (shoulder / elbow correction order 07a3f24c §2, SAURIN-RP6-DEF-ELBOW-MUSCLE-1).
#   Authored (not fitted) rest-space shapes on the upper arm, driven by the elbow flexion driver of each arm:
#     biceps / brachialis (anterior): shorten and bulge -- the belly rises and its centre moves proximally as the elbow flexes;
#     triceps (posterior): lengthens and flattens -- a broad inward displacement whose centre moves distally.
#   Driver = the swing-twist twist of forearm_<t> about the elbow flexion axis of elbow_130_x<side> (the same driver the corrective families use,
#   sa6_correctives.Correctives.driver), x = flexion / flexion(130 deg pose), s(x) = smoothstep(clamp(x, 0, 1)) = 3x^2 - 2x^3 (0 at neutral, flat at both ends).
#   Geometry per arm (rest body of the rig given: base or creator state, so the shapes follow the body): humeral axis u = GH (upperarm head) -> elbow
#   (forearm head), length L; t = axial position 0..1; radial unit vector r^ (displacement direction, ~ the surface normal of the arm); anterior
#   direction a = the direction the forearm moves under flexion, made perpendicular to u; c = r^ . a (1 = front, -1 = back); rho(t) = local mean radius.
#     window   W(t) = smoothstep((t - 0.10) / 0.15) * smoothstep((0.93 - t) / 0.12)                  (zero at the shoulder cap and at the elbow crease)
#     biceps   B(t, s) = exp(-((t - (0.58 - 0.10 s)) / (0.17 (1 - 0.15 s)))^2) + 0.40 exp(-((t - 0.80) / 0.08)^2)   (brachialis: the distal anterior swelling)
#              angular max(0, c)^1.5
#     triceps  T(t, s) = exp(-((t - (0.50 + 0.06 s)) / (0.26 (1 + 0.15 s)))^2),  angular max(0, -c)^1.5
#     delta(v) = s [ A_b B - A_t T ] W r^,   A_b = BICEPS_REL x rho(t),   A_t = the value that makes the closed-mesh volume change of the delta 0 at s = 1
#              (sum over the layer of delta . vertex area normal = 0), capped at A_b (|A_t| <= A_b).
#   Bounded (max |delta| <= A_b <= BICEPS_REL x max rho), local (upper-arm vertices of that side only, W = 0 at both ends), zero at neutral.
#   Stored as one corrective family per arm (layer = 'muscle'), samples every 1/13 of the 130-deg driver value (10 deg), hat-interpolated like every
#   family (piecewise linear between 10-deg samples: interpolation error <= 0.005 cm), held beyond 130 deg, 0 for extension.  The fit never adds to it
#   (Correctives.resolve skips layer families); folds / contact / volume it causes are corrected by the fitted families on top.
#   CLI:  sa6_muscle.py add IN_CORRECTIVES.json OUT.json CFG [STATE]   (adds / replaces the muscle families; STATE = creator state rest body)
#         sa6_muscle.py report CFG [STATE]                             (per-arm parameters, max displacement, region size, volume)
import sys, os, json, numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sa6_common as C, sa6_pose as SP, sa6_correctives as CC
BICEPS_REL = float(os.environ.get('MUSCLE_BICEPS_REL', '0.16'))
NS = 13
def smooth(x): x = np.clip(x, 0.0, 1.0); return x * x * (3 - 2 * x)
def arm_frame(R, t):
    side = 'xpos' if t == 'l' else 'xneg'; spec = R.suite('anat')['elbow_130_' + side]; (fb, piv, ax, deg), = [e for e in spec if e[0].startswith('forearm')]
    ax = np.asarray(ax, float) / np.linalg.norm(ax); H = R.H('upperarm_' + t); E = R.H(fb); u = E - H; L = np.linalg.norm(u); u = u / L
    Tl = R.Tl(fb) - piv; mv = SP.rot(ax, 5.0 * np.sign(deg)) @ Tl - Tl; a = mv - (mv @ u) * u; a = a / np.linalg.norm(a)
    x130 = CC.Correctives(R).driver(R.pose(spec), dict(bone=fb, axis=ax))
    return dict(spec=spec, bone=fb, pivot=np.asarray(piv, float), axis=ax, H=H, E=E, u=u, L=L, a=a, x130=float(x130))
def region(R, t, fr):
    """upper-arm vertices of arm t (quad label 'upper_arm', nearer this arm's humeral axis than the other's)"""
    lab = np.zeros(R.nv, bool); lab[R.Q[R.ql == 'upper_arm'].ravel()] = True
    o = 'r' if t == 'l' else 'l'; Ho, Eo = R.H('upperarm_' + o), R.H(arm_frame(R, o)['bone'])
    def dseg(P, A, B): ab = B - A; s = np.clip(((P - A) @ ab) / (ab @ ab), 0, 1); return np.linalg.norm(P - (A + s[:, None] * ab), axis=1)
    return np.nonzero(lab & (dseg(R.V, fr['H'], fr['E']) < dseg(R.V, Ho, Eo)))[0]
def vertex_area_normals(R):
    P = R.V; Q = R.Q; n = np.zeros_like(P)
    for a, b, c in ((0, 1, 2), (0, 2, 3)):
        fn = 0.5 * np.cross(P[Q[:, b]] - P[Q[:, a]], P[Q[:, c]] - P[Q[:, a]])
        for k in (a, b, c): np.add.at(n, Q[:, k], fn / 3.0)
    return n
def profiles(R, t, fr, idx):
    X = R.V[idx] - fr['H']; tt = X @ fr['u'] / fr['L']; rad = X - np.outer(X @ fr['u'], fr['u']); rho = np.linalg.norm(rad, axis=1); rh = rad / rho[:, None]
    c = rh @ fr['a']
    bins = np.clip((tt * 20).astype(int), 0, 19); rb = np.array([np.median(rho[bins == k]) if (bins == k).any() else np.nan for k in range(20)])
    rb = np.where(np.isnan(rb), np.nanmedian(rb), rb); rloc = np.interp(tt, (np.arange(20) + 0.5) / 20, rb)
    W = smooth((tt - 0.10) / 0.15) * smooth((0.93 - tt) / 0.12)
    return tt, rh, c, rloc, W
def shape(R, t, fr, idx, s, At=None):
    tt, rh, c, rloc, W = profiles(R, t, fr, idx)
    B = (np.exp(-((tt - (0.58 - 0.10 * s)) / (0.17 * (1 - 0.15 * s))) ** 2) + 0.40 * np.exp(-((tt - 0.80) / 0.08) ** 2)) * np.maximum(0, c) ** 1.5
    Tp = np.exp(-((tt - (0.50 + 0.06 * s)) / (0.26 * (1 + 0.15 * s))) ** 2) * np.maximum(0, -c) ** 1.5
    Ab = BICEPS_REL * rloc
    if At is None:      # volume balance at full flexion: sum (Ab B - At T) W (r^ . area normal) = 0  ->  At (scalar multiple of the local radius)
        An = vertex_area_normals(R)[idx]; g = (rh * An).sum(1); num = (Ab * B * W * g).sum(); den = (BICEPS_REL * rloc * Tp * W * g).sum()
        At = min(1.0, num / den) if den > 0 else 0.0
    return smooth(s) * (Ab * B - At * BICEPS_REL * rloc * Tp)[:, None] * W[:, None] * rh, At
def families(R):
    out = []
    for t in ('l', 'r'):
        fr = arm_frame(R, t); idx = region(R, t, fr); _, At = shape(R, t, fr, idx, 1.0)
        samples = [fr['x130'] * k / NS for k in range(1, NS + 1)]; D = []
        for k, sv in enumerate(samples, 1):
            d, _ = shape(R, t, fr, idx, k / NS, At); nz = np.nonzero(np.linalg.norm(d, axis=1) > 1e-6)[0]; D.append((idx[nz], d[nz]))
        params = dict(biceps_rel_radius=BICEPS_REL, triceps_rel_radius=round(float(At * BICEPS_REL), 5), triceps_over_biceps=round(float(At), 5), driver_130_deg=round(fr['x130'], 4),
                      samples=NS, region_vertices=int(len(idx)), humerus_length_cm=round(float(fr['L']), 3), gh=np.round(fr['H'], 3).tolist(), elbow=np.round(fr['E'], 3).tolist(),
                      anterior=np.round(fr['a'], 4).tolist(), max_delta_cm=round(float(max(np.linalg.norm(dd, axis=1).max() for _, dd in D)), 4))
        out.append(dict(bone=fr['bone'], axis=list(fr['axis']), pivot=list(fr['pivot']), samples=samples, D=D, layer='muscle', layer_params=params))
    return out
def add(Cr, R):
    for k in [k for k, f in Cr.F.items() if f.get('layer') == 'muscle']: del Cr.F[k]
    for f in families(R): Cr.F[CC.fam_key(f['bone'], f['axis'], 'muscle')] = f
    return Cr
def state_rig(cfg, state):
    if not state: return SP.Rig(cfg, C.w_path(cfg))
    import sa6_pd2_fit as PF; return PF.state_rig(state)[0]
if __name__ == '__main__':
    if sys.argv[1] == 'add':
        IN, OUT, cfg = sys.argv[2:5]; st = sys.argv[5] if len(sys.argv) > 5 else None; R = state_rig(cfg, st); Cr = add(CC.Correctives.load(R, IN), R)
        meta = {k: v for k, v in json.load(open(IN)).items() if k not in ('families', 'pose_keys')}; meta['muscle_layer'] = 'sa6_muscle.py (order 07a3f24c §2)'
        Cr.save(OUT, meta); print('muscle families', [f['layer_params'] for f in Cr.F.values() if f.get('layer')])
    else:
        cfg = sys.argv[2]; st = sys.argv[3] if len(sys.argv) > 3 else None; R = state_rig(cfg, st); fams = families(R)
        Cr = CC.Correctives(R); [Cr.F.__setitem__(CC.fam_key(f['bone'], f['axis'], 'muscle'), f) for f in fams]
        S = CC.Solver(R); V0 = S.body_volume(R.V); rep = {}
        for f, t in zip(fams, 'lr'):
            spec = R.suite('anat')['elbow_130_' + ('xpos' if t == 'l' else 'xneg')]; T = R.pose(spec)
            rep[t] = dict(f['layer_params'], dV_lbs_cm3=round(float(S.body_volume(R.skin(T)) - V0), 2), dV_muscle_cm3=round(float(S.body_volume(R.skin(T, R.V + Cr.delta(T))) - V0), 2),
                          neutral_max_cm=float(np.abs(Cr.delta(R.pose([]))).max()))
        print(json.dumps(rep, indent=1))
