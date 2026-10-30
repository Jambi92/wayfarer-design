import sys, json, numpy as np
sys.path.insert(0,'/home/claude/wayfarer-design/tools/rac/rp/durrim_rp4_v002'); sys.path.insert(0,'/home/claude/wayfarer-design/tools/rac/rp/marchfolk_rp3_v001')
import thumb_patch as TP, quick_eval as QE, uv_check as UC
from core3lib import quality
br=json.load(open('thumb_def.json')); R=json.load(open(sys.argv[1])); ov={int(k):tuple(v) for k,v in R['override'].items()}
for id in sys.argv[2].split(','):
    z=dict(np.load(f'../du/fam/{id}_fam.npz')); r=TP.realize(z,br,override=ov); V,Q=r['V'],r['Q']
    f=np.r_[r['removed'],np.arange(len(z['Q']),len(Q))]; ang,asp,ba,bs=quality(V,Q[f]); a0,s0,b0,c0=quality(z['V'].astype(float),np.asarray(z['Q'])[r['removed']])
    st,summ=QE.validate(V,Q,json.loads(str(z['meta'])))
    print(id,QE.integrity(Q,len(V))['boundary_edges'], '| branch: angle %d aspect %d ang %.1f-%.1f asp max %.2f | parent: angle %d | UV flips %d | firm %d %s'%(ba.sum(),bs.sum(),ang.min(),ang.max(),asp.max(),b0.sum(),UC.uv_flips(Q,r['UV'],f)[0],summ['firm_pass_count'],summ['D1_D3_firm_fail']))
    print('    ',{k:(st[k]['status'][:24],st[k]['loops'],st[k]['crease']) for k in ['thumb_mcp_l','thumb_mcp_r','hip_l','hip_r']})
    bad=np.nonzero(ba|bs)[0]; print('     bad faces', [(int(f[i]), round(float(ang[i].min()),1), round(float(ang[i].max()),1), round(float(asp[i]),2)) for i in bad][:12])
