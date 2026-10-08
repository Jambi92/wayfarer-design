# RAC W2E (Sagekin W2) body builder. Routes = the accepted Marchfolk W2A boundary route rule applied to the accepted Sagekin W1 build:
#   >= 159 cm: generator height macro re-solved from the accepted SG build (build_variant.py, resolve_stature) - same Sagekin targets;
#   < 159 cm: native short-adult regional route (native_short.py) from SG's accepted base macro (0.537109375; the W2A
#             'base_height_macro' rule), one length factor, girth / hands / feet / head on the generator adult allometry slopes.
# Frames = the accepted human (Marchfolk W2A1) multi-domain frame writes, set B Broad / set C Narrow. Composition = generator muscle /
# weight macros on the same skeleton construction (as W2A). Named validators = Sagekin target-strength variants (see JOBS).
# No uniform scaling anywhere.   Usage: python3 sg_build.py JOBSET   (JOBSET: stature | mf | named | sg04 | frames | comp)
import sys, os, json, subprocess
from concurrent.futures import ThreadPoolExecutor
T = '/home/claude/wayfarer-design/tools/rac/w1'; S = '/tmp/claude-0/-home-claude-wayfarer-design/19af7d50-3b61-5fda-9fe0-7a30770fb334/scratchpad'
W = S + '/w2e'; REF = S + '/w1f/final/MF-M-R_rest.npz'; SGB = S + '/w1f/final/SG_build.json'; MFB = S + '/w1f/final/MF-M-R_build.json'
SGCFG = json.load(open(T + '/cfg/SG.json'))
BROAD = {"bone_scales": {"LR:clavicle": [1, 1.05, 1], "spine_01": [1.05, 1, 1.025], "spine_02": [1.05, 1, 1.025], "spine_03": [1.05, 1, 1.025], "pelvis": [1.05, 1, 1.025],
         "LR:upperarm": [1.035, 1, 1.035], "LR:lowerarm": [1.035, 1, 1.035], "LR:thigh": [1.035, 1, 1.035], "LR:calf": [1.035, 1, 1.035]},
         "targets": {"measure-wrist-circ-incr": 0.15, "measure-ankle-circ-incr": 0.15}}
NARROW = {"bone_scales": {"LR:clavicle": [1, 0.95, 1], "spine_01": [0.95, 1, 0.975], "spine_02": [0.95, 1, 0.975], "spine_03": [0.95, 1, 0.975], "pelvis": [0.95, 1, 0.975],
          "LR:upperarm": [0.985, 1, 0.985], "LR:lowerarm": [0.985, 1, 0.985], "LR:thigh": [0.985, 1, 0.985], "LR:calf": [0.985, 1, 0.985]},
          "targets": {"measure-wrist-circ-decr": 0.1, "measure-ankle-circ-decr": 0.1}}
LIMB = ("measure-upperleg-height-incr", "measure-lowerleg-height-incr", "measure-lowerarm-length-incr", "LR:hand-fingers-length-incr")
def sh(cmd, log):
    with open(W + '/logs/%s.log' % log, 'w') as f: return subprocess.run(cmd, cwd=T, stdout=f, stderr=subprocess.STDOUT).returncode
def variant(base, ov, out, nid):
    os.makedirs(out, exist_ok=True); json.dump(ov, open(out + '/%s.ov.json' % nid, 'w'))
    rc = sh(['python3', 'build_variant.py', base, out + '/%s.ov.json' % nid, out, nid], nid)
    if rc == 0: sh(['python3', 'run_candidate.py', out, nid, REF], nid + '.rc')
    print('BUILT' if rc == 0 else 'FAILED', nid, flush=True)
def native(cfg, out, nid):
    os.makedirs(out, exist_ok=True); p = out + '/%s.cfg.json' % nid; json.dump(cfg, open(p, 'w'))
    rc = sh(['python3', 'native_short.py', p, out], nid)
    if rc == 0: sh(['python3', 'run_candidate.py', out, nid + '-NAT', REF], nid + '.rc')
    print('BUILT' if rc == 0 else 'FAILED', nid, flush=True)
def scaled_targets(f, keys=None):
    t = dict(SGCFG["targets"])
    return {k: (round(v * f, 4) if (keys is None or k in keys) else v) for k, v in t.items()}
def jobs(which):
    J = []
    if which == 'stature':
        J.append((native, (dict(SGCFG, stature=152.0, id="SG152", base_height_macro=0.537109375), W + '/st', 'SG152')))
        for h in (163, 173, 181, 190, 203, 208): J.append((variant, (SGB, {"stature": float(h), "resolve_stature": True}, W + '/st', 'SG%d' % h)))
    if which == 'mf':
        for h in (163, 178, 181): J.append((variant, (MFB, {"stature": float(h), "resolve_stature": True}, W + '/mf', 'MF%d' % h)))
    if which == 'named':
        # SG-04 long-limbed near the boundary: Sagekin limb / hand targets at twice the accepted strength; SG-09 long torso: nape-to-waist
        # decrease (torso shortening) replaced by an equal increase; SG-10 Marchfolk-overlap edge: every Sagekin target at half strength.
        J.append((variant, (SGB, {"targets": scaled_targets(2.0, LIMB), "resolve_stature": True, "stature": 178.0}, W + '/nm', 'SG04')))
        J.append((variant, (SGB, {"targets": {"measure-napetowaist-dist-decr": None, "measure-napetowaist-dist-incr": 0.15}, "resolve_stature": True, "stature": 178.0}, W + '/nm', 'SG09')))
        J.append((variant, (SGB, {"targets": scaled_targets(0.5), "resolve_stature": True, "stature": 178.0}, W + '/nm', 'SG10')))
    if which == 'sg04':
        # SG-04 strength probes: x1.5 / x1.75 of the Sagekin limb / hand targets (x2.0 = first build, SG04)
        for f in (1.5, 1.75): J.append((variant, (SGB, {"targets": scaled_targets(f, LIMB), "resolve_stature": True, "stature": 178.0}, W + '/nm', 'SG04x%d' % round(f * 100))))
    if which == 'frames':
        J.append((variant, (SGB, BROAD, W + '/fr', 'SGB178'))); J.append((variant, (SGB, NARROW, W + '/fr', 'SGN178')))
        J.append((variant, (W + '/st/SG208_build.json', NARROW, W + '/fr', 'SGN208'))); J.append((variant, (W + '/st/SG208_build.json', BROAD, W + '/fr', 'SGB208')))
        J.append((variant, (W + '/st/SG152-NAT_build.json', BROAD, W + '/fr', 'SGB152'))); J.append((variant, (W + '/st/SG152-NAT_build.json', NARROW, W + '/fr', 'SGN152')))
    if which == 'comp':
        for nm, m, w in (("LOWMUS", 0, 0.5), ("HIMUS", 1, 0.5), ("HIFAT", 0.5, 1), ("HIBOTH", 1, 1), ("LOW", 0.25, 0.25), ("MIN", 0, 0)):
            J.append((variant, (W + '/st/SG173_build.json', {"muscle": m, "weight": w}, W + '/comp', 'SG173-' + nm)))
        for nm, src, m, w in (("SG06", "SGB178", 1, 0.5), ("SG07", "SGB178", 0.5, 1), ("SG08", "SGN178", 1, 0.5)):
            J.append((variant, (W + '/fr/%s_build.json' % src, {"muscle": m, "weight": w}, W + '/comp', nm)))
    return J
if __name__ == '__main__':
    J = jobs(sys.argv[1])
    with ThreadPoolExecutor(2) as ex: list(ex.map(lambda j: j[0](*j[1]), J))
    print('DONE', sys.argv[1])
