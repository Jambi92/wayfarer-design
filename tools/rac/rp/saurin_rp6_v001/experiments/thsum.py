import json,sys
sys.path.insert(0,'/home/claude/wayfarer-design/tools/rac/rp/saurin_rp6_v001');import sa6_fit as FT
for c in 'MF':
    e=json.load(open('/tmp/claude-0/rp6/ev_%s.json'%c));th=e['thresholds'];e=e['poses'];out=[];vr=[];st=[]
    for pn,r in e.items():
        if pn in FT.NONREAL or pn=='jaw_open_20_rp5lit': continue
        for b,m in r.get('joint_metrics',{}).items():
            v=m['volume_ratio_corrected'];vr.append(v);s=m['stretch_corrected'];st+= [s[0],s[3]]
            if not(th['volume_ratio'][0]<=v<=th['volume_ratio'][1]) or s[0]<th['stretch'][0] or s[3]>th['stretch'][1]: out.append((pn,b,v,s[0],s[3],'lbs',m['volume_ratio_lbs'],m['stretch_lbs'][0],m['stretch_lbs'][3]))
    print(c,'thresholds',th,'| joint vol ratio range %.3f-%.3f stretch %.3f-%.3f'%(min(vr),max(vr),min(st),max(st)),'\n  outside:',out)
