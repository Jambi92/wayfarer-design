import json,sys
sys.path.insert(0,'/home/claude/wayfarer-design/tools/rac/rp/saurin_rp6_v001');import sa6_fit as FT
for c in 'MF':
    e=json.load(open('/tmp/claude-0/rp6/ev_%s.json'%c))['poses'];w=[]
    for pn,r in e.items():
        if pn in FT.NONREAL or pn=='jaw_open_20_rp5lit': continue
        for b,m in r.get('joint_metrics',{}).items():
            s,l=m['stretch_corrected'],m['stretch_lbs']
            if s[3]>max(1.8,l[3]*1.25) or s[0]<min(0.5,l[0]*0.75) or s[2]>max(1.5,l[2]*1.15) or s[1]<min(0.6,l[1]*0.85): w.append((pn,b,'corr',s,'lbs',l))
    print(c,len(w))
    for x in sorted(w,key=lambda t:-t[3][3])[:25]: print('  ',x)
