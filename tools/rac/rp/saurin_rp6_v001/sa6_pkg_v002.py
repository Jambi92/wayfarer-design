# sa6_pkg_v002.py WORKDIR LAYERDIR : corrective package v002 (corrective-layer validation order 3e76b509).
#   Packaging defects found while reconstructing the correctives from the committed package (v001):
#     (1) SA_RP6_correctives_v001.json lists the families only; the base pose-space keys (c1 7, c2 7: 'PK...' arrays present in the npz) had no
#         driver metadata in the JSON, so the base corrective set could not be rebuilt from the package alone (the .blend files carry them);
#     (2) SA_RP6_creator_layers_v001.json stores each key as base reference or array, but not the family / pose-key metadata (bone, parent-frame axis,
#         pivot, sample angle, pose-key drivers) needed to rebuild a state set without the fitted CF_state files.
#   v002 adds that metadata; arrays are unchanged (v001 npz files are reused byte-for-byte: SA_RP6_correctives_{M,F}_v001.npz,
#   SA_RP6_creator_layers_v001.npz).  The v001 JSON files stay as accepted evidence.
#   Outputs (EV6): SA_RP6_correctives_v002.json, SA_RP6_creator_layers_v002.json.  Rebuild + identity check: sa6_layer_harness.py.
import sys, os, glob, json, numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); import sa6_common as C
WD, LD = sys.argv[1:3]; ST = 'RP6 RIG PILOT / NOT FROZEN'
def famkey(bone, axis, s): return 'F|%s|%s|%+.4f' % (bone, ','.join('%.6f' % a for a in axis), s)
cj = {c: json.load(open(WD + '/CF_%s.json' % c)) for c in 'MF'}
out = dict(status=ST, name='SA_RP6_correctives_v002', supersedes='SA_RP6_correctives_v001.json (metadata only; arrays unchanged)', semantics=cj['M']['method'],
           arrays={c: 'SA_RP6_correctives_%s_v001.npz' % c for c in 'MF'},
           array_sha256={c: C.sha(C.EV6 + '/SA_RP6_correctives_%s_v001.npz' % c) for c in 'MF'},
           configurations={c: dict(weights='SA_RP6_weights_%s_v001.npz' % c, families=cj[c]['families'], pose_keys=cj[c]['pose_keys']) for c in 'MF'})
json.dump(out, open(C.EV6 + '/SA_RP6_correctives_v002.json', 'w'), indent=1)
base_name = {}
for c in 'MF':
    t = {}
    for f in cj[c]['families']:
        for k in f['keys']: t[famkey(f['bone'], f['axis_parent_frame'], k['sample_deg'])] = k['name']
    for p in cj[c]['pose_keys']: t['P|' + p['pose']] = p['name']
    base_name[c] = t
L1 = json.load(open(C.EV6 + '/SA_RP6_creator_layers_v001.json'))
lay = dict(status=ST, name='SA_RP6_creator_layers_v002', supersedes='SA_RP6_creator_layers_v001.json (metadata only; arrays unchanged)',
           arrays='SA_RP6_creator_layers_v001.npz', array_sha256=C.sha(C.EV6 + '/SA_RP6_creator_layers_v001.npz'), semantics=L1['semantics'],
           base_correctives='SA_RP6_correctives_v002.json', states={})
for p in sorted(glob.glob(LD + '/CF_state_*.json')):
    j = json.load(open(p)); nm = j['state']; cfg = j['base_config']; v1 = L1['states'][nm]['keys']; fams = []; pks = []
    for f in j['families']:
        keys = []
        for k in f['keys']:
            sk = famkey(f['bone'], f['axis_parent_frame'], k['sample_deg']); e = v1[sk]
            keys.append(dict(sample_deg=k['sample_deg'], **({'source': 'base', 'base_key': e['base_key']} if e['source'] == 'base' else {'source': 'layer', 'kind': e['kind'], 'array': e['array']})))
        fams.append(dict(bone=f['bone'], axis_parent_frame=f['axis_parent_frame'], pivot_rest_cm=f['pivot_rest_cm'], keys=keys))
    for pk in j.get('pose_keys', []):
        e = v1['P|' + pk['pose']]
        pks.append(dict(pose=pk['pose'], drivers=pk['drivers'], **({'source': 'base', 'base_key': e['base_key']} if e['source'] == 'base' else {'source': 'layer', 'kind': e['kind'], 'array': e['array']})))
    s1 = L1['states'][nm]
    lay['states'][nm] = dict(base_config=cfg, converged=s1['converged'], layer_keys_changed=s1['layer_keys_changed'], layer_keys_new=s1['layer_keys_new'],
                             base_keys_reused=s1['base_keys_reused'], source_sha256=s1['source_sha256'], families=fams, pose_keys=pks)
json.dump(lay, open(C.EV6 + '/SA_RP6_creator_layers_v002.json', 'w'), indent=1)
print('v002 written:', {c: (len(out['configurations'][c]['families']), len(out['configurations'][c]['pose_keys'])) for c in 'MF'}, len(lay['states']), 'states')
