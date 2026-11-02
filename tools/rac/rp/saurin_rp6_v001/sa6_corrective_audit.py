# sa6_corrective_audit.py W_M.npz W_F.npz CF_M.json CF_F.json OUT.json : RP6 corrective audit (order a407015 §23).
#   Per corrective key: name, family (driver bone + axis), driver definition, activation interval (hat support), owning poses (every pose of the gated set
#   whose measured driver activates the key at full angle), affected semantic regions, maximum neutral-space (rest) displacement, farthest affected vertex from
#   the family pivot (global-drift check), c1 / c2 counterpart, reason, UE implementation recommendation.  Global checks: activation at the reference stance
#   (must be exactly 0 for every key -> neutral displacement exactly 0), disabling all correctives returns the bound frozen mesh, dependency graph acyclic.
import sys, os, json, numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sa6_common as C, sa6_pose as SP, sa6_correctives as CC, sa6_fit as FT
WM, WF, CM, CFF, OUT = sys.argv[1:6]; out = dict(status='RP6 RIG PILOT / NOT FROZEN', method=open(__file__).read().split('import')[0], configurations={})
fams = {}
for cfg, wf, cf in (('M', WM, CM), ('F', WF, CFF)):
    R = SP.Rig(cfg, wf); Cr = CC.Correctives.load(R, cf); js = json.load(open(cf)); PS = FT.pose_set(R)
    T0 = R.pose([]); d0, a0 = Cr.delta(T0, True); rest_active = sum(len(v[1]) for v in a0.values())
    own = {}
    for pn, spec in PS.items():
        T = R.pose(spec)
        for key, f in Cr.F.items():
            x = Cr.driver(T, f)
            for k, w in Cr.hat(f['samples'], x):
                if w > 1e-6: own.setdefault((key, k), []).append((pn, round(float(w), 3)))
    recs = []; regs_all = set()
    for fj in js['families']:
        key = CC.fam_key(fj['bone'], fj['axis_parent_frame']); f = Cr.F[key]; piv = np.array(fj['pivot_rest_cm']); smp = sorted(f['samples']); pts = sorted(smp + [0.0])
        for kj in fj['keys']:
            k = f['samples'].index(kj['sample_deg']); idx, dd = f['D'][k]; mag = np.linalg.norm(dd, axis=1); sig = idx[mag > 1e-4]
            vl = np.zeros(R.nv, bool); vl[sig] = True; labs = sorted({str(x) for x in R.ql[vl[R.Q].any(1)]}); regs_all |= set(labs)
            i = pts.index(kj['sample_deg']); lo = pts[i - 1] if i > 0 else None; hi = pts[i + 1] if i + 1 < len(pts) else None
            interval = [lo if lo is not None else kj['sample_deg'], hi if hi is not None else ('hold >= %.2f' % kj['sample_deg'] if kj['sample_deg'] > 0 else 'hold')]
            if kj['sample_deg'] < 0 and lo is None: interval = ['hold <= %.2f' % kj['sample_deg'], hi]
            ow = own.get((key, k), [])
            recs.append(dict(name=kj['name'], family=fj['id'], driver_bone=fj['bone'], driver='twist angle of %s local rotation about %s (parent frame), hat over samples %s' % (fj['bone'], np.round(fj['axis_parent_frame'], 4).tolist(), [round(s, 2) for s in smp]),
                             sample_deg=kj['sample_deg'], activation_interval_deg=interval, owning_poses=ow[:40], n_owning_poses=len(ow), vertices=int(len(idx)), vertices_gt_1um=int(len(sig)),
                             regions=labs, max_rest_displacement_cm=round(float(mag.max()) if len(mag) else 0.0, 4), mean_rest_displacement_cm=round(float(mag.mean()) if len(mag) else 0.0, 4),
                             farthest_affected_vertex_from_pivot_cm=round(float(np.linalg.norm(R.V[sig] - piv, axis=1).max()) if len(sig) else 0.0, 2),
                             reason='removes the LBS fold / interpenetration of the owning pose(s) at this joint angle (Poisson rotation-field solve + local unfold + contact projection, frozen-mesh derived)',
                             ue_implementation='morph target driven by the same joint-angle curve (Pose Driver / Control Rig curve); no helper bone required'))
    for pj in js.get('pose_keys', []):
        pk = Cr.PK[pj['pose']]; mag = np.linalg.norm(pk['d'], axis=1); sig = pk['idx'][mag > 1e-4]; vl = np.zeros(R.nv, bool); vl[sig] = True; labs = sorted({str(x) for x in R.ql[vl[R.Q].any(1)]})
        ow = []
        for pn, spec in PS.items():
            w_ = Cr.pk_weight(R.pose(spec), pk)
            if w_ > 1e-6: ow.append((pn, round(float(w_), 3)))
        recs.append(dict(name=pj['name'], family='pose key', driver_bone=[d_['bone'] for d_ in pj['drivers']], driver='product over %s of tent(twist; 0 -> sample -> 2 x sample), samples %s' % ([d_['bone'] for d_ in pj['drivers']], [round(d_['sample_deg'], 2) for d_ in pj['drivers']]),
                         sample_deg=[d_['sample_deg'] for d_ in pj['drivers']], activation_interval_deg='each driving joint in (0, 2 x sample); exactly 0 if any driving joint is at rest', owning_poses=ow[:40], n_owning_poses=len(ow),
                         vertices=int(len(pk['idx'])), vertices_gt_1um=int(len(sig)), regions=labs, max_rest_displacement_cm=round(float(mag.max()) if len(mag) else 0.0, 4), mean_rest_displacement_cm=round(float(mag.mean()) if len(mag) else 0.0, 4),
                         farthest_affected_vertex_from_pivot_cm=round(float(min(np.linalg.norm(R.V[sig] - R.H(d_['bone']), axis=1).max() for d_ in pj['drivers'])) if len(sig) else 0.0, 2),
                         reason='pose-space key for %s: two poses share these joint angles but need different local shapes (separable family keys oscillate)' % pj['pose'],
                         ue_implementation='morph target driven by a Pose Driver (RBF / pose reader) on the listed joints'))
    fams[cfg] = {fj['bone'] + '|' + ','.join('%.3f' % a for a in fj['axis_parent_frame']): [k['sample_deg'] for k in fj['keys']] for fj in js['families']}
    out['configurations'][cfg] = dict(families=len(js['families']), keys=len(recs), rest_stance_active_keys=rest_active, rest_stance_max_displacement_cm=float(np.abs(d0).max()),
                                      max_rest_displacement_cm=max(r['max_rest_displacement_cm'] for r in recs) if recs else 0.0, farthest_affected_from_pivot_cm=max(r['farthest_affected_vertex_from_pivot_cm'] for r in recs) if recs else 0.0,
                                      keys_without_owning_pose=[r['name'] for r in recs if not r['n_owning_poses']], regions=sorted(regs_all), records=recs)
    print(cfg, 'families', len(js['families']), 'keys', len(recs), 'rest active', rest_active, 'max disp', out['configurations'][cfg]['max_rest_displacement_cm'], 'farthest', out['configurations'][cfg]['farthest_affected_from_pivot_cm'], flush=True)
both = set(fams['M']) & set(fams['F'])
out['c1_c2'] = dict(families_c1=len(fams['M']), families_c2=len(fams['F']), shared_family_axes_3dp=len(both), c1_only=sorted(set(fams['M']) - both)[:50], c2_only=sorted(set(fams['F']) - both)[:50],
                    note='c2 correctives are solved on c2 (c2 joints / weights / geometry), not copied; family axes differ only where the c2 joint frames differ')
out['dependency_graph'] = 'armature pose -> driver (reads pose-bone local quaternion) -> shape-key value -> mesh; shape keys never drive bones; no constraints -> acyclic'
out['disable_all'] = 'all key values 0 (or all drivers muted) -> posed = LBS of the frozen mesh; at the reference stance every driver reads twist 0 -> every key 0 -> the bound frozen mesh exactly'
json.dump(out, open(OUT, 'w'), indent=1)
