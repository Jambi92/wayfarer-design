# sa6_bake_full.py NAME BODYDIR UNBAKED_ARTDIR OUTDIR [MAXIT=3] [SHARDS=4] : offline per-body bake with the FULL validation suite from the first pass
#   (offline bake validation order 8e3b7b4d §1-2).  Portable (Windows / Linux), every stage resumable (skipped when its output exists; shards checkpoint per pose).
#   OUTDIR/unbaked/  the same suite on the unbaked body (UNBAKED_ARTDIR/BK_<NAME>: empty K, so baked == packaged blend v004): reproduces the known failures.
#   OUTDIR/it<k>/    k = 0: fit from the packaged blend v004 on the exact body (sa6_bake.py fit, 34 poses x 25/50/75/100 %).  k >= 1: adaptive refit from it<k-1>
#                    with every failing (pose, fraction) of it<k-1> as an extra fit sample (anatomical poses by name, special gates as 'gate:<pose>'; BAKE_EXTRA).
#                    Each iteration reopens its artifact from disk and runs:
#                      EV  34 anatomical poses x 4 fractions + neutral (sa6_bake.py eval)
#                      GT  50 special gates x 4 fractions + neutral (sa6_bake_gates.py, sharded)
#                      SW  full-suite sweep: 0.025 on heavy-joint + K poses, 0.125 elsewhere, +-0.25 deg at every bake and packaged-blend transition (sharded)
#                      GS  every special-gate pose that ever entered the fit: 0.025 grid + +-0.25 deg at its transitions (sa6_bake_gates.py GATES_TRANSITIONS, sharded)
#                      MO  motion: every anatomical pose played on a 1/240 grid + transitions, frame excursion vs max(0.50 cm, packaged blend) (sharded)
#                      DS  (BAKE_DENSE=1, run only once every stage above is clean) dense between-sample audit, sa6_bake_dense.py: the sweep's dense pose set
#                          on a 0.0025 grid; its failing fractions are refit samples like any other (added after pass 2: END_MUFAHI leaked between 0.025 samples)
#                    BAKE_SEED_EXTRA=<json>: extra fit samples merged in before the first refit (e.g. a dense audit of an earlier run).
#                    Stop when all are clean, or after MAXIT refits (remaining failures are reported exactly).
#   Final: IN (RP5 / package integrity, sa6_bake_integrity.py), RL (RP5-literal diagnostics, EVAL_SUITE=rp5, not gates), BA (before / after at the same body,
#   pose and fraction for every unbaked failure, sa6_bake_beforeafter.py).  Record -> OUTDIR/FULL_<NAME>.json (stages, wall seconds, rc, peak MB, retries).
#
#   APPROVED STANDARD RECIPE (author decision, standards approval order c65e6c93, 2026-11-20).  BAKE_RECIPE=standard (default) sets, unless the caller sets them:
#     BAKE_PK_MINW=0.25        pose-key tent HALF-width floor, as a fraction of the pose's full angle (a key at angle s ramps from s - w to s + w,
#                              w >= 0.25 x full angle; sa6_bake.BakeProxy.add_pose_key)
#     BAKE_DENSE=1, DENSE_STEP=0.0025   dense audit stage (every bake-affected anatomical pose + the heavy-joint risk set, +-0.25 deg at baked and
#                              initialization-layer transitions)
#     BAKE_GATE_ALIGNED_ALLOW=1  fit composition allowance = gate ownership rule;  BAKE_MOTION=1, BAKE_MOTION_RULE=local (provisional local motion rule)
#     MAXIT=3 adaptive refits, then remaining failures are reported for review.
#   Every failure feeds the adaptive fit: gate / sweep / dense failures as fit samples; a motion-gate failure as 'motion:<pose>' (sa6_bake.py: the frame
#   pair's fractions become fit samples and that pose's pose-key floor doubles, existing keys widened).
#   BAKE_RECIPE=archived restores the pre-standard defaults (floor 0, no dense stage, unaligned allowance, motion verdict = BAKE_MOTION_RULE, default
#   'original' = first rule, motion failures reported but not fed back) so the archived runners reproduce with their recorded settings.
#   python sa6_bake_full.py --recipe prints the effective recipe and exits.  Acceptance record -> OUTDIR/ACCEPT_<NAME>.json.
import sys, os, json, time, shutil, subprocess, hashlib, glob
STANDARD = dict(BAKE_PK_MINW='0.25', BAKE_DENSE='1', DENSE_STEP='0.0025', BAKE_GATE_ALIGNED_ALLOW='1', BAKE_MOTION='1', BAKE_MOTION_RULE='local',
                BAKE_MOTION_REFIT='1', BAKE_MOTION_REFIT_MODE='grid', BAKE_MOTION_GRID='step', BAKE_LOCAL_MARGIN='0.03')    # motion-fed pose: refit from the initialisation layer on the step grid (order 07a3f24c §3)
ARCHIVED = dict(BAKE_PK_MINW='0', BAKE_DENSE='0', DENSE_STEP='0.0025', BAKE_MOTION='1', BAKE_MOTION_RULE='original', BAKE_MOTION_REFIT='0')
RECIPE = os.environ.get('BAKE_RECIPE', 'standard')
if RECIPE not in ('standard', 'archived'): raise SystemExit('BAKE_RECIPE must be standard or archived')
for k_, v_ in (STANDARD if RECIPE == 'standard' else ARCHIVED).items(): os.environ.setdefault(k_, v_)
RECIPE_KEYS = sorted(set(STANDARD) | set(ARCHIVED) | {'BAKE_LOCAL_NEAR', 'BAKE_SEED_EXTRA', 'BAKE_PEN_MARGIN', 'BAKE_FRACS', 'ROUNDS', 'RP6_LAYERS', 'BAKE_PK_TENT', 'RP6_RIG', 'BAKE_PK_GRID_ALL'})
def effective_recipe(): return dict(recipe=RECIPE, env={k: os.environ.get(k) for k in RECIPE_KEYS if os.environ.get(k) is not None})
if len(sys.argv) > 1 and sys.argv[1] == '--recipe': print(json.dumps(effective_recipe(), indent=1)); sys.exit(0)
T = os.path.dirname(os.path.abspath(__file__)); PY = sys.executable
nm, BD, UA, OD = sys.argv[1:5]; MAXIT = int(sys.argv[5]) if len(sys.argv) > 5 else 3; NSH = int(sys.argv[6]) if len(sys.argv) > 6 else 4
os.makedirs(OD, exist_ok=True); RECF = os.path.join(OD, 'FULL_%s.json' % nm)
rec = json.load(open(RECF)) if os.path.exists(RECF) else dict(name=nm, status='RP6 RIG PILOT / NOT FROZEN', shards=NSH, max_refits=MAXIT, stages=[], iterations=[])
DENSE = os.environ['BAKE_DENSE'] == '1'           # DS stage (sa6_bake_dense.py); standard recipe on, archived off
MOTION = os.environ['BAKE_MOTION'] == '1'         # MO stage (sa6_bake_motion.py)
MRULE = os.environ['BAKE_MOTION_RULE']            # 'local' (approved provisional rule: verdict 'pass') | 'original' (first rule: 'pass_original')
if MRULE not in ('local', 'original'): raise SystemExit('BAKE_MOTION_RULE must be local or original')
rec.setdefault('recipes', []).append(dict(started=time.strftime('%Y-%m-%d %H:%M:%S'), **effective_recipe()))
LOW = 0x00004000 if os.name == 'nt' else 0   # BELOW_NORMAL_PRIORITY_CLASS on Windows
def save(): json.dump(rec, open(RECF + '.tmp', 'w'), indent=1); os.replace(RECF + '.tmp', RECF)
def log(): return open(os.path.join(OD, 'log_%s.txt' % nm), 'a')
def stage(name, d, out, cmds, merge=None):
    """run cmds (list of (args, env)) in parallel unless d/out exists; then merge; one retry of the whole stage on a non-zero rc"""
    if os.path.exists(os.path.join(d, out)): return
    for attempt in (0, 1):
        t = time.time(); L = log(); ps = [subprocess.Popen([PY] + a, env=dict(os.environ, **e), stdout=L, stderr=subprocess.STDOUT, creationflags=LOW) for a, e in cmds]
        rcs = [p.wait() for p in ps]
        if merge and not any(rcs): rcs.append(subprocess.call([PY] + merge, stdout=L, stderr=subprocess.STDOUT))
        L.close(); ok = not any(rcs) and os.path.exists(os.path.join(d, out))
        rec['stages'].append(dict(stage=name, dir=os.path.basename(d), processes=len(cmds), wall_s=round(time.time() - t, 1), rc=rcs, attempt=attempt, end=time.strftime('%Y-%m-%d %H:%M:%S')))
        save()
        if ok: return
    raise SystemExit('stage %s failed twice in %s (see log)' % (name, d))
def suite(d, art_dir, gate_sweep, motion=True):
    """EV, GT, SW (+ GS) (+ MO) of the artifact in art_dir, written to d"""
    stage('gates', d, 'GT_%s.json' % nm, [([os.path.join(T, 'sa6_bake_gates.py'), nm, BD, art_dir, d], dict(GATES_SHARD='%d/%d' % (i, NSH), GATES_CKPT=os.path.join(d, 'GT_%s.s%dof%d.partial.json' % (nm, i, NSH))))
                                          for i in range(NSH) if not os.path.exists(os.path.join(d, 'GT_%s.s%dof%d.json' % (nm, i, NSH)))], [os.path.join(T, 'sa6_bake_gates_merge.py'), nm, d, str(NSH)])
    stage('sweep', d, 'SW_%s.json' % nm, [([os.path.join(T, 'sa6_bake_sweep.py'), nm, BD, art_dir, d], dict(SWEEP_SET='all', SWEEP_STEP_OTHER='0.125', SWEEP_SHARD='%d/%d' % (i, NSH)))
                                          for i in range(NSH) if not os.path.exists(os.path.join(d, 'SW_%s.s%dof%d.json' % (nm, i, NSH)))], [os.path.join(T, 'sa6_bake_sweep_merge.py'), nm, d, str(NSH)])
    if gate_sweep:
        gd = os.path.join(d, 'gate_sweep'); os.makedirs(gd, exist_ok=True); n = min(NSH, len(gate_sweep))
        grid = ','.join('%.3f' % (k * 0.025) for k in range(1, 41))
        stage('gate_sweep', gd, 'GT_%s.json' % nm, [([os.path.join(T, 'sa6_bake_gates.py'), nm, BD, art_dir, gd], dict(GATES_ONLY=','.join(gate_sweep), GATES_FRACS=grid, GATES_TRANSITIONS='1',
                                          GATES_SHARD='%d/%d' % (i, n), GATES_CKPT=os.path.join(gd, 'GT_%s.s%dof%d.partial.json' % (nm, i, n)))) for i in range(n)
                                          if not os.path.exists(os.path.join(gd, 'GT_%s.s%dof%d.json' % (nm, i, n)))], [os.path.join(T, 'sa6_bake_gates_merge.py'), nm, gd, str(n)])
    if motion and MOTION:
        stage('motion', d, 'MO_%s.json' % nm, [([os.path.join(T, 'sa6_bake_motion.py'), nm, BD, art_dir, d], dict(MOTION_SHARD='%d/%d' % (i, NSH))) for i in range(NSH)],
              [os.path.join(T, 'sa6_bake_motion.py'), '--merge', nm, d])
def bad(row): return row['rig_flips'] or row['rig_pen'] or row['rig_tears'] or not row['volume_ok']
def failures(d, gate_sweep):
    """every failing (pose, fraction): anatomical poses by name, special gates as 'gate:<pose>'; plus non-sample failures (rigid / neutral)"""
    f = {}; other = []
    ev = json.load(open(os.path.join(d, 'EV_%s.json' % nm)))
    for pn, rows in ev['poses'].items():
        for fr, r in rows.items():
            if bad(r['bake']): f.setdefault(pn, set()).add(round(float(fr), 5))
            if r['bake'].get('rigid_max_cm', 0) > 0.05: other.append(('rigid', pn, fr))
    nb = ev['neutral_max_displacement_cm'].get('bake', 0) if isinstance(ev['neutral_max_displacement_cm'], dict) else ev['neutral_max_displacement_cm']
    if nb: other.append(('neutral', nb))
    for g in [os.path.join(d, 'GT_%s.json' % nm)] + ([os.path.join(d, 'gate_sweep', 'GT_%s.json' % nm)] if gate_sweep else []):
        gt = json.load(open(g))
        for pn, rows in gt['poses'].items():
            for fr, r in rows.items():
                if bad(r['bake']): f.setdefault('gate:' + pn, set()).add(round(float(fr), 5))
                if r['bake'].get('rigid_max_cm', 0) > 0.05: other.append(('rigid', 'gate:' + pn, fr))
        if gt['neutral_bake_max_displacement_cm']: other.append(('neutral', gt['neutral_bake_max_displacement_cm']))
    sw = json.load(open(os.path.join(d, 'SW_%s.json' % nm)))
    for pn, v in sw['poses'].items():
        for g in v['gate_failures']: f.setdefault(pn, set()).add(round(float(g['frac']), 5))
        if v['rigid_max_cm'] > 0.05: other.append(('rigid', pn, 'sweep'))
    mo = os.path.join(d, 'MO_%s.json' % nm)
    if os.path.exists(mo):      # standard: a motion failure feeds the fit as 'motion:<pose>' (frame-pair fractions; sa6_bake widens that pose's keys)
        for pn, v in json.load(open(mo))['poses'].items():
            ok = v['pass'] if MRULE == 'local' else v.get('pass_original', v['pass'])
            if ok: continue
            if RECIPE == 'standard': f.setdefault('motion:' + pn, set()).update(round(float(x), 5) for x in (v['local'] if 'local' in v else v['bake'])['at'])
            else: other.append(('motion', pn, v['bake']['frame_excursion_cm'], v['limit_cm']))
    ds = os.path.join(d, 'DS_%s.json' % nm)
    if os.path.exists(ds):
        for pn, v in json.load(open(ds))['poses'].items():
            for fr in v['bake_failing']: f.setdefault(pn, set()).add(round(float(fr), 5))
    return {k: sorted(v) for k, v in f.items()}, other
def dense(d, art_dir):
    stage('dense', d, 'DS_%s.json' % nm, [([os.path.join(T, 'sa6_bake_dense.py'), nm, BD, art_dir, d], dict(DENSE_SHARD='%d/%d' % (i, NSH), DENSE_STEP=os.environ['DENSE_STEP'])) for i in range(NSH)],
          [os.path.join(T, 'sa6_bake_dense.py'), '--merge', nm, d])
# --- unbaked reference (same suite, same body) ---
ud = os.path.join(OD, 'unbaked'); os.makedirs(ud, exist_ok=True)
for ext in ('.json', '.npz'):
    src = os.path.join(UA, 'BK_%s%s' % (nm, ext))
    if not os.path.exists(os.path.join(ud, os.path.basename(src))): shutil.copy(src, ud)
stage('eval', ud, 'EV_%s.json' % nm, [([os.path.join(T, 'sa6_bake.py'), 'eval', nm, BD, ud], {})]); suite(ud, ud, [], motion=False)
uf, uo = failures(ud, []); rec['unbaked'] = dict(failures=uf, other=uo, n_failing_samples=sum(len(v) for v in uf.values())); save()
# --- bake + adaptive refits ---
extra = {}; gs = []
if os.environ.get('BAKE_SEED_EXTRA'):
    extra = {k: sorted(set(v)) for k, v in json.load(open(os.environ['BAKE_SEED_EXTRA'])).items()}; gs = sorted({k[5:] for k in extra if k.startswith('gate:')})
for it in range(MAXIT + 1):
    d = os.path.join(OD, 'it%d' % it); os.makedirs(d, exist_ok=True)
    env = {} if it == 0 else dict(BAKE_INIT=os.path.join(OD, 'it%d' % (it - 1), 'BK_%s.json' % nm), BAKE_EXTRA=os.path.join(d, 'extra.json'))
    if it and not os.path.exists(os.path.join(d, 'BK_%s.json' % nm)): json.dump(extra, open(os.path.join(d, 'extra.json'), 'w'), indent=1)   # a resumed iteration keeps its record
    stage('fit', d, 'BK_%s.json' % nm, [([os.path.join(T, 'sa6_bake.py'), 'fit', nm, BD, d], env)])
    stage('eval', d, 'EV_%s.json' % nm, [([os.path.join(T, 'sa6_bake.py'), 'eval', nm, BD, d], {})])
    suite(d, d, gs)
    f, other = failures(d, gs)
    if DENSE and not f and not other: dense(d, d); f, other = failures(d, gs)
    bk = json.load(open(os.path.join(d, 'BK_%s.json' % nm)))
    row = dict(it=it, clean=not f and not other, failures=f, other=other, n_failing_samples=sum(len(v) for v in f.values()), extra_samples=sum(len(v) for v in extra.values()),
               gate_sweep_poses=list(gs), families=len(bk.get('families', {})), pose_keys=len(bk.get('pose_keys', {})), converged=bk.get('converged'), fit_timing=bk.get('timing'))
    rec['iterations'] = [r for r in rec['iterations'] if r['it'] != it] + [row]; save()
    print(time.strftime('%H:%M'), nm, 'it', it, 'clean', row['clean'], 'failing samples', row['n_failing_samples'], {k: len(v) for k, v in f.items()}, other, flush=True)
    if row['clean'] or it == MAXIT or not f: break      # nothing the fit can address (e.g. rigid / neutral, or archived-recipe motion): stop and report
    for pn, fs in f.items(): extra[pn] = sorted(set(extra.get(pn, [])) | set(fs))
    gs = sorted({k[5:] for k in extra if k.startswith('gate:')})
fd = os.path.join(OD, 'it%d' % rec['iterations'][-1]['it'])
rec['final'] = dict(iteration=rec['iterations'][-1]['it'], dir=os.path.basename(fd), clean=rec['iterations'][-1]['clean'], remaining=rec['iterations'][-1]['failures'] if not rec['iterations'][-1]['clean'] else {})
# --- final: integrity, RP5-literal diagnostics, before / after ---
stage('integrity', fd, 'IN_%s.json' % nm, [([os.path.join(T, 'sa6_bake_integrity.py'), nm, BD, fd, fd], {})])
rl = os.path.join(fd, 'rp5lit'); os.makedirs(rl, exist_ok=True)
for ext in ('.json', '.npz'):
    if not os.path.exists(os.path.join(rl, 'BK_%s%s' % (nm, ext))): shutil.copy(os.path.join(fd, 'BK_%s%s' % (nm, ext)), rl)
stage('rp5lit', rl, 'EV_%s.json' % nm, [([os.path.join(T, 'sa6_bake.py'), 'eval', nm, BD, rl], dict(EVAL_SUITE='rp5'))])
stage('before_after', fd, 'BA_%s.json' % nm, [([os.path.join(T, 'sa6_bake_beforeafter.py'), nm, BD, ud, fd], {})])
rec['integrity_clean'] = json.load(open(os.path.join(fd, 'IN_%s.json' % nm)))['clean']; rec['done'] = time.strftime('%Y-%m-%d %H:%M:%S'); save()
def _sha(p): return hashlib.sha256(open(p, 'rb').read()).hexdigest() if os.path.exists(p) else None
def _j(p): return json.load(open(p)) if os.path.exists(p) else None
bk = _j(os.path.join(fd, 'BK_%s.json' % nm)); ev = _j(os.path.join(fd, 'EV_%s.json' % nm)); gt = _j(os.path.join(fd, 'GT_%s.json' % nm)); sw = _j(os.path.join(fd, 'SW_%s.json' % nm))
mo = _j(os.path.join(fd, 'MO_%s.json' % nm)); ds = _j(os.path.join(fd, 'DS_%s.json' % nm)); gsj = _j(os.path.join(fd, 'gate_sweep', 'GT_%s.json' % nm))
acc = dict(status='RP6 RIG PILOT / NOT FROZEN', name=nm, accepted_candidate=bool(rec['final']['clean'] and rec['integrity_clean']), final=rec['final'],
    recipe=effective_recipe(), maxit=MAXIT, shards=NSH,
    tools={os.path.basename(p): _sha(p) for p in sorted(glob.glob(os.path.join(T, 'sa6_*.py')))},
    inputs=dict(body=nm, bodies_json=os.path.join(BD, 'bodies.json'), bodies_json_sha256=_sha(os.path.join(BD, 'bodies.json')), body_npz_sha256=_sha(os.path.join(BD, nm + '.npz')),
                body_vs_sha256=bk.get('body_vs_sha256'), body_recipe=bk.get('recipe'), initialised_from=bk.get('initialised_from'), unbaked_artifact_dir=UA),
    artifact=dict(json=os.path.join(fd, 'BK_%s.json' % nm), json_sha256=_sha(os.path.join(fd, 'BK_%s.json' % nm)), npz_sha256=_sha(os.path.join(fd, 'BK_%s.npz' % nm)),
                  families=len(bk.get('families', {})), pose_keys=len(bk.get('pose_keys', [])), pk_min_width=bk.get('pk_min_width'), converged=bk.get('converged')),
    sampled=dict(anatomical=dict(poses=len(ev['poses']), fractions=sorted({float(f_) for v in ev['poses'].values() for f_ in v}), neutral=True, clean=ev['clean']),
                 special_gates=dict(poses=len(gt['poses']), fractions=sorted({float(f_) for v in gt['poses'].values() for f_ in v}), neutral=True, clean=gt['clean']),
                 sweep=dict(set=sw.get('sweep_set'), step_dense=sw.get('step_dense'), step_other=sw.get('step_other'), samples={k: v['n_samples'] for k, v in sw['poses'].items()}, clean=sw['clean']),
                 gate_sweep=(dict(poses=list(gsj['poses']), samples=sum(len(v) for v in gsj['poses'].values()), clean=gsj['clean']) if gsj else None),
                 motion=(dict(rule=mo['gate'], frame=mo['gate']['frame'], grid=mo['gate']['grid'], poses=len(mo['poses']), verdict_used=MRULE, clean=all((v['pass'] if MRULE == 'local' else v.get('pass_original', v['pass'])) for v in mo['poses'].values()))
                         if mo else None),
                 dense=(dict(step=ds['step'], poses=sorted(ds['poses']), samples=ds['n_samples'], bake_failing=ds['bake_failing_samples'], clean=ds['clean']) if ds else None)),
    integrity_clean=rec['integrity_clean'], before_after=os.path.join(fd, 'BA_%s.json' % nm), record=RECF)
json.dump(acc, open(os.path.join(OD, 'ACCEPT_%s.json' % nm), 'w'), indent=1)
print(time.strftime('%H:%M'), nm, 'FULL done: final it%d clean %s integrity %s' % (rec['final']['iteration'], rec['final']['clean'], rec['integrity_clean']), flush=True)
