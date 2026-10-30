# cg_density_sum.py OUT.json : RP4 Cogling compact-scale density diagnosis (order 9424c72 §6) -- v005 realizations at 76 / 91 c1 / 91 c2 / 107 cm from
# du_density.py (edge length as % of stature: mean / p95; contract ceilings face 0.25, hands / feet 0.3; local support = mean edge / digit or palm length).
# Context: the frozen Pipkin v005 realization at 91 cm (PK91-NAT) -- same v005 topology, different body -- so Cogling-specific density effects (long fingers,
# small head) read against a compact body of the same height. Thumb-base palm sub-zone and digit station loops are listed separately (§6 'critical zone').
import sys, json
OUT = sys.argv[1]; W = '/tmp/claude-0/rt/cg/dens'; P = '/tmp/claude-0/rt/pk/dens'
B = [('CG76H-NAT', W), ('CGJ7', W), ('CGF91-NAT', W), ('CG107-NAT', W), ('PK91-NAT (context)', P)]
res = {}
for b, d in B:
    x = json.load(open('%s/%s_fam_density.json' % (d, b.split(' ')[0])))
    res[b] = dict(stature_cm=x['stature_cm'], subzones={k: dict(mean_pct=v['mean_pct'], p95_pct=v['p95_pct'], mean_mm=v['mean_mm'], p95_mm=v['p95_mm'], ceiling_pct=v['ceiling_pct'],
                                                               mean_within=v['mean_within_ceiling'], local_support={kk: v[kk] for kk in v if kk.startswith('mean_edge_over')})
                                                          for k, v in x['subzones'].items()},
                  digit_lengths=x.get('digit_lengths'), face_rings=x.get('face_rings'))
json.dump(res, open(OUT, 'w'), indent=1)
keys = list(res['CGJ7']['subzones'])
print('%-24s' % 'subzone mean / p95 %stat', ' '.join('%-17s' % b[:17] for b, _ in B))
for k in keys:
    print('%-24s' % k, ' '.join('%-17s' % ('%.3f / %.3f%s' % (res[b]['subzones'][k]['mean_pct'], res[b]['subzones'][k]['p95_pct'], '' if res[b]['subzones'][k]['mean_within'] else '*')) for b, _ in B))
for k in keys:
    ls = {b: res[b]['subzones'][k]['local_support'] for b, _ in B if res[b]['subzones'][k]['local_support']}
    if ls: print('local support', k, ls)
