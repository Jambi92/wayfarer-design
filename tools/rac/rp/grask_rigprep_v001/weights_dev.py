# weights_dev.py RIG.json W0.npz LANDMARKS.json OUTDIR TAG K : logged LOCAL diagnostic weight candidate (order 8918cea §5).
# Starting from the baseline array W0 (bone heat + midline cleanup), in the shoulder/axilla, elbow, wrist, hand/thumb/fingers, hip/groin
# and knee regions only:
#   1. leakage removal  — a vertex of a limb part keeps weight only on bones of its own chain (+ girdle / pelvis roots);
#   2. smooth joint transitions — for the limb's own vertices near a joint, the parent/child split becomes a smoothstep of the signed
#      distance along the joint axis, scaled by the local limb radius (half-width K * r); the pair's total share is preserved and the
#      parent share keeps its existing distribution over the parent set;
#   3. three Laplacian smoothing passes inside the edited regions, then normalisation;
#   4. nail binding — nail-cap vertices of each distal phalanx are bound 100 % to the distal digit bone.
# Geometry, skeleton and bone set are untouched. Writes OUTDIR/weights_TAG.npz, OUTDIR/weights_TAG_log.json (changed vertex ids per region).
import sys, os, json, hashlib, numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); sys.path.insert(0, '/tmp/claude-0/rt')
from diag_lib import bl_to_src
from common import PARTS
RJ, W0F, LMF, O, TAG, K = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], float(sys.argv[6])
os.makedirs(O, exist_ok=True)
rig = json.load(open(RJ)); B = {b['name']: b for b in rig['bones']}
z = np.load(W0F); W = z['W'].astype(np.float64).copy(); names = [str(n) for n in z['names']]; col = {n: i for i, n in enumerate(names)}; W0 = W.copy()
M = np.load('/tmp/claude-0/rt/frz/v003_frz.npz'); V = M['V'].astype(float); Q = np.asarray(M['Q']); FP = M['FP']
LM = json.load(open(LMF))['joints']; Jc = lambda k: np.array(LM[k]['position_source_frame_cm'])
vpart = np.empty(len(V), object); vpart[Q.ravel()] = np.repeat(np.array(PARTS, object)[FP], 4)
head = lambda n: bl_to_src(np.array(B[n]['head'])[None])[0]; tail = lambda n: bl_to_src(np.array(B[n]['tail'])[None])[0]
bdir = lambda n: (tail(n) - head(n)) / np.linalg.norm(tail(n) - head(n))
E = np.concatenate([Q[:, [0, 1]], Q[:, [1, 2]], Q[:, [2, 3]], Q[:, [3, 0]]]); E = np.unique(np.sort(E, 1), axis=0)
LOG = dict(tag=TAG, K=K, method=__doc__ if __doc__ else 'see header', regions={})
def ss(x): x = np.clip(x, 0, 1); return x * x * (3 - 2 * x)
def chain_ok(s):
    arm = ['clavicle_' + s, 'scapula_' + s, 'upperarm_' + s, 'forearm_' + s, 'hand_' + s, 'thoracic_01', 'thoracic_02', 'thoracic_03', 'spine_03']
    hand = ['forearm_' + s, 'hand_' + s] + [n for n in names if n.endswith('_' + s) and n.startswith(('index', 'middle', 'ring', 'pinky', 'thumb'))]
    leg = ['pelvis', 'spine_01', 'spine_02', 'thigh_' + s, 'shin_' + s, 'foot_' + s]
    return {'arm_' + s: arm, 'hand_' + s: hand, 'leg_' + s: leg,
            **{'%s_%s' % (d, s): hand for d in ('thumb', 'index', 'middle', 'ring', 'pinky')}}
EDIT = np.zeros(len(V), bool)
for s, sg in (('l', 1), ('r', -1)):
    # ---------------- 1. leakage removal (limb parts only; axial vertices keep their heat weights)
    for part, ok in chain_ok(s).items():
        vi = np.nonzero(vpart == part)[0]
        if not len(vi): continue
        bad = [col[n] for n in names if n not in ok]
        before = W[vi][:, bad].sum(1); W[np.ix_(vi, bad)] = 0; ch = vi[before > 1e-6]
        if len(ch): LOG['regions'].setdefault('leakage_' + part, dict(vertices=ch.tolist()[:0], count=int(len(ch)), max_removed=float(before.max())))
        EDIT[ch] = True
    # ---------------- 2. smooth transitions: (name, centre, parent set, child bone, axis, own parts, radius cm, region cm)
    J = [('shoulder', Jc('glenohumeral_' + s), ['clavicle_' + s, 'scapula_' + s], 'upperarm_' + s, bdir('upperarm_' + s), ('arm_' + s,), 4.8, 9.0),
         ('elbow', Jc('elbow_' + s), ['upperarm_' + s], 'forearm_' + s, (bdir('upperarm_' + s) + bdir('forearm_' + s)) / 2, ('arm_' + s,), 4.0, 8.0),
         ('wrist', Jc('wrist_' + s), ['forearm_' + s], 'hand_' + s, bdir('forearm_' + s), ('arm_' + s, 'hand_' + s), 3.0, 6.0),
         ('hip', Jc('hip_' + s), ['pelvis', 'spine_01'], 'thigh_' + s, bdir('thigh_' + s), ('leg_' + s,), 8.0, 14.0),
         ('knee', Jc('knee_' + s), ['thigh_' + s], 'shin_' + s, (bdir('thigh_' + s) + bdir('shin_' + s)) / 2, ('leg_' + s,), 6.0, 10.0),
         ('thumb_cmc', Jc('thumb_cmc_' + s), ['hand_' + s], 'thumb_mc_' + s, bdir('thumb_mc_' + s), ('thumb_' + s, 'hand_' + s), 1.7, 3.0),
         ('thumb_mcp', Jc('thumb_mcp_' + s), ['thumb_mc_' + s], 'thumb_p1_' + s, bdir('thumb_p1_' + s), ('thumb_' + s,), 1.5, 2.5),
         ('thumb_ip', Jc('thumb_ip_' + s), ['thumb_p1_' + s], 'thumb_p2_' + s, bdir('thumb_p2_' + s), ('thumb_' + s,), 1.3, 2.2)]
    for f in ('index', 'middle', 'ring', 'pinky'):
        J += [('%s_mcp' % f, Jc('%s_mcp_%s' % (f, s)), ['hand_' + s], '%s_p1_%s' % (f, s), bdir('%s_p1_%s' % (f, s)), ('%s_%s' % (f, s), 'hand_' + s), 1.3, 2.2),
              ('%s_pip' % f, Jc('%s_pip_%s' % (f, s)), ['%s_p1_%s' % (f, s)], '%s_p2_%s' % (f, s), bdir('%s_p2_%s' % (f, s)), ('%s_%s' % (f, s),), 1.2, 2.0),
              ('%s_dip' % f, Jc('%s_dip_%s' % (f, s)), ['%s_p2_%s' % (f, s)], '%s_p3_%s' % (f, s), bdir('%s_p3_%s' % (f, s)), ('%s_%s' % (f, s),), 1.1, 1.8)]
    for nm, c, Pset, Cb, ax, parts, r, R_ in J:
        ax = ax / np.linalg.norm(ax); pc = [col[n] for n in Pset]; cc = col[Cb]
        vi = np.nonzero(np.isin(vpart, parts) & (np.linalg.norm(V - c, axis=1) <= R_))[0]
        share = W[vi][:, pc].sum(1) + W[vi, cc]; dom = share >= 0.5 * W[vi].sum(1)       # vertices governed by this joint pair
        vi = vi[dom]; share = share[dom]
        if not len(vi): continue
        t = ((V[vi] - c) @ ax) / (K * r); wc = ss(0.5 + 0.5 * t)
        Pw = W[vi][:, pc]; Ps = Pw.sum(1, keepdims=True); Pd = np.where(Ps > 1e-9, Pw / np.maximum(Ps, 1e-12), 0); Pd[Ps[:, 0] <= 1e-9, 0] = 1.0
        W[np.ix_(vi, pc)] = Pd * (share * (1 - wc))[:, None]; W[vi, cc] = share * wc
        EDIT[vi] = True; LOG['regions']['%s_%s' % (nm, s)] = dict(count=int(len(vi)), half_width_cm=K * r, radius_cm=R_)
# ---------------- 3. Laplacian smoothing inside edited regions (3 passes, lambda 0.5), only among edited vertices
nb = [[] for _ in range(len(V))]
for a, b in E:
    if EDIT[a] and EDIT[b]: nb[a].append(b); nb[b].append(a)
ed = np.nonzero(EDIT)[0]
for _ in range(3):
    Wn = W.copy()
    for v in ed:
        if nb[v]: Wn[v] = 0.5 * W[v] + 0.5 * W[nb[v]].mean(0)
    W = Wn
# ---------------- 4. nail binding (selection identical to diag_run.py's nail-rigidity set, both hands)
FIT5 = json.load(open('/tmp/claude-0/rt/rpr/fit_v005.json')); nails = {}
for s in 'lr':
    for f in ('index', 'middle', 'ring', 'pinky', 'thumb'):
        jd = '%s_dip_%s' % (f, s) if f != 'thumb' else 'thumb_ip_' + s; d, tp = Jc(jd), Jc('%s_tip_%s' % (f, s)); dor = np.array(FIT5['cx_' + jd]['dorsal'])
        u = (tp - d) / np.linalg.norm(tp - d); q = V - d; al = q @ u; rad = q - np.outer(al, u); rn = np.linalg.norm(rad, axis=1)
        cand = (al > 0.35 * np.linalg.norm(tp - d)) & (al < np.linalg.norm(tp - d) + 0.5) & (rn < 1.6); rmed = np.median(rn[cand]) if cand.any() else 1.0
        ix = np.nonzero(cand & ((rad @ dor) > 0.6 * rmed))[0]; b3 = col['%s_p3_%s' % (f, s)] if f != 'thumb' else col['thumb_p2_' + s]
        W[ix] = 0; W[ix, b3] = 1.0; EDIT[ix] = True; nails['%s_%s' % (f, s)] = dict(count=int(len(ix)), bone=names[b3])
LOG['nail_binding'] = dict(selection='distal-phalanx dorsal cap: 0.35 L3 .. L3+0.5 cm along the DIP->tip axis, radial < 1.6 cm, dorsal offset > 0.6 x median radius', bound=nails)
# ---------------- normalise, log
ed = np.nonzero(EDIT)[0]; We = W[ed]; We[We < 1e-6] = 0; te = We.sum(1); We[te > 0] /= te[te > 0, None]; W[ed] = We   # normalise edited vertices only
W[~EDIT] = W0[~EDIT]                                                                                                       # everything else bit-identical to the baseline
dW = np.abs(W - W0).max(1); chg = np.nonzero(dW > 1e-6)[0]
Wf = W.astype(np.float32); sha = hashlib.sha256(np.ascontiguousarray(Wf).tobytes()).hexdigest()
LOG.update(changed_vertices=int(len(chg)), max_abs_change=float(dW.max()), zero_weight_vertices=int((W.sum(1) <= 0).sum()), weights_sha256=sha,
           baseline_sha256=hashlib.sha256(np.ascontiguousarray(W0.astype(np.float32)).tobytes()).hexdigest())
np.savez_compressed(os.path.join(O, 'weights_%s.npz' % TAG), W=Wf, names=np.array(names)); np.save(os.path.join(O, 'weights_%s_changed_vertex_ids.npy' % TAG), chg.astype(np.int32))
json.dump(LOG, open(os.path.join(O, 'weights_%s_log.json' % TAG), 'w'), indent=1)
print(TAG, 'changed', len(chg), 'max dW %.3f' % dW.max(), 'sha', sha[:12])
