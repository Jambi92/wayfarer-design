# sa6_bake.py fit NAME BODYDIR OUTDIR | eval NAME BODYDIR OUTDIR : per-body corrective bake (per-body bake feasibility order a13cae71).
#   fit : the exact creator body NAME (sa6_blend body: dense convex body blend, frozen embedding, RP6 joints recomputed on the body, base-configuration weights)
#         starts from the PACKAGED blend (RP6_LAYERS, default SA_RP6_creator_layers_v004.json):  production_0(T) = (1 - sum w) B(T) + sum w_i S_i(T, w_i).
#         The existing RP6 local solver (sa6_fit.solve_one, sa6_pd2_fit composition mask / locality rules, sa6_node_fit guard + fade fallback) then adds a bounded
#         pose-driven set K on that exact body until all 34 anatomical poses at 100 / 75 / 50 / 25 % are clean (4 rounds, pose keys from round 1, resumable):
#             baked(T) = production_0(T) + K(T)
#         K is a standard corrective set (families keyed by bone + parent-frame axis, hat-interpolated samples, pose keys = products of driver tents), so it is
#         exactly 0 at neutral; base / layers / weights / rest geometry are not changed.  Artifact OUTDIR/BK_<NAME>.json/.npz records the body (weights,
#         base configuration, body + package hashes), the package it was initialised from, timings and peak memory.
#   eval: reopens the artifact FROM DISK and runs sa6_blend.evaluate with the 'bake' column (columns lbs | base | packaged blend | bake; gates on bake,
#         closure ownership rules unchanged) -> OUTDIR/EV_<NAME>.json.
import sys, os, json, time, copy, hashlib, platform, numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('RP6_LAYERS', 'SA_RP6_creator_layers_v004.json')
import sa6_common as C, sa6_correctives as CC, sa6_fit as FT, sa6_pd2_fit as PF, sa6_layer_harness as H, sa6_blend as BL, sa6_node_fit as NF
ROUNDS = int(os.environ.get('ROUNDS', 8));   # early exit on the first clean round; 8 allows Gauss-Seidel trades between fractions to settle
FRACS = tuple(float(x) for x in os.environ.get('BAKE_FRACS', '1.0,0.75,0.5,0.25').split(','))   # bake angle fractions (uniform spacing)
STEP = min(abs(a - b) for a in FRACS + (0.0,) for b in FRACS + (0.0,) if a != b); GAPS = {}
def peak_mb():
    """peak resident memory of this process (MB): getrusage on Linux, PeakWorkingSetSize on Windows"""
    try:
        import resource; return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024.0
    except ImportError:
        import ctypes, ctypes.wintypes as wt
        class PMC(ctypes.Structure): _fields_ = [('cb', wt.DWORD), ('PageFaultCount', wt.DWORD)] + [(n, ctypes.c_size_t) for n in ('PeakWorkingSetSize', 'WorkingSetSize', 'QuotaPeakPagedPoolUsage', 'QuotaPagedPoolUsage', 'QuotaPeakNonPagedPoolUsage', 'QuotaNonPagedPoolUsage', 'PagefileUsage', 'PeakPagefileUsage')]
        k = ctypes.windll.kernel32; k.GetCurrentProcess.restype = wt.HANDLE; f = ctypes.windll.psapi.GetProcessMemoryInfo; f.argtypes = [wt.HANDLE, ctypes.POINTER(PMC), wt.DWORD]
        c = PMC(); c.cb = ctypes.sizeof(PMC); f(k.GetCurrentProcess(), ctypes.byref(c), c.cb); return c.PeakWorkingSetSize / 2 ** 20
class BakeProxy:
    """what the solver sees on the exact body: packaged blend + K; increments go to K unscaled.  (w / B / S / E attributes = the interface the
    sa6_node_fit fade fallback uses: its 'start from the blend' candidate is the packaged blend itself)"""
    def __init__(self, P0, K): self.P0, self.K = P0, K; self.r = K.r; self.F = K.F; self.PK = K.PK; self.w = 1.0; self.B = P0; self.S = P0; self.E = None
    def delta(self, T): return self.P0.delta(T) + self.K.delta(T)
    def driver(self, T, f): return self.K.driver(T, f)
    def resolve(self, bone, axis, tol_deg=30.0): return self.K.resolve(bone, axis, tol_deg)
    def add(self, key, bone, axis, pivot, x, idx, dd): self.K.add(key, bone, axis, pivot, x, idx, dd)
    def add_pose_key(self, name, drivers, idx, dd):
        """bake pose keys are per angle fraction ('pose@0.75'): their tents span exactly to the neighbouring fraction samples (width = 0.25 of the pose's full
        angle per driver), so the keys of one pose at 25 / 50 / 75 / 100 % interpolate like hat samples instead of overlapping (an overlapping 0 -> s -> 2s tent
        made the 75 % and 100 % fixes of hip_flex70 undo each other round after round)"""
        new = name not in self.K.PK; self.K.add_pose_key(name, drivers, idx, dd)
        if new and os.environ.get('BAKE_PK_TENT', 'fraction') == 'fraction' and '@' in name:
            pn_, fr = name.rsplit('@', 1); fr = float(fr); gap = GAPS.get((pn_, round(fr, 4)), STEP)
            self.K.PK[name]['width'] = [abs(s_) * gap / fr for _, _, s_ in self.K.PK[name]['drivers']]
def body_sha(BD, nm): return hashlib.sha256(np.ascontiguousarray(np.load(os.path.join(BD, nm + '.npz'))['Vs']).tobytes()).hexdigest()
if __name__ == '__main__':
    mode, nm, BD, OD = sys.argv[1:5]; os.makedirs(OD + '/ckpt', exist_ok=True); b = json.load(open(os.path.join(BD, 'bodies.json')))['bodies'][nm]
    art = os.path.join(OD, 'BK_%s.json' % nm)
    if mode == 'eval':
        t0 = time.time(); r = BL.evaluate(nm, b, BD, bake=art); r['seconds_eval'] = round(time.time() - t0, 1); r['peak_mb_eval'] = round(peak_mb(), 1)
        json.dump(r, open(os.path.join(OD, 'EV_%s.json' % nm), 'w'), indent=1); t = r['totals']
        print('%-26s clean %s | bake rig flips %d pen %d tears %d volfail %d rigid %.4f | blend rig %d | comp %d | neutral %s | %.0fs %.0f MB' % (
            nm, r['clean'], t['rig_flips'], t['rig_pen'], t['rig_tears'], t['vol_fail'], t['rigid_max_cm'], t['blend_rig'], t['comp'], r['neutral_max_displacement_cm'],
            r['seconds_eval'], r['peak_mb_eval']), flush=True)
        sys.exit(0)
    if os.path.exists(art) and os.environ.get('RETRY') == '1':      # retry of an unconverged bake: continue from the artifact for ROUNDS more rounds
        j = json.load(open(art))
        if not j.get('converged', True):
            os.makedirs(OD + '/retried', exist_ok=True); import shutil
            for ext in ('.json', '.npz'): shutil.copy(art.replace('.json', ext), os.path.join(OD, 'ckpt', 'BK_%s%s' % (nm, ext))); shutil.move(art.replace('.json', ext), os.path.join(OD, 'retried', 'BK_%s%s' % (nm, ext)))
            c = json.load(open(os.path.join(OD, 'ckpt', 'BK_%s.json' % nm))); c.update(ck_round=0, ck_next=0, ck_tot=0, ck_fit_seconds=j['timing']['fit_s']); json.dump(c, open(os.path.join(OD, 'ckpt', 'BK_%s.json' % nm), 'w'))
            print(nm, 'RETRY from unconverged artifact', flush=True)
    t0 = time.time(); R, z = BL.rig_of(nm, b, BD); R.rest_inverted = z['rest_inverted']; PF.mask_composition(R, z['comp'])
    Bc = H.load_base(R, b['cfg']); P0 = H.Blend(Bc, [(w, H.load_state(R, s)[0]) for s, w in b['w'].items()]); ck = OD + '/ckpt/BK_%s.json' % nm
    ini = os.environ.get('BAKE_INIT', '')      # adaptive pass: start from an earlier artifact of this body (its keys kept, refined)
    K = CC.Correctives.load(R, ck) if os.path.exists(ck) else (CC.Correctives.load(R, ini) if ini else CC.Correctives(R)); P = BakeProxy(P0, K); t_setup = time.time() - t0
    Sv = CC.Solver(R); Sv.V0 = Sv.body_volume(R.V); Sv.protect = Sv.protect | BL.rigid_ids(b['cfg'])
    F = np.r_[R.Q[:, [0, 1, 2]], R.Q[:, [0, 2, 3]]].astype(np.int64); w0 = FT.wn_out(R.V, F); PS = R.suite('anat')
    order = sorted(PS, key=lambda k: (len(PS[k]), max(abs(e[3]) for e in PS[k]))); log, r0, i0, tot0, el0 = [], 0, 0, 0, 0.0
    if os.path.exists(ck):
        m = json.load(open(ck)); log, r0, i0, tot0, el0 = m['fit_log'], m['ck_round'], m['ck_next'], m['ck_tot'], m.get('ck_fit_seconds', 0.0); print(nm, 'resume round', r0, 'item', i0, flush=True)
    EXTRA = json.load(open(os.environ['BAKE_EXTRA'])) if os.environ.get('BAKE_EXTRA') else {}   # adaptive samples {pose: [fractions]} (from a sweep)
    if any(k.startswith('gate:') for k in EXTRA):      # special-gate poses (sa6_gates, 'gate:<name>') that failed on this body join the fit set at all fractions
        import sa6_gates as GT; GP = GT.gate_poses(R)
        for k in EXTRA:
            if k.startswith('gate:'): PS[k] = GP[k[5:]]
        order = sorted(PS, key=lambda k: (len(PS[k]), max(abs(e[3]) for e in PS[k])))
    items = [(pn, fr) for pn in order for fr in sorted(set(FRACS) | set(EXTRA.get(pn, [])), reverse=True)]
    for pn in order:
        fs = sorted(set(FRACS) | set(EXTRA.get(pn, [])) | {0.0})
        for i, f in enumerate(fs[1:], 1): GAPS[(pn, round(f, 4))] = min(f - fs[i - 1], (fs[i + 1] - f) if i + 1 < len(fs) else f - fs[i - 1])
    tot = 0; t1 = time.time(); n_entering = {}
    for rnd in range(r0, ROUNDS):
        tot = tot0 if rnd == r0 else 0
        for ii, (pn, fr) in enumerate(items):
            if rnd == r0 and ii < i0: continue
            spec = [(bb, p, a, dg * fr) for bb, p, a, dg in PS[pn]]; t = time.time(); PF.start_pose(R, P, spec, F, w0, Sv)
            n0 = NF.defects(R, P, Sv, spec, F, w0); snap = copy.deepcopy((K.F, K.PK)) if n0 else None
            a, c, _ = FT.solve_one(R, P, Sv, spec, F, w0, log, pose_key=('%s@%.4f' % (pn, fr)) if rnd >= 1 else None); tot += a
            if n0:
                n1 = NF.defects(R, P, Sv, spec, F, w0)
                if n1 > n0: K.F.clear(); K.F.update(snap[0]); K.PK.clear(); K.PK.update(snap[1]); log.append(dict(round=rnd, pose=pn, frac=fr, reverted=[n0, n1])); n1 = n0
                if n1:
                    k_ = NF.fade(R, P, Sv, spec, F, w0, Sv.protect); c = NF.defects(R, P, Sv, spec, F, w0) if k_ else n1
                    log.append(dict(round=rnd, pose=pn, frac=fr, fade_ring=k_, after=c)) if k_ else None
            if a or c: print('%s round %d %-24s x%.2f before %4d after %4d  %.1fs' % (nm, rnd, pn, fr, a, c, time.time() - t), flush=True)
            log.append(dict(round=rnd, pose=pn, frac=fr, flips_before=a, flips_after_solve=c))
            if a or c or ii % 16 == 15: K.save(ck, dict(name=nm, fit_log=log, ck_round=rnd, ck_next=ii + 1, ck_tot=tot, ck_fit_seconds=el0 + time.time() - t1))
        n_entering[rnd] = tot; print(nm, 'round', rnd, 'total entering', tot, flush=True)
        if tot == 0: break
    t_fit = el0 + time.time() - t1; t2 = time.time()
    pk = os.path.join(H.PKG, H.LAYERS)
    K.save(art, dict(status='RP6 RIG PILOT / NOT FROZEN', name='SA_RP6_bake_%s' % nm, body=nm, recipe=dict(base_config=b['cfg'], weights=b['w'], kind=b.get('kind'),
                     geometry='sa6_blend dense convex body blend (bodies.json method), frozen barycentric cage embedding, RP6 joints recomputed on the body, base-config weights'),
                     body_vs_sha256=body_sha(BD, nm), body_json_sha256=b.get('sha256'), initialised_from=dict(layers=H.LAYERS, layers_sha256=C.sha(pk),
                     base='SA_RP6_correctives_v002.json', base_arrays_sha256={c: C.sha(os.path.join(H.PKG, 'SA_RP6_correctives_%s_v001.npz' % c)) for c in 'MF'}),
                     semantics='baked(T) = packaged blend(T) + K(T); K = pose-driven corrective set on this exact body (0 at neutral)',
                     converged=bool(tot == 0), bake_fracs=list(FRACS), adaptive_samples=EXTRA, initialised_from_artifact=ini or None, rounds_entering=n_entering, fit_log=log,
                     timing=dict(setup_s=round(t_setup, 1), fit_s=round(t_fit, 1), peak_mb=round(peak_mb(), 1), host=platform.node(), cpu=platform.processor(), os=platform.platform(), cpus_used=1,
                                 threads=os.environ.get('OMP_NUM_THREADS'))))
    t_write = time.time() - t2
    j = json.load(open(art)); j['timing']['write_s'] = round(t_write, 2); json.dump(j, open(art, 'w'), indent=1)
    print(nm, 'BAKED converged', tot == 0, 'families', len(K.F), 'pose keys', len(K.PK), 'fit %.0fs peak %.0f MB' % (t_fit, peak_mb()), flush=True)
