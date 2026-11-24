# sa6_bake_beforeafter.py NAME BODYDIR UNBAKED_DIR FINAL_DIR : before / after at the SAME body, pose and fraction (offline bake validation order 8e3b7b4d §1).
#   Every failing (pose, fraction) of the unbaked suite (UNBAKED_DIR: EV 34x4, GT 50x4, SW full sweep; unbaked = empty K = packaged blend v004) is re-evaluated
#   on the final baked artifact FINAL_DIR/BK_<NAME> at exactly that fraction, with the same evaluator and ownership rules:
#   anatomical poses -> sa6_blend.evaluate (columns lbs | base | packaged blend | bake), special gates -> sa6_bake_gates.run.
#   'before' = packaged blend v004 (the unbaked production), 'after' = baked.  -> FINAL_DIR/BA_<NAME>.json
import sys, os, json, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('RP6_LAYERS', 'SA_RP6_creator_layers_v005.json' if os.environ.get('RP6_RIG') == 'v002' else 'SA_RP6_creator_layers_v004.json')   # rig v002: layers v005
import sa6_blend as BL, sa6_bake_gates as GTS
nm, BD, UD, FD = sys.argv[1:5]; b = json.load(open(os.path.join(BD, 'bodies.json')))['bodies'][nm]; art = os.path.join(FD, 'BK_%s.json' % nm); t0 = time.time()
def bad(r): return bool(r['rig_flips'] or r['rig_pen'] or r['rig_tears'] or not r['volume_ok'])
anat, gate = {}, {}
ev = json.load(open(os.path.join(UD, 'EV_%s.json' % nm)))
for pn, rows in ev['poses'].items():
    for fr, r in rows.items():
        if bad(r['bake']): anat.setdefault(pn, set()).add(float(fr))
for pn, v in json.load(open(os.path.join(UD, 'SW_%s.json' % nm)))['poses'].items():
    for g in v['gate_failures']: anat.setdefault(pn, set()).add(float(g['frac']))
for pn, rows in json.load(open(os.path.join(UD, 'GT_%s.json' % nm)))['poses'].items():
    for fr, r in rows.items():
        if bad(r['bake']): gate.setdefault(pn, set()).add(float(fr))
K = ('rig_flips', 'rig_pen', 'rig_tears', 'dV_cm3', 'volume_ok', 'regions')
out = dict(status='RP6 RIG PILOT / NOT FROZEN', name=nm, unbaked='packaged blend %s (empty K)' % os.environ['RP6_LAYERS'].rsplit('_', 1)[-1].replace('.json', ''), baked=os.path.relpath(art, FD), rows=[])
for pn, fs in anat.items():
    r = BL.evaluate(nm, b, BD, sorted(fs), [pn], bake=art)
    for fr, row in r['poses'][pn].items():
        out['rows'].append(dict(kind='anatomical', pose=pn, frac=float(fr), before={k: row['prod'][k] for k in K}, after={k: row['bake'][k] for k in K}, lbs_rig_flips=row['lbs']['rig_flips'],
                                before_fails=bad(row['prod']), after_fails=bad(row['bake'])))
for pn, fs in gate.items():
    os.environ['GATES_ONLY'] = pn; os.environ.pop('GATES_SHARD', None); os.environ.pop('GATES_TRANSITIONS', None); GTS.FRACS = tuple(sorted(fs, reverse=True))
    r = GTS.run(nm, BD, FD)
    for fr, row in r['poses'][pn].items():
        bef = row.get('prod', row['bake'])   # prod is recorded only where K != 0 on the pose; elsewhere baked == packaged blend exactly
        out['rows'].append(dict(kind='special_gate', pose=pn, frac=float(fr), before={k: bef[k] for k in K}, after={k: row['bake'][k] for k in K}, lbs_rig_flips=row['lbs']['rig_flips'],
                                k_max_cm=row['k_max_cm'], before_fails=bad(bef), after_fails=bad(row['bake'])))
out['n'] = len(out['rows']); out['before_failing'] = sum(r['before_fails'] for r in out['rows']); out['after_failing'] = sum(r['after_fails'] for r in out['rows'])
out['seconds'] = round(time.time() - t0, 1)
json.dump(out, open(os.path.join(FD, 'BA_%s.json' % nm), 'w'), indent=1)
print(nm, 'BEFORE/AFTER rows', out['n'], 'failing before', out['before_failing'], 'after', out['after_failing'], flush=True)
