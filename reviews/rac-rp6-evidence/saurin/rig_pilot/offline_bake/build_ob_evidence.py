# build_ob_evidence.py : offline bake validation (order 8e3b7b4d) evidence -> reviews/rac-rp6-evidence/saurin/rig_pilot/offline_bake/
#   Inputs (staged from Tyler's PC): S = staged SaurinRP6_offline.  Final run per body (SRC), superseded runs (SUP), the motion re-runs under the local rule
#   (out_mo/v2L) and the dense audits (out_dense) for bakes whose own run had no DS stage; cloud tail-calibration data and renders.
#   Writes SA_RP6_offline_bake_results_v001.json (per body: roster, run, unbaked failures, iterations, final gates, dense audit, motion (local rule + first
#   rule), integrity, before / after, RP5-literal diagnostics, timings) and SA_RP6_offline_bake_manifest_v001.json (sha256 of every file).
import os, sys, json, glob, shutil, hashlib, collections
S = '/mnt/user-data/uploads/RaceBodies/SaurinRP6_offline'; R6 = '/tmp/claude-0/rp6'
REPO = '/home/claude/wayfarer-design'; EV = REPO + '/reviews/rac-rp6-evidence/saurin/rig_pilot/offline_bake'
SRC = dict(BASE_c1=('out_v2', 'pass 2 (pose-key floor 1/8)'), BASE_c2=('out_v2', 'pass 2 (pose-key floor 1/8)'),
           END_FAHI=('out_v2wd', 'repair 2: w25 run (floor 1/4) continued with the dense audit'), END_MUFAHI=('out_v3', 'repair 2: rebake from v004, floor 1/4, dense audit'))
MO_EXT = dict(BASE_c1='out_mo/v2L', BASE_c2='out_mo/v2L')          # pass-2 runs predate the local motion rule: re-run on the final artifact
DS_EXT = dict(BASE_c1='out_dense/v2', BASE_c2='out_dense/v2')       # pass-2 runs predate the DS stage: audited on the final artifact
SUP = {'END_FAHI_pass2': ('out_v2/END_FAHI', 'it3', 'pass 2: clean on samples; first-rule motion FAIL hip_flex70_xpos 0.6205 vs 0.6183 (superseded by w25)'),
       'END_FAHI_w25': ('out_v2w/END_FAHI', 'it2', 'repair 1 (floor 1/4): samples clean, local motion PASS; dense audit 14 leaks (superseded by repair 2)'),
       'END_MUFAHI_pass2': ('out_v2/END_MUFAHI', 'it3', 'pass 2: 2 sweep samples failing (fit ping-pong); dense audit 11 leaks (superseded)'),
       'END_MUFAHI_dense': ('out_v2d/END_MUFAHI', 'it5', 'repair 1 (pass 2 continued + dense): it4 dense cleared the trunk_twist_30 leaks, 1 left (hip_flex70_xpos 0.2125, it4/DS); it5 refit clean on samples but LOCAL motion FAIL shoulder_abd90_xneg (pose key width 11.25 deg, 2.77 cm: trunk 0.73 cm in one frame), so its dense stage did not run (superseded by repair 2)')}
SUP_EXTRA = {'END_MUFAHI_dense': ['it4/DS_END_MUFAHI.json', 'it4/BK_END_MUFAHI.json', 'it4/MO_END_MUFAHI.json']}
SUP_DS = {'END_FAHI_w25': 'out_dense/v2w/END_FAHI/DS_END_FAHI.json', 'END_MUFAHI_pass2': 'out_dense/v2/END_MUFAHI/DS_END_MUFAHI.json'}
SUP_MO = {'END_FAHI_w25': 'out_mo/v2L/END_FAHI/MO_END_FAHI.json'}
NAMES = list(SRC)
def sha(p): return hashlib.sha256(open(p, 'rb').read()).hexdigest()
def J(p): return json.load(open(p))
def shard(p): import re; return re.search(r'\.s\d+of\d+\.json$', p) is not None
def motion_summary(M):
    P = M['poses']; loc = 'local' in next(iter(P.values()))
    out = dict(rule=M['gate']['pass_rule'], clean=M['clean'], failing=M['failing'], poses=len(P))
    if loc:
        w = max(P.items(), key=lambda kv: kv[1]['local']['worst_excess_cm'])
        out.update(failing_original_rule=sorted(k for k, v in P.items() if not v['pass_original']), tightest=dict(pose=w[0], **w[1]['local']),
                   max_bake=max(((k, v['bake']['frame_excursion_cm'], v['prod']['frame_excursion_cm']) for k, v in P.items()), key=lambda x: x[1]),
                   max_k=max(((k, v['k']['frame_excursion_cm'], v['k']['at_deg'], v['k']['region']) for k, v in P.items()), key=lambda x: x[1]),
                   per_pose={k: dict(prod=v['prod']['frame_excursion_cm'], bake=v['bake']['frame_excursion_cm'], k=v['k']['frame_excursion_cm'], local_excess=v['local']['worst_excess_cm'],
                                     passed=v['pass'], passed_original=v['pass_original']) for k, v in P.items()})
    return out
def dense_summary(D):
    return dict(clean=D['clean'], step=D['step'], samples=D['n_samples'], bake_failing=D['bake_failing_samples'], bake_added=D['bake_added'], prod_failing=D['prod_failing_samples'],
                poses=len(D['poses']), failing={k: v['bake_failing'] for k, v in D['poses'].items() if v['bake_failing']})
os.makedirs(EV, exist_ok=True); res = dict(status='RP6 RIG PILOT / NOT FROZEN', order='8e3b7b4d', roster=J(EV + '/SA_RP6_offline_bake_roster_v001.json'), bodies={}, superseded={})
for d in ('bodies', 'superseded', 'tail', 'motion'):
    if os.path.exists(os.path.join(EV, d)): shutil.rmtree(os.path.join(EV, d))
for nm in NAMES:
    run, desc = SRC[nm]; src = os.path.join(S, run, nm); dst = os.path.join(EV, 'bodies', nm)
    shutil.copytree(src, dst, ignore=lambda d, fs: [f for f in fs if f == 'ckpt' or f.endswith(('.partial.json', '.tmp')) or shard(f)])
    F = J(os.path.join(src, 'FULL_%s.json' % nm)); fd = os.path.join(src, F['final']['dir'])
    ev = J(os.path.join(fd, 'EV_%s.json' % nm)); gt = J(os.path.join(fd, 'GT_%s.json' % nm)); sw = J(os.path.join(fd, 'SW_%s.json' % nm))
    gs = os.path.join(fd, 'gate_sweep', 'GT_%s.json' % nm); gs = J(gs) if os.path.exists(gs) else None
    IN = J(os.path.join(fd, 'IN_%s.json' % nm)); BA = J(os.path.join(fd, 'BA_%s.json' % nm)); RL = J(os.path.join(fd, 'rp5lit', 'EV_%s.json' % nm)); bk = J(os.path.join(fd, 'BK_%s.json' % nm))
    mo = os.path.join(S, MO_EXT[nm], nm, 'MO_%s.json' % nm) if nm in MO_EXT else os.path.join(fd, 'MO_%s.json' % nm)
    ds = os.path.join(S, DS_EXT[nm], nm, 'DS_%s.json' % nm) if nm in DS_EXT else os.path.join(fd, 'DS_%s.json' % nm)
    if nm in MO_EXT: shutil.copy(mo, os.path.join(dst, F['final']['dir'], 'MO_%s.local.json' % nm))
    if nm in DS_EXT: shutil.copy(ds, os.path.join(dst, F['final']['dir'], 'DS_%s.json' % nm))
    M = J(mo); D = J(ds); assert M['artifact'] == D['artifact'] == 'BK_%s.json' % nm
    st = collections.defaultdict(float)
    for s_ in F['stages']: st[s_['stage']] += s_['wall_s']
    res['bodies'][nm] = dict(run=run, run_description=desc, recipe=bk.get('recipe'), final=F['final'], done=F.get('done'), unbaked=F['unbaked'],
        iterations=[dict(it=i['it'], clean=i['clean'], n_failing_samples=i['n_failing_samples'], failures=i['failures'], other=i['other'], extra_samples=i['extra_samples'],
                         gate_sweep_poses=i['gate_sweep_poses'], families=i['families'], pose_keys=i['pose_keys'], converged=i['converged'], fit_timing=i['fit_timing']) for i in F['iterations']],
        final_gates=dict(eval=dict(clean=ev['clean'], totals=ev['totals'], neutral=ev['neutral_max_displacement_cm']), special_gates=dict(clean=gt['clean'], totals=gt['totals']),
                         sweep=dict(clean=sw['clean'], poses=len(sw['poses']), samples=sum(v['n_samples'] for v in sw['poses'].values()), rate_ratio_max=max(v['rate_ratio'] for v in sw['poses'].values())),
                         gate_sweep=(dict(clean=gs['clean'], poses=list(gs['poses']), samples=sum(len(v) for v in gs['poses'].values()), totals=gs['totals']) if gs else None)),
        dense=dict(source=os.path.relpath(ds, S), **dense_summary(D)), motion=dict(source=os.path.relpath(mo, S), **motion_summary(M)),
        integrity=dict(clean=IN['clean'], checks=IN['checks'], frozen_files=IN['frozen_files'], neutral=IN['neutral'], ranges=IN['ranges']),
        before_after=dict(n=BA['n'], before_failing=BA['before_failing'], after_failing=BA['after_failing'], rows=BA['rows']),
        rp5_literal=dict(clean_under_gates=RL['clean'], totals=RL['totals'], note='RP5-literal definitions are diagnostics (the pilot retains them as records; gates are on the anatomical suite)'),
        artifact=dict(json_sha256=sha(os.path.join(fd, 'BK_%s.json' % nm)), npz_sha256=sha(os.path.join(fd, 'BK_%s.npz' % nm)), families=len(bk.get('families', {})), pose_keys=len(bk.get('pose_keys', [])),
                      pose_key_widths_deg={p['pose']: round(p['drivers'][0]['width_deg'], 3) for p in bk.get('pose_keys', [])}),
        stage_seconds=dict(st), stages=F['stages'])
for tag, (rd, it, why) in SUP.items():
    src = os.path.join(S, rd); dst = os.path.join(EV, 'superseded', tag); os.makedirs(os.path.join(dst, it), exist_ok=True); nm = rd.split('/')[-1]
    for f in ['FULL_%s.json' % nm, 'log_%s.txt' % nm]:
        if os.path.exists(os.path.join(src, f)): shutil.copy(os.path.join(src, f), dst)
    for p in glob.glob(os.path.join(src, it, '*')):
        if os.path.isfile(p) and not shard(p): shutil.copy(p, os.path.join(dst, it))
    for e in SUP_EXTRA.get(tag, []):
        os.makedirs(os.path.dirname(os.path.join(dst, e)), exist_ok=True); shutil.copy(os.path.join(src, e), os.path.join(dst, e))
    rec = dict(run=rd, iteration=it, why_superseded=why)
    if tag == 'END_MUFAHI_dense': rec['dense_it4'] = dense_summary(J(os.path.join(src, 'it4', 'DS_%s.json' % nm)))
    Fp = os.path.join(src, 'FULL_%s.json' % nm)
    if os.path.exists(Fp):
        F = J(Fp); rec['iterations'] = [dict(it=i['it'], clean=i['clean'], n_failing_samples=i['n_failing_samples'], other=i['other'], pose_keys=i['pose_keys']) for i in F['iterations']]
    if tag in SUP_DS: shutil.copy(os.path.join(S, SUP_DS[tag]), os.path.join(dst, it)); rec['dense'] = dense_summary(J(os.path.join(S, SUP_DS[tag])))
    elif os.path.exists(os.path.join(src, it, 'DS_%s.json' % nm)): rec['dense'] = dense_summary(J(os.path.join(src, it, 'DS_%s.json' % nm)))
    if tag in SUP_MO: shutil.copy(os.path.join(S, SUP_MO[tag]), os.path.join(dst, it, 'MO_%s.local.json' % nm)); rec['motion_local'] = {k: v for k, v in motion_summary(J(os.path.join(S, SUP_MO[tag]))).items() if k != 'per_pose'}
    mo = os.path.join(src, it, 'MO_%s.json' % nm)
    if os.path.exists(mo): rec['motion_in_run'] = {k: v for k, v in motion_summary(J(mo)).items() if k != 'per_pose'}
    bkp = os.path.join(src, it, 'BK_%s.json' % nm)
    if os.path.exists(bkp):
        b = J(bkp); rec['pose_key_widths_deg'] = {p['pose']: round(p['drivers'][0]['width_deg'], 3) for p in b.get('pose_keys', [])}; rec['artifact_json_sha256'] = sha(bkp)
    res['superseded'][tag] = rec
# tail calibration (final artifacts) + proposed criterion
T = os.path.join(EV, 'tail'); os.makedirs(T + '/renders', exist_ok=True)
for p in glob.glob(R6 + '/tailcal2/TC_*.json') + glob.glob(R6 + '/tailcal2/TK_*.json') + [R6 + '/tailcal/TK_benchmark.json', R6 + '/tailcal/frames_benchmark.json']: shutil.copy(p, T)
for p in glob.glob(R6 + '/tailrender/*.png'): shutil.copy(p, T + '/renders')
# elbow motion-rate curves (unbaked + baked dense playback) and playback gifs
M_ = os.path.join(EV, 'motion'); os.makedirs(M_ + '/unbaked', exist_ok=True); os.makedirs(M_ + '/baked_pass1', exist_ok=True)
for p in glob.glob(R6 + '/motion/MR_*') + glob.glob(R6 + '/motion/MG_*') + glob.glob(R6 + '/motion_spike/MR_*'): shutil.copy(p, M_ + '/unbaked')
for p in glob.glob(R6 + '/motion_baked/MR_*') + glob.glob(R6 + '/motion_baked/MG_*'): shutil.copy(p, M_ + '/baked_pass1')
for f in sorted(os.listdir(S)):
    p = os.path.join(S, f)
    if os.path.isfile(p) and (f.endswith(('.py', '.bat', '.jsonl', '.log')) or (f.startswith('seed_') and f.endswith('.json')) or f in ('dense_jobs.json', 'mo_jobs.json')):
        shutil.copy(p, os.path.join(EV, ('pc_' + f) if f.endswith('.log') else f))
json.dump(res, open(EV + '/SA_RP6_offline_bake_results_v001.json', 'w'), indent=1)
man = {os.path.relpath(p, EV): sha(p) for p in sorted(glob.glob(EV + '/**/*', recursive=True)) if os.path.isfile(p) and not p.endswith('_manifest_v001.json')}
json.dump(dict(status='RP6 RIG PILOT / NOT FROZEN', files=man), open(EV + '/SA_RP6_offline_bake_manifest_v001.json', 'w'), indent=1)
for nm, b in res['bodies'].items():
    print(nm, b['run'], b['final'], 'integrity', b['integrity']['clean'], 'BA', b['before_after']['before_failing'], '->', b['before_after']['after_failing'],
          'dense', b['dense']['clean'], b['dense']['samples'], b['dense']['bake_failing'], 'motion', b['motion']['clean'], b['motion'].get('tightest', {}).get('worst_excess_cm'))
for t, r in res['superseded'].items(): print('superseded', t, r.get('dense', {}).get('bake_failing'), r.get('motion_local', r.get('motion_in_run', {})).get('failing'))
print('files', len(man))
