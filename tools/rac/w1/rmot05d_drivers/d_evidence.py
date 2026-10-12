# RAC RM-OT-05D: copy the gate evidence into the repository and register the candidate R-6 assets in reviews/reference-assets
# (PENDING AUTHOR / NOT ACCEPTED). Copies: Stage A section strips + allowed-movement tables, floor views, Stage B sheets, blind sets / keys /
# raw classifications (runs 1-3), guards, candidate specs, search history and probes, construction records.
import os, json, shutil, hashlib, glob
S = '/tmp/claude-0/-home-claude-wayfarer-design/19af7d50-3b61-5fda-9fe0-7a30770fb334/scratchpad'; A = S + '/rmot05d'; R = '/home/claude/wayfarer-design'
EV = R + '/reviews/rac-rmot05d-evidence'
for d in ('stageA', 'sheets', 'blind', 'guards', 'search', 'construction'): os.makedirs(EV + '/' + d, exist_ok=True)
for f in glob.glob(A + '/stageA/*'): shutil.copy(f, EV + '/stageA/')
for f in glob.glob(A + '/floorview/fv_v3_*.jpg'): shutil.copy(f, EV + '/stageA/floorview_' + os.path.basename(f)[6:])
for f in glob.glob(A + '/sheets/*.jpg'): shutil.copy(f, EV + '/sheets/')
for f in glob.glob(A + '/blind/*'): shutil.copy(f, EV + '/blind/')
shutil.copy(A + '/guard_all_merged.json', EV + '/guards/guard_all.json')
shutil.copy(A + '/specs_final.json', EV + '/candidates.json')
for f in sorted(glob.glob(A + '/specs/*.json')) + sorted(glob.glob(A + '/specs/mk*.py')): shutil.copy(f, EV + '/search/' + os.path.basename(f))
PS = S + '/rmot05c/prevsheets'
for pat in ('cmb_*_d1b*', 'cmb_*_d2*', 'cmb_*_d3b*', 'cmb_*_e1*', 'cmb_*_e2*', 'cmb_*_e3*', 'cmb_*_kv2*', 'cmb_*_t5*', 'blindq_d1*', 'blindq_e1*', 'blindq_e3*'):
    for f in glob.glob(PS + '/' + pat): shutil.copy(f, EV + '/search/' + os.path.basename(f))
NAMES = {}
for c, cl in (('E1', 'moderate'), ('E2', 'strong'), ('E3', 'assertive')):
    for race, h in (('GR', '218'), ('GO', '230.9')):
        if race == 'GO' and c == 'E3': continue
        n = race + '5D' + c; rn = 'Grask' if race == 'GR' else 'Gorrund'
        NAMES[n] = (rn, '05D candidate %s (%s), reference %s' % (c, cl, h)); NAMES[n + '-LOW'] = (rn, '05D candidate %s low composition (muscle 0 / weight 0.5)' % c)
        NAMES[n + 'N'] = (rn, '05D candidate %s Narrow frame' % c); NAMES[n + 'B'] = (rn, '05D candidate %s Broad frame' % c)
mp = R + '/reviews/reference-assets/manifest.json'; M = json.load(open(mp)); con = {}
for n, (race, role) in NAMES.items():
    d = S + ('/w2c/b/' if race == 'Grask' else '/w2d/b/') + n
    if not os.path.exists(d + '/%s_r6.npz' % n): print('missing', n); continue
    dst = R + '/reviews/reference-assets/r6/%s_r6.npz' % n; shutil.copy(d + '/%s_r6.npz' % n, dst)
    for suf in ('_w2c.json', '_w2d.json', '_meas.json', '_cib.json'):
        if os.path.exists(d + '/' + n + suf): shutil.copy(d + '/' + n + suf, EV + '/construction/' + n + suf)
    rf = [x for x in os.listdir(d) if x.endswith(('_w2c.json', '_w2d.json'))]; con[n] = json.load(open(d + '/' + rf[0])) if rf else {}
    st = json.load(open(d + '/%s_meas.json' % n))['combined']['stature'] if os.path.exists(d + '/%s_meas.json' % n) else None
    M['assets'][n] = {"race": race, "role": role + ' (RM-OT-05D true-skeletal-envelope candidate)', "accepted": "PENDING AUTHOR / NOT ACCEPTED (RM-OT-05D gate)",
                      "stature_r6": st, "file": "r6/%s_r6.npz" % n, "sha256": hashlib.sha256(open(dst, 'rb').read()).hexdigest(), "scratch_source": "$S" + d[len(S):],
                      "recipe": "05B skeleton route (reviews/rac-rmot05b-evidence/cfg_final.json arch + holds, no 05B surface stage) + race_base.organize with reviews/rac-rmot05d-evidence/candidates.json (floor = true skeletal envelope, tools/rac/w1/true_envelope.py)"}
json.dump(M, open(mp, 'w'), indent=1); json.dump(con, open(EV + '/construction/construction.json', 'w'), indent=1, default=str)
print('evidence files', sum(len(f) for _, _, f in os.walk(EV)))
