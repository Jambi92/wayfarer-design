# hv_defs.py OUTDIR [TAG ...] : Halvren bounded body / face source-authoring order (2026-10-29) -- source-authoring definitions of the central mixed-
# expression candidates HB1 / HB2 / HB3 (body) and HF1 / HF2 / HF3 (craniofacial), and the override files for every requested tag
# (tag = HBn, HBnHFm, or HV0HFm for a face on the current HVC1 body). Existing MPFB targets / bone scales only (no custom field, no mesh blending).
# The same definition applies to c1 (HVC1 record + overrides) and c2 (MF-F-R base + overrides): no configuration-specific ancestry architecture.
# Design (HALVREN_V1 Part 2 / 3; order §5 / §11): every system takes its own mixed relationship -- not one elf's package scaled, not a scalar blend:
#   axial   ribcage a little shallower AND a little narrower than Marchfolk (relational, not Fenn's compact torso / Vael's depth / Aelari's verticality)
#   shoulder modest clavicle shortening + modest neck lengthening (neither Aelari's long neck nor Vael's broad neck integration)
#   arm     modest total elongation with forearm emphasis kept; long-bone shaft gracility well short of Fenn; joint (wrist) coupled
#   leg     modest total elongation, femur and lower leg both (balance kept; no Fenn lower-leg copy); knee / ankle coupled to the shafts
#   hand    longer fingers + slightly longer hand on a palm narrowed less than Fenn and not broadened like Vael; finger diameter slightly reduced
#   foot    slightly longer and slightly narrower, a little deeper (ankle-foot transition); humanoid
#   pelvis  HELD (order §16): no pelvic target / bone scale
#   face    cranium a little less deep and slightly taller (oval tendency), forehead slightly taller, cheekbone placement raised a little with a small
#           zygomatic increase (not gaunt), chin slightly longer with slightly lighter mandibular body (jaw width untouched); nose / mouth / eye size UNCHANGED
#           (anti-beauty: no eye enlargement, no nose reduction, no jaw narrowing)
import sys, os, json
STR = {'1': 0.6, '2': 1.0, '3': 1.5}                    # HB1 / HB2 / HB3 strengths of the one shared body definition
STRF = {'1': 0.85, '2': 1.1, '3': 1.45}                   # HF1 / HF2 / HF3 strengths of the one shared face definition (HF1 must still depart in several regions)
BODY = {'targets': {'torso-scale-depth-decr': 0.05, 'measure-underbust-circ-decr': 0.25, 'measure-napetowaist-dist-decr': 0.05, 'measure-shoulder-dist-decr': 0.15,
                    'measure-neck-height-incr': 0.15, 'measure-upperarm-length-incr': 0.08, 'measure-lowerarm-length-incr': 0.15, 'measure-upperleg-height-incr': 0.08,
                    'measure-lowerleg-height-incr': 0.15, 'measure-wrist-circ-decr': 0.2, 'measure-ankle-circ-decr': 0.15,
                    'LR:hand-fingers-length-incr': 0.18, 'LR:hand-scale-incr': 0.06, 'LR:foot-scale-incr': 0.1, 'LR:foot-scale-depth-incr': 0.05},
        'bone_scales': {'LR:upperarm': [0.98, 1.0, 0.98], 'LR:lowerarm': [0.98, 1.0, 0.98], 'LR:thigh': [0.985, 1.0, 0.985], 'LR:calf': [0.985, 1.0, 0.985]}}
FACE = {'targets': {'head-back-scale-depth-decr': 0.25, 'head-oval': 0.08, 'forehead-scale-vert-incr': 0.06, 'forehead-temple-decr': 0.15,
                    'LR:cheek-trans-up': 0.35, 'LR:cheek-volume-decr': 0.1, 'chin-height-incr': 0.12, 'LR:eye-trans-out': 0.1}}
HVC1_T = ['measure-napetowaist-dist-decr', 'measure-lowerarm-length-incr', 'measure-lowerleg-height-incr', 'torso-scale-depth-decr', 'LR:hand-fingers-length-incr', 'measure-wrist-circ-decr', 'measure-ankle-circ-decr']
HVC1_V = dict(zip(HVC1_T, [0.1, 0.12, 0.12, 0.05, 0.12, 0.15, 0.1]))
def sc(v, s): return [round(1 + (x - 1) * s, 5) for x in v] if isinstance(v, list) else round(v * s, 5)
def overrides(tag):
    t = {}; b = {}
    if tag.startswith('HB'):
        s = STR[tag[2]]; t.update({k: sc(v, s) for k, v in BODY['targets'].items()}); b.update({k: sc(v, s) for k, v in BODY['bone_scales'].items()})
    else:                                                # HV0: the current HVC1 body design
        t.update(HVC1_V)
    for k in HVC1_T: t.setdefault(k, None)               # c1 base is the HVC1 record: an HVC1 key not in the new design is removed
    if 'HF' in tag: s = STRF[tag[tag.index('HF') + 2]]; t.update({k: sc(v, s) for k, v in FACE['targets'].items()})
    return dict(targets=t, bone_scales=b, stature=178.0, resolve_stature=True)
def c2(ov): o = json.loads(json.dumps(ov)); o['targets'] = {k: v for k, v in o['targets'].items() if v is not None}; return o   # c2 base MF-F-R has no HVC1 keys
if __name__ == '__main__':
    O = sys.argv[1]; os.makedirs(O, exist_ok=True)
    json.dump(dict(version='HVDEF1', strengths=dict(body=STR, face=STRF), body=BODY, face=FACE, hvc1_targets=HVC1_V, pelvis='held (no pelvic target or bone scale)',
                   note='HB / HF strengths scale the single shared definition; c1 = HVC1 record + overrides, c2 = MF-F-R base + the same overrides; stature re-solved to 178 cm'),
              open(os.path.join(O, 'HV_source_definitions.json'), 'w'), indent=1)
    for tag in sys.argv[2:]:
        ov = overrides(tag); json.dump(ov, open(os.path.join(O, 'c1_%s.json' % tag), 'w'), indent=1); json.dump(c2(ov), open(os.path.join(O, 'c2_%s.json' % tag), 'w'), indent=1)
    print('defs', sys.argv[2:])
