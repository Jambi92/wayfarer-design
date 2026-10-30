import sys, json, time, numpy as np
sys.path.insert(0,'/home/claude/wayfarer-design/tools/rac/rp/durrim_rp4_v002'); sys.path.insert(0,'/home/claude/wayfarer-design/tools/rac/rp/marchfolk_rp3_v001')
import neck_reroute as NR, surface_relax as SR, quick_eval as QE
from neck_probe import frame, adjacency, crease_poles
from core3lib import quality
ops=json.load(open('neck_ops.json')); ring=int(sys.argv[1]) if len(sys.argv)>1 else 0
z=np.load('../du/fam/DU137C-NAT_fam.npz'); V0=z['V'].astype(float); Q0=np.asarray(z['Q']); meta=json.loads(str(z['meta']))
Q,t=NR.apply_def(Q0,ops); nb0=adjacency(Q0,len(V0)); nbn=adjacency(Q,len(V0))
F=frame(V0,Q,meta); zc,h=F['c'][2],F['h']
res={}
for side in 'lr':
    tf=[f for f in t if any(int(x) in {o[0] for o in ops[side]} | {y for o in ops[side] for y in o[2]} for x in Q[f])] 
    free=set(int(x) for f in tf for x in Q[f])
    for _ in range(ring): free|={w for v in list(free) for w in nbn[v]}
    reg=set(free)
    for _ in range(3): reg|={w for v in list(reg) for w in nb0[v]}
    pf=[i for i,q in enumerate(Q0) if all(int(x) in reg for x in q)]
    surf=SR.Surface(V0,Q0,pf)
    val=np.array([len(nbn[i]) for i in range(len(V0))]); poles=[v for v in free if val[v]!=4]
    cons=[lambda Vt,p=p: 200*max(0,(zc+1.7*h)-Vt[p,2])**2/h**2 for p in poles]
    t0=time.time(); r,Vn=SR.relax(V0,Q,sorted(free),surf,cons=cons); V0=Vn; res.update(r)
    print(side,'free',len(free),'poles',poles,'%.0fs'%(time.time()-t0), 'max slide %.3f cm'%max(np.linalg.norm(Vn[v]-z['V'][v]) for v in free))
aff=np.array([i for i,q in enumerate(Q) if any(int(x) in res for x in q)])
a0,s0,b0,c0=quality(z['V'].astype(float),Q0[aff]); a1,s1,b1,c1=quality(V0,Q[aff])
print('affected faces',len(aff),'v005: angle viol',b0.sum(),'asp>4',c0.sum(),'ang %.0f-%.0f'%(a0.min(),a0.max()),' | relaxed: angle viol',b1.sum(),'asp>4',c1.sum(),'ang %.0f-%.0f asp max %.2f'%(a1.min(),a1.max(),s1.max()))
json.dump({str(k):v for k,v in res.items()},open(f'neck_slide_r{ring}b.json','w'))
