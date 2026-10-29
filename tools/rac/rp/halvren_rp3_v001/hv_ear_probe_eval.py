# hv_ear_probe_eval.py WORK CAND HEAD OUT.json : Halvren mixed-ear order §22 shape-probe record -- per probe (hv_ear_probes.sh): technical state of the
# probe realization (integrity / branch self-intersections / min corner / aspect / T-4) and the response of the measured ear domains (hv_ear_domains.py,
# normalised by the source pooled SD) and of the ear_measure dimensions, vs the unprobed candidate. Independence read: the probed control's own domain
# carries the largest normalised response (the controls move independently, within the coupled anatomy).
import sys, os, json, glob, numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); import hv_ear_domains as D
W, C, H, OUT = sys.argv[1:5]; jl = lambda p: json.load(open(p))
OWN = dict(len='length_over_HH', proj='projection_deg', sweep='sweep_cm', tilt='backward_angle_deg', wb='width_over_length', tip='tip_angle_deg', lobe='lobe_fraction')
SD = jl(os.environ.get('HV_EAR_AUDIT', '/tmp/claude-0/rt/hv/ear/HV_ear_audit.json'))['measured']['pooled_sd']
def meas(npz, mj):
    d = D.measure('branch', npz, H); m = jl(mj); av = lambda q: float(np.mean([m['sides'][s][q] for s in ('l', 'r')]))
    d['sweep_cm'] = av('sweep_max_axis_deviation_cm'); return d
base = meas('%s/build/%s_%s_branch.npz' % (W, H, C), '%s/meas/%s_%s_measure.json' % (W, H, C)); SD = dict(SD, sweep_cm=0.1)
R = dict(order='chatgpt-rac-rp3-halvren-central-accept-ear-architecture-order §22', cand=C, head=H, base={k: base[k] for k in list(D.DOM) + ['sweep_cm']}, probes={})
for d in sorted(glob.glob(W + '/probe/*/')):
    n = os.path.basename(d.rstrip('/')); npz = '%s/%s_%s_branch.npz' % (d, H, C)
    if not os.path.exists(npz) or not os.path.exists(d + 'audit.json'): continue
    A = jl(d + 'audit.json'); m = meas(npz, d + 'measure.json'); keys = list(D.DOM) + ['sweep_cm']
    z = {k: (m[k] - base[k]) / SD[k] for k in keys}; own = OWN[n.split('_')[0]]
    tech = dict(components=A['components'], boundary=A['boundary_edges'], nonmanifold=A['nonmanifold_edges'], branch_selfx=A['self_intersection_pairs_touching_branch'], min_angle=A['T4']['min_angle'],
                aspect_max=A['T4']['aspect_max'], T4=A['T4']['angle_violations'])
    tech['pass'] = bool(A['components'] == 1 and A['boundary_edges'] == 0 and A['nonmanifold_edges'] == 0 and A['self_intersection_pairs_touching_branch'] == 0 and A['T4']['aspect_max'] < 10 and A['T4']['min_angle'] >= 10)
    top = max(keys, key=lambda k: abs(z[k])); kx = [k for k in keys if k != 'tragus_height_frac']; top2 = max(kx, key=lambda k: abs(z[k]))   # cavum-level proxy is an argmax (unstable): also judged without it
    sgn = {'len_m': -1, 'len_p': 1, 'proj_m': -1, 'proj_p': 1, 'sweep_m': -1, 'sweep_p': 1, 'tilt_m': -1, 'tilt_p': 1, 'wb_m': -1, 'wb_p': 1, 'tip_blunt': 1, 'tip_sharp': -1, 'lobe_m': -1, 'lobe_p': 1}[n]
    R['probes'][n] = dict(technical=tech, response_sd={k: round(v, 3) for k, v in z.items()}, own_domain=own, own_response_sd=round(z[own], 3), largest=top, largest_excl_cavum_proxy=top2, own_sign_correct=bool(np.sign(z[own]) == sgn and abs(z[own]) >= 0.1),
                          independent=bool(top == own or abs(z[own]) >= 0.8 * abs(z[top])), independent_excl_cavum_proxy=bool(top2 == own or abs(z[own]) >= 0.8 * abs(z[top2])))
    print(n, 'tech', tech['pass'], 'own %s %+.2f' % (own, z[own]), 'sign', R['probes'][n]['own_sign_correct'], 'largest', top, '%+.2f' % z[top], 'excl', top2, '%+.2f' % z[top2], 'min %.1f asp %.2f selfx %d' % (tech['min_angle'], tech['aspect_max'], tech['branch_selfx']), flush=True)
R['all_technical'] = all(p['technical']['pass'] for p in R['probes'].values()); R['all_independent'] = all(p['independent'] for p in R['probes'].values()); R['own_sign_correct'] = sum(p['own_sign_correct'] for p in R['probes'].values()); R['technical_pass_count'] = sum(p['technical']['pass'] for p in R['probes'].values()); R['n'] = len(R['probes'])
json.dump(R, open(OUT, 'w'), indent=1)
