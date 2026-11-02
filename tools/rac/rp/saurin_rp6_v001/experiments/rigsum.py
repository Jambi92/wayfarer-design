import json,sys
sys.path.insert(0,'/home/claude/wayfarer-design/tools/rac/rp/saurin_rp6_v001');import sa6_fit as FT
for c in 'MF':
    e=json.load(open('/tmp/claude-0/rp6/ev_%s.json'%c))['poses']
    lm=[(pn,r['landmarks']['max_rigid_cm']) for pn,r in e.items() if r['landmarks']['max_rigid_cm']>0.05 and pn not in FT.NONREAL]
    hd=[(pn,{k:v for k,v in r['gate_metrics'].items() if 'rigid' in k and v>0.05}) for pn,r in e.items() if any('rigid' in k and v>0.05 for k,v in r['gate_metrics'].items())]
    print(c,'landmark rigid >0.05:',lm,'\n   head rigid >0.05:',hd)
