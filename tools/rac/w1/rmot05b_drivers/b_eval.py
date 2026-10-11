# RAC RM-OT-05B validator rerun: the accepted W2C (Grask) and W2D (Gorrund) evaluation chains with the rebuilt candidates in the race slots
# (same evaluators, same specs, same accepted comparators; the W2 bodies stay in the registry only as provenance rows "<id>-W2").
# Steps: am_win module -> jbw.py (W2C stature-scaled slab joints) and w2c1 joint_section.py (W2D exact-plane joints) on every new body ->
# registries -> w2c_eval.py / w2d_eval.py.   Usage: python3 a_eval.py OUTDIR
import os, sys, json, subprocess, shutil
D = os.path.dirname(os.path.abspath(__file__)); W1 = os.path.dirname(D); R = '/home/claude/wayfarer-design'
S = '/tmp/claude-0/-home-claude-wayfarer-design/19af7d50-3b61-5fda-9fe0-7a30770fb334/scratchpad'; O = sys.argv[1]; os.makedirs(O, exist_ok=True)
EV_C = R + '/reviews/rac-w2c-gr-evidence'; EV_D = R + '/reviews/rac-w2d-go-evidence'
GRN = {"GR198": "GR5B198", "GR208": "GR5B208", "GR218": "GR5B218", "GR229": "GR5B229", "GR239": "GR5B239", "GRN5": "GR5BN", "GRB2": "GR5BB"}
GRT = {k: 'B_' + k for k in ('GR-BODY-10', 'GR-BODY-11', 'GR-BODY-12', 'GR-BODY-13', 'GR-BODY-14', 'GR-BODY-17', 'GR-BODY-18')}
GRC = {k: 'B_' + k for k in ('GR-BODY-15', 'GR-BODY-16', 'GR-BODY-06', 'GR-BODY-07', 'GR-BODY-08', 'GR-BODY-09', 'GR-LOW')}
GOT = {k: 'B_' + k for k in ('GOD14_9', 'GOD14_9_218', 'GOLP218')}
GOC = {k: 'B_' + k for k in ['GOR-BODY-06', 'GOR-BODY-07', 'GOR-BODY-08', 'GOR-BODY-09', 'GOR-BODY-10', 'GOR-BODY-11'] + ['GOR-BODY-%s_%s' % (c, h) for h in ('208', '218') for c in ('06', '07', '09', '10', '16')] + ['GOR-BODY-16']}
GON = {"GO208": "GO5B208", "GO218": "GO5B218", "GO229": "GO5B229", "GOREF": "GO5BREF", "GO239": "GO5B239", "GO251": "GO5B251", "GON5": "GO5BN", "GOB7": "GO5BB", "GON5_218": "GO5BN218", "GOB7_218": "GO5BB218"}
MOD = O + '/am'; subprocess.run(['sh', W1 + '/w1r_drivers/make_am_win.sh', MOD], check=True)
gp = lambda n: S + '/w2c/b/%s/%s' % (n, n); op = lambda n: S + '/w2d/b/%s/%s' % (n, n)
def run(args, log):
    with open(O + '/' + log, 'w') as f: subprocess.run(args, stdout=f, stderr=subprocess.STDOUT, cwd=W1, check=True, env=dict(os.environ, PYTHONPATH=W1))
if not os.path.exists(O + '/jbw_new.json'):
    run(['python3', W1 + '/w1r_drivers/jbw.py', MOD, O + '/jbw_new.json'] + [gp(n) for n in list(GRN.values()) + list(GRT.values())], 'jbw.log')
if not os.path.exists(O + '/jsec_new.json'):
    run(['python3', W1 + '/w2c1_drivers/joint_section.py', MOD, O + '/jsec_new.json'] + [gp(n) for n in list(GRN.values()) + list(GRT.values())] + [op(n) for n in list(GON.values()) + list(GOT.values())], 'jsec.log')
# ---- W2C (Grask) ----
reg = json.load(open(EV_C + '/registry.json')); JB = json.load(open(EV_C + '/joint_breadths.json')); JB.update(json.load(open(O + '/jbw_new.json')))
for k in [k for k in reg if k in ('GRN2', 'GRN3', 'GRN4', 'GRN', 'GRB')]: reg.pop(k)       # W2C search frames (not accepted bodies): not transported
for k, n in list(GRN.items()) + list(GRT.items()):
    if k in reg: reg[k + '-W2'] = dict(reg[k]); reg[k + '-W2']['grask'] = False      # provenance row
    reg[k] = {"meas": gp(n), "skp": S + '/w2c/b/%s/skp_%s' % (n, n), "skp_id": n, "jbw": n, "grask": True}
for k, n in GRC.items():
    if k in reg: reg[k + '-W2'] = dict(reg[k]); reg[k + '-W2'].pop('grask', None)
    reg[k] = {"meas": gp(n)}
json.dump(reg, open(O + '/w2c_registry.json', 'w'), indent=1); json.dump(JB, open(O + '/w2c_jbw.json', 'w'), indent=1)
env = dict(os.environ, W2C_SPEC=EV_C + '/spec.json', W2C_FRAMES='GRN5,GRB2', EVDIR=O + '/ev_c')
with open(O + '/w2c_eval.log', 'w') as f:
    subprocess.run(['python3', W1 + '/w2c_drivers/w2c_eval.py', O + '/w2c_registry.json', O + '/w2c_jbw.json', O + '/w2c.json'], env=env, stdout=f, stderr=subprocess.STDOUT, cwd=W1)
# ---- W2D (Gorrund) ----
reg = json.load(open(EV_D + '/registry.json')); JS = json.load(open(R + '/reviews/rac-w2c1-joint-evidence/joint_sections.json')); JS.update(json.load(open(EV_D + '/joint_sections.json'))); new = json.load(open(O + '/jsec_new.json'))
for k in [k for k in reg if k in ('GON', 'GONF', 'GOB', 'GOBF', 'GON3', 'GON4', 'GOB3', 'GOB4', 'GOB5', 'GOB6', 'GON3_218', 'GON4_218')]: reg.pop(k)   # W2D search frames: not transported
for k, n in list(GON.items()) + list(GOT.items()):
    if k in reg: reg[k + '-W2'] = dict(reg[k]); reg[k + '-W2']['gorrund'] = False
    reg[k] = {"meas": op(n), "skp": S + '/w2d/b/%s/skp_%s' % (n, n), "skp_id": n, "joint": n, "gorrund": True, "dir": S + '/w2d/b/' + n}
    for t in ('0.0', '0.5', '1.0'):       # gn3.checks reads <dir>/skp_<registry key>/t*/<key>_meas.json: alias the candidate's own reading
        dd = S + '/w2d/b/%s/skp_%s/t%s' % (n, k, t); os.makedirs(dd, exist_ok=True)
        shutil.copy(S + '/w2d/b/%s/skp_%s/t%s/%s_meas.json' % (n, n, t, n), dd + '/%s_meas.json' % k)
    shutil.copy(op(n) + '_meas.json', S + '/w2d/b/%s/%s_meas.json' % (n, k))     # go_search.ev reads <dir>/<key>_meas.json
for k, n in list(GRN.items()) + list(GRT.items()):
    if k in reg:
        reg[k + '-W2'] = dict(reg[k]); reg[k] = {"meas": gp(n), "skp": S + '/w2c/b/%s/skp_%s' % (n, n), "skp_id": n, "joint": n}
for k, n in GRC.items():
    if k in reg: reg[k + '-W2'] = dict(reg[k]); reg[k] = {"meas": gp(n)}
for k, n in GOC.items():
    if k in reg: reg[k + '-W2'] = dict(reg[k]); reg[k + '-W2']['gorrund'] = False
    reg[k] = {"meas": op(n), "skp": None, "joint": None, "gorrund": True, "comp": True, "dir": S + '/w2d/b/' + n}
    shutil.copy(op(n) + '_meas.json', S + '/w2d/b/%s/%s_meas.json' % (n, k))
JS.update(new)
json.dump(reg, open(O + '/w2d_registry.json', 'w'), indent=1); json.dump(JS, open(O + '/w2d_joints.json', 'w'), indent=1)
with open(O + '/w2d_eval.log', 'w') as f:
    subprocess.run(['python3', W1 + '/w2d_drivers/w2d_eval.py', O + '/w2d_registry.json', EV_D + '/spec.json', O + '/w2d.json', O + '/w2d_joints.json'], stdout=f, stderr=subprocess.STDOUT, cwd=W1)
print(open(O + '/w2c_eval.log').read()[-3000:]); print(open(O + '/w2d_eval.log').read()[-3000:])
