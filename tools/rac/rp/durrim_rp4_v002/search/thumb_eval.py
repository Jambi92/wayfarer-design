import sys, json, numpy as np
sys.path.insert(0,'/home/claude/wayfarer-design/tools/rac/rp/durrim_rp4_v002'); sys.path.insert(0,'/home/claude/wayfarer-design/tools/rac/rp/marchfolk_rp3_v001')
import thumb_patch as TP, quick_eval as QE, uv_check as UC
from core3lib import quality
br=json.load(open('thumb_def.json')); R=json.load(open(sys.argv[1])); ov={int(k):tuple(v) for k,v in R['override'].items()}
for id in ['DU122C-NAT','DU137C-NAT','DUF137C-NAT','DU152C-NAT','MF152-NAT']:
    z=dict(np.load(f'../du/fam/{id}_fam.npz')); r=TP.realize(z,br,R.get('params'),override=ov); V,Q=r['V'],r['Q']
    f=np.r_[r['removed'],np.arange(len(z['Q']),len(Q))]; ang,asp,ba,bs=quality(V,Q[f]); a0,s0,b0,c0=quality(z['V'].astype(float),np.asarray(z['Q'])[r['removed']])
    st,_=QE.validate(V,Q,json.loads(str(z['meta'])),names=['thumb_mcp_l','thumb_mcp_r','thumb_ip_l','thumb_ip_r'])
    print(id,QE.integrity(Q,len(V)) if id=='DU137C-NAT' else '', '| v002 branch: angle %d aspect %d (union %d) ang %.1f-%.1f asp max %.2f | parent: angle %d aspect %d | UV flips %s'%(ba.sum(),bs.sum(),(ba|bs).sum(),ang.min(),ang.max(),asp.max(),b0.sum(),c0.sum(),UC.uv_flips(Q,r['UV'],f)[0]))
    print('    ',{k:(v['status'],v['loops'],v['margin'],v['crease'],v['within2']) for k,v in st.items()})
