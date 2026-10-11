# RAC RM-OT-05C: copy the candidate-gate evidence into the repository and register the candidate R-6 assets in reviews/reference-assets
# (PENDING AUTHOR / NOT ACCEPTED). Copies:
#   - sheets, blind sets / keys / scores and the minimal-guard results;
#   - the candidate specs (candidates.json) and the search history (specs, preview sheets, uninformed probes);
#   - the construction records.
import os, sys, json, shutil, hashlib, glob
S = '/tmp/claude-0/-home-claude-wayfarer-design/19af7d50-3b61-5fda-9fe0-7a30770fb334/scratchpad'; A = S + '/rmot05c'; R = '/home/claude/wayfarer-design'
EV = R + '/reviews/rac-rmot05c-evidence'
for d in ('sheets', 'blind', 'guards', 'search', 'construction'): os.makedirs(EV + '/' + d, exist_ok=True)
for f in glob.glob(A + '/sheets/*.jpg'): shutil.copy(f, EV + '/sheets/')
for f in glob.glob(A + '/blind/*.jpg') + glob.glob(A + '/blind/*.json'): shutil.copy(f, EV + '/blind/')
for f in glob.glob(A + '/guard_*.json'): shutil.copy(f, EV + '/guards/')
shutil.copy(A + '/specs_final.json', EV + '/candidates.json')
for f in sorted(glob.glob(A + '/specs/s*.json')) + sorted(glob.glob(A + '/specs/mk*.py')): shutil.copy(f, EV + '/search/' + os.path.basename(f))
for f in glob.glob(A + '/prevsheets/cmb_*.jpg') + glob.glob(A + '/prevsheets/blindq_*'): shutil.copy(f, EV + '/search/' + os.path.basename(f))
NAMES = {}
for c, cl in (('A', 'restrained'), ('B', 'balanced'), ('C', 'assertive')):
    NAMES['GR5C' + c] = ('Grask', 'candidate %s (%s), reference 218' % (c, cl)); NAMES['GR5C%s-LOW' % c] = ('Grask', 'candidate %s low composition (muscle 0 / weight 0.5) on GR5C%s' % (c, c))
    NAMES['GR5C%s229' % c] = ('Grask', 'candidate %s matched-height 229' % c); NAMES['GR5C%sN' % c] = ('Grask', 'candidate %s Narrow frame 218' % c); NAMES['GR5C%sB' % c] = ('Grask', 'candidate %s Broad frame 218' % c)
    NAMES['GO5C' + c] = ('Gorrund', 'candidate %s (%s), reference 230.9' % (c, cl)); NAMES['GO5C%s-LOW' % c] = ('Gorrund', 'candidate %s low composition (muscle 0 / weight 0.5) on GO5C%s' % (c, c))
    NAMES['GO5C%sN' % c] = ('Gorrund', 'candidate %s Narrow frame 230.9' % c); NAMES['GO5C%sB' % c] = ('Gorrund', 'candidate %s Broad frame 230.9' % c)
mp = R + '/reviews/reference-assets/manifest.json'; M = json.load(open(mp)); con = {}
for n, (race, role) in NAMES.items():
    d = S + ('/w2c/b/' if race == 'Grask' else '/w2d/b/') + n
    if not os.path.exists(d + '/%s_r6.npz' % n): print('missing', n); continue
    dst = R + '/reviews/reference-assets/r6/%s_r6.npz' % n; shutil.copy(d + '/%s_r6.npz' % n, dst)
    for suf in ('_w2c.json', '_w2d.json', '_meas.json', '_cib.json'):
        if os.path.exists(d + '/' + n + suf): shutil.copy(d + '/' + n + suf, EV + '/construction/' + n + suf)
    rf = [x for x in os.listdir(d) if x.endswith(('_w2c.json', '_w2d.json'))]
    con[n] = json.load(open(d + '/' + rf[0])) if rf else {}
    st = json.load(open(d + '/%s_meas.json' % n))['combined']['stature'] if os.path.exists(d + '/%s_meas.json' % n) else None
    M['assets'][n] = {"race": race, "role": role + ' (RM-OT-05C base-surface candidate)', "accepted": "PENDING AUTHOR / NOT ACCEPTED (RM-OT-05C author candidate gate)",
                      "stature_r6": st, "file": "r6/%s_r6.npz" % n, "sha256": hashlib.sha256(open(dst, 'rb').read()).hexdigest(), "scratch_source": "$S" + d[len(S):],
                      "recipe": "05B skeleton route (reviews/rac-rmot05b-evidence/cfg_final.json arch + holds, no 05B surface stage) + race_base.organize with reviews/rac-rmot05c-evidence/candidates.json"}
json.dump(M, open(mp, 'w'), indent=1); json.dump(con, open(EV + '/construction/construction.json', 'w'), indent=1, default=str)
print('evidence files', sum(len(f) for _, _, f in os.walk(EV)))
