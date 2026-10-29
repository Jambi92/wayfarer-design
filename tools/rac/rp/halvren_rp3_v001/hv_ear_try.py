# hv_ear_try.py WORK NAME CAND HEAD [PROBE k=v,...] : Halvren HE2 closure order -- one rest-state ear realization (no deformation guard) for control
# calibration: ear_build + ear_audit + measured ear domains + the measured-domain arithmetic firewall vs Marchfolk / Fenn / Aelari / Vael (sources from the
# committed HV_ear_domains.json, same common head). Prints one line; writes WORK/NAME/try.json.
import sys, os, json, subprocess, numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); import hv_ear_domains as D; import hv_ear_summary as S
W, NAME, C, H = sys.argv[1:5]; PR = sys.argv[5] if len(sys.argv) > 5 else ''
T = '/home/claude/wayfarer-design/tools/rac/rp/fenn_rp3_v001'; B = '/home/claude/stc/bin/python3'; d = os.path.join(W, NAME); os.makedirs(d, exist_ok=True)
CANON = os.environ.get('HV_CANON', '/home/claude/wayfarer-design/reviews/rac-rp3-evidence/vael_rp3_ear_root_integration/topology/VAEL_EAR_CUFF_CANON_v001.json')
env = dict(os.environ, EAR_CF=os.environ.get('EAR_CF', '/tmp/claude-0/rt/hv/hpe'), EAR_TOPO='v002', EAR_UNT_MODE='contacts')
cmd = [B, T + '/ear_build.py', H, C, d, '--canon', CANON] + (['--probe', PR] if PR else [])
subprocess.run(cmd, env=env, stdout=open(d + '/build.log', 'w'), stderr=subprocess.STDOUT)
npz = '%s/%s_%s_branch.npz' % (d, H, C)
if os.environ.get('HV_REPAIR', '0') == '1':
    subprocess.run(['python3', os.path.dirname(os.path.abspath(__file__)) + '/hv_cuff_repair.py', npz, H], env=env, stdout=open(d + '/repair.log', 'w'), stderr=subprocess.STDOUT)
subprocess.run([B, T + '/ear_audit.py', '--', npz, '%s/fam/%s_fam.npz' % (env['EAR_CF'], H), d + '/audit.json'], env=env, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
A = json.load(open(d + '/audit.json')); m = D.measure('branch', npz, H); z = np.load(npz); rc = S.root_concha(z, json.load(open(npz.replace('.npz', '.json'))), H)
SRC = json.load(open(os.environ.get('HV_DOMSRC', '/tmp/claude-0/rt/hv/ear/src_dom.json')))['items']
DOM = D.DOM; X = {s: np.array([SRC[s][q] for q in DOM]) for s in ('MF', 'FN', 'AE', 'VA')}; sd = np.maximum(np.array(list(X.values())).std(0), [D.FLOOR[q] for q in DOM])
h = np.array([m[q] for q in DOM]); fw = {}
for e in ('FN', 'AE', 'VA'):
    dx = (X[e] - X['MF']) / sd; y = (h - X['MF']) / sd; k = np.abs(dx) > 0.5; a = float(dx[k] @ y[k] / (dx[k] @ dx[k])); r = y[k] - a * dx[k]
    fw['MF-' + e] = dict(n=int(k.sum()), r2=round(float(1 - r @ r / (y[k] @ y[k])), 3), alpha=round(a, 3))
em = np.mean([X[e] for e in ('FN', 'AE', 'VA')], 0); t = (h - X['MF']) / np.where(np.abs(em - X['MF']) > 1e-9, em - X['MF'], 1)
tech = dict(min_angle=round(A['T4']['min_angle'], 1), aspect=round(A['T4']['aspect_max'], 2), selfx=A['self_intersection_pairs_touching_branch'], T4=A['T4']['angle_violations'], clear=round(A['ear_to_head_clearance']['min_cm'], 2))
tech['clean'] = bool(tech['min_angle'] >= 10 and tech['aspect'] < 10 and tech['selfx'] == 0 and A['components'] == 1 and A['boundary_edges'] == 0)
R = dict(name=NAME, cand=C, head=H, probe=PR, tech=tech, mound=round(rc['anterior_cuff_mound_p90_cm'], 3), junction=round(rc['junction_anterior_height_mean_cm'], 3),
         domains={q: round(m[q], 4) for q in DOM}, t_vs_elf_mean={q: round(float(v), 2) for q, v in zip(DOM, t)}, firewall=fw, best_r2=max(v['r2'] for v in fw.values()))
json.dump(R, open(d + '/try.json', 'w'), indent=1)
print(NAME, 'clean' if tech['clean'] else 'FAIL', tech, 'mound %.2f junc %.2f' % (R['mound'], R['junction']), 'R2', {k: v['r2'] for k, v in fw.items()},
      't', ' '.join('%s %.2f' % (q[:8], v) for q, v in zip(DOM, t)), flush=True)
