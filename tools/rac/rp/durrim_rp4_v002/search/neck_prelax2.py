import sys, json, time, numpy as np
sys.path.insert(0,'/home/claude/wayfarer-design/tools/rac/rp/durrim_rp4_v002'); sys.path.insert(0,'/home/claude/wayfarer-design/tools/rac/rp/marchfolk_rp3_v001')
import neck_reroute as NR, surface_relax as SR, param_relax as PR
from neck_probe import frame, adjacency
LO,HI=float(sys.argv[4]) if len(sys.argv)>4 else 47.,float(sys.argv[5]) if len(sys.argv)>5 else 133.
import os; ops=json.load(open(os.environ.get('NECK_OPS','neck_ops.json'))); ring=int(sys.argv[1])
ids=['DU137C-NAT','DUF137C-NAT','DU122C-NAT','DU152C-NAT','MF152-NAT']; req={'DU137C-NAT':1.6,'DU152C-NAT':1.6,'DU122C-NAT':1.0,'DUF137C-NAT':1.0,'MF152-NAT':1.0}
Zs=[np.load(f'../du/fam/{i}_fam.npz') for i in ids]; Q0=np.asarray(Zs[0]['Q']); Vs=[z['V'].astype(float) for z in Zs]
Q,t=NR.apply_def(Q0,ops); nbn=adjacency(Q,len(Vs[0]))
FR=[frame(V,Q,json.loads(str(z['meta']))) for V,z in zip(Vs,Zs)]
B=PR.Bodies(Vs,Q0); out={}
fidx={}
for f,q in enumerate(Q0):
    for x in q: fidx.setdefault(int(x),[]).append(f)
for side in 'lr':
    core={o[0] for o in ops[side]}|{y for o in ops[side] for y in o[2]}
    free=set(int(x) for f in t for x in Q[f] if any(int(y) in core for y in Q[f]))
    for _ in range(ring): free|={w for v in list(free) for w in nbn[v]}
    free=sorted(free); val=np.array([len(nbn[i]) for i in range(len(Vs[0]))]); poles=[v for v in free if val[v]!=4]
    init={}; prev={int(k):v for k,v in json.load(open(sys.argv[2])).items()} if len(sys.argv)>2 else {}
    for v in free:
        if v in prev: init[v]=tuple(prev[v]); continue
        f=fidx[v][0]; k=list(Q0[f]).index(v); su=[(0.0,0.0),(1.0,0.0),(1.0,1.0),(0.0,1.0)][k]; su=tuple(min(max(c,1e-3),1-1e-3) for c in su); init[v]=(f,)+su
    pidx=[free.index(p) for p in poles]
    def pen(free_,F,S,U,B_):
        e=0.0
        for b,i in enumerate(ids):
            P=B_.pos(b,F[pidx],S[pidx],U[pidx]); th=np.abs(P[:,2]-FR[b]['c'][2])/FR[b]['h']; e+=200*(np.clip(req[i]-th,0,None)**2).sum()
        return e
    t0=time.time(); par=PR.relax(B,Q,Vs,free,init,penalty=pen,weights=[1,1,.7,.7,.3],verbose=True,lo=LO,hi=HI,rounds=8); out.update(par)
    print(side,'free',len(free),'poles',poles,'%.0fs'%(time.time()-t0),flush=True)
json.dump({str(k):v for k,v in out.items()},open(f'neck_par_r{ring}{sys.argv[3] if len(sys.argv)>3 else ""}.json','w'))
