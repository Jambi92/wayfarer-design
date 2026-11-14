# sa6_node_fade.py NODE POSE FRAC BODYDIR LAYERDIR NODEDIR : local fade fallback for a node fit (layer v003, corrective-layer validation order 3e76b509).
#   When the standard solver leaves a single persistent fold on a node body (FAHI@0.50, hip_flex70_xpos 100 %: one pelvis quad inside the composition zone
#   that plain LBS keeps unfolded but the blended corrective folds), the production corrective is faded out locally: d' = (1 - f) d with f = 1 on the
#   folded quad's vertices and a linear falloff over k quad rings (k = 1, 2, 3, 4, 6; base-config rigid set untouched); the first k whose result has no
#   rig fold, no new penetration, no new tear and |dV| <= 60 cm3 is kept.  The change (d' - d) is written into the node's creator key K (scaled 1 / w) as a
#   sample of the driving family at the pose's driver angle (the standard key assignment); the node is then re-verified by sa6_node_fit.py on the whole
#   suite (every pose at 100 / 75 / 50 / 25 %) from round 0, so any side effect at other angles is caught and solved.
import sys, os, json, numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sa6_correctives as CC, sa6_fit as FT, sa6_pd2_fit as PF, sa6_layer_harness as H, sa6_blend as BL, sa6_node_fit as NF
node, pose, fr, BD, LD, ND = sys.argv[1], sys.argv[2], float(sys.argv[3]), sys.argv[4], sys.argv[5], sys.argv[6]; st, ws = node.rsplit('@', 1); w = float(ws)
bm = json.load(open(os.path.join(BD, 'bodies.json')))['bodies']; bn = [k for k in ('c1-' + node, 'c2-' + node) if k in bm][0]; b = bm[bn]
R, z = BL.rig_of(bn, b, BD); R.rest_inverted = z['rest_inverted']; PF.mask_composition(R, z['comp'])
B = H.load_base(R, b['cfg']); S = CC.Correctives.load(R, os.path.join(LD, 'CF_state_%s.json' % st)); src = os.path.join(ND, 'CK_%s.json' % node); K = CC.Correctives.load(R, src)
P = NF.NodeProxy(B, S, K, w); Sv = CC.Solver(R); Sv.V0 = Sv.body_volume(R.V); F = np.r_[R.Q[:, [0, 1, 2]], R.Q[:, [0, 2, 3]]].astype(np.int64); w0 = FT.wn_out(R.V, F)
spec = [(bb, p, a, dg * fr) for bb, p, a, dg in R.suite('anat')[pose]]; PF.start_pose(R, P, spec, F, w0, Sv); T = R.pose(spec); d = P.delta(T)
def score(dl):
    Pc = R.skin(T, R.V + dl); return int((R.relcos(Pc, T) < 0).sum()), int(FT.penetration(R, Pc, F, w0).sum()), int(Sv.tear_edges(Pc)[0].sum()), float(Sv.body_volume(Pc) - Sv.V0)
s0 = score(d); print('before', s0, flush=True)
fl = np.nonzero(R.relcos(R.skin(T, R.V + d), T) < 0)[0]; seed = np.zeros(R.nv, bool); seed[R.Q[fl].ravel()] = True; rig = BL.rigid_ids(b['cfg']) | Sv.protect; best = None
for k in (1, 2, 3, 4, 6):
    rings = [seed]
    for _ in range(k): rings.append(Sv.dilate(rings[-1], 1))
    f = np.zeros(R.nv)
    for j, m in enumerate(rings): f[m & (f == 0)] = 1.0 - j / (k + 1.0)
    f[rig] = 0.0; dn = d * (1 - f[:, None]); s = score(dn); print('ring', k, s, flush=True)
    if s[0] == 0 and s[1] <= s0[1] and s[2] <= s0[2] and abs(s[3]) <= FT.VOL_ACCEPT: best = (k, dn); break
assert best, 'no local fade clears the fold'
k, dn = best; I = np.nonzero(np.abs(dn - d).sum(1) > 1e-9)[0]; ent = FT.entries(R, spec, T); bone, pv, ax = ent[0]
key, axf = P.resolve(bone, ax); x = P.driver(T, dict(bone=bone, axis=axf)); P.add(key, bone, axf, pv, x, I, (dn - d)[I]); print('after', score(P.delta(T)), 'ring', k, 'verts', len(I), 'family', key, 'x %.2f' % x)
K.save(os.path.join(ND, 'ckpt', 'CK_%s.json' % node), dict(node=node, fit_log=[dict(fade=dict(pose=pose, frac=fr, ring=k, n_vertices=int(len(I)), driver_deg=x))], ck_round=0, ck_next=0, ck_tot=0))
os.makedirs(os.path.join(ND, 'prefade'), exist_ok=True); os.rename(src, os.path.join(ND, 'prefade', os.path.basename(src))); os.rename(src.replace('.json', '.npz'), os.path.join(ND, 'prefade', os.path.basename(src).replace('.json', '.npz')))
print('wrote checkpoint; re-verify with sa6_node_fit.py', node)
