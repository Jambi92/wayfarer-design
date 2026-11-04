# sa6_package.py WORKDIR : assemble the RP6 rig-pilot evidence package into reviews/rac-rp6-evidence/saurin/rig_pilot (order a407015 §20).
#   WORKDIR holds the run outputs: W_{M,F}.npz, CF_{M,F}.json/.npz, ev_{M,F}.json (sa6_eval), wa.json (weight audit), ca.json (corrective audit),
#   pd2.json, rb_{M,F}.json (Blender read-back), SA_{M,F}_REF_RP6_rigpilot_v001.blend.  Writes the named package files + the manifest (sha256 of every file).
import sys, os, json, shutil, hashlib, numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); import sa6_common as C, sa6_pose as SP, sa6_fit as FT
WD = sys.argv[1]; EV = C.EV6; ST = 'RP6 RIG PILOT / NOT FROZEN'
def sha(p): return hashlib.sha256(open(p, 'rb').read()).hexdigest()
for c in 'MF':
    shutil.copyfile(WD + '/W_%s.npz' % c, EV + '/SA_RP6_weights_%s_v001.npz' % c)
    shutil.copyfile(WD + '/CF_%s.npz' % c, EV + '/SA_RP6_correctives_%s_v001.npz' % c)
# correctives JSON (both configurations, without the bulky fit log -> fit log kept separately)
cj = {}
for c in 'MF':
    j = json.load(open(WD + '/CF_%s.json' % c)); cj[c] = j
    json.dump(dict(status=ST, configuration=c, fit_log=j['fit_log']), open(EV + '/SA_RP6_corrective_fit_log_%s_v001.json' % c, 'w'), indent=0)
json.dump(dict(status=ST, name='SA_RP6_correctives_v001', semantics=cj['M']['method'], arrays={c: 'SA_RP6_correctives_%s_v001.npz (keys <name>_idx int32 vertex ids, <name>_d float32 rest-space deltas cm)' % c for c in 'MF'},
               configurations={c: dict(weights='SA_RP6_weights_%s_v001.npz' % c, families=cj[c]['families']) for c in 'MF'}), open(EV + '/SA_RP6_correctives_v001.json', 'w'), indent=1)
# pose suite definitions
R = {c: SP.Rig(c) for c in 'MF'}; suite = {}
for c in 'MF':
    PS = FT.pose_set(R[c]); PS['jaw_open_20_rp5lit'] = R[c].suite('rp5')['jaw_open_20']; out = {}
    for k, v in PS.items():
        kind = 'gate' if k.startswith('gate:') else ('rp5-literal' if k.endswith('_rp5lit') else ('rp5-exact (non-sagittal: identical in both sign conventions)' if (k + '_rp5lit') not in PS else 'anatomical-sign variant of the RP5 pose'))
        out[k] = dict(kind=kind, entries=[dict(bone=b, pivot_cm=np.round(np.asarray(p, float), 4).tolist(), axis=np.round(np.asarray(a, float) / np.linalg.norm(a), 6).tolist(), deg=round(float(dg), 4)) for b, p, a, dg in v])
    suite[c] = out
json.dump(dict(status=ST, name='SA_RP6_pose_suite_v001', units='cm / deg; rotation right-handed about axis through pivot, applied in list order, each to the bone and its subtree (sa6_pose.Rig.pose)',
               required_suite='34 RP5 poses (sa_deform4 definitions re-targeted to RP6 bones) evaluated with the EXACT RP5 signs (non-sagittal names + *_rp5lit) and with anatomical sagittal signs (unsuffixed sagittal names)',
               sign_finding='the RP5 sagittal definitions assume +y posterior: as written, jaw_open_20 closes the jaw, neck_flex / lower_axial_flex / shoulder_flex / hip_flex extend, elbow_* / knee_90 hyper-extend, ankle_dorsi20 plantar-flexes (frame: +y anterior, rostrum at +y)',
               fractions_evaluated=[0.25, 0.5, 0.75, 1.0], configurations=suite), open(EV + '/SA_RP6_pose_suite_v001.json', 'w'), indent=1)
# deformation audit
ev = {('c1' if c == 'M' else 'c2'): json.load(open(WD + '/ev_%s.json' % c)) for c in 'MF'}
aud = dict(status=ST, name='SA_RP6_deformation_audit_v001', configurations=ev, weight_audit=json.load(open(WD + '/wa.json')), corrective_audit=json.load(open(WD + '/ca.json')),
           pd2=json.load(open(WD + '/pd2.json')), rig_prep={c: json.load(open(EV + '/SA_RP6_rig_prep_%s_v001.json' % c)) for c in 'MF'},
           blender_readback={c: json.load(open(WD + '/rb_%s.json' % c)) for c in 'MF'}, tail_count_study=json.load(open(EV + '/SA_RP6_tail_count_study.json')))
json.dump(aud, open(EV + '/SA_RP6_deformation_audit_v001.json', 'w'), indent=1)
for c in 'MF':
    src = WD + '/SA_%s_REF_RP6_rigpilot_v001.blend.xz' % c
    if os.path.exists(src): shutil.copyfile(src, EV + '/SA_%s_REF_RP6_rigpilot_v001.blend.xz' % c)
files = sorted(os.path.relpath(os.path.join(r, f), EV) for r, ds, fs in os.walk(EV) for f in fs if not os.path.relpath(r, EV).startswith('wip') and f != 'SA_RP6_rig_manifest_v001.json')   # incl. renders/
man = dict(status=ST, name='SA_RP6_rig_manifest_v001', race='Saurin', stage='RP6 production rig / skin-weighting pilot', order='reviews/chatgpt-rac-rp6-saurin-production-rig-skin-weighting-pilot-order.md (a407015)',
           frozen_inputs={k: v for k, v in C.FROZEN.items()} | {'topology_sha256': C.TOPO}, tools='tools/rac/rp/saurin_rp6_v001/', files={f: dict(sha256=sha(os.path.join(EV, f)), bytes=os.path.getsize(os.path.join(EV, f))) for f in files},
           blend_files={c: dict(container='SA_%s_REF_RP6_rigpilot_v001.blend.xz' % c, blend_sha256=json.load(open(WD + '/rb_%s.json' % c))['sha256'], blend_bytes=os.path.getsize(WD + '/SA_%s_REF_RP6_rigpilot_v001.blend' % c) if os.path.exists(WD + '/SA_%s_REF_RP6_rigpilot_v001.blend' % c) else None) for c in 'MF'})
json.dump(man, open(EV + '/SA_RP6_rig_manifest_v001.json', 'w'), indent=1); print('files', len(files))
