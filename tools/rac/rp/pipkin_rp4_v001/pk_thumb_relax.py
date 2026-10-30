# pk_thumb_relax.py OUT.json [WIN] [WARM.json] [SIDES] : MPFB_PIPKIN_COMPACT_BRANCH_v001 thumb placement -- joint on-surface relaxation on PK-NAT / PKF107 / PK91 / PK122
# (shared (face, s, u) per vertex), warm start = the Durrim v002 full-split relaxation mapped by row / column keys (engineering start point only).
# Penalties: counted rings B / T1 / T2 inside each body's validator window and radius; transition poles outside the thumb_mcp crease band (|pb| >= 0.8 h)
# and outside every non-digit station band; fold guard; seam vertices pinned. Adapted from durrim_rp4_v002/search/thumb_prelax3.py.
# local re-relaxation of the thumb patch around the unsplit sector, warm-started from thumb_relax2.json (old topology, mapped by keys),
# + crease-band penalty for every thumb pole vs every non-digit validator station (hip etc.) on every body
import sys, json, time, numpy as np
sys.path.insert(0,'/home/claude/wayfarer-design/tools/rac/rp/durrim_rp4_v002'); sys.path.insert(0,'/home/claude/wayfarer-design/tools/rac/rp/pipkin_rp4_v001'); sys.path.insert(0,'/home/claude/wayfarer-design/tools/rac/rp/marchfolk_rp3_v001')
import pk_thumb_patch as TP, param_relax as PR, thumb_rings as TR, thumb_grid as TG, quick_eval as QE
from core3lib import stations, topo
from neck_probe import adjacency
br=json.load(open('thumb_def.json')); OUT=sys.argv[1]; WIN=int(sys.argv[2]) if len(sys.argv)>2 else 3
ids=['PK-NAT','PKF107-NAT','PK91-NAT','PK122-NAT']; Zs=[dict(np.load(f'../fam/{i}_fam.npz')) for i in ids]
Q0=np.asarray(Zs[0]['Q']); Vs=[z['V'].astype(float) for z in Zs]; nV=len(Vs[0])
# old vid -> key (old generator order: per side, per column k: Zm, Am, Bm, T1l, T1m, T2l, T2m, Cm)
old=json.load(open(sys.argv[3] if len(sys.argv)>3 else '/tmp/claude-0/rt/du2/thumb_relax2.json'))['override']; ORD=[('Z',1),('A',1),('B',1),('T1',0),('T1',1),('T2',0),('T2',1),('C',1)]
okey={}
for si,side in enumerate('lr'):
    for k in range(20):
        for t,(row,odd) in enumerate(ORD): okey[nV+160*si+8*k+t]=(side,row,2*k+odd)
R0=TP.realize(Zs[0],br); keys=R0['keys']; k2v={v:k for k,v in keys.items()}
warm={}
NEWW=len(sys.argv)>3
for ov,(f,a,b) in old.items():
    if NEWW: warm[int(ov)]=(f,a,b); continue
    ov=int(ov)
    if ov<nV: warm[ov]=(f,a,b)                                             # moved parent: same id
    elif okey[ov] in k2v: warm[k2v[okey[ov]]]=(f,a,b)
print('warm mapped',len(warm),'of',len(R0['param']))
# check mapping sanity: mapped new vertices' warm face must be within 1 ring of their default face
bad=[v for v,(f,a,b) in warm.items() if v>=nV and not (set(Q0[f])&set(Q0[R0['param'][v][0]]))]; print('mapping far',len(bad)); assert not bad
R=[TP.realize(z,br,override=warm) for z in Zs]; Q=R[0]['Q']; base=[r['V'] for r in R]; param=R[0]['param']; Bd=PR.Bodies(Vs,Q0)
nb=adjacency(Q,nV+0*len(base[0])) if False else adjacency(Q,len(base[0]))
# station frames per body (non-digit stations), h from the realized mesh
ST=[]
for b,(z,r) in enumerate(zip(Zs,R)):
    meta=json.loads(str(z['meta'])); V=r['V']; s=(V[:,2].max()-V[:,2].min())/173.143; uE,_=topo(r['Q'],len(V)); L=[]
    for nm,c,d,Wd,Rr_,need,Rp in stations(meta):
        if any(nm.startswith(x) for x in ('index','middle','ring','pinky','thumb','toe')): continue
        c=np.asarray(c,float); d=np.asarray(d,float); d/=np.linalg.norm(d); Rr_*=s; Rp=Rr_ if Rp is None else Rp*s
        near=np.linalg.norm(V[uE[:,0]]-c,axis=1)<Rr_; h=float(np.median(np.linalg.norm(V[uE[near,0]]-V[uE[near,1]],axis=1)))
        L.append((nm,c,d,h,Rp))
    ST.append(L)
hs=[]
for z,r in zip(Zs,R):
    st,_=QE.validate(r['V'],r['Q'],json.loads(str(z['meta'])),names=['thumb_mcp_l','thumb_mcp_r']); hs.append({k[-1]:v['h'] for k,v in st.items()})
out=dict(warm)
SIDES=sys.argv[4] if len(sys.argv)>4 else 'lr'
FORCE=json.loads(sys.argv[5]) if len(sys.argv)>5 else {}
for side in SIDES:
    info=R[0]['info'][side]; U=info['unsplit_columns']; n=20
    cols=set(range(n))                                                   # Pipkin: whole patch free (placement re-solved on Pipkin bodies)
    free=[v for v in param if keys[v][0]==side and (keys[v][2]//2) in cols]
    fidx={v:i for i,v in enumerate(free)}; rings={k:info['fine_rings'][k] for k in ('B','T1','T2')}
    FRM=[TR.frame(z,side) for z in Zs]; FC=[TG.crease_frame(z,side) for z in Zs]
    poles=[v for v in free if len(nb[v])!=4]; pid=np.array([fidx[v] for v in poles]) if poles else np.array([],int)
    # ring penalty uses all ring vertices (free ones from params, fixed ones from base)
    def ringpos(b,F,S,U_,vs):
        P=base[b][vs].copy(); m=np.array([v in fidx for v in vs])
        if m.any(): ii=np.array([fidx[v] for v in np.array(vs)[m]]); P[m]=Bd.pos(b,F[ii],S[ii],U_[ii])
        return P
    def pen(free_,F,S,U_,B_):
        e=0.0
        for b in range(len(ids)):
            fr=FRM[b]; fc=FC[b]
            for k,vs in rings.items():
                P=ringpos(b,F,S,U_,vs)-fr['c']; t=P@fr['d']; r=np.linalg.norm(P-np.outer(t,fr['d']),axis=1)
                e+=2000*max(0,abs(t.mean())-(fr['win']-0.012))**2+2000*max(0,r.max()-(fr['rlim']-0.012))**2
            if len(pid):
                P=B_.pos(b,F[pid],S[pid],U_[pid]); X=P-fc['c']; pb=X@fc['d']; pr=np.linalg.norm(X-np.outer(pb,fc['d']),axis=1); h=hs[b][side]
                e+=500*(np.clip(0.8*h-np.abs(pb),0,None)**2*np.clip((fc['Rp']*1.04-pr)/(0.05*fc['Rp']),0,1)).sum()/h**2
                for nm,c,d,h2,Rp in ST[b]:
                    X=P-c; pb=X@d; pr=np.linalg.norm(X-np.outer(pb,d),axis=1)
                    e+=500*(np.clip(0.65*h2-np.abs(pb),0,None)**2*np.clip((Rp*1.04-pr)/(0.05*Rp),0,1)).sum()/h2**2
        return e
    Rw=np.array(br['zones']['hand:thumb_mcp_'+side]['rows']); pin={}
    for v in free:
        sd,row,j=keys[v]
        if j%2==0 and (j//2) in TP.SEAM[side]:
            f,a,b=param[v]; d0=R0['param'][v]; ca=(d0[1]<1e-9 or d0[1]>1-1e-9); cb=(d0[2]<1e-9 or d0[2]>1-1e-9)
            out_d=d0
            if ca and cb: pin[v]='fix'
            elif ca: pin[v]=(0,round(d0[1]))
            elif cb: pin[v]=(1,round(d0[2]))
    init={v:(tuple(warm[v]) if v in warm else param[v]) for v in free}
    Rw_=np.array(br['zones']['hand:thumb_mcp_'+side]['rows'])
    for key,u in FORCE.get(side,{}).items():                                # forced seed: Z line vertex at u along its Z->A rung, slide along the rung only
        line=int(key); zv=int(Rw_[1][line]); corners=(Rw_[1][line],Rw_[1][(line+1)%20],Rw_[2][(line+1)%20],Rw_[2][line])
        f=next(g for g in TP.FACES_OF(Q0,[int(c) for c in corners]) if set(int(x) for x in Q0[g])==set(int(c) for c in corners))
        W=np.zeros(4); pos=[list(Q0[f]).index(int(c)) for c in corners]; w=[1-u,0,0,u]; W[pos]=w; init[zv]=(int(f),float(W[1]+W[2]),float(W[2]+W[3]))
        a_,b_=init[zv][1],init[zv][2]; ci=0 if (a_<1e-9 or a_>1-1e-9) else 1; fc_=init[zv][1+(1-ci)]
        # free coordinate range that keeps the A-side weight >= UMIN (A weight is linear in the free coordinate along this edge)
        def aw(x): ss,uu=(round(a_),x) if ci==0 else (x,round(b_)); w=[(1-ss)*(1-uu),ss*(1-uu),ss*uu,(1-ss)*uu]; return sum(w[list(Q0[f]).index(int(Rw_[2][line]))] for _ in [0])
        UMIN=0.55; x_at=[aw(0.0),aw(1.0)]; lo_,hi_=(0.0,1.0)
        if x_at[1]>x_at[0]: lo_=(UMIN-x_at[0])/(x_at[1]-x_at[0])
        else: hi_=(UMIN-x_at[0])/(x_at[1]-x_at[0])
        pin[zv]=('box',ci,round(init[zv][1+ci]),max(0.0,min(lo_,hi_)),min(1.0,max(lo_,hi_))); print('forced',zv,init[zv],pin[zv],'A weight at bounds',x_at)
    for v in pin: init[v]=R0['param'][v] if pin[v]=='fix' else init[v]
    print(side,'free',len(free),'pinned',len(pin),'poles',len(poles),flush=True)
    t0=time.time(); par=PR.relax(Bd,Q,base,free,init,penalty=pen,weights=[1,1,1,.7],verbose=True,maxiter=250,pin=pin,rounds=5); out.update(par)
    for b in range(len(ids)):
        for v,(f,a,bb) in par.items(): base[b][v]=Bd.pos(b,np.array([f]),np.array([a]),np.array([bb]))[0]
    print(side,'%.0fs'%(time.time()-t0),flush=True)
json.dump(dict(params=None,override={str(k):list(v) for k,v in out.items()},keys={str(k):list(v) for k,v in keys.items()}),open(OUT,'w'))
