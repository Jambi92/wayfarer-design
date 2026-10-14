# HISTORICAL (RM-OT-05U3). Limitation found in RM-OT-05U4: s0 and the section component are derived from the mesh being measured,
# so applied to an edited return the planes / chords move with the editable anchors (moving-plane limitation). The fixed-reference
# replacement is tools/rac/w1/rmot05u4_drivers/u4_crease_ref.py; this file is kept unchanged otherwise as evidence.
# RM-OT-05U3 (READ-ONLY): reproducible crease-depth baselines on the UNCHANGED 05U RETURN for the proposed 05U2 region.
# Definition (all lengths in cm, Blender/world units, 1 unit = 1 cm):
#   frame      : the 05Q arm frame (origin O, axis d, e1 = normalize(Y x d), e2 = d x e1) from patch_selection.json;
#   plane      : P(s0) = { x : (x - O).d = s0 }, perpendicular to the arm axis, with s0 = (v - O).d for the named S3 vertex;
#   section    : exact mesh/plane intersection (edge interpolation) of every face crossing P(s0); segments are chained into
#                polylines; the polyline that passes through the region faces nearest the named vertex is used;
#   region     : the proposed 05U2 editable faces (797 interface + 35 added = 832); the in-region run is the contiguous part of
#                that polyline lying on region faces; it must enter and leave the region exactly once (2 endpoints), otherwise
#                the section is reported AMBIGUOUS and not used (a closed section loop is first rotated to start on a
#                non-region face, so a run cannot be split at the loop's start index);
#   endpoints  : the two points where the run crosses a region/non-region edge; both vertices of such an edge are frozen
#                (proposed frozen ring), so the chord is fixed geometry during any approved sculpt;
#   depth      : for every run point p, signed distance from the chord line within the plane, positive toward the arm axis
#                point O + s0 d (i.e. into the groove); crease depth = the maximum positive value; deepest point reported;
#   limit      : 75 % of the baseline depth (the 05U2 stop condition).
import argparse, json, os, sys, numpy as np, trimesh
from collections import defaultdict
here = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(here, '..', 'rmot05s_drivers')); import s_lib
def section(V, F, region, O, d, s0):
    sd = (V - O) @ d - s0; sv = sd[F]; cr = np.where((sv.min(1) < 0) & (sv.max(1) > 0))[0]
    segs = []
    for fi in cr:
        f = F[fi]; pts = []; eds = []
        for i, j in ((0, 1), (1, 2), (2, 0)):
            a_, b_ = f[i], f[j]
            if (sd[a_] < 0) != (sd[b_] < 0):
                t = sd[a_] / (sd[a_] - sd[b_]); pts.append(V[a_] + t * (V[b_] - V[a_])); eds.append(tuple(sorted((int(a_), int(b_)))))
        if len(pts) == 2: segs.append((int(fi), eds[0], eds[1], pts[0], pts[1]))
    return segs
def chain(segs):
    by_edge = defaultdict(list)
    for k, s in enumerate(segs): by_edge[s[1]].append(k); by_edge[s[2]].append(k)
    used = set(); lines = []
    for k0 in range(len(segs)):
        if k0 in used: continue
        line = [k0]; used.add(k0)
        for direction in (0, 1):
            cur = k0; e = segs[k0][2] if direction == 0 else segs[k0][1]
            while True:
                nx = [k for k in by_edge[e] if k not in used]
                if not nx: break
                k = nx[0]; used.add(k); line = line + [k] if direction == 0 else [k] + line; e = segs[k][2] if segs[k][1] == e else segs[k][1]
        lines.append(line)
    return lines
def ordered_points(segs, line):
    if len(line) == 1: s = segs[line[0]]; return [s[3], s[4]], [s[0]]
    pts = []; faces = []
    first = segs[line[0]]; second = segs[line[1]]; shared = set(first[1:3]) & set(second[1:3]); e_prev = (set(first[1:3]) - shared).pop()
    for k in line:
        s = segs[k]; p_in, p_out = (s[3], s[4]) if s[1] == e_prev else (s[4], s[3]); e_out = s[2] if s[1] == e_prev else s[1]
        if not pts: pts.append(p_in)
        pts.append(p_out); faces.append(s[0]); e_prev = e_out
    return pts, faces
def measure(V, F, region, fr, v, name):
    s0 = float((V[v] - fr.O) @ fr.d); segs = section(V, F, region, fr.O, fr.d, s0); lines = chain(segs)
    best = None
    for line in lines:
        pts, faces = ordered_points(segs, line); P = np.array(pts); dist = np.linalg.norm(P - V[v], axis=1).min()
        if any(region[f] for f in faces) and (best is None or dist < best[0]): best = (dist, P, faces)
    _, P, faces = best; closed = bool(np.linalg.norm(P[0] - P[-1]) < 1e-9)
    if closed:                                              # closed section loop: rotate to start on a non-region face so a run cannot wrap
        r0 = next(i for i, f in enumerate(faces) if not region[f]); faces = faces[r0:] + faces[:r0]; P = np.vstack([P[r0:-1], P[:r0], P[r0:r0 + 1]])
    inr = np.array([region[f] for f in faces])
    runs = []; k = 0
    while k < len(inr):
        if inr[k]:
            j = k
            while j + 1 < len(inr) and inr[j + 1]: j += 1
            runs.append((k, j)); k = j + 1
        else: k += 1
    res = dict(name=name, s3_vertex0=int(v), s0_cm=round(s0, 4), closed_section_loop=closed, plane='(x - O).d = s0 (perpendicular to the 05Q arm axis)', section_polyline_points=int(len(P)), region_runs=len(runs))
    if len(runs) != 1 or (not closed and (runs[0][0] == 0 or runs[0][1] == len(inr) - 1)):   # open polylines must enter and exit inside the mesh
        res['status'] = 'AMBIGUOUS'; return res, None
    i0, i1 = runs[0]; R_ = P[i0:i1 + 2]                     # point i is the entry of face i; run faces i0..i1 -> points i0..i1+1
    A_, B_ = R_[0], R_[-1]; axisp = fr.O + s0 * fr.d; u = (B_ - A_) / np.linalg.norm(B_ - A_)
    nrm = np.cross(fr.d, u); nrm /= np.linalg.norm(nrm)
    if (axisp - A_) @ nrm < 0: nrm = -nrm
    dep = (R_ - A_) @ nrm; k = int(np.argmax(dep))
    res.update(status='OK', endpoints=[np.round(A_, 5).tolist(), np.round(B_, 5).tolist()], chord_cm=round(float(np.linalg.norm(B_ - A_)), 4), run_points=int(len(R_)),
               depth_cm=round(float(dep[k]), 4), deepest_point=np.round(R_[k], 5).tolist(), limit_75pct_cm=round(0.75 * float(dep[k]), 4),
               min_signed_depth_cm=round(float(dep.min()), 4), sign='positive = toward the arm-axis point O + s0 d (into the groove)')
    return res, (R_, A_, B_, nrm, u, k, P, s0)
if __name__ == '__main__':
    ap = argparse.ArgumentParser(); [ap.add_argument(k) for k in ('--s3', '--baseline', '--proposal', '--out')]; a = ap.parse_args(); os.makedirs(a.out, exist_ok=True)
    fr = s_lib.Frame('reviews/rac-rmot05q-evidence/plan/patch_selection.json')
    s3 = trimesh.load(a.s3, process=False); Vs = np.asarray(s3.vertices); F = np.asarray(s3.faces)
    B = np.load(a.baseline); bid = B['s3_vid1'] - 1; V = Vs.copy(); mv = ~np.all(B['V'] == Vs[bid].astype(np.float32), 1); V[bid[mv]] = B['V'][mv].astype(np.float64)
    lab = np.load('reviews/rac-rmot05s-evidence/repair/S3/GO-05S-S3_face_labels.npy'); region = (lab == 4) | (lab == 5)
    region[np.load(os.path.join(a.proposal, 'proposal_sets.npz'))['added_faces']] = True
    import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
    out = dict(definition=open(__file__).read().split('import argparse')[0], baseline='05U RETURN (unchanged), return.npz sha 0989caf4...', results=[])
    fig, ax = plt.subplots(1, 2, figsize=(14, 6.5))
    for i, (nm, v) in enumerate((('section_A_61581', 61581), ('section_B_61580', 61580))):
        r, g = measure(V, F, region, fr, v, nm); out['results'].append(r); print(json.dumps(r))
        A = ax[i]
        if g is None: A.set_title('%s: AMBIGUOUS' % nm); continue
        R_, A_, B_, nrm, u, k, P, s0 = g
        to2 = lambda X: np.c_[(X - A_) @ u, (X - A_) @ nrm]
        Pp = to2(P); A.plot(Pp[:, 0], Pp[:, 1], color='0.7', lw=1, label='full section (05U baseline)')
        Rp = to2(R_); A.plot(Rp[:, 0], Rp[:, 1], 'b-', lw=2, label='in proposed region'); A.plot([0, Rp[-1, 0]], [0, 0], 'k--', lw=1, label='chord (frozen-ring endpoints)')
        A.plot(Rp[[0, -1], 0], Rp[[0, -1], 1], 'ks', ms=6); A.plot(Rp[k, 0], Rp[k, 1], 'ro', ms=7, label='deepest point: %.3f cm' % r['depth_cm'])
        A.axhline(0.75 * r['depth_cm'], color='r', lw=0.8, ls=':', label='75 %% limit: %.3f cm' % r['limit_75pct_cm'])
        A.set_title('%s  (S3 v%d, s0 = %.3f cm, plane perpendicular to arm axis)' % (nm, v, s0), fontsize=9); A.set_xlabel('along chord (cm)'); A.set_ylabel('depth toward arm axis (cm)')
        A.set_aspect('equal'); A.grid(alpha=.3); A.legend(fontsize=7); A.set_xlim(Rp[:, 0].min() - 2, Rp[:, 0].max() + 2); A.set_ylim(min(Rp[:, 1].min(), 0) - 1.5, Rp[:, 1].max() + 1.5)
    plt.tight_layout(); plt.savefig(os.path.join(a.out, 'crease_sections.png'), dpi=110); json.dump(out, open(os.path.join(a.out, 'crease_baseline.json'), 'w'), indent=1)
