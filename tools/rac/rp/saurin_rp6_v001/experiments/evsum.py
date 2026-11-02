import json,sys
sys.path.insert(0,'/home/claude/wayfarer-design/tools/rac/rp/saurin_rp6_v001');import sa6_fit as FT
for c in sys.argv[1:]:
    e=json.load(open('/tmp/claude-0/rp6/ev_%s.json'%c))['poses'];bad=[];vol=[];cls={}
    for pn,r in e.items():
        nr=pn in FT.NONREAL; corr=max(v['corrected_flips'] for v in r['fractions'].values()); pen=max(v['corrected_new_penetration_vertices'] for v in r['fractions'].values())
        dv=r['body_volume_change_cm3']['corrected']; k=r['classification'].split(' (')[0]; cls[k]=cls.get(k,0)+1
        if not nr and (corr or pen): bad.append((pn,corr,pen))
        isjaw='jaw' in pn
        if not nr and not isjaw and abs(dv)>100: vol.append((pn,dv))
        if r.get('rigid_vertex_drift',{}).get('max_cm',0)>0.01 and not nr: bad.append((pn,'rigid drift',r['rigid_vertex_drift']['max_cm']))
    vm=max(abs(r['body_volume_change_cm3']['corrected']) for pn,r in e.items() if pn not in FT.NONREAL and 'jaw' not in pn)
    print(c,'poses',len(e),'classes',cls,'\n  folds/pen fails',bad,'\n  volume >100',vol,'\n  max |dV| (realisable, non-jaw) %.1f'%vm)
