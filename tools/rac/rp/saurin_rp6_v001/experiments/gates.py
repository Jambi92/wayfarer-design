import json,sys
sys.path.insert(0,'/home/claude/wayfarer-design/tools/rac/rp/saurin_rp6_v001');import sa6_fit as FT
for c in sys.argv[1:]:
    e=json.load(open('/tmp/claude-0/rp6/ev_%s.json'%c))['poses'];fail=[];vm=0;tm=0;em=0
    for pn,r in e.items():
        if pn in FT.NONREAL or pn=='jaw_open_20_rp5lit': continue
        fx=r['fractions'].values();corr=max(v['corrected_flips'] for v in fx);pen=max(v['corrected_new_penetration_vertices'] for v in fx)
        te=max(v['corrected_tear_edges'] for v in fx);el=max(v['corrected_max_elongation_cm'] for v in fx);dv=r['body_volume_change_cm3']['corrected']
        lmr=r['landmarks']['max_rigid_cm'];hr=max([v for k,v in r['gate_metrics'].items() if 'rigid' in k]+[0])
        if 'jaw' not in pn: vm=max(vm,abs(dv))
        tm=max(tm,te);em=max(em,el)
        bad=[]
        if corr: bad.append('folds %d'%corr)
        if pen: bad.append('pen %d'%pen)
        if te: bad.append('tears %d (%.2f cm)'%(te,el))
        if 'jaw' not in pn and abs(dv)>100: bad.append('dV %.0f'%dv)
        if lmr>0.05: bad.append('landmark %.3f'%lmr)
        if hr>0.05: bad.append('head %.3f'%hr)
        if bad: fail.append((pn,bad))
    print(c,'gated poses',sum(1 for p in e if p not in FT.NONREAL and p!='jaw_open_20_rp5lit'),'| FAILS',len(fail),fail,'| max|dV| %.1f max tears %d max elong %.2f'%(vm,tm,em))
