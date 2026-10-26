# rigprep_fit.py MESH.npz OUT.json : Grask rig-prep joint-centre / axis MEASUREMENTS on one mesh (analysis SOURCE frame, cm).
# Read-only. Run on the frozen v005 source (primary) and on the frozen v003 production read-back (cross-check, same frame).
# Every internal centre is measured by >= 2 independent surface definitions; the frozen package value is carried only as a
# comparison alternative. The superseded MPFB/E3 skeleton is NOT read here.
import sys, os, json, numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, '/tmp/claude-0/src3d/v5/tools')            # frozen v005 extremity construction (hand / foot parametric model)
from fitlib import *
from hand_model import DEF as HDEF, scaled, finger_chain, rot as hrot
from hand_frame import frame as hand_frame
import foot_model as fm

MESH, OUT = sys.argv[1], sys.argv[2]
FROZEN = json.load(open(os.environ.get('FROZEN_LM', '/home/claude/wayfarer-design/reviews/rac-rp2-evidence/'
                    'grask_retopo_v003_audit_closure/production/GR_U_REF_RP2_retopo_v003_landmarks.json')))['landmarks']
FZ = lambda k: np.array(FROZEN[k]['source_frame_cm'], float)       # frozen package value, source frame
m = load(MESH); V = m.vertices
TC = m.triangles_center; TN = m.face_normals; TA = m.area_faces
R = {}                                                               # results
def rec(k, **kw):
    R.setdefault(k, {}).update({a: (b.tolist() if isinstance(b, np.ndarray) else b) for a, b in kw.items()})
def hsec(z, keep):
    s = m.section(plane_origin=[0, 0, z], plane_normal=[0, 0, 1.0])
    return [] if s is None else [e for e in s.discrete if len(e) > 5 and keep(e)]
def top_band(mask, score, k):
    i = np.nonzero(mask)[0]; sc = score[i]; j = i[sc >= sc.max() - k]; w = TA[j]; return (TC[j] * w[:, None]).sum(0) / w.sum()
def smooth(y, k=3):
    y = np.asarray(y, float).copy(); ok = np.isfinite(y)
    if ok.sum() >= 2 and not ok.all(): y[~ok] = np.interp(np.nonzero(~ok)[0], np.nonzero(ok)[0], y[ok])
    return np.convolve(np.pad(y, k, mode='edge'), np.ones(2 * k + 1) / (2 * k + 1), mode='valid')

# ---------------------------------------------------------------- crotch / armpit merge levels
def leg_loop_z(sg):
    """highest z at which the leg is still a separate horizontal-section loop (crotch level)"""
    zt = None
    for z in np.arange(100, 125, 0.25):
        ok = any(sg * e[:, 0].min() > 0.3 for e in hsec(z, lambda e: True) if 3 < sg * e[:, 0].mean() < 20)
        if ok: zt = z
        else: break
    return zt
for s, sg in (('l', 1), ('r', -1)):
    rec('crotch_' + s, z=leg_loop_z(sg), method='highest z at which the thigh is a separate horizontal-section loop')

# ---------------------------------------------------------------- legs
for s, sg in (('l', 1), ('r', -1)):
    Kf, Af, Hf = FZ('knee_' + s), FZ('ankle_' + s), FZ('hip_' + s)
    zc = R['crotch_' + s]['z']
    # thigh soft-tissue axis (sections between knee+8 and crotch-3); shank axis on the distal shank only (z 14..40, below the calf belly)
    ct, dt, Ct, rt = axis_from_sections(m, np.array([Kf[0], Kf[1], Kf[2] + 8]), np.array([Kf[0], Kf[1] - 2, zc - 3]), np.linspace(0, 1, 16), 12)
    cs, ds, Cs, rs = axis_from_sections(m, np.array([Af[0], Af[1], 14.0]), np.array([Af[0], Af[1], 40.0]), np.linspace(0, 1, 14), 9)
    rec('thigh_axis_' + s, point=ct, dir=dt, rms_cm=rt, n=len(Ct), method='line through centroids of sections perpendicular to the thigh, knee+8 cm .. crotch-3 cm')
    rec('shank_axis_' + s, point=cs, dir=ds, rms_cm=rs, n=len(Cs), method='line through centroids of sections perpendicular to the distal shank, z 14..40 cm (below the calf belly)')
    on_t = lambda z: ct + dt * ((z - ct[2]) / dt[2]); on_s = lambda z: cs + ds * ((z - cs[2]) / ds[2])
    # ---- knee: A = cross-section-area minimum ("knee waist"), B = patellar flattening of the anterior contour, along the mean axis
    dm = dt + ds; dm /= np.linalg.norm(dm)
    zs = np.arange(Kf[2] - 12, Kf[2] + 12.01, 0.25); prof = []
    for z in zs:
        p0 = 0.5 * (on_t(z) + on_s(z)); sc = section(m, p0, dm, p0, 12)
        prof.append((sc['area'], *sc['c'], sc['pts'][:, 1].max()) if sc else (np.nan,) * 5)
    prof = np.array(prof); A_ = smooth(prof[:, 0], 2); iA = int(np.nanargmin(A_)); kA = prof[iA, 1:4]
    ant = smooth(prof[:, 4], 4); slope = np.gradient(ant, zs); band = (zs > Kf[2] - 6) & (zs < Kf[2] + 10)
    iB = int(np.nonzero(band)[0][np.argmin(slope[band])]); kB = prof[iB, 1:4]
    rec('knee_' + s, A=kA, B=kB, C_frozen=Kf, A_z=float(zs[iA]), B_z=float(zs[iB]),
        A_method='centroid of the minimum-area section across the knee (perpendicular to the mean thigh/shank axis)',
        B_method='centroid of the section at the patellar flattening (minimum slope of the anterior contour)',
        profile_z=zs, profile_area=prof[:, 0], profile_ant=prof[:, 4])
    # ---- ankle level: A = anterior ankle crease (max curvature of the anterior contour), B = Achilles concavity (most anterior posterior contour)
    za = np.arange(4, 24.01, 0.25); antf = []; postf = []
    for z in za:
        p0 = on_s(z); P = np.vstack(hsec(z, lambda e: sg * e[:, 0].mean() > 3)); P = P[np.abs(P[:, 0] - p0[0]) < 4.0]
        antf.append(P[:, 1].max()); postf.append(P[:, 1].min())
    antf = smooth(np.array(antf), 2); postf = smooth(np.array(postf), 2)
    curv = np.gradient(np.gradient(antf, za), za); m1 = (za > 7) & (za < 18); iA = int(np.nonzero(m1)[0][np.argmax(curv[m1])])
    m2 = (za > 6) & (za < 22); iB = int(np.nonzero(m2)[0][np.argmax(postf[m2])])
    rec('ankle_' + s, A=on_s(za[iA]), B=on_s(za[iB]), C_frozen=Af, A_z=float(za[iA]), B_z=float(za[iB]),
        A_method='distal-shank axis at the anterior ankle crease (maximum curvature of the anterior contour)',
        B_method='distal-shank axis at the Achilles concavity (most anterior point of the posterior contour above the heel)',
        note='no malleolar relief in the source: the medial/lateral extents show no malleolus bump, so the talocrural axis obliquity is unsupported')
    # ---- foot progression: heel (posterior-most sole point) -> toe2 MTP (construction)
    heel = top_band((sg * TC[:, 0] > 5) & (TC[:, 2] < 3.0), -TC[:, 1], 0.05)
    rec('heel_' + s, p=heel, method='area-weighted posterior-most surface band of the sole region (z<3 cm)')
    # ---- hip: A = inguinal-fold level (first local minimum of the anterior contour above the crotch) on the thigh axis.
    #      The greater-trochanter prominence was also searched for: the lateral hip contour is monotonic (widest at the thigh), so no
    #      trochanter level exists in the source and that definition is reported as unavailable, not used.
    zh = np.arange(zc - 6, zc + 22.01, 0.25); lat = []; antc = []
    for z in zh:
        P = np.vstack(hsec(z, lambda e: True)); P = P[(sg * P[:, 0] > 3) & (sg * P[:, 0] < 25.5)]
        lat.append((sg * P[:, 0]).max())
        q = P[np.abs(P[:, 0] - on_t(z)[0]) < 1.5]; antc.append(q[:, 1].max() if len(q) else np.nan)
    lat = smooth(np.array(lat), 2); antc = smooth(np.array(antc), 4)
    seg = (zh > zc) & (zh < zc + 20); lat_seg = lat[(zh > zc - 4) & (zh < zc + 12)]
    troch = bool(np.any(np.diff(np.sign(np.diff(lat_seg))) < 0))       # an interior local maximum of the lateral contour
    loc = [k for k in np.nonzero(seg)[0] if 4 <= k < len(zh) - 4 and antc[k] <= antc[k - 4:k + 5].min() + 1e-9]
    iA = loc[0] if loc else int(np.nonzero(seg)[0][np.nanargmin(antc[seg])])
    rec('hip_' + s, A=on_t(zh[iA]), C_frozen=Hf, A_z=float(zh[iA]), trochanter_prominence_found=troch,
        A_method='thigh axis extended to the level of the inguinal fold (first local minimum of the anterior contour above the crotch)',
        lateral_profile_z=zh, lateral_profile=lat, anterior_profile=antc,
        note='femoral head is internal and the source has no trochanteric relief; the inguinal-fold level on the soft-tissue thigh axis and the frozen value are the only alternatives')

# ---------------------------------------------------------------- arms
for s, sg in (('l', 1), ('r', -1)):
    Gf, Ef, Wf = FZ('glenohumeral_' + s), FZ('elbow_' + s), FZ('wrist_' + s)
    d0 = (Gf - Ef) / np.linalg.norm(Gf - Ef)
    # free upper arm: march proximally from the elbow while the arm is a separate loop
    C = []; t = -5.0; zmerge = None
    while t < 40:
        o = Ef + d0 * t; sc = section(m, o, d0, o, 7.0)
        if sc is None or sc['area'] > 160: zmerge = o[2]; break
        C.append(sc['c']); t += 0.5
    C = np.array(C); C = C[(C - Ef) @ d0 > 3.0]                       # exclude the elbow itself
    cu, du, ru = line_fit(C); du = du if du @ d0 > 0 else -du
    rec('upperarm_axis_' + s, point=cu, dir=du, rms_cm=ru, n=len(C), armpit_merge_z=zmerge,
        method='line through centroids of sections perpendicular to the free upper arm (elbow+3 cm .. armpit contact)')
    cf, df, Cf, rf = axis_from_sections(m, Wf + (Ef - Wf) * 0.25, Wf + (Ef - Wf) * 0.78, np.linspace(0, 1, 14), 8)
    df = -df if df @ (Ef - Wf) < 0 else df
    rec('forearm_axis_' + s, point=cf, dir=df, rms_cm=rf, n=len(Cf), method='line through centroids of forearm sections, 25%..78% wrist->elbow')
    # ---- elbow: A = minimum-area section across the elbow, B = cubital-fossa level (most posterior anterior contour);
    #      D (diagnostic only) = closest approach of the upper-arm and forearm axes, conditioned only by the small stance flexion
    dm = du + df; dm /= np.linalg.norm(dm); aa = np.array([0, 1.0, 0]) - (np.array([0, 1.0, 0]) @ dm) * dm; aa /= np.linalg.norm(aa)
    ts = np.arange(-10, 8.01, 0.25); ar = []
    for t in ts:
        p0 = Ef + dm * t; sc = section(m, p0, dm, p0, 8); ar.append((sc['area'], *sc['c'], (sc['pts'] @ aa).max()) if sc else (np.nan,) * 5)
    ar = np.array(ar); iA = int(np.nanargmin(smooth(ar[:, 0], 2))); an = smooth(ar[:, 4], 2); bd = (ts > -9) & (ts < 5)
    iB = int(np.nonzero(bd)[0][np.argmin(an[bd])])
    eD, gap, ang = closest_between_lines(cu, du, cf, df)
    rec('elbow_' + s, A=ar[iA, 1:4], B=ar[iB, 1:4], C_frozen=Ef, D_axes=eD, D_gap_cm=gap, axis_angle_deg=ang,
        A_method='centroid of the minimum-area section across the elbow',
        B_method='centroid of the section at the cubital fossa (most posterior point of the anterior contour)',
        D_method='closest approach of the upper-arm and forearm axes; diagnostic only (stance flexion %.1f deg makes it ill-conditioned)' % ang,
        flex_axis_from_bend=np.cross(du, df) / (np.linalg.norm(np.cross(du, df)) + 1e-12))
    # ---- wrist: A = v005 hand-frame origin (construction), B = forearm waist (min area, distal forearm)
    W, Mh = hand_frame(s.upper()); ts = np.arange(0, 12.01, 0.25); ar = []
    for t in ts:
        p0 = W + df * t; sc = section(m, p0, df, p0, 7); ar.append((sc['area'], *sc['c']) if sc else (np.nan,) * 4)
    ar = np.array(ar); iB = int(np.nanargmin(smooth(ar[:, 0], 2)))
    rec('wrist_' + s, A=W, B=ar[iB, 1:], B_offset_proximal_cm=float(ts[iB]), C_frozen=Wf, hand_frame=Mh,
        A_method='v005 hand-construction frame origin (copied construction coordinate)',
        B_method='centroid of the minimum-area distal-forearm section proximal of the hand')
    # ---- glenohumeral: two sphere fits on the shoulder cap around the measured acromion (A: lateral+superior cap, B: lateral
    #      deltoid only); both are reported with their offset from the free upper-arm axis. C = frozen package value.
    acr = FZ('acromion_' + s); dA = np.linalg.norm(TC - acr, axis=1)
    selA = (dA < 9) & (TC[:, 2] > acr[2] - 10) & (sg * TC[:, 0] > sg * acr[0] - 4) & ((sg * TN[:, 0] > 0.35) | (TN[:, 2] > 0.5)) & (TN[:, 1] > -0.6)
    selB = (dA < 11) & (TC[:, 2] > acr[2] - 12) & (TC[:, 2] < acr[2] - 1) & (sg * TN[:, 0] > 0.7)
    gA, rA, resA = sphere_fit(TC[selA]); gB, rB, resB = sphere_fit(TC[selB])
    offl = lambda p: float(np.linalg.norm((p - cu) - ((p - cu) @ du) * du))
    rec('glenohumeral_' + s, A=gA, B=gB, C_frozen=Gf, A_sphere_r_cm=rA, A_rms_cm=resA, A_n=int(selA.sum()), B_sphere_r_cm=rB, B_rms_cm=resB, B_n=int(selB.sum()),
        offset_from_upperarm_axis_cm=dict(A=offl(gA), B=offl(gB), C=offl(Gf)), acromion_to=dict(A=float(acr[2] - gA[2]), B=float(acr[2] - gB[2]), C=float(acr[2] - Gf[2])),
        A_method='least-squares sphere on the lateral/superior shoulder cap (faces within 9 cm of the measured acromion, normals lateral or up)',
        B_method='least-squares sphere on the lateral deltoid only (faces within 11 cm of the acromion, 1..12 cm below it, normal lateral > 0.7)')
    # ---- sternoclavicular surface proxy: anterior summit of the medial clavicle head beside the jugular notch
    zSC = FZ('sternoclavicular_' + s)[2]
    mk = (sg * TC[:, 0] > 1.2) & (sg * TC[:, 0] < 5) & (np.abs(TC[:, 2] - zSC) < 2.5) & (TC[:, 1] > -8) & (TN[:, 1] > 0.3)
    scs = top_band(mk, TC[:, 1], 0.1) if mk.any() else None
    rec('sternoclavicular_' + s, surface_point=scs, C_frozen=FZ('sternoclavicular_' + s),
        method='anterior surface summit beside the jugular notch at the frozen SC height (joint depth behind it unresolved)')

# ---------------------------------------------------------------- hands: construction chains + surface validation
P_ = scaled(HDEF)
def thumb_chain():
    T = P_['thumb']; dth = np.array(T['dir'], float); dth /= np.linalg.norm(dth); dor = np.array(T['dors'], float); dor -= (dor @ dth) * dth; dor /= np.linalg.norm(dor)
    J = [np.array(T['cmc'], float)]; dirs = [dth]; dors = [dor]; J.append(J[0] + T['L'][0] * dth)
    for k in range(2):
        lat = np.cross(dirs[-1], dors[-1]); Rr = hrot(lat, np.radians(T['flex'][k]))
        if ((Rr @ dirs[-1]) @ dors[-1] > 0) == (T.get('flexsign', 1) > 0): Rr = hrot(lat, -np.radians(T['flex'][k]))
        dirs.append(Rr @ dirs[-1]); dors.append(Rr @ dors[-1]); J.append(J[-1] + T['L'][k + 1] * dirs[-1])
    return J, dirs, dors
CHK = []                                                             # construction points to validate against this surface
for s in 'lr':
    W, Mh = hand_frame(s.upper())
    for nm, f in P_['fingers'].items():
        J, dirs, dors = finger_chain(f['mcp'], f['L'], f['splay'], f['flex'])
        names = ['mcp', 'pip', 'dip', 'tip']
        for i, n_ in enumerate(names):
            d_in = dirs[min(i, 2)]; d_out = dirs[i - 1] if i else dirs[0]
            ax = Mh @ (d_in if i < 3 else dirs[2]); fl = Mh @ np.cross(dirs[min(i, 2)], dors[min(i, 2)])
            CHK.append(('%s_%s_%s' % (nm, n_, s), W + Mh @ J[i], ax, fl, Mh @ dors[min(i, 2)]))
    J, dirs, dors = thumb_chain()
    for i, n_ in enumerate(['cmc', 'mcp', 'ip', 'tip']):
        ax = Mh @ dirs[min(i, 2)]; fl = Mh @ np.cross(dirs[min(i, 2)], dors[min(i, 2)])
        CHK.append(('thumb_%s_%s' % (n_, s), W + Mh @ J[i], ax, fl, Mh @ dors[min(i, 2)]))
# feet (left-foot construction; right = mirror x, as in the v004/v005 build)
for s, sg in (('l', 1), ('r', -1)):
    for t in fm.DEF['toes']:
        J, dirs, dors = fm.chain(t); n = len(J)
        names = ['mtp'] + (['ip'] if n == 3 else ['pip', 'dip']) + ['tip']
        for i, n_ in enumerate(names):
            P = np.array(J[i], float); a = np.array(dirs[min(i, n - 2)], float); dr = np.array(dors[min(i, n - 2)], float)
            P[0] *= sg; a[0] *= sg; dr[0] *= sg
            fl = np.cross(a, dr)
            CHK.append(('%s_%s_%s' % (t['n'], n_, s), P, a, fl, dr))
# validate every construction point: inside?, distance to surface, digit-section centroid offset (IP joints / tips excluded)
pts = np.array([c[1] for c in CHK]); inside = m.contains(pts)
cp, dist, _ = m.nearest.on_surface(pts)
for (k, p, ax, fl, dr), ins, dd in zip(CHK, inside, dist):
    out = dict(p=p, axis_long=ax / np.linalg.norm(ax), axis_flex=fl / np.linalg.norm(fl), dorsal=dr / np.linalg.norm(dr),
               inside=bool(ins), surface_dist_cm=float(dd))
    if not k.split('_')[1] in ('mcp', 'mtp', 'cmc', 'tip'):
        sc = section(m, p, ax, p, 1.6)
        if sc is not None: out.update(section_centroid=sc['c'], section_offset_cm=float(np.linalg.norm(sc['c'] - p)), section_area_cm2=sc['area'])
    if k.split('_')[1] == 'tip':                                     # surface tip: farthest digit surface along the distal direction
        u = ax / np.linalg.norm(ax); q = TC - p; along = q @ u; rad = np.linalg.norm(q - np.outer(along, u), axis=1)
        mk = (rad < 1.0) & (along > -1.5) & (along < 2.0) & (TN @ u > 0.2)
        if mk.any(): j = np.argmax(np.where(mk, along, -1e9)); out.update(surface_tip=TC[j], tip_to_surface_tip_cm=float(along[j]))
    rec('cx_' + k, **out)

# ---------------------------------------------------------------- axial
for k in ('pelvis_root', 'spine_01', 'spine_02', 'spine_03', 'neck_base', 'head_pivot'):
    z = FZ(k)[2]; L_ = hsec(z, lambda e: abs(e[:, 0].mean()) < 6)
    if not L_: continue
    e = max(L_, key=lambda e: len(e)); pr = poly_props(e, np.array([0, 0, z]), np.array([1.0, 0, 0]), np.array([0, 1.0, 0]))
    mid = e[np.abs(e[:, 0]) < 1.0]
    rec('axial_' + k, z=z, section_centroid=pr[1], section_area=pr[0], back_surface_f=float(mid[:, 1].min()), front_surface_f=float(mid[:, 1].max()), C_frozen=FZ(k))
# neck waist and head-pivot alternative at the ear-root height
zs = np.arange(184, 202.01, 0.25); ar = []
for z in zs:
    L_ = hsec(z, lambda e: abs(e[:, 0].mean()) < 6)
    if L_:
        e = max(L_, key=lambda e: len(e)); pr = poly_props(e, np.array([0, 0, z]), np.array([1.0, 0, 0]), np.array([0, 1.0, 0])); ar.append((pr[0], *pr[1]))
    else: ar.append((np.nan,) * 4)
ar = np.array(ar); i = int(np.nanargmin(smooth(ar[:, 0], 2)))
rec('neck_waist', p=ar[i, 1:], area=float(ar[i, 0]), method='minimum-area horizontal neck section (184..202 cm)')
zer = 0.5 * (FZ('ear_root_l')[2] + FZ('ear_root_r')[2]); j = int(np.argmin(np.abs(zs - zer)))
rec('head_pivot_alt', p=ar[j, 1:], z=zer, method='neck/head horizontal-section centroid at the mean ear-root height')
# eyes: sphere on the anterior-facing eye surface patch
for s, sg in (('l', 1), ('r', -1)):
    e0 = FZ('eye_' + s); mk = (np.linalg.norm(TC - e0, axis=1) < 1.6) & (TN[:, 1] > 0.2)
    if mk.sum() > 20:
        c, r, res = sphere_fit(TC[mk]); rec('eye_' + s, A=e0, B=c, B_r_cm=r, B_rms_cm=res, B_n=int(mk.sum()),
                                          A_method='v003 eyeball-volume centre (construction)', B_method='sphere on the anterior-facing eye surface within 1.6 cm')
# mouth / oral cavity check: is there any opening or interior at the lip seam?
mk = (np.abs(TC[:, 0]) < 3) & (TC[:, 2] > 192) & (TC[:, 2] < 197) & (TC[:, 1] > 10) & (TN[:, 1] < -0.3)
rec('mouth_check', inward_facing_faces_in_lip_region=int(mk.sum()), mesh_components=int(len(m.split(only_watertight=False))) if os.environ.get('SPLIT') else 'see topology (1)',
    note='a closed sculpted mouth has no inward-facing interior faces behind the lip seam')
json.dump(R, open(OUT, 'w'), indent=1, default=float); print('wrote', OUT, len(R))
