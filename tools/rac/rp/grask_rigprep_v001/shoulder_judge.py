# shoulder_judge.py WORKDIR : Track S tables (order 69f2660 §16): every D1 pose x W0 / S1 / S2 (+ the GH placement probe where run), retained criteria,
# axillary contact depth, girdle kinematics (S1 rule; S2 uses the same poses), and the rest-return. Writes diag/trackS_tables.md + diag/trackS_judgement.json.
import sys, os, json, glob, numpy as np
W = sys.argv[1]
src = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'judge.py')).read(); ns = {}; exec(src[src.index('VOLTOL'):src.index('def cause')], ns); crit = ns['crit']
K = json.load(open(W + '/s1/kinematics_S1.json'))['kinematics']
PZ = ('abd45', 'abd90', 'flex90', 'ext30', 'abd90_girdle', 'flex90_girdle')
R = {t: json.load(open('%s/diag/diag_results_s_%s.json' % (W, t)))['results'] for t in ('W0', 'S1', 'S2w', 'S2')}
PR = {}
for fp in sorted(glob.glob(W + '/diag/diag_results_probe_*.json')): PR[os.path.basename(fp)[len('diag_results_probe_'):-5]] = json.load(open(fp))['results']
def row(r, p):
    i = r['intersections']
    return dict(nc=i['non_contact'], crease=i['crease'], crease_mm=round(i['crease_depth_mm'], 2), contact=i['contact'], contact_mm=round(i.get('contact_depth_mm', 0.0), 2), orient=r['flips']['total'],
                inv=r['inversions']['total'], folds_out=r['folds']['outside'], loop=round(r['loop_spacing_min_ratio'], 3), loop_worst=r['loop_spacing_worst'], p95=round(r['strain']['zone_p95_pct'], 1),
                smax=round(r['strain']['zone_max_pct'], 1), zone=round(r['volume']['zone_pct'], 2), T1=r['rest_return_T1_mm'], fails=[c[0] for c in crit(p, r) if not c[1]])
OUT = {}; MD = ['cells: non-contact / crease (depth mm) / axillary contact pairs (depth mm) / orientation / local inv / folds outside / loop / p95 (max) strain % / zone proxy % [failing retained criteria]', '']
for s in 'lr':
    MD += ['### %s side' % ('left' if s == 'l' else 'right'), '', '| pose | W0 | S1 (mechanics) | S2w (weights only, W0 mechanics) | S2 (S1 + weights) |' + ''.join(' probe %s |' % k for k in PR), '|---|---|---|---|---|' + '---|' * len(PR)]
    for pz in PZ:
        p = 'D1_%s_%s' % (s, pz); cells = []; OUT[p] = {}
        for t, RR in list(R.items()) + list(PR.items()):
            if p not in RR: cells.append('—'); continue
            k = row(RR[p], p); OUT[p][t] = k
            cells.append('%d / %d (%.1f) / %d (%.1f) / %d / %d / %d / %.2f / %.0f (%.0f) / %+.1f [%d]' % (k['nc'], k['crease'], k['crease_mm'], k['contact'], k['contact_mm'], k['orient'], k['inv'], k['folds_out'], k['loop'], k['p95'], k['smax'], k['zone'], len(k['fails'])))
        MD.append('| %s | %s |' % (pz, ' | '.join(cells)))
    MD += ['', '#### girdle kinematics (%s): W0 -> S1 (S2 = S1 poses)' % s, '', '| pose | humeral elevation deg | ST share deg | clavicle rot deg | scapula rot deg | glenohumeral motion deg W0 -> S1 | GH displacement cm | scap. inferior proxy displacement cm (x, f, u) | GH-acromion dist cm W0 / S1 | humeral dir error deg |', '|---|---|---|---|---|---|---|---|---|---|']
    for pz in PZ:
        p = 'D1_%s_%s' % (s, pz); a, b = K[p]['W0'], K[p]['S1']
        MD.append('| %s | %.1f | %.1f | %.1f | %.1f | %.1f -> %.1f | %.2f | %s | %.2f / %.2f | %.4f |' % (pz, b['humeral_elevation_deg'], b['scapulothoracic_share_deg'], b['clavicle_rotation_deg'], b['scapula_rotation_deg'], a['glenohumeral_motion_deg'], b['glenohumeral_motion_deg'],
                                                                             b['GH_disp_cm'], b['scapula_inferior_disp_cm'], a['GH_acromion_dist_cm'], b['GH_acromion_dist_cm'], b['humeral_dir_err_deg']))
    MD.append('')
json.dump(dict(tables=OUT, kinematics=K), open(W + '/diag/trackS_judgement.json', 'w'), indent=1, default=float)
open(W + '/diag/trackS_tables.md', 'w').write('\n'.join(MD) + '\n'); print('\n'.join(MD))
