# sa6_v2_init.py WD : initial corrective sets for the rig v002 refit (order 07a3f24c §1-§2).
#   base c1 / c2: the accepted v001 base set (SA_RP6_correctives_v002.json) WITHOUT the shoulder families (bone upperarm_* / clavicle_*) and without
#   pose keys driven by those bones (the pivot, weights and girdle changed: their shapes no longer apply), PLUS the v002 elbow muscle layer
#   (sa6_muscle.py, on the base body).  -> WD/INIT_{M,F}.json/.npz, WD/W_{M,F}.npz (= rig v002 weights).
#   creator states (STATES env, default all 19): the accepted v004 state set (rig v001 package) with the same stripping, plus the muscle layer
#   evaluated on the state's rest body -> WD/init_layer/CF_state_<STATE>.json/.npz (sa6_pd2_fit INIT_LAYER).
#   Nothing else is changed: every other family / key is carried over as the starting point and re-verified by the fits.
import sys, os, json, shutil, numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
assert os.environ.get('RP6_RIG') == 'v002'
import sa6_common as C, sa6_pose as SP, sa6_correctives as CC, sa6_muscle as MU
WD = sys.argv[1]; os.makedirs(WD + '/init_layer', exist_ok=True); os.environ.setdefault('RP6_WD', WD)
SH = ('upperarm_', 'clavicle_')
def strip(src, R):
    c = CC.Correctives(R); n = dict(families_removed=[], pose_keys_removed=[])
    for k, f in src.F.items():
        if f['bone'].startswith(SH): n['families_removed'].append(f['bone']); continue
        c.F[k] = f
    for k, pk in src.PK.items():
        if any(b.startswith(SH) for b, _, _ in pk['drivers']): n['pose_keys_removed'].append(k); continue
        c.PK[k] = pk
    return MU.add(c, R), n
def load_v001(kind, cfg_or_state):
    """the accepted rig-v001 set from the v001 package (read straight from the json / npz; rig only used for the container)"""
    js = json.load(open(C.EV6 + '/SA_RP6_correctives_v002.json')); out = []
    if kind == 'base':
        j = js['configurations'][cfg_or_state]; z = np.load(C.EV6 + '/' + js['arrays'][cfg_or_state])
        arr = lambda k: (z[k['name'] + '_idx'].astype(np.int64), z[k['name'] + '_d'].astype(np.float64)); return j['families'], j['pose_keys'], arr
    L = json.load(open(C.EV6 + '/SA_RP6_creator_layers_v004.json')); s = L['states'][cfg_or_state]; zb = np.load(C.EV6 + '/' + js['arrays'][s['base_config']]); zl = np.load(C.EV6 + '/' + L['arrays'])
    def arr(k):
        if k['source'] == 'base': return zb[k['base_key'] + '_idx'].astype(np.int64), zb[k['base_key'] + '_d'].astype(np.float64)
        return zl[k['array'] + '_idx'].astype(np.int64), zl[k['array'] + '_d'].astype(np.float64)
    return s['families'], s['pose_keys'], arr
def build(R, fams, pks, arr):
    c = CC.Correctives(R)
    for f in fams:
        c.F[CC.fam_key(f['bone'], f['axis_parent_frame'])] = dict(bone=f['bone'], axis=f['axis_parent_frame'], pivot=f['pivot_rest_cm'], samples=[k['sample_deg'] for k in f['keys']], D=[arr(k) for k in f['keys']])
    for p in pks:
        idx, d = arr(p); c.PK[p['pose']] = dict(drivers=[(x['bone'], x['axis_parent_frame'], x['sample_deg']) for x in p['drivers']], idx=idx, d=d)
        if all('width_deg' in x for x in p['drivers']): c.PK[p['pose']]['width'] = [x['width_deg'] for x in p['drivers']]
    return c
rec = {}
for cfg in ('M', 'F'):
    shutil.copy(C.w_path(cfg), WD + '/W_%s.npz' % cfg); R = SP.Rig(cfg, WD + '/W_%s.npz' % cfg)
    c, n = strip(build(R, *load_v001('base', cfg)), R)
    c.save(WD + '/INIT_%s.json' % cfg, dict(status='RP6 RIG PILOT / NOT FROZEN', rig_version='v002', source='SA_RP6_correctives_v002.json (rig v001) stripped + muscle layer', **n))
    rec[cfg] = dict(n, families=len(c.F), pose_keys=len(c.PK)); print(cfg, rec[cfg], flush=True)
import sa6_pd2_fit as PF
for st in [s for s in os.environ.get('STATES', ','.join(sorted(json.load(open(C.EV6 + '/SA_RP6_creator_layers_v004.json'))['states']))).split(',') if s]:
    R, cfg = PF.state_rig(st); c, n = strip(build(R, *load_v001('state', st)), R)
    c.save(WD + '/init_layer/CF_state_%s.json' % st, dict(status='RP6 RIG PILOT / NOT FROZEN', rig_version='v002', state=st, base_config=cfg, source='SA_RP6_creator_layers_v004 state (rig v001) stripped + muscle layer on the state body', **n))
    rec[st] = dict(n, families=len(c.F), pose_keys=len(c.PK)); print(st, {k: (len(v) if isinstance(v, list) else v) for k, v in rec[st].items()}, flush=True)
json.dump(rec, open(WD + '/INIT_record.json', 'w'), indent=1)
