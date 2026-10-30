import sys, json, time, numpy as np
sys.path.insert(0,'/home/claude/wayfarer-design/tools/rac/rp/durrim_rp4_v002')
import neck_reroute as NR
from neck_probe import frame, adjacency
W='/tmp/claude-0/rt/du'; fams={k:f'{W}/fam/{k}_fam.npz' for k in NR.BODIES}
Z={k:np.load(f) for k,f in fams.items()}; z0=Z['DU137C-NAT']; Q0=np.asarray(z0['Q']); nV=len(z0['V']); nb=adjacency(Q0,nV)
FR={k:frame(z['V'].astype(float),Q0,json.loads(str(z['meta']))) for k,z in Z.items()}
TH={k:(z['V'][:,2].astype(float)-FR[k]['c'][2])/FR[k]['h'] for k,z in Z.items()}
fl,region=NR.local_faces(Q0,nb,5299,6); _,inner=NR.local_faces(Q0,nb,5299,3); Ql=Q0[fl]
t137=TH['DU137C-NAT']; val0={v:len(nb[v]) for v in region}
def sig(Q): return tuple(sorted(tuple(sorted(map(int,q))) for q in Q))
def loc(Qn):
    vl={}
    for q in Qn:
        for k in range(4): a,b=int(q[k]),int(q[(k+1)%4]); vl.setdefault(a,set()).add(b); vl.setdefault(b,set()).add(a)
    return {v:len(x) for v,x in vl.items()}
L0=None
def vals_of(Qn):
    l=loc(Qn); return {v:len(nb[v])+l[v]-L0[v] for v in l}
def score(vals):
    poles=[v for v in vals if vals[v]!=4 and (vals[v]!=val0[v] or v==5299)]
    if not poles: return 9,[]
    return min(min(abs(TH[k][v]) for v in poles)-req for k,req in NR.BODIES.items()), poles
def ops_of(Qn):
    E=set()
    for q in Qn:
        for k in range(4):
            a,b=int(q[k]),int(q[(k+1)%4])
            if a in inner and b in inner and min(t137[a],t137[b])>-0.6: E.add((min(a,b),max(a,b)))
    return [(a,b,d) for a,b in sorted(E) for d in (1,-1)]
L0=loc(Ql); front={sig(Ql):(Ql,())}; seen=set(front); best=[]; t=time.time()
for depth in range(1,int(sys.argv[1])+1):
    nxt={}
    for s,(Qc,seq) in front.items():
        for o in ops_of(Qc):
            Qn=NR.apply_ops(Qc,[o])
            if Qn is None: continue
            vals=vals_of(Qn)
            if any(vals[v]<3 or vals[v]>5 for v in vals): continue
            sg=sig(Qn)
            if sg in seen: continue
            seen.add(sg); npole=sum(1 for v in vals if vals[v]!=4 and (vals[v]!=val0[v] or v==5299))
            if npole>7: continue
            if not best: pass
            nxt[sg]=(Qn,seq+(o,)); sc,poles=score(vals); best.append((sc,npole,seq+(o,),poles))
    front=nxt; print('depth',depth,'states',len(front),'%.0fs'%(time.time()-t),'best %.2f'%(max(b[0] for b in best) if best else -9),flush=True)
best.sort(key=lambda x:(-x[0],x[1],len(x[2])))
for b in best[:8]: print('score %+.2f poles %d ops %s'%(b[0],b[1],b[2]),{k:[round(float(TH[k][v]),2) for v in b[3]] for k in TH})
json.dump([[b[0],b[1],[list(o) for o in b[2]],[int(v) for v in b[3]]] for b in best[:100]],open('/tmp/claude-0/rt/du2/neck_bfs.json','w'))
