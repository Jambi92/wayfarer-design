# RAC W1f driver script AS RUN (scratch paths are the session's working directories; kept for provenance of the AD-G14 construction)
import json, sys; sys.path.insert(0,'.'); sys.path.insert(0,'/home/claude/wayfarer-design/tools/rac/w1')
import gn2, profile_bump as PB
x = json.loads(sys.argv[1]); name = sys.argv[2]
B, sc, r = gn2.build(x, name); rows = gn2.checks(name)
print('H %.2f' % r['r6']['stature'])
for y in rows:
    if (y['cand']=='GO' or y.get('b')=='GO') and y['result'] not in ('PASS','REPORT','NOT RUN'):
        print(y['result'], '|', y['check'], {t: (round(v['va'],4) if v['va'] is not None else None) for t,v in y['by_t'].items()}, y['op'], y['vb'])
sk = json.load(open(gn2.D + '/skp_%s/%s_skp.json' % (name, name)))
R = sk['by_t']['0.5']['ratio']; G = gn2.GRr['0.5']
print('torso %.4f>GR %.4f leg %.4f<GR %.4f arm %.4f<GR %.4f' % (R['torso_share'], G['torso_share'], R['leg_share'], G['leg_share'], R['arm_share'], G['arm_share']))
print('chest lead env %.4f lean %.4f buttock %.4f' % (PB.chest_lead(gn2.D+'/%s_r6.npz'%name), PB.chest_lead(gn2.D+'/%s-LEAN_r6.npz'%name), PB.buttock_lead(gn2.D+'/%s_r6.npz'%name)))
