# toe2_local_audit.py V4_CORE V5_CORE TW0_CORE OUT.json : order 33a2dfe §9 / §12 -- local toe-2 web / root audit of the final successor (v005 racetrack)
# against the rejected v004 closed ring and the ring-free parent (tw0), on all four configurations:
#   quality of the toe-2 patch (faces touching the toe-2 support vertices): T-4 angle / aspect violations, aspect > 10, max / p95 aspect, angle p1 / p99;
#   anatomy of the foot: production -> source deviation of the patch, source -> production near the patch, toe-tip / MTP / IP joint positions, forefoot
#   width at the ball, sole contact (lowest 2 mm vertex count, minimum z), retained-vertex displacement v004 -> v005.
import sys, json, numpy as np, trimesh
sys.path.insert(0, '/home/claude/wayfarer-design/tools/rac/rp/marchfolk_rp3_v001')
from v004_lib import *
z4, z5, z0 = (np.load(p) for p in sys.argv[1:4]); OUT = sys.argv[4]; B = load_base(); n3 = int(z5['n_v003']); nb = int(z5['n_base'])
M4, M5, M0 = csr(z4), csr(z5), csr(z0); Q4, Q5, Q0 = (np.asarray(z['Q']) for z in (z4, z5, z0))
t2_4 = n3 + np.nonzero(np.char.startswith(z4['ring_name'], 'toe2'))[0]; rc5 = z5['row_class']; t2_5 = np.array(sorted(set(np.nonzero(rc5 >= 5)[0].tolist()) | {t['val5_corner'] for t in json.loads(str(z5['log']))['turns']}), int)   # racetrack vertices + its valence-5 corners
f4 = np.nonzero(np.isin(Q4, t2_4).any(1))[0]; f5 = np.nonzero(np.isin(Q5, t2_5).any(1))[0]
k5 = {tuple(sorted(q)) for q in Q5.tolist()}; k4 = {tuple(sorted(q)) for q in Q4.tolist()}
p5 = [f for f, q in enumerate(Q0.tolist()) if tuple(sorted(q)) not in k5]; p4 = [f for f, q in enumerate(Q0.tolist()) if tuple(sorted(q)) not in k4 and max(q) < nb]
def qstats(V, Q):
    a, s, va, vs = quality(V, Q); return dict(quads=int(len(Q)), T4=int((va | vs).sum()), angle_viol=int(va.sum()), aspect_viol=int(vs.sum()), aspect_gt10=int((s > 10).sum()), aspect_max=round(float(s.max()), 2),
                                              aspect_p95=round(float(np.percentile(s, 95)), 2), angle_p1=round(float(np.percentile(a, 1)), 1), angle_p99=round(float(np.percentile(a, 99)), 1))
R = {}
for cid in CFG:
    Vh = B['C'][cid]['Vh']; V4, V5, V0 = M4 @ Vh, M5 @ Vh, M0 @ Vh; meta = B['C'][cid]['meta']; JC = {k: np.array(v) for k, v in meta['joint_cubes'].items()}; H = {k: np.array(v) for k, v in meta['heads'].items()}
    r6 = np.load(R6[cid]); src = trimesh.Trimesh(r6['V'].astype(float), r6['F'], process=False); _, d5, _ = trimesh.proximity.closest_point(src, V5[t2_5])
    from scipy.spatial import cKDTree
    near = r6['V'][r6['keep']].astype(float); near = near[cKDTree(V5[t2_5]).query(near)[0] < 1.5]
    prod = trimesh.Trimesh(V5, np.r_[Q5[:, [0, 1, 2]], Q5[:, [0, 2, 3]]], process=False); _, ds, _ = trimesh.proximity.closest_point(prod, near)
    prod4 = trimesh.Trimesh(V4, np.r_[Q4[:, [0, 1, 2]], Q4[:, [0, 2, 3]]], process=False); _, ds4, _ = trimesh.proximity.closest_point(prod4, near)
    common = np.arange(n3); mv = np.linalg.norm(V5[common] - V4[common], axis=1)
    feet = {}
    for s in 'lr':
        fv = V5[(np.abs(V5[:, 0] - H['foot_' + s][0]) < 8) & (V5[:, 2] < 12)]; fv4 = V4[(np.abs(V4[:, 0] - H['foot_' + s][0]) < 8) & (V4[:, 2] < 12)]
        ball = lambda P: P[np.abs(P[:, 1] - H['ball_' + s][1]) < 1.0]
        tips = {}
        for t in range(1, 6):
            ks = sorted([k for k in JC if k.startswith('%s-toe-%d-' % (s, t))], key=lambda k: int(k.split('-')[-1])); a_, b_ = JC[ks[-2]], JC[ks[-1]]; ax = unit(b_ - a_)
            sel5 = V5[np.linalg.norm(V5 - b_, axis=1) < 2.0]; sel4 = V4[np.linalg.norm(V4 - b_, axis=1) < 2.0]
            tips['toe%d' % t] = round(float(np.linalg.norm(sel5[np.argmax(sel5 @ ax)] - sel4[np.argmax(sel4 @ ax)]) * 10), 4)
        feet[s] = dict(forefoot_width_cm=[round(float(np.ptp(ball(fv4)[:, 0])), 4), round(float(np.ptp(ball(fv)[:, 0])), 4)], sole_min_z_cm=[round(float(fv4[:, 2].min()), 4), round(float(fv[:, 2].min()), 4)],
                       sole_contact_verts_2mm=[int((fv4[:, 2] < fv4[:, 2].min() + 0.2).sum()), int((fv[:, 2] < fv[:, 2].min() + 0.2).sum())], toe_tip_shift_v004_to_v005_mm=tips)
    R[cid] = dict(v004_toe2_ring_patch=qstats(V4, Q4[f4]), v005_racetrack_patch=qstats(V5, Q5[f5]), tw0_parent_faces_of_racetrack=qstats(V0, Q0[p5]), tw0_parent_faces_of_v004_ring=qstats(V0, Q0[p4]) if len(p4) else None,
                  patch_prod_to_source_max_mm=round(float(d5.max() * 10), 4), source_to_prod_near_patch_max_mm=dict(v004=round(float(ds4.max() * 10), 4), v005=round(float(ds.max() * 10), 4)),
                  retained_vertex_shift_v004_to_v005=dict(moved=int((mv > 1e-9).sum()), max_mm=round(float(mv.max() * 10), 4)), joints='rig joint cubes / landmarks unchanged (source rig; see landmark diff)', feet=feet)
    # region delta vs the ring-free parent tw0: candidate region = faces touching the toe-2 support vertices; tw0 footprint = the tw0 faces those
    # replace (split parents) + the same unchanged faces. Delta = what the toe-2 support itself adds.
    k0 = {tuple(sorted(q)): f for f, q in enumerate(Q0.tolist())}
    def delta(Vc, Qc, faces, Mc):
        unchanged = [k0[tuple(sorted(Qc[f].tolist()))] for f in faces if tuple(sorted(Qc[f].tolist())) in k0]
        kc = {tuple(sorted(q)) for q in Qc.tolist()}; parents = [f for f, q in enumerate(Q0.tolist()) if tuple(sorted(q)) not in kc and max(q) < nb]
        foot = sorted(set(unchanged) | set(parents)); a, s_, va, vs = quality(Vc, Qc[faces]); a0, s0, va0, vs0 = quality(V0, Q0[foot])
        return dict(region_quads=int(len(faces)), tw0_footprint_quads=int(len(foot)), T4=[int((va0 | vs0).sum()), int((va | vs).sum())], angle_viol=[int(va0.sum()), int(va.sum())], aspect_viol=[int(vs0.sum()), int(vs.sum())],
                    aspect_gt10=[int((s0 > 10).sum()), int((s_ > 10).sum())], angle_min=[round(float(a0.min()), 1), round(float(a.min()), 1)], angle_max=[round(float(a0.max()), 1), round(float(a.max()), 1)],
                    aspect_p95=[round(float(np.percentile(s0, 95)), 2), round(float(np.percentile(s_, 95)), 2)], note='[tw0 footprint, candidate]')
    R[cid]['delta_vs_tw0'] = dict(v004_ring=delta(V4, Q4, f4, M4), v005_racetrack=delta(V5, Q5, f5, M5))
    print(cid, json.dumps({k: v for k, v in R[cid].items() if k != 'feet'}), flush=True)
json.dump(R, open(OUT, 'w'), indent=1)
