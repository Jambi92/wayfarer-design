# RAC RM-OT-05B: copy the evidence into the repository (sheets, blind sets / keys / scores, validator reruns, tables, the final arch recipe,
# the search history) and register the candidate R-6 assets in reviews/reference-assets (PENDING AUTHOR; W2 bodies stay as provenance).
import os, sys, json, shutil, hashlib, glob
S = '/tmp/claude-0/-home-claude-wayfarer-design/19af7d50-3b61-5fda-9fe0-7a30770fb334/scratchpad'; A = S + '/rmot05b'; R = '/home/claude/wayfarer-design'
EV = R + '/reviews/rac-rmot05b-evidence'; os.makedirs(EV + '/sheets', exist_ok=True); os.makedirs(EV + '/blind', exist_ok=True); os.makedirs(EV + '/validators', exist_ok=True)
os.makedirs(EV + '/search', exist_ok=True); os.makedirs(EV + '/construction', exist_ok=True)
for f in glob.glob(A + '/sheets/*.jpg'): shutil.copy(f, EV + '/sheets/')
for f in glob.glob(A + '/blind/*'): shutil.copy(f, EV + '/blind/')
for f in ('w2c.json', 'w2d.json', 'w2c_registry.json', 'w2d_registry.json', 'w2c_jbw.json', 'w2d_joints.json', 'jbw_new.json', 'jsec_new.json', 'tables.json', 'w2c_eval.log', 'w2d_eval.log', 'contour.txt', 'arm_clearance.txt'):
    shutil.copy(A + '/eval/' + f, EV + '/validators/' + f)
shutil.copy(A + '/cfg_B2.json', EV + '/cfg_final.json'); shutil.copy(A + '/cfg_B1.json', EV + '/search/cfg_B1.json')
for f in sorted(glob.glob(A + '/surf_s*.json')): shutil.copy(f, EV + '/search/' + os.path.basename(f))
for f in glob.glob(A + '/prev/blindq_*.jpg') + glob.glob(A + '/prev/blindq_*.key.json') + glob.glob(A + '/prev/p_s*_*.jpg'): shutil.copy(f, EV + '/search/' + os.path.basename(f))
GR = ['GR5B198', 'GR5B208', 'GR5B218', 'GR5B229', 'GR5B239', 'GR5BN', 'GR5BB', 'B_GR-BODY-06', 'B_GR-LOW']
GO = ['GO5B208', 'GO5B218', 'GO5B229', 'GO5BREF', 'GO5B239', 'GO5B251', 'GO5BN', 'GO5BB', 'B_GOR-BODY-06', 'B_GOR-BODY-16']
ROLE = {'GR5B198': 'min 198', 'GR5B208': '208', 'GR5B218': 'central reference 218', 'GR5B229': '229', 'GR5B239': 'max 239', 'GR5BN': 'Narrow frame 218', 'GR5BB': 'Broad frame 218',
        'B_GR-BODY-06': 'low muscle (0 / 0.5) on GR5B218', 'B_GR-LOW': 'low muscle + low fat (0.25 / 0.25) on GR5B218',
        'GO5B208': 'min 208', 'GO5B218': '218', 'GO5B229': '229 nominal design reference', 'GO5BREF': '230.9 ARM realization', 'GO5B239': '239', 'GO5B251': '251 current world-validation upper end (not permanent)',
        'GO5BN': 'Narrow frame 230.9', 'GO5BB': 'Broad frame 230.9', 'B_GOR-BODY-06': 'low muscle (0 / 0.5) on GO5BREF', 'B_GOR-BODY-16': 'GOR-BODY-16 low muscle + low fat (0.25 / 0.25) on GO5BREF'}
mp = R + '/reviews/reference-assets/manifest.json'; M = json.load(open(mp)); con = {}
for n in GR + GO:
    d = S + ('/w2c/b/' if n.startswith(('GR', 'B_GR')) else '/w2d/b/') + n
    src = d + '/%s_r6.npz' % n; dst = R + '/reviews/reference-assets/r6/%s_r6.npz' % n; shutil.copy(src, dst)
    for suf in ('_w2c.json', '_w2d.json', '_meas.json'):
        if os.path.exists(d + '/' + n + suf): shutil.copy(d + '/' + n + suf, EV + '/construction/' + n + suf)
    rec = json.load(open(d + '/' + n + ('_w2c.json' if n.startswith(('GR', 'B_GR')) else '_w2d.json'))); con[n] = rec
    st = json.load(open(d + '/%s_meas.json' % n))['combined']['stature']
    M['assets'][n] = {"race": "Grask" if n.startswith(('GR', 'B_GR')) else "Gorrund", "role": ROLE[n] + ' (RM-OT-05B architecture + surface-anatomy candidate)',
                      "accepted": "PENDING AUTHOR (RM-OT-05B gate: not passed; NEEDS ART / BASE-SURFACE ESCALATION)", "stature_r6": st, "file": "r6/%s_r6.npz" % n,
                      "sha256": hashlib.sha256(open(dst, 'rb').read()).hexdigest(), "scratch_source": "$S" + d[len(S):],
                      "recipe": "reviews/rac-rmot05b-evidence/cfg_final.json (arch + surface) on the accepted W2C / W2D route"}
json.dump(M, open(mp, 'w'), indent=1); json.dump(con, open(EV + '/construction/construction.json', 'w'), indent=1, default=str)
T = {}
for n in sorted(os.listdir(S + '/w2c/b')) + sorted(os.listdir(S + '/w2d/b')):
    if n.startswith('B_'):
        d = S + ('/w2c/b/' if n.startswith('B_GR') else '/w2d/b/') + n; f = [x for x in os.listdir(d) if x.endswith(('_w2c.json', '_w2d.json'))]
        if f: T[n] = json.load(open(d + '/' + f[0])); shutil.copy(d + '/' + n + '_meas.json', EV + '/construction/' + n + '_meas.json')
json.dump(T, open(EV + '/construction/transport.json', 'w'), indent=1, default=str)
print('evidence files', sum(len(f) for _, _, f in os.walk(EV)))
