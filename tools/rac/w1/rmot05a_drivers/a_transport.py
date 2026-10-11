# RAC RM-OT-05A §10 transport: rebuild every other accepted W2C / W2D Grask / Gorrund body (frames at 218, named valid extremes, composition
# states) with the final arch sculpt on the same route and parameters as its W2 record. New name = 'A_' + old name. Composition states are
# rebuilt on the corresponding RM-OT-05A skeleton. Writes the old -> new map.   Usage: python3 a_transport.py ARCH.json GROUP
import os, sys, json, subprocess, numpy as np
D = os.path.dirname(os.path.abspath(__file__)); W1 = os.path.dirname(D)
for p in (W1, W1 + '/w2c_drivers', W1 + '/w2d_drivers', W1 + '/w1g_drivers', W1 + '/w1h_drivers', W1 + '/w1i_drivers'): sys.path.insert(0, p)
S = '/tmp/claude-0/-home-claude-wayfarer-design/19af7d50-3b61-5fda-9fe0-7a30770fb334/scratchpad'
A = json.load(open(sys.argv[1])); G = sys.argv[2]
W1L = {"spine_01": None, "LR:clavicle": [1.0, 0.98, 1.0], "pelvis": [0.925, 1.0, 1.0], "LR:thigh": [1.20, 1.0, 1.20]}
SKMAP = {'GOREF': 'GOAREF', 'GO208': 'GOA208', 'GO218': 'GOA218', 'GO229': 'GOA229', 'GR218R': 'GRA218', 'GRB2': 'GRAB', 'GRN5': 'GRAN'}
GO_FULL = ['GON5_218', 'GOB7_218', 'GOD14_9', 'GOD14_9_218', 'GOLP218']
GO_COMP = ['GOR-BODY-06', 'GOR-BODY-07', 'GOR-BODY-08', 'GOR-BODY-09', 'GOR-BODY-10', 'GOR-BODY-11'] + ['GOR-BODY-%s_%s' % (c, h) for h in ('208', '218') for c in ('06', '07', '09', '10', '16')]
GR_FULL = ['GR-BODY-10', 'GR-BODY-11', 'GR-BODY-12', 'GR-BODY-13', 'GR-BODY-14', 'GR-BODY-17', 'GR-BODY-18']
GR_COMP = ['GR-BODY-15', 'GR-BODY-16']
GR_W1L = ['GR-BODY-06', 'GR-BODY-07', 'GR-BODY-08', 'GR-BODY-09', 'GR-LOW']
def run(args): r = subprocess.run(['python3'] + args, capture_output=True, text=True, cwd=W1); print(r.stdout[-300:], r.stderr[-800:], flush=True)
if G == 'gofull':
    import go_body as OB
    for n in GO_FULL:
        rec = json.load(open(S + '/w2d/b/%s/%s_w2d.json' % (n, n))); OB.build('A_' + n, rec['height_macro'], rec['frame'], rec['extra_targets'], arch=A['GO'])
if G == 'gocomp':
    for n in GO_COMP:
        rec = json.load(open(S + '/w2d/b/%s/%s_w2d.json' % (n, n))); run([W1 + '/w2d_drivers/go_comp.py', 'A_' + n, SKMAP[rec['skeleton']], str(rec['muscle']), str(rec['weight'])])
if G == 'grfull':
    import gr_body as GB
    for n in GR_FULL:
        rec = json.load(open(S + '/w2c/b/%s/%s_w2c.json' % (n, n)))
        eb = {k: v for k, v in rec['bone_scales'].items() if k not in W1L or v != W1L[k]}
        GB.build('A_' + n, rec['stature_target'], eb or None, rec['extra_targets'] or None, arch=A['GR'])
if G == 'grcomp':
    for n in GR_COMP:
        rec = json.load(open(S + '/w2c/b/%s/%s_w2c.json' % (n, n))); run([W1 + '/w2c_drivers/gr_comp.py', 'A_' + n, SKMAP[rec['skeleton']], str(rec['muscle']), str(rec['weight'])])
    for n in GR_W1L:
        m = json.loads(str(np.load(S + '/w1l/comp_w1l/%s_r6.npz' % n, allow_pickle=True)['meta'])); c = m['tissue_donor'][0].split('-C')[1]
        run([W1 + '/w2c_drivers/gr_comp.py', 'A_' + n, 'GRA218', str(int(c[:3]) / 100), str(int(c[3:]) / 100)])
