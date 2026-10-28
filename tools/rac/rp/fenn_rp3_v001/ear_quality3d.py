# ear_quality3d.py : order 0d9c70b -- 3-D corner-angle quality pass for the Fenn ear-branch cuff (+ the bounded transition ring).
# Free: cuff + transition vertices. Fixed: root loop, junction ring J, ear sheet, the rest of v005.
# E = sum over corners of faces touching free vertices of relu(theta - hi)^2 + relu(lo - theta)^2 (deg)
#   + ks * sum over their edges (l / l0 - 1)^2                      (keep the faired sizing)
#   + kn * sum over free vertices ((x - x0) . n0 / h0)^2             (slide tangentially on the faired skin; h0 = local mean edge)
#   + (kt [transition] + kd [all free]) * |x - x0|^2 / h0^2          (transition ring stays bounded; kd limits all slides)
#   + barrier: no edge shorter than rho x its starting length
import numpy as np
from scipy.optimize import minimize

def _vertex_normals(V, Q):
    n = np.zeros_like(V)
    for k in range(4):
        a = V[Q[:, k]]; b = V[Q[:, (k + 1) % 4]]; c = V[Q[:, (k - 1) % 4]]; fn = np.cross(b - a, c - a)
        np.add.at(n, Q[:, k], fn)
    return n / (np.linalg.norm(n, axis=1, keepdims=True) + 1e-12)

def contact_pairs(V, Q, free, region, r=0.6, dmax=0.45, tol=0.15, keep=None):
    """(vertex, face, initial side, margin) pairs: free vertex v whose foot point lies inside a nearby face f not incident to v or its 1-ring"""
    from scipy.spatial import cKDTree
    Fc = np.nonzero(region[Q].all(1))[0]; C = V[Q[Fc]].mean(1); t = cKDTree(C); nb = [set() for _ in range(len(V))]
    for q in Q[np.nonzero(region[Q].any(1))[0]]:
        for v in q: nb[v].update(q.tolist())
    out = []
    for v in np.nonzero(free)[0]:
        ex = {int(v)}
        for j in t.query_ball_point(V[v], r):
            f = Fc[j]; q = Q[f]
            if ex & set(q.tolist()): continue
            P = V[q]; n = np.cross(P[2] - P[0], P[3] - P[1]); n /= np.linalg.norm(n) + 1e-12; d = (V[v] - P.mean(0)) @ n
            if abs(d) > dmax: continue
            x = V[v] - d * n; inside = False
            for tri in ((0, 1, 2), (0, 2, 3)):
                a, b, c = P[list(tri)]; v0, v1, v2 = b - a, c - a, x - a; d00, d01, d11, d20, d21 = v0 @ v0, v0 @ v1, v1 @ v1, v2 @ v0, v2 @ v1
                den = d00 * d11 - d01 * d01 + 1e-18; bb = (d11 * d20 - d01 * d21) / den; cc = (d00 * d21 - d01 * d20) / den
                if bb >= -tol and cc >= -tol and bb + cc <= 1 + tol: inside = True
            if inside: out.append((int(v), int(f), float(np.sign(d) or 1.0), float(keep * abs(d)) if keep else float(min(0.5 * abs(d), 0.03))))
    return out

def quality3d(V, Q, free, trans, lo=55.0, hi=125.0, ks=50.0, kn=400.0, kt=20.0, rho=0.5, kap=2.0e4, iters=600, kd=0.0, pairs=None, kc=2.0e5, amax=6.0, ka=2.0e3, _energy_only=False, warm=None, root_pairs=None, kr=2.0e3, th_cap=55.0):
    Fsel = np.nonzero(free[Q].any(1))[0]; Fq = Q[Fsel]
    e = np.unique(np.sort(np.r_[Fq[:, [0, 1]], Fq[:, [1, 2]], Fq[:, [2, 3]], Fq[:, [3, 0]]], 1), axis=0)
    l0 = np.linalg.norm(V[e[:, 0]] - V[e[:, 1]], axis=1) + 1e-9
    fi = np.nonzero(free)[0]; X0 = V.copy(); n0 = _vertex_normals(V, Q)[fi]
    h = np.zeros(len(V)); c = np.zeros(len(V)); np.add.at(h, e[:, 0], l0); np.add.at(h, e[:, 1], l0); np.add.at(c, e[:, 0], 1); np.add.at(c, e[:, 1], 1)
    h0 = (h / np.maximum(c, 1))[fi]; istr = trans[fi]
    if pairs:
        pv = np.array([p_[0] for p_ in pairs]); pq = Q[np.array([p_[1] for p_ in pairs])]; ps = np.array([p_[2] for p_ in pairs]); pm = np.array([p_[3] for p_ in pairs])
    else: pv = None
    G2 = np.zeros_like(V)
    if root_pairs:
        rf1 = Q[np.array([r_[0] for r_ in root_pairs])]; rf2 = Q[np.array([r_[1] for r_ in root_pairs])]; rsg = np.array([r_[2] for r_ in root_pairs], float); rp = True
    else: rp = None
    def energy(z):
        X = X0.copy(); X[fi] = z.reshape(-1, 3); G = np.zeros_like(X); P = X[Fq]; E_ = 0.0
        for k in range(4):
            pk = P[:, k]; w = P[:, (k + 1) % 4] - pk; u = P[:, (k - 1) % 4] - pk
            cr = np.cross(w, u); a = np.sqrt((cr * cr).sum(1) + 1e-10); b = (w * u).sum(1); th = np.degrees(np.arctan2(a, b))   # smooth at 0 / 180 deg
            eh = np.maximum(th - hi, 0); el = np.maximum(lo - th, 0); E_ += (eh ** 2 + el ** 2).sum()
            dE = (2 * eh - 2 * el) * (180 / np.pi); den = a * a + b * b + 1e-18
            # d theta = (b da - a db) / (a^2 + b^2); da/dw = (u x cr_hat), da/du = (cr_hat x w); db/dw = u, db/du = w
            ch = cr / a[:, None]
            gw = ((b / den)[:, None] * np.cross(u, ch) - (a / den)[:, None] * u) * dE[:, None]
            gu = ((b / den)[:, None] * np.cross(ch, w) - (a / den)[:, None] * w) * dE[:, None]
            np.add.at(G, Fq[:, (k + 1) % 4], gw); np.add.at(G, Fq[:, (k - 1) % 4], gu); np.add.at(G, Fq[:, k], -gw - gu)
        d = X[e[:, 0]] - X[e[:, 1]]; l = np.linalg.norm(d, axis=1) + 1e-12; r_ = l / l0 - 1; v = np.maximum(rho * l0 - l, 0) / l0
        E_ += ks * (r_ ** 2).sum() + kap * (v ** 2).sum(); gl = ((2 * ks * r_ - 2 * kap * v) / l0)[:, None] * d / l[:, None]
        np.add.at(G, e[:, 0], gl); np.add.at(G, e[:, 1], -gl)
        D = X[fi] - X0[fi]; dn = (D * n0).sum(1) / h0; E_ += kn * (dn ** 2).sum(); G0f = G[fi].copy(); Gf = G[fi] + (2 * kn * dn / h0)[:, None] * n0
        dt = (D ** 2).sum(1) / h0 ** 2; wd = kt * istr + kd; E_ += (wd * dt).sum(); Gf += (2 * wd / h0 ** 2)[:, None] * D
        if ka > 0:                                                                # aspect barrier: no edge-length ratio inside a quad above amax
            Ls = []; Ds = []
            for k in range(4):
                dk = P[:, (k + 1) % 4] - P[:, k]; Ds.append(dk); Ls.append(np.linalg.norm(dk, axis=1) + 1e-12)
            for i_ in range(4):
                for j_ in range(4):
                    if i_ == j_: continue
                    vv = np.maximum(np.log(Ls[i_] / Ls[j_]) - np.log(amax), 0)                 # log-ratio barrier (well scaled on short edges)
                    if not vv.any(): continue
                    E_ += ka * (vv ** 2).sum(); c_ = 2 * ka * vv
                    gi = (c_ / Ls[i_] / Ls[i_])[:, None] * Ds[i_]; gj = (-c_ / Ls[j_] / Ls[j_])[:, None] * Ds[j_]
                    np.add.at(G, Fq[:, (i_ + 1) % 4], gi); np.add.at(G, Fq[:, i_], -gi); np.add.at(G, Fq[:, (j_ + 1) % 4], gj); np.add.at(G, Fq[:, j_], -gj)
            Gf = Gf + G[fi] - G0f                                               # (G was already folded into Gf above; add only the new part)
        if rp is not None:                                                        # root crease: dihedral across each root-loop edge <= th_cap (deg)
            ns_ = []; gm_ = []
            for FF in (rf1, rf2):
                P4 = X[FF]; a4 = P4[:, 2] - P4[:, 0]; b4 = P4[:, 3] - P4[:, 1]; m4 = np.cross(a4, b4); mn = np.linalg.norm(m4, axis=1) + 1e-12; ns_.append((m4 / mn[:, None], mn, a4, b4))
            n1, mn1, a1, b1 = ns_[0]; n2, mn2, a2, b2 = ns_[1]; cc = np.clip((n1 * n2).sum(1) * rsg, -1 + 1e-9, 1 - 1e-9); th_ = np.degrees(np.arccos(cc))
            vi = np.maximum(th_ - th_cap, 0); E_ += kr * (vi ** 2).sum()
            dEdc = 2 * kr * vi * (180 / np.pi) * (-1 / np.sqrt(1 - cc ** 2)) * rsg
            for (nA, mnA, aA, bA, FF, nB) in ((n1, mn1, a1, b1, rf1, n2), (n2, mn2, a2, b2, rf2, n1)):
                gn = dEdc[:, None] * nB; gm = (gn - (gn * nA).sum(1)[:, None] * nA) / mnA[:, None]; ga = np.cross(bA, gm); gb = np.cross(gm, aA)
                np.add.at(G2, FF[:, 2], ga); np.add.at(G2, FF[:, 0], -ga); np.add.at(G2, FF[:, 3], gb); np.add.at(G2, FF[:, 1], -gb)
            Gf += G2[fi]; G2[:] = 0
        if pv is not None:                                                        # contact guard: keep each (vertex, face) pair on its side
            P4 = X[pq]; a4 = P4[:, 2] - P4[:, 0]; b4 = P4[:, 3] - P4[:, 1]; m4 = np.cross(a4, b4); mn = np.linalg.norm(m4, axis=1) + 1e-12; nf = m4 / mn[:, None]
            r4 = X[pv] - P4.mean(1); dd = (r4 * nf).sum(1) * ps; vi = np.maximum(pm - dd, 0); E_ += kc * (vi ** 2).sum()
            cg = (-2 * kc * vi * ps)                                               # dE / d(signed distance d)
            gv = cg[:, None] * nf; np.add.at(G2, pv, gv)
            for k in range(4): np.add.at(G2, pq[:, k], -0.25 * gv)
            gm = cg[:, None] * (r4 - (r4 * nf).sum(1)[:, None] * nf) / mn[:, None]    # through the normal: d n / d m = (I - n n^T) / |m|
            ga = np.cross(b4, gm); gb = np.cross(gm, a4)
            np.add.at(G2, pq[:, 2], ga); np.add.at(G2, pq[:, 0], -ga); np.add.at(G2, pq[:, 3], gb); np.add.at(G2, pq[:, 1], -gb)
            Gf += G2[fi]; G2[:] = 0
        return E_, Gf.ravel()
    if _energy_only: return energy, X0[fi].ravel()
    E0 = energy(X0[fi].ravel())[0]
    x_start = X0[fi].ravel() if warm is None else warm[fi].ravel()
    r = minimize(energy, x_start, jac=True, method='L-BFGS-B', options=dict(maxiter=iters))
    Vn = X0.copy(); Vn[fi] = r.x.reshape(-1, 3)
    disp = np.linalg.norm(Vn[fi] - X0[fi], axis=1); dn = np.abs(((Vn[fi] - X0[fi]) * n0).sum(1))
    return Vn, dict(E0=float(E0), E1=float(r.fun), nit=int(r.nit), msg=str(r.message), free=int(len(fi)), faces=int(len(Fsel)), disp_max_cm=float(disp.max()), disp_mean_cm=float(disp.mean()),
                    normal_dev_max_cm=float(dn.max()), transition_disp_max_cm=float(disp[istr.astype(bool)].max()) if istr.any() else 0.0,
                    params=dict(lo=lo, hi=hi, ks=ks, kn=kn, kt=kt, kd=kd, rho=rho, iters=iters, kc=kc, amax=amax, ka=ka, contact_pairs=len(pairs or []), root_pairs=len(root_pairs or []), kr=kr, th_cap=th_cap))
