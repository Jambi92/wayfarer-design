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
os.environ.setdefault('RP6_LAYERS', 'SA_RP6_creator_layers_v005.json' if os.environ.get('RP6_RIG') == 'v002' else 'SA_RP6_creator_layers_v004.json')   # rig v002: layers v005
os.environ['PK_HAT_EXACT'] = '0'      # bake keys keep the bake's own tents (floor / neighbour gaps); the exact-hat regroup is for the layer fits only
import sa6_common as C, sa6_correctives as CC, sa6_fit as FT, sa6_pd2_fit as PF, sa6_layer_harness as H, sa6_blend as BL, sa6_node_fit as NF
ROUNDS = int(os.environ.get('ROUNDS', 8));   # early exit on the first clean round; 8 allows Gauss-Seidel trades between fractions to settle
FRACS = tuple(float(x) for x in os.environ.get('BAKE_FRACS', '1.0,0.75,0.5,0.25').split(','))   # bake angle fractions (uniform spacing)
STEP = min(abs(a - b) for a in FRACS + (0.0,) for b in FRACS + (0.0,) if a != b); GAPS = {}
# BAKE_PK_MINW (fraction of the pose's full angle, default 0 = off): minimum half-width of a fraction pose-key tent.  Adaptive samples from the dense sweep sit
# 0.025 or 0.25 deg apart, so their tents became 0.25-1.75 deg wide and a 0.2-1.8 cm key switched on inside one 30 fps frame (a pop in motion; offline bake
# order 8e3b7b4d, END_FAHI / END_MUFAHI).  With a floor the key ramps over at least MINW x full angle; neighbouring keys may overlap (Gauss-Seidel rounds settle it).
PK_MINW = float(os.environ.get('BAKE_PK_MINW', '0'))
MOT_REFIT = os.environ.get('BAKE_MOTION_REFIT', '0') == '1'      # standard recipe: 1 (order 07a3f24c §3); archived: 0 (keys widened in place)
PK_GRID = {}; MOT_DROPPED = []; CUR = [None]      # CUR[0] = the pose being solved
MOT_MODE = os.environ.get('BAKE_MOTION_REFIT_MODE', 'grid')    # experiment switch: grid (keys + family samples on the floor grid) | gridkeys | nokeys
MOT_SNAP = MOT_MODE == 'grid'
PK_GRID_ALL = os.environ.get('BAKE_PK_GRID_ALL', '0') == '1'   # every pose's fraction keys on the step grid (adaptive samples snap to the nearest grid key)
def pk_name(pn, fr):
    """pose-key name of a fit sample: the sample's own fraction, or (motion refit) the nearest key of the pose's grid"""
    if PK_GRID_ALL and pn not in PK_GRID: fr = min([round(k_ * max(PK_MINW, STEP), 4) for k_ in range(1, int(np.ceil(1.0 / max(PK_MINW, STEP) - 1e-9)) + 1)], key=lambda g: (abs(g - fr), -g))
    if pn in PK_GRID:
        if MOT_MODE == 'nokeys': return None          # the motion-fed pose is refit with families only (no fraction pose keys)
        fr = min(PK_GRID[pn], key=lambda g: (abs(g - fr), -g))
    return '%s@%.4f' % (pn, fr)
PK_FLOOR = {}       # per-pose floor override: poses that failed the motion gate ('motion:<pose>' in BAKE_EXTRA) get twice the floor (standards approval order)
# BAKE_PEN_MARGIN (cm, default 0 = off): the FIT also treats a vertex as in contact when the point MARGIN OUTSIDE its surface lies inside the body (and did not
# at rest) -- a clearance; gates unchanged (PEN_TOL 0.02 cm inside).  Without clearance, adjacent adaptive samples 0.25 deg apart
# (END_MUFAHI trunk_twist_30 0.58333 / 0.59167, offline bake pass 2) ping-pong: each solve clears its own sample exactly and leaves the neighbour 1 vertex in.
PEN_MARGIN = float(os.environ.get('BAKE_PEN_MARGIN', '0'))
LOCAL_MARGIN = float(os.environ.get('BAKE_LOCAL_MARGIN', '0')); NEAR = float(os.environ.get('BAKE_LOCAL_NEAR', '0.02'))   # standard: 0.03 cm, 0.02 of the pose
ONLY = set(x for x in os.environ.get('BAKE_ONLY_POSES', '').split(',') if x)     # experiments: restrict the fit to these poses (never set for a bake)
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
    def add(self, key, bone, axis, pivot, x, idx, dd):
        if MOT_SNAP and CUR[0] in PK_GRID and bone in self.r.bones_of(globals()['PS'][CUR[0]]):      # motion refit: family sample on the pose's grid angle
            sp_ = globals()['PS'][CUR[0]]; xs = [self.K.driver(self.r.pose([(b_, p_, a_, dg * g) for b_, p_, a_, dg in sp_]), dict(bone=bone, axis=axis)) for g in PK_GRID[CUR[0]]]
            x = min(xs, key=lambda v: abs(v - x))
        self.K.add(key, bone, axis, pivot, x, idx, dd)
    def add_pose_key(self, name, drivers, idx, dd):
        """bake pose keys are per angle fraction ('pose@0.75'): their tents span exactly to the neighbouring fraction samples (width = 0.25 of the pose's full
        angle per driver), so the keys of one pose at 25 / 50 / 75 / 100 % interpolate like hat samples instead of overlapping (an overlapping 0 -> s -> 2s tent
        made the 75 % and 100 % fixes of hip_flex70 undo each other round after round)"""
        n0 = len(self.K.PK); name = self.K.add_pose_key(name, drivers, idx, dd) or name; new = len(self.K.PK) > n0      # (merged into an equivalent key: not new)
        if new and os.environ.get('BAKE_PK_TENT', 'fraction') == 'fraction' and '@' in name:
            pn_, fr = name.rsplit('@', 1); fr = float(fr); gap = max(GAPS.get((pn_, round(fr, 4)), STEP), PK_FLOOR.get(pn_, PK_MINW))
            self.K.PK[name]['width'] = [abs(s_) * gap / fr for _, _, s_ in self.K.PK[name]['drivers']]
            sp = globals().get('PS', {}).get(pn_)
            if C.RIGV != 'v001' and sp is not None and len(self.r.expand(sp)) != len(sp):
                # rig v002 coupled pose: the humeral driver is not linear in the fraction, so the tent spans to the driver value at the neighbouring
                # fraction sample (fr - gap) measured on the rig (equal to |s| gap / fr when linear)
                Tg = self.r.pose([(bb, p, a, dg * max(0.0, fr - gap)) for bb, p, a, dg in sp])
                self.K.PK[name]['width'] = [abs(s_ - self.K.driver(Tg, dict(bone=b_, axis=a_))) for b_, a_, s_ in self.K.PK[name]['drivers']]
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
    if os.environ.get('BAKE_GATE_ALIGNED_ALLOW') == '1':
        # Fit allowance aligned to the gate's ownership rule (sa6_blend.evaluate): a composition-zone fold / contact that plain LBS of the pose shows is ignored by
        # the fit ONLY if it also lies within 1.0 cm of a pre-rig defect point (the evaluator's 'near' test); elsewhere it is a rig defect the fit must repair.
        # The default allowance (composition zone & LBS) is wider than the gate, so a contact 1.0-1.5 cm from the pre-rig points could pass the fit and fail
        # the gate (END_MUFAHI trunk_twist_30 vertex 4524 at 1.40 cm, offline bake order 8e3b7b4d).  Gates unchanged; the fit only becomes stricter.
        from scipy.spatial import cKDTree
        _kd = cKDTree(z['pts']) if len(z['pts']) else None
        _nv = (_kd.query(R.V)[0] <= 1.0) if _kd is not None else np.zeros(R.nv, bool); _nq = (_kd.query(R.V[R.Q].mean(1))[0] <= 1.0) if _kd is not None else np.zeros(len(R.Q), bool)
        _sp = PF.start_pose
        def _start_pose(R_, Cs, spec, F_, w0_, S=None):
            _sp(R_, Cs, spec, F_, w0_, S)
            if hasattr(R_, '_allow_v'): R_._allow_v = R_._allow_v & _nv; R_._allow_q = (R_._allow_q & _nq) | R_.rest_inverted
        PF.start_pose = _start_pose
    Bc = H.load_base(R, b['cfg']); P0 = H.Blend(Bc, [(w, H.load_state(R, s)[0]) for s, w in b['w'].items()]); ck = OD + '/ckpt/BK_%s.json' % nm
    ini = os.environ.get('BAKE_INIT', '')      # adaptive pass: start from an earlier artifact of this body (its keys kept, refined)
    K = CC.Correctives.load(R, ck) if os.path.exists(ck) else (CC.Correctives.load(R, ini) if ini else CC.Correctives(R)); P = BakeProxy(P0, K); t_setup = time.time() - t0
    Sv = CC.Solver(R); Sv.V0 = Sv.body_volume(R.V); Sv.protect = Sv.protect | BL.rigid_ids(b['cfg'])
    F = np.r_[R.Q[:, [0, 1, 2]], R.Q[:, [0, 2, 3]]].astype(np.int64); w0 = FT.wn_out(R.V, F); PS = R.suite('anat')
    if PEN_MARGIN:      # clearance: also a contact when the point MARGIN OUTSIDE the vertex lies inside the body (winding > 0.5) where it does not at rest
        import igl
        _raw = getattr(FT, '_pen_raw', FT.penetration)
        def _out(P_, F_): return igl.fast_winding_number(P_, F_, P_ + PEN_MARGIN * igl.per_vertex_normals(P_, F_))
        _w0m = _out(R.V, F)
        def _pen_margin(R_, P_, F_, w0_): return _raw(R_, P_, F_, w0_) | ((_out(P_, F_) > 0.5) & (_w0m < 0.5))
        if hasattr(FT, '_pen_raw'): FT._pen_raw = _pen_margin
        else: FT.penetration = _pen_margin
    CLEAR = set(); CURM = [False]; ENT = {}
    if LOCAL_MARGIN > 0 and not PEN_MARGIN:
        # neighbouring-contact ping-pong (order 07a3f24c §3 regression case: END_MUFAHI pass 2 trunk_twist_30 0.58333 / 0.59167): two samples of a pose a few
        # tenths of a degree apart share the same family sample / key; each solve clears its own contact exactly and leaves the neighbour touching, so the rounds
        # alternate.  Detected at the end of a round (a sample entering while a same-pose sample within NEAR entered this or the previous round), both
        # samples are then solved with a local clearance: contact also counts where the point LOCAL_MARGIN outside the vertex is inside the body (and was not
        # at rest).  Only those samples; gates unchanged.
        import igl
        _raw2 = getattr(FT, '_pen_raw', FT.penetration)
        def _out2(P_, F_): return igl.fast_winding_number(P_, F_, P_ + LOCAL_MARGIN * igl.per_vertex_normals(P_, F_))
        _w0m2 = _out2(R.V, F)
        def _pen_local(R_, P_, F_, w0_):
            p_ = _raw2(R_, P_, F_, w0_)
            return (p_ | ((_out2(P_, F_) > 0.5) & (_w0m2 < 0.5))) if CURM[0] else p_
        if hasattr(FT, '_pen_raw'): FT._pen_raw = _pen_local
        else: FT.penetration = _pen_local
    if ONLY: PS = {k: v for k, v in PS.items() if k in ONLY}
    order = sorted(PS, key=lambda k: (len(PS[k]), max(abs(e[3]) for e in PS[k]))); log, r0, i0, tot0, el0 = [], 0, 0, 0, 0.0
    if os.path.exists(ck):
        m = json.load(open(ck)); log, r0, i0, tot0, el0 = m['fit_log'], m['ck_round'], m['ck_next'], m['ck_tot'], m.get('ck_fit_seconds', 0.0); print(nm, 'resume round', r0, 'item', i0, flush=True)
    EXTRA = json.load(open(os.environ['BAKE_EXTRA'])) if os.environ.get('BAKE_EXTRA') else {}   # adaptive samples {pose: [fractions]} (from a sweep)
    if any(k.startswith('gate:') for k in EXTRA):      # special-gate poses (sa6_gates, 'gate:<name>') that failed on this body join the fit set at all fractions
        import sa6_gates as GT; GP = GT.gate_poses(R)
        for k in EXTRA:
            if k.startswith('gate:'): PS[k] = GP[k[5:]]
        order = sorted(PS, key=lambda k: (len(PS[k]), max(abs(e[3]) for e in PS[k])))
    MOT = {k[7:]: v for k, v in EXTRA.items() if k.startswith('motion:')}
    if MOT:     # motion-gate failure (standard recipe): the failing frame pair's fractions become fit samples of that pose, and its pose keys ramp over at
        #         least twice the floor (half-width min(1, 2 x max(BAKE_PK_MINW, sample step)) of the full angle); keys kept from BAKE_INIT are widened to it.
        for pn_, fs_ in MOT.items():
            if pn_ in PS: EXTRA[pn_] = sorted(set(EXTRA.get(pn_, [])) | {float(x) for x in fs_}); PK_FLOOR[pn_] = min(1.0, 2.0 * max(PK_MINW, STEP))
        for name_, pk_ in K.PK.items():
            pn_, fr_ = name_.rsplit('@', 1) if '@' in name_ else (name_, None)
            if fr_ is not None and pn_ in PK_FLOOR:
                fr_ = float(fr_); ws = pk_.get('width') or [abs(s_) for _, _, s_ in pk_['drivers']]
                pk_['width'] = [max(w_, abs(s_) * PK_FLOOR[pn_] / fr_) for w_, (_, _, s_) in zip(ws, pk_['drivers'])]
        if MOT_REFIT:
            # convergence fix (order 07a3f24c §3): widening the existing keys in place made neighbouring fraction keys overlap (tents of half-width 0.5 at
            # 0.75 / 0.875 / 0.908 / 1.0: at any fraction 2-3 keys are active with weights summing to > 1), so a fix at one fraction moved its neighbours
            # and the rounds ping-ponged (7, 15, 15, 11, 4, 13, 3, 7 entering, never clean).  Instead the motion-fed pose is REFIT from the initialisation
            # layer: its bake pose keys are dropped and rebuilt on a uniform grid of spacing = the doubled floor (keys at w, 2w, ..., 1; hat tents of
            # half-width w = a partition of unity, like family samples).  Every fit sample of the pose (standard fractions, motion frames, sweep / dense
            # extras) is solved at its own fraction and its pose-key correction goes to the nearest grid key (snap, as family samples snap within 4 deg).
            # the restart also drops the bake FAMILIES driven by the pose's joints (their samples sat a few degrees apart from earlier dense refits: a
            # 1.2 cm step between 83 and 86 deg once the wide key was gone); every pose using those joints is refit from the initialisation layer, and
            # while the motion-fed pose is solved its family corrections snap to the same grid angles (sample spacing >= the floor).
            for name_ in [k_ for k_ in K.PK if '@' in k_ and k_.rsplit('@', 1)[0] in PK_FLOOR]: del K.PK[name_]; MOT_DROPPED.append(name_)
            mb_ = set().union(*[R.bones_of(PS[pn_]) for pn_ in PK_FLOOR])
            for k_ in [k_ for k_, f_ in K.F.items() if f_['bone'] in mb_]: del K.F[k_]; MOT_DROPPED.append('family ' + k_)
            MG_ = os.environ.get('BAKE_MOTION_GRID', 'floor')
            if MG_ == 'step':      # grid spacing = the sample step (max(floor, step)) instead of the doubled floor
                for pn_ in PK_FLOOR: PK_FLOOR[pn_] = max(PK_MINW, STEP)
            elif MG_ not in ('floor', ''):      # a number: explicit grid spacing (pass 9b END_FAHI local-motion experiments, mfx/)
                for pn_ in PK_FLOOR: PK_FLOOR[pn_] = float(MG_)
            for it_ in [x_ for x_ in os.environ.get('BAKE_MOTION_GRID_POSE', '').split(',') if x_]:      # per-pose spacing override, pose=spacing (pass 9b END_FAHI
                pn_, w_ = it_.split('=')                                                                     # hip_flex70_xpos=0.33333: the step grid misses the local
                if pn_ in PK_FLOOR: PK_FLOOR[pn_] = float(w_)                                                # motion allowance by 0.044 cm, the doubled floor diverges)
            for pn_, w_ in PK_FLOOR.items(): PK_GRID[pn_] = [round(min(1.0, k_ * w_), 4) for k_ in range(1, int(np.ceil(1.0 / w_ - 1e-9)) + 1)]
            print(nm, 'motion refit: dropped', MOT_DROPPED, 'grid', PK_GRID, flush=True)
        print(nm, 'motion feedback: poses', sorted(PK_FLOOR), 'floor', sorted(set(PK_FLOOR.values())), flush=True)
    if ONLY: order = [k for k in order if k in ONLY]
    items = [(pn, fr) for pn in order for fr in sorted(set(FRACS) | set(EXTRA.get(pn, [])), reverse=True)]
    for pn in order:
        fs = sorted(set(FRACS) | set(EXTRA.get(pn, [])) | {0.0})
        for i, f in enumerate(fs[1:], 1): GAPS[(pn, round(f, 4))] = min(f - fs[i - 1], (fs[i + 1] - f) if i + 1 < len(fs) else f - fs[i - 1])
    tot = 0; t1 = time.time(); n_entering = {}
    for rnd in range(r0, ROUNDS):
        tot = tot0 if rnd == r0 else 0
        for ii, (pn, fr) in enumerate(items):
            if rnd == r0 and ii < i0: continue
            spec = [(bb, p, a, dg * fr) for bb, p, a, dg in PS[pn]]; t = time.time(); CURM[0] = (pn, fr) in CLEAR; PF.start_pose(R, P, spec, F, w0, Sv); CUR[0] = pn
            n0 = NF.defects(R, P, Sv, spec, F, w0); snap = copy.deepcopy((K.F, K.PK)) if n0 else None
            a, c, _ = FT.solve_one(R, P, Sv, spec, F, w0, log, pose_key=pk_name(pn, fr) if rnd >= 1 else None); tot += a
            if n0:
                n1 = NF.defects(R, P, Sv, spec, F, w0)
                if n1 > n0: K.F.clear(); K.F.update(snap[0]); K.PK.clear(); K.PK.update(snap[1]); log.append(dict(round=rnd, pose=pn, frac=fr, reverted=[n0, n1])); n1 = n0
                if n1:
                    k_ = NF.fade(R, P, Sv, spec, F, w0, Sv.protect); c = NF.defects(R, P, Sv, spec, F, w0) if k_ else n1
                    log.append(dict(round=rnd, pose=pn, frac=fr, fade_ring=k_, after=c)) if k_ else None
            if a or c: print('%s round %d %-24s x%.2f before %4d after %4d  %.1fs' % (nm, rnd, pn, fr, a, c, time.time() - t), flush=True)
            log.append(dict(round=rnd, pose=pn, frac=fr, flips_before=a, flips_after_solve=c))
            if a: ENT.setdefault((pn, fr), set()).add(rnd)
            if a or c or ii % 16 == 15: K.save(ck, dict(name=nm, fit_log=log, ck_round=rnd, ck_next=ii + 1, ck_tot=tot, ck_fit_seconds=el0 + time.time() - t1))
        n_entering[rnd] = tot; print(nm, 'round', rnd, 'total entering', tot, flush=True)
        if LOCAL_MARGIN > 0 and not PEN_MARGIN:
            for (pn_, f_), rs_ in list(ENT.items()):
                if rnd not in rs_: continue
                for (pm_, g_), qs_ in ENT.items():
                    if pm_ == pn_ and g_ != f_ and abs(g_ - f_) <= NEAR and (rnd in qs_ or rnd - 1 in qs_) and not {(pn_, f_), (pm_, g_)} <= CLEAR:
                        CLEAR.update({(pn_, f_), (pm_, g_)}); log.append(dict(round=rnd, local_clearance=[pn_, f_, g_], margin_cm=LOCAL_MARGIN)); print(nm, 'local clearance', pn_, f_, g_, flush=True)
        if tot == 0: break
    t_fit = el0 + time.time() - t1; t2 = time.time()
    pk = os.path.join(H.PKG, H.LAYERS)
    K.save(art, dict(status='RP6 RIG PILOT / NOT FROZEN', name='SA_RP6_bake_%s' % nm, body=nm, recipe=dict(base_config=b['cfg'], weights=b['w'], kind=b.get('kind'),
                     geometry='sa6_blend dense convex body blend (bodies.json method), frozen barycentric cage embedding, RP6 joints recomputed on the body, base-config weights'),
                     body_vs_sha256=body_sha(BD, nm), body_json_sha256=b.get('sha256'), initialised_from=dict(layers=H.LAYERS, layers_sha256=C.sha(pk),
                     base=C.BASE_CORR, rig_version=C.RIGV, base_arrays_sha256={c: C.sha(os.path.join(H.PKG, H._js(C.BASE_CORR)['arrays'][c])) for c in 'MF'}),
                     semantics='baked(T) = packaged blend(T) + K(T); K = pose-driven corrective set on this exact body (0 at neutral)',
                     converged=bool(tot == 0), bake_fracs=list(FRACS), pk_min_width=PK_MINW, pk_floor_per_pose=PK_FLOOR or None, motion_refit=dict(grid=PK_GRID, dropped_keys=MOT_DROPPED) if PK_GRID else None, pen_margin_cm=PEN_MARGIN, local_clearance=dict(margin_cm=LOCAL_MARGIN, near=NEAR, samples=sorted([list(x_) for x_ in CLEAR])) if LOCAL_MARGIN else None, only_poses=sorted(ONLY) or None, adaptive_samples=EXTRA, initialised_from_artifact=ini or None, rounds_entering=n_entering, fit_log=log,
                     timing=dict(setup_s=round(t_setup, 1), fit_s=round(t_fit, 1), peak_mb=round(peak_mb(), 1), host=platform.node(), cpu=platform.processor(), os=platform.platform(), cpus_used=1,
                                 threads=os.environ.get('OMP_NUM_THREADS'))))
    t_write = time.time() - t2
    j = json.load(open(art)); j['timing']['write_s'] = round(t_write, 2); json.dump(j, open(art, 'w'), indent=1)
    print(nm, 'BAKED converged', tot == 0, 'families', len(K.F), 'pose keys', len(K.PK), 'fit %.0fs peak %.0f MB' % (t_fit, peak_mb()), flush=True)
