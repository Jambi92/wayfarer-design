# RAC RM-OT-05A: copy the evidence into the repository (sheets, blind sets / keys / scores, validator reruns, tables, the final arch recipe,
# the search history) and register the candidate R-6 assets in reviews/reference-assets (PENDING AUTHOR; W2 bodies stay as provenance).
import os, sys, json, shutil, hashlib, glob
S = '/tmp/claude-0/-home-claude-wayfarer-design/19af7d50-3b61-5fda-9fe0-7a30770fb334/scratchpad'; A = S + '/rmot05a'; R = '/home/claude/wayfarer-design'
EV = R + '/reviews/rac-rmot05a-evidence'; os.makedirs(EV + '/sheets', exist_ok=True); os.makedirs(EV + '/blind', exist_ok=True); os.makedirs(EV + '/validators', exist_ok=True)
os.makedirs(EV + '/search', exist_ok=True); os.makedirs(EV + '/construction', exist_ok=True)
for f in glob.glob(A + '/sheets/*.jpg'): shutil.copy(f, EV + '/sheets/')
for f in glob.glob(A + '/blind/*'): shutil.copy(f, EV + '/blind/')
for f in ('w2c.json', 'w2d.json', 'w2c_registry.json', 'w2d_registry.json', 'w2c_jbw.json', 'w2d_joints.json', 'jbw_new.json', 'jsec_new.json', 'tables.json', 'w2c_eval.log', 'w2d_eval.log', 'contour.txt', 'arm_clearance.txt'):
    shutil.copy(A + '/eval/' + f, EV + '/validators/' + f)
shutil.copy(A + '/arch_R7.json', EV + '/arch_final.json')
for f in sorted(glob.glob(A + '/arch_v*.json') + glob.glob(A + '/arch_R*.json')): shutil.copy(f, EV + '/search/' + os.path.basename(f))
for f in glob.glob(A + '/prev/blindq_*.jpg') + glob.glob(A + '/prev/blindq_*.key.json'): shutil.copy(f, EV + '/search/' + os.path.basename(f))
GR = ['GRA198', 'GRA208', 'GRA218', 'GRA229', 'GRA239', 'GRAN', 'GRAB', 'GRA218-LOW', 'GRA-LOW']
GO = ['GOA208', 'GOA218', 'GOA229', 'GOAREF', 'GOA239', 'GOA251', 'GOAN', 'GOAB', 'GOAREF-LOW', 'GOA-L16']
ROLE = {'GRA198': 'min 198', 'GRA208': '208', 'GRA218': 'central reference 218', 'GRA229': '229', 'GRA239': 'max 239', 'GRAN': 'Narrow frame 218', 'GRAB': 'Broad frame 218',
        'GRA218-LOW': 'low muscle (0 / 0.5) on GRA218', 'GRA-LOW': 'low muscle + low fat (0.25 / 0.25) on GRA218',
        'GOA208': 'min 208', 'GOA218': '218', 'GOA229': '229 nominal design reference', 'GOAREF': '230.9 ARM realization', 'GOA239': '239', 'GOA251': '251 current world-validation upper end (not permanent)',
        'GOAN': 'Narrow frame 230.9', 'GOAB': 'Broad frame 230.9', 'GOAREF-LOW': 'low muscle (0 / 0.5) on GOAREF', 'GOA-L16': 'GOR-BODY-16 low muscle + low fat (0.25 / 0.25) on GOAREF'}
mp = R + '/reviews/reference-assets/manifest.json'; M = json.load(open(mp)); con = {}
for n in GR + GO:
    d = S + ('/w2c/b/' if n.startswith('GR') else '/w2d/b/') + n
    src = d + '/%s_r6.npz' % n; dst = R + '/reviews/reference-assets/r6/%s_r6.npz' % n; shutil.copy(src, dst)
    for suf in ('_w2c.json', '_w2d.json', '_meas.json'):
        if os.path.exists(d + '/' + n + suf): shutil.copy(d + '/' + n + suf, EV + '/construction/' + n + suf)
    rec = json.load(open(d + '/' + n + ('_w2c.json' if n.startswith('GR') else '_w2d.json'))); con[n] = rec
    st = json.load(open(d + '/%s_meas.json' % n))['combined']['stature']
    M['assets'][n] = {"race": "Grask" if n.startswith('GR') else "Gorrund", "role": ROLE[n] + ' (RM-OT-05A architecture-rebuild candidate)',
                      "accepted": "PENDING AUTHOR (RM-OT-05A gate: CONSTRAIN / FAIL; not accepted)", "stature_r6": st, "file": "r6/%s_r6.npz" % n,
                      "sha256": hashlib.sha256(open(dst, 'rb').read()).hexdigest(), "scratch_source": "$S" + d[len(S):],
                      "recipe": "reviews/rac-rmot05a-evidence/arch_final.json (" + ("GR" if n.startswith('GR') else "GO") + ") on the accepted W2C / W2D route"}
json.dump(M, open(mp, 'w'), indent=1); json.dump(con, open(EV + '/construction/construction.json', 'w'), indent=1, default=str)
T = {}
for n in sorted(os.listdir(S + '/w2c/b')) + sorted(os.listdir(S + '/w2d/b')):
    if n.startswith('A_'):
        d = S + ('/w2c/b/' if n.startswith('A_GR') else '/w2d/b/') + n; f = [x for x in os.listdir(d) if x.endswith(('_w2c.json', '_w2d.json'))]
        if f: T[n] = json.load(open(d + '/' + f[0])); shutil.copy(d + '/' + n + '_meas.json', EV + '/construction/' + n + '_meas.json')
json.dump(T, open(EV + '/construction/transport.json', 'w'), indent=1, default=str)
print('evidence files', sum(len(f) for _, _, f in os.walk(EV)))
