# RAC RM-OT-05K Branch B: Saurin-style reference-first Gorrund body sculpt (GO-RF*-REF / GO-RF*-LOW), order §13-§20.
# NO starting Gorrund skeleton: no GO rig, no GO5 route, no Gorrund joint placement, no S1-S4 mesh, no Gorrund generator.
# Substrate (order §14 "neutral humanoid topology / sculpting medium"): the accepted ordinary-human Marchfolk reference MF-M-R
# (reviews/reference-assets/r6) for GO-RF-REF and a low-muscle / low-fat build of the same substrate, MFM-RFLOW (muscle 0.1, weight 0.25; same topology, rf/sub) for GO-RF-LOW. The substrate's own
# segment weights are used only as soft sculpt masks (which vertices belong to a thigh, a forearm ...) and its own joint points only as the
# sculptor's working axes; neither is a Gorrund skeleton and neither is kept as one: the measurement scaffold is derived from the accepted
# body afterwards (k_scaffold.py, §21).
# The body form is authored by explicit, documented sculpt fields (all values below = the sculpt), applied in this order:
#   1. segment relation  : leg share lowered, axial (trunk) share raised (canon: Gorrund use axial architecture, not limb elongation);
#                          arms shortened with the legs so reach is not dominant (no Grask cue)
#   2. pelvis / stance   : hip joints carried wider (broad load-bearing pelvis), legs follow
#   3. trunk sections    : deep three-dimensional thorax, broad skeletal girdle, recessed lower axial wall, deep posterior pelvis;
#                          3b. gluteal mass reduced (posterior pelvis / upper thigh)
#   4. shoulder girdle   : arms carried wider by the broader thorax / girdle (no trapezius bulk)
#   5. limb bone scale   : radial (cross-section) scale along each long bone, larger at the joints than at the shafts
#   6. hands / feet      : larger in absolute terms (scaled about the wrist / under the ankle), five digits, plantigrade
#   7. neck root         : broad neck root integrated into the girdle
#   8. stature           : the finished body is placed at the Gorrund reference stature (229 cm)
# Usage: python3 k_rf.py PARAMS.json OUT_PREFIX     -> OUT_PREFIX-REF_r6.npz / -LOW_r6.npz (+ .obj) and a JSON report
import os, sys, json, numpy as np
REPO = '/home/claude/wayfarer-design'; RA = REPO + '/reviews/reference-assets/r6'
S = '/tmp/claude-0/-home-claude-wayfarer-design/19af7d50-3b61-5fda-9fe0-7a30770fb334/scratchpad'
SUB = {'REF': RA + '/MF-M-R_r6.npz', 'LOW': S + '/rf/sub/MFM-RFLOW_r6.npz'}
ARMS = ('upperarm', 'lowerarm', 'hand', 'fingers'); LEGS = ('thigh', 'calf', 'foot', 'ball')

def smooth(x, a, b):
    t = np.clip((x - a) / (b - a), 0, 1); return t * t * (3 - 2 * t)
def interp(z, pts):
    zs, vs = zip(*pts); return np.interp(z, zs, vs)

def sculpt(sub, P):
    d = np.load(sub, allow_pickle=True); V = d['V'].astype(float).copy(); keep = d['keep'].astype(bool)
    J = {k: [np.array(h, float), np.array(t, float)] for k, (h, t) in json.loads(str(d['joints'])).items()}
    W = {k[2:]: d[k].astype(float) for k in d.files if k.startswith('w_')}
    tot = np.maximum(sum(W.values()), 1e-6); W = {k: v / tot for k, v in W.items()}     # substrate weights are not normalized (0.48-1)
    side = lambda k: k[-1]
    wA = {s: sum(W['%s_%s' % (a, s)] for a in ARMS) for s in 'lr'}; wL = {s: sum(W['%s_%s' % (a, s)] for a in LEGS) for s in 'lr'}
    armw = np.clip(wA['l'] + wA['r'], 0, 1); legw = np.clip(wL['l'] + wL['r'], 0, 1); hnw = np.clip(W['head'] + W['neck_01'], 0, 1)
    trw = np.clip(1 - armw - legw - hnw, 0, 1)
    H = 0.5 * (J['thigh_l'][0][2] + J['thigh_r'][0][2]); SH = 0.5 * (J['upperarm_l'][0][2] + J['upperarm_r'][0][2]); NK = J['neck_01'][0][2]
    rep = {'substrate': os.path.basename(sub), 'hip_z': H, 'shoulder_z': SH}
    # ---- 1. segment relation: z-map (legs x kL below the hip; trunk stretched so the shoulder stays; above unchanged) --------------------
    kL = P['leg_scale']; m = 1 + H * (1 - kL) / (SH - H)
    def zmap(z):
        return np.where(z < H, z * kL, np.where(z < SH, H * kL + (z - H) * m, z))
    def armmap(Q, s):      # arms move rigidly with the shoulder, then are shortened about the shoulder joint by arm_scale
        sh = J['upperarm_' + s][0]; return sh + (Q - sh) * np.array([1, 1, P['arm_scale']])
    V1 = V.copy(); V1[:, 2] = zmap(V[:, 2])
    for s in 'lr':
        w = wA[s][:, None]; V1 = V1 * (1 - w) + armmap(V, s) * w
    Jm = {}
    for k, (h, t) in J.items():
        s = k[-1] if k[-2] == '_' else None
        if s and any(k.startswith(a) for a in ARMS + ('index', 'middle', 'ring', 'pinky', 'thumb')): Jm[k] = [armmap(h, s), armmap(t, s)]
        else: Jm[k] = [np.array([h[0], h[1], zmap(h[2])]), np.array([t[0], t[1], zmap(t[2])])]
    V = V1; J = Jm
    # ---- 2. pelvis / stance: legs (and the hip joints) carried laterally by hip_shift; the pelvis flank follows in step 3 ----------------
    for s, sg in (('l', 1), ('r', -1)):
        w = np.clip(wL[s] + 0.6 * W['pelvis'] * (np.sign(V[:, 0]) == sg) * smooth(np.abs(V[:, 0]), 4, 12), 0, 1)
        V[:, 0] += sg * P['hip_shift'] * w
        for k in J:
            if k.endswith('_' + s) and any(k.startswith(a) for a in LEGS): J[k] = [J[k][0] + [sg * P['hip_shift'], 0, 0], J[k][1] + [sg * P['hip_shift'], 0, 0]]
    # ---- 3. trunk sections: breadth / anterior depth / posterior depth factors by height (centre = section mid-depth) ---------------------
    z = V[:, 2]; H1 = J['thigh_l'][0][2]; SH1 = J['upperarm_l'][0][2]
    rz = (z - H1) / (SH1 - H1)                      # 0 at the hip joints, 1 at the shoulder joints (sculptor's working scale)
    bx = interp(rz, P['trunk_bx']); ba = interp(rz, P['trunk_ant']); bp = interp(rz, P['trunk_post'])
    cyz = {}
    for zc in np.arange(np.floor(z.min()), np.ceil(z.max()) + 1):
        mm = keep & (trw > 0.6) & (np.abs(z - zc) < 1.0)
        if mm.sum() > 8: cyz[zc] = 0.5 * (V[mm, 1].min() + V[mm, 1].max())
    zz = np.array(sorted(cyz)); cy = np.interp(z, zz, [cyz[k] for k in zz])
    wt = np.clip(trw + 0.7 * hnw * (z < NK + 4), 0, 1) * (1 - armw)
    dy = V[:, 1] - cy
    V[:, 0] = V[:, 0] + (bx - 1) * V[:, 0] * wt
    V[:, 1] = cy + dy * (1 + (np.where(dy > 0, ba, bp) - 1) * wt)
    # 3b. posterior pelvis: the soft human gluteal mass is reduced (sacrum -> hamstring continuity, no buttock dominance); applies to the
    #     posterior surface of the pelvis / upper thigh whatever its segment weight (gluteal skin is thigh-weighted in the substrate)
    gl = interp(rz, P['glute_post']); dy = V[:, 1] - cy; wg = (1 - armw) * (dy < 0) * smooth(-dy, 0.0, 8.0)
    V[:, 1] = cy + dy * (1 + (gl - 1) * wg)
    # ---- 4. shoulder girdle: arms carried outward with the thorax / girdle breadth -------------------------------------------------------
    for s, sg in (('l', 1), ('r', -1)):
        bxs = float(interp(np.array([1.0]), P['trunk_bx'])[0]); dx = (bxs - 1) * abs(J['upperarm_' + s][0][0]) + P['arm_extra_out']
        w = np.clip(wA[s] + W['clavicle_' + s] * smooth(np.abs(V[:, 0]), 6, 14), 0, 1)
        V[:, 0] += sg * dx * w
        for k in J:
            if k.endswith('_' + s) and any(k.startswith(a) for a in ARMS + ('index', 'middle', 'ring', 'pinky', 'thumb')): J[k] = [J[k][0] + [sg * dx, 0, 0], J[k][1] + [sg * dx, 0, 0]]
    # ---- 5. limb bone scale: radial cross-section scale about each long-bone axis, profile s(t) proximal -> distal ----------------------
    for seg, prof in P['limb_radial'].items():
        for s in 'lr':
            a, b = J['%s_%s' % (seg, s)]; ax = b - a; L = np.linalg.norm(ax); u = ax / L
            t = np.clip((V - a) @ u / L, -0.15, 1.15); foot = a + np.outer(t, ax); r = V - foot
            sc = interp(t, prof); w = W['%s_%s' % (seg, s)]
            V = V + r * ((sc - 1) * w)[:, None]
    # ---- 6. hands / feet: absolute size (hands about the wrist, feet about the ground point under the ankle) ---------------------------
    for s in 'lr':
        wr = J['hand_' + s][0]; wh = np.clip(W['hand_' + s] + W['fingers_' + s], 0, 1)[:, None]
        V = V * (1 - wh) + (wr + (V - wr) * P['hand_scale']) * wh
        an = J['foot_' + s][0].copy(); g0 = an.copy(); g0[2] = 0.0; wf = np.clip(W['foot_' + s] + W['ball_' + s] + 0.5 * W['calf_' + s] * smooth(-V[:, 2], -14, -6), 0, 1)[:, None]
        V = V * (1 - wf) + (g0 + (V - g0) * np.array([P['foot_scale'][0], P['foot_scale'][1], P['foot_scale'][2]])) * wf
    # ---- 7. neck root -------------------------------------------------------------------------------------------------------------------
    z = V[:, 2]; nw = np.clip(W['neck_01'] + 0.5 * W['head'], 0, 1) * (1 - smooth(z, NK + P['neck_root_span'][0], NK + P['neck_root_span'][1]))
    cxy = np.array([0.0, float(np.median(V[(W['neck_01'] > 0.5) & keep, 1]))])
    V[:, :2] = cxy + (V[:, :2] - cxy) * (1 + (P['neck_root_scale'] - 1) * nw)[:, None]
    # ---- 7b. surface fairing: Taubin smoothing of the sculpted body (hands, feet, head excluded) to remove field seams --------------------
    F0 = d['F']; F0 = F0[keep[F0].all(1)]; E = np.vstack([F0[:, [0, 1]], F0[:, [1, 2]], F0[:, [2, 0]]])
    deg = np.bincount(E.ravel(), minlength=len(V)).astype(float)
    fm = (keep * (1 - np.clip(sum(W[k] for k in W if k.startswith(('hand', 'fingers', 'foot', 'ball', 'head', 'ears'))), 0, 1)))[:, None]
    for it in range(2 * P.get('fair_iter', 4)):
        acc = np.zeros_like(V); np.add.at(acc, E[:, 0], V[E[:, 1]]); np.add.at(acc, E[:, 1], V[E[:, 0]])
        L = acc / np.maximum(deg, 1)[:, None] - V; V = V + (0.5 if it % 2 == 0 else -0.53) * L * fm
    # ---- 8. stature ---------------------------------------------------------------------------------------------------------------------
    V[:, 2] -= V[keep, 2].min(); st = V[keep, 2].max(); f = P['stature_cm'] / st; V *= f
    J = {k: [(h * f).tolist(), (t * f).tolist()] for k, (h, t) in J.items()}
    rep.update({'stature_cm': float(V[keep, 2].max()), 'final_scale': f})
    out = {k: d[k] for k in d.files}; out['V'] = V.astype(np.float32); out['joints'] = json.dumps(J)
    out['meta'] = json.dumps({'id': 'GO-RF', 'note': 'RM-OT-05K Branch B reference-first sculpt; joints = sculptor working axes carried through the sculpt, NOT a Gorrund skeleton', 'substrate': os.path.basename(sub), 'params': P})
    return out, rep

def write_obj(fn, V, F, keep):
    idx = np.where(keep)[0]; m = np.full(len(V), -1); m[idx] = np.arange(len(idx)); ff = m[F[keep[F].all(1)]]
    with open(fn, 'w') as o:
        o.write('# RAC RM-OT-05K Branch B GO-RF reference-first sculpt (k_rf.py); cm, Z up, +Y anterior, +X body left\n')
        for v in V[idx]: o.write('v %.5f %.5f %.5f\n' % tuple(v))
        for t in ff: o.write('f %d %d %d\n' % tuple(t + 1))

if __name__ == '__main__':
    P = json.load(open(sys.argv[1])); pre = sys.argv[2]; R = {}
    for st, sub in SUB.items():
        out, rep = sculpt(sub, P); np.savez(pre + '-%s_r6.npz' % st, **out)
        write_obj(pre + '-%s.obj' % st, out['V'], out['F'], out['keep'].astype(bool)); R[st] = rep
    json.dump(R, open(pre + '_build.json', 'w'), indent=1, default=float); print(json.dumps(R, default=float))
