import sys, json, time, numpy as np
sys.path.insert(0,'/home/claude/wayfarer-design/tools/rac/rp/durrim_rp4_v002'); sys.path.insert(0,'/home/claude/wayfarer-design/tools/rac/rp/marchfolk_rp3_v001')
import thumb_patch as TP, param_relax as PR, thumb_rings as TR, thumb_grid as TG
br=json.load(open('thumb_def.json')); params=json.load(open(sys.argv[1]))['params'] if sys.argv[1]!='def' else None; OUT=sys.argv[2]
ids=['DU137C-NAT','DUF137C-NAT','DU122C-NAT','DU152C-NAT']; Zs=[dict(np.load(f'../du/fam/{i}_fam.npz')) for i in ids]
Q0=np.asarray(Zs[0]['Q']); Vs=[z['V'].astype(float) for z in Zs]
R=[TP.realize(z,br,params) for z in Zs]; Q=R[0]['Q']; base=[r['V'] for r in R]; param=R[0]['param']; param0=dict(param)
WARM={int(k):v for k,v in json.load(open(sys.argv[3]))['override'].items()} if len(sys.argv)>3 else {}
Bd=PR.Bodies(Vs,Q0)
import quick_eval as QE
hs=[]
for z,r in zip(Zs,R):
    st,_=QE.validate(r['V'],r['Q'],json.loads(str(z['meta'])),names=['thumb_mcp_l','thumb_mcp_r']); hs.append({k[-1]:v['h'] for k,v in st.items()})
out={}
for side in 'lr':
    info=R[0]['info'][side]; rings={k:info['fine_rings'][k] for k in ('B','T1','T2')}
    nV0=len(Vs[0]); free=sorted(v for v in param if v in set(np.asarray(Q)[[f for f in range(len(Q)) if 0]].ravel()) or True)
    # only this side's vertices: those in this side's rows
    rows=set(np.array(br['zones']['hand:thumb_mcp_'+side]['rows']).ravel().tolist())
    sidev=set(v for k in info['fine_rings'] for v in info['fine_rings'][k])
    free=[v for v in param if (v in rows) or (v>=nV0 and np.linalg.norm(base[0][v]-base[0][list(sidev)[0]])<6)]
    fidx={v:i for i,v in enumerate(free)}
    FRM=[TR.frame(z,side) for z in Zs]; FC=[TG.crease_frame(z,side) for z in Zs]
    # poles to watch: fine-side transition poles (valence 3) in free set
    from neck_probe import adjacency
    nb=adjacency(Q,len(base[0])); poles=[v for v in free if len(nb[v])!=4]
    pid=np.array([fidx[v] for v in poles]); rid={k:np.array([fidx[v] for v in vs]) for k,vs in rings.items()}
    def pen(free_,F,S,U,B_):
        e=0.0
        for b in range(len(ids)):
            fr=FRM[b]; fc=FC[b]
            for k,ix in rid.items():
                P=B_.pos(b,F[ix],S[ix],U[ix])-fr['c']; t=P@fr['d']; r=np.linalg.norm(P-np.outer(t,fr['d']),axis=1)
                e+=2000*max(0,abs(t.mean())-(fr['win']-0.012))**2+2000*max(0,r.max()-(fr['rlim']-0.012))**2
            P=B_.pos(b,F[pid],S[pid],U[pid])-fc['c']; pb=P@fc['d']; pr=np.linalg.norm(P-np.outer(pb,fc['d']),axis=1); h=hs[b][side]
            e+=500*(np.clip(0.8*h-np.abs(pb),0,None)**2*(pr<fc['Rp']*1.03)).sum()/h**2
        return e
    Rw=np.array(br['zones']['hand:thumb_mcp_'+side]['rows']); pin={}; init_={v:(tuple(WARM[v]) if v in WARM else param[v]) for v in free}
    for k in TP.SEAM[side]:
        for v in [Rw[1][k],Rw[2][k],Rw[3][k],Rw[4][k]]+[info['fine_rings'][rn][2*k] for rn in ('A','B','T1','T2')]:
            f,a,b=param0[int(v)]; init_[int(v)]=param0[int(v)]          # seam vertex: back to its on-seam default placement
            ca=(a<1e-9 or a>1-1e-9); cb=(b<1e-9 or b>1-1e-9)
            if ca and cb: pin[int(v)]='fix'                               # v005 corner on the seam: fixed
            elif ca: pin[int(v)]=(0,round(a))                             # on the rung (seam) edge: slide along it only
            elif cb: pin[int(v)]=(1,round(b))
            else: raise SystemExit('seam vertex not on an edge %d'%v)
    print(side,'pinned seam vertices',len(pin),flush=True)
    t0=time.time(); par=PR.relax(Bd,Q,base,free,init_,rounds=6,penalty=pen,weights=[1,1,1,.7],verbose=True,maxiter=300,pin=pin); out.update(par)
    print(side,'free',len(free),'poles',len(poles),'%.0fs'%(time.time()-t0),flush=True)
json.dump(dict(params=params,override={str(k):list(v) for k,v in out.items()}),open(OUT,'w'))
