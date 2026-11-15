# sa6_pkg_v003.py LAYERDIR NODEDIR : creator-state corrective layer package v003 (corrective-layer validation order 3e76b509).
#   Revision vs v002 (found by the blend coverage, SA_RP6_blend_eval v001):
#     (1) the state layers were fitted at 100 % / 50 % of each pose only; at 25 % / 75 % a few rig-owned folds / volume misses remained on some endpoints
#         (e.g. BRD, B-T80).  v003 state layers = the v002 layers refined by the same solver at 100 / 75 / 50 / 25 % (sa6_pd2_fit.py FRACS=1.0,0.75,0.5,0.25,
#         INIT_LAYER = the accepted layers);
#     (2) the linear blend is not sufficient between the base and an extreme state: optional CREATOR KEYS per state (sa6_node_fit.py; semantics in
#         sa6_layer_harness.py).
#   Every key is stored either as a reference to the identical base key (source 'base') or as its own array (source 'layer'); creator keys are arrays.
#   Outputs (EV6): SA_RP6_creator_layers_v003.json + SA_RP6_creator_layers_v003.npz.  Base correctives unchanged (SA_RP6_correctives_v002.json).
import sys, os, glob, json, numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); import sa6_common as C
LD, ND = sys.argv[1:3]; ST = 'RP6 RIG PILOT / NOT FROZEN'; VER = os.environ.get('PKG_VER', 'v003')   # v004: + creator keys at 0.25 / 0.75 (NODEDIR = all nodes)
base = json.load(open(C.EV6 + '/SA_RP6_correctives_v002.json')); arr = {}; stats = {}
def famkey(bone, axis, s): return '%s|%s|%+.4f' % (bone, ','.join('%.6f' % a for a in axis), s)
bkeys = {}
for c in 'MF':
    z = np.load(C.EV6 + '/' + base['arrays'][c]); t = {}
    for f in base['configurations'][c]['families']:
        for k in f['keys']: t[famkey(f['bone'], f['axis_parent_frame'], k['sample_deg'])] = (k['name'], z[k['name'] + '_idx'], z[k['name'] + '_d'])
    for p in base['configurations'][c]['pose_keys']: t['P|' + p['pose']] = (p['name'], z[p['name'] + '_idx'], z[p['name'] + '_d'])
    bkeys[c] = t
def entry(c, sk, aname, idx, d, st):
    b = bkeys[c].get(sk)
    if b is not None and np.array_equal(b[1], idx) and np.array_equal(b[2], d): st['reused'] += 1; return dict(source='base', base_key=b[0])
    arr[aname + '_idx'] = idx; arr[aname + '_d'] = d; st['changed' if b is not None else 'new'] += 1
    return dict(source='layer', kind='changed' if b is not None else 'new', array=aname)
def pack(js, z, c, pre, st):
    fams, pks = [], []
    for f in js['families']:
        keys = []
        for k in f['keys']:
            keys.append(dict(sample_deg=k['sample_deg'], **entry(c, famkey(f['bone'], f['axis_parent_frame'], k['sample_deg']), pre + k['name'], z[k['name'] + '_idx'], z[k['name'] + '_d'], st)))
        fams.append(dict(bone=f['bone'], axis_parent_frame=f['axis_parent_frame'], pivot_rest_cm=f['pivot_rest_cm'], keys=keys))
    for p in js.get('pose_keys', []):
        pks.append(dict(pose=p['pose'], drivers=p['drivers'], **entry(c, 'P|' + p['pose'], pre + p['name'], z[p['name'] + '_idx'], z[p['name'] + '_d'], st)))
    return fams, pks
lay = dict(status=ST, name='SA_RP6_creator_layers_' + VER, supersedes='SA_RP6_creator_layers_v002.json' if VER == 'v003' else 'SA_RP6_creator_layers_v003.json', arrays='SA_RP6_creator_layers_%s.npz' % VER,
           base_correctives='SA_RP6_correctives_v002.json', semantics=open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'sa6_layer_harness.py')).read().split('import os')[0],
           states={})
for p in sorted(glob.glob(LD + '/CF_state_*.json')):
    js = json.load(open(p)); nm = js['state']; c = js['base_config']; z = np.load(p.replace('.json', '.npz')); st = dict(reused=0, changed=0, new=0)
    fams, pks = pack(js, z, c, 'S_%s__' % nm, st)
    ent = dict(base_config=c, converged=js['converged'], source_sha256=C.sha(p.replace('.json', '.npz')), layer_keys_changed=st['changed'], layer_keys_new=st['new'],
               base_keys_reused=st['reused'], families=fams, pose_keys=pks, creator_keys=[])
    for q in sorted(glob.glob(ND + '/CK_%s@*.json' % nm)):
        if 'placeholder' in json.load(open(q)): raise SystemExit('node fit still running: ' + q)
        kj = json.load(open(q))
        if not kj['converged']: raise SystemExit('node fit not converged: ' + q)
        kz = np.load(q.replace('.json', '.npz')); sk = dict(reused=0, changed=0, new=0); bkeys_save = bkeys[c]; bkeys[c] = {}   # creator keys never reference base keys
        kf, kp = pack(kj, kz, c, 'K_%s@%.2f__' % (nm, kj['node_weight']), sk); bkeys[c] = bkeys_save
        ent['creator_keys'].append(dict(node_weight=kj['node_weight'], body=kj['body'], converged=kj['converged'], composite=kj.get('composite', []), source_sha256=C.sha(q.replace('.json', '.npz')),
                                        n_keys=sk['new'], families=kf, pose_keys=kp))
    lay['states'][nm] = ent; stats[nm] = (st, [k['node_weight'] for k in ent['creator_keys']])
np.savez_compressed(C.EV6 + '/SA_RP6_creator_layers_%s.npz' % VER, **{k: (v.astype(np.int32) if k.endswith('_idx') else v.astype(np.float32)) for k, v in arr.items()})
lay['array_sha256'] = C.sha(C.EV6 + '/SA_RP6_creator_layers_%s.npz' % VER); json.dump(lay, open(C.EV6 + '/SA_RP6_creator_layers_%s.json' % VER, 'w'), indent=1)
for k, v in stats.items(): print(k, v)
