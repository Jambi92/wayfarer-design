# sa6_layer_pack.py WORKDIR LAYERDIR : package the RP6 creator-state corrective layers (sa6_pd2_fit.py outputs) as deltas against the base correctives.
#   Every corrective key of a state set (families keyed by bone + parent-frame axis + sample angle; pose keys by pose name) is either IDENTICAL to the
#   base-configuration key (stored as a reference to the base key name) or stored in full (changed or new key = the state layer).  The tool rebuilds every
#   state set from base + layer and asserts exact equality of all index and delta arrays before writing.
#   Output: EV6/SA_RP6_creator_layers_v001.json (per state: base config, convergence, fit summary, key table) + SA_RP6_creator_layers_v001.npz.
import sys, os, glob, json, numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); import sa6_common as C
WD, LD = sys.argv[1:3]; ST = 'RP6 RIG PILOT / NOT FROZEN'
def table(path):
    j = json.load(open(path)); z = np.load(path.replace('.json', '.npz')); t = {}
    for f in j['families']:
        for k in f['keys']: t['F|%s|%s|%+.4f' % (f['bone'], ','.join('%.6f' % a for a in f['axis_parent_frame']), k['sample_deg'])] = (k['name'], z[k['name'] + '_idx'], z[k['name'] + '_d'])
    for p in j.get('pose_keys', []): t['P|' + p['pose']] = (p['name'], z[p['name'] + '_idx'], z[p['name'] + '_d'])
    return j, t
base = {c: table(WD + '/CF_%s.json' % c) for c in 'MF'}
out = dict(status=ST, name='SA_RP6_creator_layers_v001', semantics='corrective(state, pose) = base corrective set of the state base configuration with the layer keys '
           'replacing / adding to it (sa6_correctives semantics: families interpolated over driver angle, pose keys gated by their driver set).  Between accepted '
           'states the creator blends layer deltas with the creator weights (SA_RP6_PD1_PD2_interfaces_v001.md).', base_correctives={c: 'SA_RP6_correctives_%s_v001.npz' % c for c in 'MF'},
           states={}); arr = {}
for p in sorted(glob.glob(LD + '/CF_state_*.json')):
    j, t = table(p); nm = j['state']; cfg = j['base_config']; bt = base[cfg][1]; keys = {}
    for sk, (kn, idx, d) in t.items():
        if sk in bt and np.array_equal(bt[sk][1], idx) and np.array_equal(bt[sk][2], d): keys[sk] = dict(source='base', base_key=bt[sk][0])
        else:
            an = '%s/%s' % (nm, kn); arr[an + '_idx'] = idx.astype(np.int32); arr[an + '_d'] = d.astype(np.float32)
            keys[sk] = dict(source='layer', kind='changed' if sk in bt else 'new', array=an, n_vertices=int(len(idx)), max_delta_cm=float(np.linalg.norm(d, axis=1).max()) if len(idx) else 0.0)
    dropped = sorted(set(bt) - set(t)); assert not dropped, (nm, dropped[:5])
    for sk, v in keys.items():                       # rebuild check
        a_idx, a_d = (bt[sk][1], bt[sk][2]) if v['source'] == 'base' else (arr[v['array'] + '_idx'], arr[v['array'] + '_d'])
        assert np.array_equal(a_idx, t[sk][1]) and np.array_equal(a_d.astype(np.float32), t[sk][2].astype(np.float32)), (nm, sk)
    lg = j['fit_log']; rounds = sorted({e['round'] for e in lg})
    out['states'][nm] = dict(base_config=cfg, converged=j['converged'], fit_rounds=len(rounds), flips_entering_per_round=[sum(e['flips_before'] for e in lg if e['round'] == r) for r in rounds],
                             layer_keys_changed=sum(v['source'] == 'layer' and v['kind'] == 'changed' for v in keys.values()), layer_keys_new=sum(v['source'] == 'layer' and v['kind'] == 'new' for v in keys.values()),
                             base_keys_reused=sum(v['source'] == 'base' for v in keys.values()), source_sha256=C.sha(p.replace('.json', '.npz')), keys=keys)
np.savez_compressed(C.EV6 + '/SA_RP6_creator_layers_v001.npz', **arr); json.dump(out, open(C.EV6 + '/SA_RP6_creator_layers_v001.json', 'w'), indent=1)
for nm, s in out['states'].items(): print('%-8s %s conv %s rounds %d entering %s changed %d new %d reused %d' % (nm, s['base_config'], s['converged'], s['fit_rounds'], s['flips_entering_per_round'], s['layer_keys_changed'], s['layer_keys_new'], s['base_keys_reused']))
print('npz MB', os.path.getsize(C.EV6 + '/SA_RP6_creator_layers_v001.npz') / 1e6)
