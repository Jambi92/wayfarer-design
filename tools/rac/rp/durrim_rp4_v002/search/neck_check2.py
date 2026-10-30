import sys, json, numpy as np
sys.path.insert(0,'/home/claude/wayfarer-design/tools/rac/rp/durrim_rp4_v002'); sys.path.insert(0,'/home/claude/wayfarer-design/tools/rac/rp/marchfolk_rp3_v001')
import neck_reroute as NR, surface_relax as SR, quick_eval as QE
from neck_probe import crease_poles
from core3lib import quality
import os; ops=json.load(open(os.environ.get('NECK_OPS','neck_ops.json'))); sl={int(k):v for k,v in json.load(open(sys.argv[1])).items()}
for id in ['DU122C-NAT','DU137C-NAT','DU152C-NAT','DUF137C-NAT','MF152-NAT']:
    z=np.load(f'../du/fam/{id}_fam.npz'); V0=z['V'].astype(float); Q0=np.asarray(z['Q']); meta=json.loads(str(z['meta']))
    Q,t=NR.apply_def(Q0,ops); V=V0.copy()
    for v,(f,a,b) in sl.items(): V[v]=SR.bil(V0[Q0[f]],a,b)
    aff=np.array([i for i,q in enumerate(Q) if any(int(x) in sl for x in q)])
    a1,s1,b1,c1=quality(V,Q[aff]); st,_=QE.validate(V,Q,meta,names=['neck']); F,cp=crease_poles(V,Q,meta)
    poles=[v for v in sl if len({w for q in Q[aff] if v in q for w in q})-1>=0]
    print(id,'angle viol',b1.sum(),'asp>4',c1.sum(),'ang %.0f-%.0f asp %.2f'%(a1.min(),a1.max(),s1.max()),'| neck',st['neck']['status'],'loops',st['neck']['loops'],'crease',st['neck']['crease'],'| poles<=3h',cp, '| max dz %.3f'%max(abs(V[v]-V0[v]).max() for v in sl))
