# gripsolve2.py (bpy python, mathutils) -- RIGDIR SIDE TASK.json OUT.json
# = gripsolve.py + soft-tissue contact correctives: skin that presses into other skin (or into a claw) is pushed back
#   to the contact surface (half each side for skin-skin, all on the skin side against a rigid claw) and the push is
#   spread harmonically over a band (soft compression). The corrected mesh is what is judged; the per-frame
#   corrective offsets are saved so they can be baked as pose-driven corrective shape keys.
# Greedy contact-aware pose solver on the diagnostic rig. Each digit advances its flexion fraction in small steps (in the
# given order); after every step the actual skinned mesh (DQS) is checked:
#   - new self-intersections vs rest: skin-skin contact allowed up to SKIN_TOL penetration, claw contact up to CLAW_TOL
#   - fixture: no vertex deeper than FIX_TOL inside; a digit stops when it reaches contact (|d| <= CONTACT)
# A blocked step first tries small abduction offsets (fingers) before the digit is frozen. Every accepted state is a
# validated intermediate keyframe; the sequence is written out.
import sys, json, numpy as np, os, math, igl
sys.path.insert(0, '/tmp/claude-0/hand/tools'); from fastpose import Hand
import bpy
from mathutils.bvhtree import BVHTree
from scipy.spatial import cKDTree
import scipy.sparse as sp
from scipy.sparse.csgraph import connected_components
import pickle
a = sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else sys.argv[1:]
rd, side, taskf, outf = a[:4]
T = json.load(open(taskf)); H = Hand(rd, side); Q = H.Q
RD = pickle.load(open(os.path.join(rd, 'rig_data.pkl'), 'rb'))[side]; own = RD['own']; ker = RD['ker']
digs = {'L': ['A_L17', 'A_L18', 'A_L19', 'A_L20', 'A_Lthumb'], 'R': ['A_R21', 'A_R22', 'A_R23', 'A_R24', 'A_Rthumb']}[side]
fown = np.array([np.bincount(own[q] + 1, minlength=6).argmax() - 1 for q in Q]); kerq = ker[Q].all(1)
SKIN_TOL = T.get('skin_tol_mm', 1.0) / 1000; CLAW_TOL = T.get('claw_tol_mm', 0.5) / 1000
FIX_TOL = T.get('fixture_tol_mm', 0.5) / 1000; CONTACT = T.get('contact_mm', 0.5) / 1000
vq = [[] for _ in range(len(H.P0))]
for qi, q in enumerate(Q):
    for v in q: vq[v].append(qi)
def ring(qs): return np.unique(np.concatenate([vq[v] for v in np.unique(Q[qs])]))
def selfx(P):
    t = BVHTree.FromPolygons(P.tolist(), Q.tolist(), all_triangles=False, epsilon=0.0)
    pr = np.array(t.overlap(t), int).reshape(-1, 2); pr = pr[pr[:, 0] < pr[:, 1]]
    if len(pr): A = Q[pr[:, 0]]; B = Q[pr[:, 1]]; pr = pr[~(A[:, :, None] == B[:, None, :]).any((1, 2))]
    return pr
def depths(P, pairs):
    d = np.zeros(len(pairs))
    if not len(pairs): return d
    C = P[Q[pairs[:, 0]]].mean(1); e = np.array(list(cKDTree(C).query_pairs(0.004)), int).reshape(-1, 2); n = len(C)
    _, lab = connected_components(sp.coo_matrix((np.ones(len(e)), (e[:, 0], e[:, 1])), shape=(n, n)), directed=False)
    for c in np.unique(lab):
        m = lab == c; A = np.unique(pairs[m, 0]); B = np.unique(pairs[m, 1]); best = 0.0
        for X_, Y_ in ((A, B), (B, A)):
            Yr = np.setdiff1d(ring(Y_), X_)
            if not len(Yr): continue
            TT = np.vstack([Q[Yr][:, [0, 1, 2]], Q[Yr][:, [0, 2, 3]]])[:, ::-1]
            sd, _, _, _ = igl.signed_distance(P[np.unique(Q[X_])], P, TT, sign_type=igl.SIGNED_DISTANCE_TYPE_PSEUDONORMAL)
            sd = sd[np.abs(sd) < 0.005]
            if len(sd) and sd.min() < 0: best = max(best, -sd.min())
        d[m] = best
    return d
def fixture_sd(P, fx):
    c = np.array(fx['c']) / 100; ax = np.array(fx['ax'], float); ax /= np.linalg.norm(ax); r = fx['r'] / 100; hl = fx['hl'] / 100
    dd = P - c; t = dd @ ax; rad = np.linalg.norm(dd - t[:, None] * ax, axis=1); dr = rad - r; dt = np.abs(t) - hl
    return np.sqrt(np.maximum(dr, 0) ** 2 + np.maximum(dt, 0) ** 2) + np.minimum(np.maximum(dr, dt), 0)
def _oid(x): return -1 if x == 'palm' else digs.index(x)
SOFT = [(_oid(a_), _oid(b_), t_) for a_, b_, t_ in T.get('soft_contact', [])]
P0 = H.pose({}); rest = set(map(tuple, selfx(P0).tolist()))   # contacts are always judged against the true rest pose
BASE = {b: list(v) for b, v in T.get('base_angles', {}).items()}
def angles_of(state):
    ang = {b: list(v) for b, v in BASE.items()}
    for k, st in state.items():
        tgt = T['targets'].get(k, {})
        for b, v in tgt.items():
            v = [(st['f'] if b.endswith('_0') else st.get('g', st['f'])) * x for x in v]
            if b.endswith('_0') and 'thumb' not in k: v[1] += st['abd']
            ang[b] = [x + y for x, y in zip(ang.get(b, [0, 0, 0]), v)]
    return ang
CORR = T.get('correctives', False); CORR_MAX = T.get('corr_max_mm', 6.0) / 1000; BANDR = T.get('corr_band_cm', 0.6) / 100
RESID = T.get('resid_tol_mm', 0.5) / 1000; CREASE_RINGS = T.get('crease_rings', 10)
from scipy.sparse.csgraph import dijkstra
from scipy.spatial import cKDTree as _KD
Eall = np.vstack([Q[:, [0, 1]], Q[:, [1, 2]], Q[:, [2, 3]], Q[:, [3, 0]]]); nV = len(H.P0)
Aall = sp.coo_matrix((np.ones(len(Eall)), (Eall[:, 0], Eall[:, 1])), shape=(nV, nV)); Aall = ((Aall + Aall.T) > 0).astype(float).tocsr()
import scipy.sparse.linalg as _sla
def resolve_once(P, pairs):
    Dsp = np.zeros_like(P); hit = np.zeros(len(P), bool)
    if not len(pairs): return Dsp, hit
    C_ = P[Q[pairs[:, 0]]].mean(1); e = np.array(list(cKDTree(C_).query_pairs(0.004)), int).reshape(-1, 2); n_ = len(C_)
    _, lab = connected_components(sp.coo_matrix((np.ones(len(e)), (e[:, 0], e[:, 1])), shape=(n_, n_)), directed=False)
    for c in np.unique(lab):
        m = lab == c; A_ = np.unique(pairs[m, 0]); B_ = np.unique(pairs[m, 1])
        vA = np.unique(Q[A_]); vB = np.unique(Q[B_])
        dg_ = dijkstra(Aall, directed=False, indices=vA, limit=CREASE_RINGS, min_only=True, unweighted=True)
        if np.isfinite(dg_[vB]).any():
            # crease fold (one continuous patch of skin folding onto itself): smallest local smoothing that unfolds it
            core = np.zeros(len(P), bool); core[np.r_[vA, vB]] = True
            loc_ = core.copy()
            for _r in range(10): loc_ = loc_ | (Aall @ loc_.astype(float) > 0)
            lq = np.where(loc_[Q].all(1))[0]; Pm = P + Dsp
            for grow in range(T.get('crease_grow', 6) + 1):
                sel_ = core.copy()
                for _r in range(1 + grow): sel_ = sel_ | (Aall @ sel_.astype(float) > 0)
                sel_ &= ~ker; mv_ = np.where(sel_)[0]
                for _it in range(2 + grow):
                    Lc = (Aall[mv_] @ Pm) / np.asarray(Aall[mv_].sum(1)) - Pm[mv_]; Pm[mv_] += 0.5 * Lc
                t_ = BVHTree.FromPolygons(Pm.tolist(), Q[lq].tolist(), all_triangles=False, epsilon=0.0)
                pp = np.array(t_.overlap(t_), int).reshape(-1, 2); pp = pp[pp[:, 0] < pp[:, 1]]
                if len(pp):
                    aa = Q[lq][pp[:, 0]]; bb = Q[lq][pp[:, 1]]; pp = pp[~(aa[:, :, None] == bb[:, None, :]).any((1, 2))]
                    pp = np.array([p_ for p_ in map(tuple, np.sort(lq[pp], 1).tolist()) if p_ not in rest], int).reshape(-1, 2)
                if not len(pp): break
            dvv = Pm - P; mvv = np.where(np.linalg.norm(dvv - Dsp, axis=1) > 1e-9)[0]
            Dsp[mvv] = dvv[mvv]; hit[mvv] = True
            continue
        for X_, Y_ in ((A_, B_), (B_, A_)):
            if kerq[Y_].mean() > 0.3 and kerq[X_].mean() < 0.3:
                # rigid claw (Y) poking into skin (X): dent the skin under the claw tip
                Xg = X_
                for _g in range(T.get('dent_rings', 4)): Xg = ring(Xg)
                Xg = Xg[~kerq[Xg]]; Xr = np.setdiff1d(Xg, Y_); TX = np.vstack([Q[Xr][:, [0, 1, 2]], Q[Xr][:, [0, 2, 3]]])[:, ::-1]
                vY = np.unique(Q[Y_]); vY = vY[ker[vY]]
                if len(vY) and len(TX):
                    sdy, _, cpy, nny = igl.signed_distance(P[vY], P, TX, sign_type=igl.SIGNED_DISTANCE_TYPE_PSEUDONORMAL)
                    inn = (sdy < 0) & (sdy > -0.006)
                    if inn.any():
                        vXs = np.unique(Q[Xg]); vXs = vXs[~ker[vXs]]
                        for j in np.where(inn)[0]:
                            dep_ = -sdy[j] + 0.0004; Rr = 3.0 * dep_ + 0.003
                            dd_ = np.linalg.norm(P[vXs] - cpy[j], axis=1); m_ = dd_ < Rr
                            if not m_.any(): continue
                            fall = 1 - (dd_[m_] / Rr) ** 2
                            dv = -nny[j][None, :] * (dep_ * fall)[:, None]
                            better = np.linalg.norm(dv, axis=1) > np.linalg.norm(Dsp[vXs[m_]], axis=1)
                            Dsp[vXs[m_][better]] = dv[better]; hit[vXs[m_][better]] = True
                continue
            Yr = np.setdiff1d(ring(Y_), X_)
            if not len(Yr): continue
            TT = np.vstack([Q[Yr][:, [0, 1, 2]], Q[Yr][:, [0, 2, 3]]])[:, ::-1]
            vX = np.unique(Q[ring(X_)]); vX = vX[~ker[vX]]
            if not len(vX): continue
            sd, _, cp, _ = igl.signed_distance(P[vX], P, TT, sign_type=igl.SIGNED_DISTANCE_TYPE_PSEUDONORMAL)
            ins = (sd < 0) & (sd > -0.006)
            if not ins.any(): continue
            yk = kerq[Y_].mean() > 0.3
            share = 1.0 if yk else 0.5
            dv = (cp[ins] - P[vX[ins]]) * (share * 1.15) 
            better = np.linalg.norm(dv, axis=1) > np.linalg.norm(Dsp[vX[ins]], axis=1)
            Dsp[vX[ins][better]] = dv[better]; hit[vX[ins][better]] = True
    return Dsp, hit
def spread(P, Dsp, hit):
    if not hit.any(): return Dsp
    D = Dsp.copy(); Lp = (sp.diags(np.asarray(Aall.sum(1)).ravel()) - Aall).tocsr()
    for o in np.unique(own[hit]):
        ho = hit & (own == o)
        kd = _KD(P[ho]); dd, _ = kd.query(P, distance_upper_bound=BANDR)
        band = np.isfinite(dd) & ~hit & ~ker & (own == o)
        free = np.where(band)[0]
        if not len(free): continue
        fixed = np.where(~band)[0]
        A_ = Lp[free][:, free].tocsc(); B_ = Lp[free][:, fixed]
        lu = _sla.splu(A_); src_ = np.where(ho[:, None], Dsp, 0.0)
        for k in range(3): D[free, k] = lu.solve(-(B_ @ src_[fixed, k]))
    return D
def corrected(P, new):
    Dtot = np.zeros_like(P); Pc = P
    for rr in range(T.get('corr_rounds', 3)):
        if not len(new): break
        dep = depths(Pc, new); isc = (kerq[new[:, 0]] | kerq[new[:, 1]])
        sel = new[(dep > RESID * 0.5) | isc]
        if not len(sel): break
        Dsp, hit = resolve_once(Pc, sel)
        if not hit.any(): break
        D = spread(Pc, Dsp, hit); Dtot = Dtot + D; Pc = P + Dtot
        pr2 = selfx(Pc); new = np.array(sorted(set(map(tuple, pr2.tolist())) - rest), int).reshape(-1, 2)
    return Pc, Dtot, new
def check(state):
    P = H.pose(angles_of(state)); pr = selfx(P)
    if CORR:
        new0 = np.array(sorted(set(map(tuple, pr.tolist())) - rest), int).reshape(-1, 2)
        P, Dtot, _new = corrected(P, new0); pr = selfx(P)
        dn_ = np.linalg.norm(Dtot, axis=1)
        if DPREV[0] is not None and MOVER[0] is not None:
            grow_ = np.linalg.norm(Dtot - DPREV[0], axis=1) > 1e-4
            cmax = float(dn_[grow_].max()) if grow_.any() else 0.0
        else: cmax = float(dn_.max())
    else: Dtot = None; cmax = 0.0
    new = np.array(sorted(set(map(tuple, pr.tolist())) - rest), int).reshape(-1, 2)
    dep = depths(P, new); isc = (kerq[new[:, 0]] | kerq[new[:, 1]]) if len(new) else np.zeros(0, bool)
    tol = np.full(len(new), RESID if CORR else SKIN_TOL)
    for (oa, ob, tmm) in SOFT:
        if len(new):
            fa = fown[new[:, 0]]; fb = fown[new[:, 1]]
            m = ((fa == oa) & (fb == ob)) | ((fa == ob) & (fb == oa)); tol[m] = np.maximum(tol[m], tmm / 1000)
    viol = new[np.where(isc, dep > CLAW_TOL, dep > tol)] if len(new) else new
    if len(viol) and MOVER[0] is not None and T.get('viol_mover_only', True):
        mo_ = digs.index(MOVER[0]); viol = viol[(fown[viol[:, 0]] == mo_) | (fown[viol[:, 1]] == mo_)]
    if CORR and cmax > CORR_MAX: viol = np.vstack([viol, new[:1]]) if len(new) else np.array([[0, 0]])
    vd = set()
    for a_, b_ in viol: vd.add(int(fown[a_])); vd.add(int(fown[b_]))
    info = dict(pairs=int(len(new)), viol=int(len(viol)), skin_depth_mm=float(dep[~isc].max() * 1000) if (~isc).any() else 0.0,
                claw_depth_mm=float(dep[isc].max() * 1000) if isc.any() else 0.0, viol_owners=sorted(vd), corr_max_mm=cmax * 1000)
    if CORR: info['_D'] = Dtot
    contact = {}
    if T.get('fixture'):
        sd = fixture_sd(P, T['fixture'])
        for i_, k in enumerate(digs):
            m = own == i_
            if m.any(): contact[k] = dict(min_mm=float(sd[m].min() * 1000), pen=bool((sd[m] < -FIX_TOL).any()), touch=bool((np.abs(sd[m]) <= CONTACT).any()))
        palm = own < 0; contact['palm'] = dict(min_mm=float(sd[palm].min() * 1000), pen=bool((sd[palm] < -FIX_TOL).any()), touch=bool((np.abs(sd[palm]) <= CONTACT).any()))
        info['fixture'] = contact
        info['fixture_claw_pen'] = int(((sd < -FIX_TOL) & ker).sum())
    return info, P
CORRS = []; RESTD = {}; MOVER = [None]; DPREV = [None]
def keepD(info):
    D = info.pop('_D', None)
    if D is not None: DPREV[0] = D
    if D is not None:
        idx = np.where(np.linalg.norm(D, axis=1) > 1e-7)[0]; CORRS.append((idx, D[idx].astype(np.float32)))
    else: CORRS.append((np.zeros(0, int), np.zeros((0, 3), np.float32)))
    return info
PH = T['phases'] if 'phases' in T else [dict(targets=T['targets'], order=T['order'])]; frames = []; phase_results = []
for pi, ph in enumerate(PH):
  T['targets'] = ph['targets']; order = ph['order']; step = ph.get('step', T.get('step', 0.05))
  state = {k: dict(f=0.0, g=0.0, abd=0.0, done=False) for k in order}
  MOVER[0] = order[0]; info, P = check(state); MOVER[0] = None; frames.append(dict(phase=pi, state={k: dict(v) for k, v in state.items()}, angles=angles_of(state), info=keepD(info)))
  if info['viol']: print('WARN phase start viol', info, flush=True)
  it = 0
  while not all(state[k]['done'] for k in order) and it < 400:
      for k in order:
          st = state[k]
          if st['done']: continue
          if st['f'] >= 1.0 - 1e-9 and st['g'] >= 1.0 - 1e-9: st['done'] = True; continue
          i_ = digs.index(k); ok = False
          moves = [(step, step), (0, step), (step, 0)]
          if T.get('fixture'):   # finer steps so a digit can settle onto the fixture instead of jumping through it
              moves = moves + [(step / 2, step / 2), (step / 4, step / 4), (step / 8, step / 8), (0, step / 4), (step / 4, 0), (0, step / 8), (step / 8, 0)]
          tk_ = T['targets'].get(k, {}); hasf = any(b.endswith('_0') for b in tk_); hasg = any(not b.endswith('_0') for b in tk_)
          if not hasg: st['g'] = 1.0
          if not hasf: st['f'] = 1.0
          moves = [(df, dg) for (df, dg) in moves if (df == 0 or hasf) and (dg == 0 or hasg)]
          cands = [(df, dg, dabd) for (df, dg) in moves for dabd in ([0, 2, -2, 4, -4] if 'thumb' not in k and T.get('abd_search', True) else [0])
                   if not ((df > 0 and st['f'] >= 1 - 1e-9) or (dg > 0 and st['g'] >= 1 - 1e-9)) and abs(st['abd'] + dabd) <= T.get('abd_max', 6)]
          for (df, dg, dabd) in cands:
              trial = {kk: dict(vv) for kk, vv in state.items()}; trial[k]['f'] = min(1.0, st['f'] + df); trial[k]['g'] = min(1.0, st['g'] + dg); trial[k]['abd'] = st['abd'] + dabd
              MOVER[0] = k; inf, Pt = check(trial); it += 1; MOVER[0] = None
              if CORR and '_D' in inf and False: pass
              bad = inf['viol'] > 0
              if T.get('fixture'):
                  fx = inf['fixture']
                  if any(v['pen'] for v in fx.values()) or inf['fixture_claw_pen']: bad = True
              if not bad: ok = True; break
          if ok:
              state = trial; frames.append(dict(phase=pi, state={kk: dict(vv) for kk, vv in state.items()}, angles=angles_of(state), info=keepD(inf)))
              print(k, 'f %.2f g %.2f abd %.0f' % (state[k]['f'], state[k]['g'], state[k]['abd']), inf['pairs'], inf['viol'], round(inf['skin_depth_mm'], 2), round(inf['claw_depth_mm'], 2), 'corr %.2f' % inf.get('corr_max_mm', 0), flush=True)
              if T.get('fixture') and inf['fixture'][k]['touch'] and T.get('stop_on_contact', True): state[k]['done'] = True
              if k in T.get('stop_new_contact', []):
                  i_k = digs.index(k); dm = (own == i_k) & ~ker; om = (own != i_k)
                  if k not in RESTD:
                      d0_, _ = cKDTree(P0[om]).query(P0[dm], distance_upper_bound=0.01); RESTD[k] = np.where(np.isfinite(d0_), d0_, 0.01)
                  dc_, _ = cKDTree(Pt[om]).query(Pt[dm], distance_upper_bound=0.01); dc_ = np.where(np.isfinite(dc_), dc_, 0.01)
                  nc = (RESTD[k] > T.get('new_contact_rest_mm', 2.0) / 1000) & (dc_ <= T.get('stop_contact_mm', 1.0) / 1000)
                  if nc.any(): state[k]['done'] = True; print(k, 'new contact (%d verts) - natural stop' % nc.sum(), flush=True)
              st_ = ph.get('stop_targets', T.get('stop_targets', {})).get(k)
              if st_ is not None:
                  dm = (own == digs.index(k)); om = np.isin(own, [(-1 if o == 'palm' else digs.index(o)) for o in st_]) & ~ker
                  if T.get('stop_pad_only', True): dm &= (RD['W'][k + '_2'] + RD['W'][k + '_1'] > 0.5)
                  kk_ = (k, tuple(st_))
                  if kk_ not in RESTD:
                      d0_, _ = cKDTree(P0[om]).query(P0[dm], distance_upper_bound=0.01); RESTD[kk_] = np.where(np.isfinite(d0_), d0_, 0.01)
                  dd_, _ = cKDTree(Pt[om]).query(Pt[dm], distance_upper_bound=0.01); dd_ = np.where(np.isfinite(dd_), dd_, 0.01)
                  okv = RESTD[kk_] > T.get('new_contact_rest_mm', 2.0) / 1000
                  near = float(dd_[okv].min()) if okv.any() else 1.0
                  if near <= ph.get('stop_mm', {}).get(k, T.get('stop_contact_mm', 1.0)) / 1000: state[k]['done'] = True; print(k, 'contact with', st_, 'at %.2f mm' % (near * 1000), flush=True)
          else:
              st['done'] = True; print(k, 'blocked at f %.2f g %.2f' % (st['f'], st['g']), inf['viol_owners'], flush=True)
  # bake this phase into the base pose
  ang_ph = angles_of(state); phase_results.append(dict(phase=pi, state={k: dict(v) for k, v in state.items()})); BASE.clear(); BASE.update(ang_ph); T['targets'] = {}
  print('PHASE', pi, 'done', json.dumps({k: (round(v['f'], 2), round(v['g'], 2), v['abd']) for k, v in state.items()}), flush=True)
final_info, Pf = check(state); final_info = keepD(final_info)
json.dump(dict(task=json.load(open(taskf)), phases=phase_results, final=final_info, angles=angles_of({}), frames=frames), open(outf, 'w'), indent=1)
np.save(outf.replace('.json', '_posed.npy'), Pf.astype(np.float32))
if CORR:
    np.savez_compressed(outf.replace('.json', '_corr.npz'), **{'i%d' % k: c[0] for k, c in enumerate(CORRS)}, **{'d%d' % k: c[1] for k, c in enumerate(CORRS)})
print('FINAL', json.dumps(final_info)[:600])
