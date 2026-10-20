# toegen.py IN.npz SPEC.json OUT.npz : rebuild a digit sub-cage (toes or fingers) distal to an attachment ring.
# Digits run along DIGDIR (unit, e.g. (0,-1,0) for toes); clefts traced in slices normal to SLAX (axis id, e.g. 2 = z slices).
# Topology:
#   attach ring A (existing, kept) -> M (new ring, |O| verts) -> O (outer loop of the digit bases) -> digit tubes (12-vert rings).
#   Digit ring order (viewed against DIGDIR, 'up' = UP axis): [T, TR, R1, R2, R3, BR, B, BL, L3, L2, L1, TL].
#   Adjacent digits share the crotch path TR-R1-R2-R3-BR (= TL-L1-L2-L3-BL of the next digit) on the traced cleft floor.
#   Support rings: walls of each cleft at distances SUP (cm) distal of the floor, then free rings from digit slices, then a cap.
import sys, json, numpy as np
from collections import defaultdict
from scipy.spatial import cKDTree
sys.path.insert(0,'/home/claude/stc/rp1e')
from earsl import slice_loops
from cleftfloor import trace
from orient import orient_patch, check
inp,specp,out=sys.argv[1:4]
S=json.load(open(specp))
z=np.load(inp); V=z['V'].astype(float); F=[[int(x) for x in f if x>=0] for f in z['F']]; col=np.load(inp.replace('.npz','_col.npy'))
SRC=np.load('/home/claude/stc/rp1/weld.npz')['V'].astype(float); scol=np.load(S.get('srccolfile','/home/claude/stc/rp1e/col_r2.npy'))
ROT=np.eye(3)
if S.get('rotz'):
    a_=np.radians(S['rotz']); ROT=np.array([[np.cos(a_),-np.sin(a_),0],[np.sin(a_),np.cos(a_),0],[0,0,1]])
    import earsl; SRC=SRC@ROT.T; earsl.S=SRC.copy(); V=V@ROT.T
kS=cKDTree(SRC)
A=S['attach']; AE=set(frozenset((A[i],A[(i+1)%len(A)])) for i in range(len(A)))
D=np.array(S['digdir'],float); D/=np.linalg.norm(D); UP=np.array(S['up'],float); UP/=np.linalg.norm(UP); RT=np.cross(D,UP)  # right = D x UP
if S.get('flipright'): RT=-RT
# ---------- remove the old distal region ----------
ef=defaultdict(list)
for k,f in enumerate(F):
    for i in range(len(f)): ef[frozenset((f[i],f[(i+1)%len(f)]))].append(k)
seedE=frozenset((A[0],A[1])); seed=max(ef[seedE],key=lambda k:-(V[F[k]].mean(0)@D))
keep={seed}; st=[seed]
while st:
    k=st.pop(); f=F[k]
    for i in range(len(f)):
        e=frozenset((f[i],f[(i+1)%len(f)]))
        if e in AE: continue
        for q in ef[e]:
            if q not in keep: keep.add(q); st.append(q)
F=[F[k] for k in sorted(keep)]
NV=[list(p) for p in V]; NC=list(col)
def add(p,c): NV.append(list(np.asarray(p,float))); NC.append(int(c)); return len(NV)-1
def srccol(p): return int(scol[kS.query(p)[1]])
# ---------- cleft traces ----------
SL=S['slax']; ij=[a for a in range(3) if a!=SL]
def to3(p2,lev):
    q=np.zeros(3); q[ij[0]]=p2[0]; q[ij[1]]=p2[1]; q[SL]=lev; return q
from planeslice import plane_loops
_c2d={}
def cl_frame(c):
    n=np.array(c['nrm'],float); n/=np.linalg.norm(n); e2=np.array(c['e2'],float); e2=e2-(e2@n)*n; e2/=np.linalg.norm(e2); e1=np.cross(e2,n)
    return np.array(c['org'],float),n,e1,e2
def cl_loops2d(c,lv):
    key=(id(c),round(lv,4))
    if key not in _c2d:
        o,n,e1,e2=cl_frame(c); p0=o+n*lv
        L=[P for P,cl in plane_loops(p0,n) if cl and np.linalg.norm(P-p0,axis=1).min()<c.get('rad',10.0)]
        _c2d[key]=[np.c_[(P-p0)@e1,(P-p0)@e2] for P in L]
    return _c2d[key]
def cl_to3(c,lv,q2):
    o,n,e1,e2=cl_frame(c); return o+n*lv+e1*q2[0]+e2*q2[1]
clefts=[]
for c in S['clefts']:
    levs=np.linspace(c['lev'][0],c['lev'][1],5)   # top .. bottom (5 crotch verts)
    s0=np.array(c['starts'][0],float); dd0=np.array(c['dir'],float); dd0/=np.linalg.norm(dd0); nn0=np.array([-dd0[1],dd0[0]])
    given=[tuple(x) for x in c['starts']]
    grid=[tuple(s0+u*nn0+w*dd0) for w in np.arange(-1.0,2.6,0.25) for u in np.arange(-1.2,1.21,0.15)]
    def run(lv,s):
        if 'nrm' in c: return trace(lv,s,c['dir'],loops2d=cl_loops2d(c,lv))
        return trace(lv,s,c['dir'],axis=SL,ij=tuple(ij))
    cand={}
    for lv in levs:
        cs=[]
        for s in given:
            p=run(lv,s)
            if p and len(p)>=3: cs.append(p)
        if not cs:
            for s in grid:
                p=run(lv,s)
                if p and len(p)>=5 and (p[-1][0]-s0)@dd0<c.get('maxdepth',3.0): cs.append(p)
        assert cs, ('trace failed',c,lv)
        cand[lv]=cs
    # consistency: pick per level the floor closest (in 2D) to the median of first choices
    first=np.array([cand[lv][0][-1][0] for lv in levs]); med=np.median(first,axis=0)
    rec=[]
    for lv in levs:
        p=min(cand[lv],key=lambda q:np.linalg.norm(q[-1][0]-med)); rec.append((lv,p))
        if np.linalg.norm(p[-1][0]-med)>c.get('maxdev',1.2): print('WARN cleft floor off median',np.round(p[-1][0],2),np.round(med,2),lv)
    clefts.append(rec)
_slc={}
def sl_loops(ax,lv):
    key=(ax,round(lv,4))
    if key not in _slc: _slc[key]=[P for P,c in slice_loops(ax,lv+1.3e-4) if c]
    return _slc[key]
from cleftfloor import ray as _ray
def wall_at(pth,lv,dist,side,d0,c=None):
    # wall point of the cleft at 'dist' back from the floor (towards the mouth, -d0), on the side*RT side
    obl=c is not None and 'nrm' in c
    T3=(lambda q2,l_: cl_to3(c,l_,q2)) if obl else (lambda q2,l_: to3(q2,l_))
    f=pth[-1][0]; d0=np.asarray(d0,float); d0/=np.linalg.norm(d0); q=f-d0*dist
    n=np.array([-d0[1],d0[0]]); n3=T3(n,lv)-T3(np.zeros(2),lv)
    if n3@RT*side<0: n=-n
    if obl: L2=cl_loops2d(c,lv); segs=[(l[k],l[(k+1)%len(l)]) for l in L2 for k in range(len(l))]
    else:
        L=sl_loops(SL,lv); segs=[(l[k][ij],l[(k+1)%len(l)][ij]) for l in L for k in range(len(l))]
    segs=[sg for sg in segs if np.linalg.norm(sg[0]-q)<3]
    l=_ray(segs,q,n)
    off=min(max(0.9*l,float(S.get('wallmin',0.15))),float(S.get('wallmax',9.0))) if l<3 else min(0.3,float(S.get('wallmax',9.0)))
    return T3(q+n*off,lv)
SUP=S['sup']
nd=len(S['digits'])
# crotch verts (shared): per cleft 5 floor verts [top..bottom]; support wall verts per cleft per sup per side
crotch=[]; wallL=[]; wallR=[]
for ci,rec in enumerate(clefts):
    ids=[]
    for lv,pth in rec:
        cc_=S['clefts'][ci]; fp=cl_to3(cc_,lv,pth[-1][0]) if 'nrm' in cc_ else to3(pth[-1][0],lv); ids.append(add(fp,srccol(fp) if not S.get('crotchcol') else S['crotchcol']))
    crotch.append(ids)
    wl=[];wr=[]
    for sd in SUP:
        wl.append([add(wall_at(pth,lv,sd,-1,S['clefts'][ci]['dir'],S['clefts'][ci]),S['digits'][ci]['col']) for lv,pth in rec])
        wr.append([add(wall_at(pth,lv,sd,+1,S['clefts'][ci]['dir'],S['clefts'][ci]),S['digits'][ci+1]['col']) for lv,pth in rec])
    wallL.append(wl); wallR.append(wr)
# ---------- digit outer sides (no cleft): medial side of digit 0, lateral side of last digit ----------
_pl={}
def ploops(p,n):
    key=(tuple(np.round(p,3)),tuple(np.round(n,3)))
    if key not in _pl: _pl[key]=[P for P,cl in plane_loops(p,n) if cl and np.linalg.norm(P-p,axis=1).min()<S.get('plrad',6.0)]
    return _pl[key]
def side_col(ref_ids,side,upL,rtL,tL):
    row=[]
    for vid in ref_ids:
        p=np.array(NV[vid]); L=ploops(p,tL); Q=np.vstack(L) if L else SRC[kS.query_ball_point(p,S['sidesearch'])]
        m=(np.abs((Q-p)@upL)<S.get('sideup',0.25))&(np.linalg.norm(Q-p,axis=1)<S['sidesearch'])
        Qm=Q[m] if m.any() else Q
        row.append(Qm[np.argmax((Qm@rtL)*side)])
    return row
def tb_point(pa,pb,sgn,upL,rtL,tL):
    c=0.5*(pa+pb); L=ploops(c,tL); Q=np.vstack(L) if L else SRC[kS.query_ball_point(c,S['tbsearch'])]
    lo,hi=sorted([pa@rtL,pb@rtL]); m=((Q@rtL)>lo)&((Q@rtL)<hi)&(np.linalg.norm(Q-c,axis=1)<S['tbsearch'])
    Qm=Q[m] if m.any() else Q[np.linalg.norm(Q-c,axis=1)<S['tbsearch']]
    return Qm[np.argmax(((Qm-c)@upL)*sgn)]
def digit_frame(di,dg):
    if 'up' in dg: u=np.array(dg['up'],float)
    else:
        ns=[np.array(S['clefts'][k]['nrm'],float) for k in (di-1,di) if 0<=k<len(S['clefts']) and 'nrm' in S['clefts'][k]]
        u=np.mean(ns,axis=0) if ns else UP.copy()
    u=u-(u@D)*D; u/=np.linalg.norm(u); r=np.cross(D,u)
    if S.get('flipright'): r=-r
    if r@RT<0: r=-r
    return u,r
dig_rings=[]; tans=[]
for di,dg in enumerate(S['digits']):
    # left side columns (L1,L2,L3 + TL, BL) and right side (TR,R1,R2,R3,BR) for ring0 and support rings
    rings=[]
    for r in range(len(SUP)+1):
        if di<nd-1: Rc=crotch[di] if r==0 else wallL[di][r-1]
        if di>0: Lc=crotch[di-1] if r==0 else wallR[di-1][r-1]
        upL,rtL=digit_frame(di,dg); tL=np.array(dg.get('tbase',list(D)),float); tL/=np.linalg.norm(tL)
        if di==0: Lc=[add(p,dg['col']) for p in side_col(Rc,-1,upL,rtL,tL)]
        if di==nd-1: Rc=[add(p,dg['col']) for p in side_col(Lc,+1,upL,rtL,tL)]
        T=add(tb_point(np.array(NV[Lc[0]]),np.array(NV[Rc[0]]),1,upL,rtL,tL),dg['col'])
        B=add(tb_point(np.array(NV[Lc[-1]]),np.array(NV[Rc[-1]]),-1,upL,rtL,tL),dg['col'])
        rings.append([T,Rc[0],Rc[1],Rc[2],Rc[3],Rc[4],B,Lc[4],Lc[3],Lc[2],Lc[1],Lc[0]])
    # free rings: axis march (oblique planes) from the digit seed; 12 arc-length samples starting at the local top
    from planeslice import axis_rings
    AR=axis_rings(dg['seed'],dg.get('t0',list(D)),dg.get('h',0.8),maxn=dg.get('maxn',12),rad=dg.get('rad',7.0),maxjump=dg.get('maxjump',2.0),minr=dg.get('minr',0.5))
    if 'ext' in dg and AR:
        ex=dg['ext']; c_last=AR[-1][0]
        AR2=axis_rings(c_last+np.array(ex['t'])/np.linalg.norm(ex['t'])*ex.get('h',0.6),ex['t'],ex.get('h',0.6),maxn=ex.get('maxn',8),rad=7.0,maxjump=2.0,minr=ex.get('minr',0.5),smooth=ex.get('smooth',0.2))
        AR=list(AR)+list(AR2)
    up=UP.copy(); dig_tan=[]
    for (cen,t,P,r) in AR[dg.get('skip',0):]:
        up=up-(up@t)*t; up/=np.linalg.norm(up); rt=np.cross(t,up)
        if S.get('flipright'): rt=-rt
        k0=int(np.argmax(P@up)); P2=np.roll(P,-k0,axis=0)
        if (P2[min(3,len(P2)-1)]-P2[0])@rt<0: P2=np.vstack([P2[:1],P2[1:][::-1]])
        Q=np.vstack([P2,P2[:1]]); s_=np.r_[0,np.cumsum(np.linalg.norm(np.diff(Q,axis=0),axis=1))]
        pts=[]
        for u in np.arange(12)/12*s_[-1]:
            k=int(np.clip(np.searchsorted(s_,u),1,len(s_)-1)); al=(u-s_[k-1])/max(s_[k]-s_[k-1],1e-12); pts.append(Q[k-1]+(Q[k]-Q[k-1])*al)
        rings.append([add(p,dg['col']) for p in pts]); dig_tan.append(t)
    tans.append(dig_tan[-1] if dig_tan else D)
    if S.get('monofix',0)>0 and len(dig_tan)>1:
        nfree=len(dig_tan); fr=rings[-nfree:]
        for k in range(1,nfree):
            t=dig_tan[k-1]; mm=S['monofix']*dg.get('h',0.8)
            for j in range(12):
                a=np.array(NV[fr[k-1][j]]); q=np.array(NV[fr[k][j]]); d=(q-a)@t
                if d<mm: NV[fr[k][j]]=list(q+t*(mm-d))
    dig_rings.append(rings)
# ---------- outer loop O (union boundary of the ring0s) and M ring ----------
O=[]
for di in range(nd):
    r0=dig_rings[di][0]
    if di==0: O+= [r0[11]]
    O+= [r0[0],r0[1]]
for v in dig_rings[-1][0][2:6]: O.append(v)          # lateral side R1..R3, BR  (last digit)
for di in range(nd-1,-1,-1):
    r0=dig_rings[di][0]; O+= [r0[6],r0[7]]           # B, BL
for v in dig_rings[0][0][8:11]: O.append(v)          # medial side L3, L2, L1
# remove consecutive duplicates (shared BL/BR etc. are identical ids)
Oc=[]
for v in O:
    if not Oc or Oc[-1]!=v: Oc.append(v)
if Oc[0]==Oc[-1]: Oc=Oc[:-1]
O=Oc
Apos=np.array([NV[a] for a in A]); cen=Apos.mean(0)
def ang(p):
    q=np.asarray(p)-cen; return np.arctan2(q@UP,q@RT)
def snap_near(p,r=0.6):
    d,i=kS.query(p); return SRC[i] if d<r else p
def at_angle(poly,th):
    P=np.vstack([poly,poly[:1]]); t=np.unwrap([ang(p) for p in P])
    if t[-1]<t[0]: P=P[::-1]; t=np.unwrap([ang(p) for p in P])
    th=t[0]+((th-t[0])%(2*np.pi))
    for k in range(len(P)-1):
        if t[k]<=th<=t[k+1]: al=(th-t[k])/(t[k+1]-t[k]+1e-12); return P[k]+(P[k+1]-P[k])*al
    return P[int(np.argmin(np.abs(np.angle(np.exp(1j*(t-th))))))]
M1=[];M=[]
f1,f2=S.get('mfracs',[0.33,0.66])
for v in O:
    p=np.array(NV[v]); q=at_angle(Apos,ang(p))
    sn=(lambda x:snap_near(x,1.0)) if S.get('msnap',True) else (lambda x:x)
    M1.append(add(sn(p+f1*(q-p)),S.get('mcol',6))); M.append(add(sn(p+f2*(q-p)),S.get('mcol',6)))
def smooth_ring(R,it,lam):
    for _ in range(it):
        P=np.array([NV[v] for v in R]); Q=0.5*(np.roll(P,1,0)+np.roll(P,-1,0)); P=P+lam*(Q-P)
        for v,p in zip(R,P): NV[v]=list(p)
smooth_ring(M,S.get('msmooth',[6,0.5])[0],S.get('msmooth',[6,0.5])[1]); smooth_ring(M1,S.get('m1smooth',[2,0.3])[0],S.get('m1smooth',[2,0.3])[1])
if S.get('mresnap'):
    for v in M+M1: NV[v]=list(snap_near(np.array(NV[v]),S.get('mresnap')))
# ---------- faces ----------
G=list(F); Fn=[]
nO=len(O)
for i in range(nO):
    Fn.append([O[i],O[(i+1)%nO],M1[(i+1)%nO],M1[i]]); Fn.append([M1[i],M1[(i+1)%nO],M[(i+1)%nO],M[i]])
# A -> M cells by angle around the section centre
def fr(l,th0):
    return ((np.array([ang(NV[v]) for v in l])-th0)/(2*np.pi))%1.0
def cells(small,big,fs,fb):
    m=len(small); n=len(big); d=lambda x,y: abs(((x-y+0.5)%1.0)-0.5)
    own=[int(np.argmin([d(fs[i],fb[j]) for i in range(m)])) for j in range(n)]; Fs=[]
    for j in range(n):
        j2=(j+1)%n; i1,i2=own[j],own[j2]
        if i1==i2: Fs.append([small[i1],big[j],big[j2]])
        else:
            k=i1; steps=(i2-i1)%m
            if steps==1: Fs.append([small[i1],big[j],big[j2],small[i2]])
            else:
                Fs.append([small[k],big[j],big[j2]])
                while k!=i2: Fs.append([small[k],big[j2],small[(k+1)%m]]); k=(k+1)%m
    return Fs
def orient_loop(l):
    t=np.unwrap([ang(NV[v]) for v in l+l[:1]]); return l if t[-1]>t[0] else l[::-1]
Ao=orient_loop(list(A)); Mo=orient_loop(list(M)); th0=ang(NV[Mo[0]])
if S.get('dbg'):
    print('A ang',np.round(np.degrees(np.unwrap([ang(NV[v]) for v in Ao])),0)); print('M ang',np.round(np.degrees(np.unwrap([ang(NV[v]) for v in Mo])),0)); print('O ang',np.round(np.degrees(np.unwrap([ang(NV[v]) for v in O])),0))
def frac_arc(l):
    P=np.array([NV[v] for v in l]); Q=np.vstack([P,P[:1]]); s_=np.r_[0,np.cumsum(np.linalg.norm(np.diff(Q,axis=0),axis=1))]; return s_[:-1]/s_[-1]
k0=int(np.argmin([np.linalg.norm(np.array(NV[v])-np.array(NV[Ao[0]])) for v in Mo])); Mo=Mo[k0:]+Mo[:k0]
Fn+=cells(Ao,Mo,frac_arc(Ao),frac_arc(Mo))
for di_,rings in enumerate(dig_rings):
    TD=tans[di_]
    for a,b in zip(rings[:-1],rings[1:]):
        for i in range(12): Fn.append([a[i],a[(i+1)%12],b[(i+1)%12],b[i]])
    l=rings[-1]
    if S.get('tipcap',True):
        P=np.array([NV[v] for v in l]); c=P.mean(0)
        idx=kS.query_ball_point(c,S.get('tipsearch',2.0)); Q=SRC[idx]
        hw=hh=np.linalg.norm(P-c,axis=1).max()
        Q=Q[((Q-c)@TD>0)&(np.linalg.norm((Q-c)-np.outer((Q-c)@TD,TD),axis=1)<0.8*min(hw,hh))] if len(Q) else Q
        tipP=Q[np.argmax(Q@TD)] if len(Q) else c+TD*0.3
        t=[]
        for k in range(4):
            dk=0.5*(P[(3*k+1)%12]+P[(3*k+2)%12])-c
            t.append(add(tipP-TD*S.get('tipback',0.2)+S.get('tipspread',0.45)*dk,NC[l[0]]))
        for k in range(4):
            Fn.append([l[3*k],l[3*k+1],l[3*k+2],t[k]]); Fn.append([l[3*k+2],l[(3*k+3)%12],t[(k+1)%4],t[k]])
        Fn.append([t[0],t[1],t[2],t[3]])
    else:
        for q in ([0,1,2,11],[2,3,10,11],[3,4,9,10],[4,5,8,9],[5,6,7,8]): Fn.append([l[i] for i in q])
Fn=orient_patch(G,Fn); G+=Fn
dd,bb=check(G)
if dd or bb:
    import collections
    de=collections.Counter((f[i],f[(i+1)%len(f)]) for f in G for i in range(len(f)))
    print('dup',[e for e,c in de.items() if c>1][:8]); print('bnd',[e for e in de if (e[1],e[0]) not in de][:8])
    raise SystemExit('topology dup %d bnd %d'%(dd,bb))
used=sorted(set(i for f in G for i in f)); remap={o:n for n,o in enumerate(used)}
V2=np.array([NV[i] for i in used])@ROT; G2=[[remap[i] for i in f] for f in G]; C2=np.array([NC[i] for i in used])
Fa=np.full((len(G2),4),-1)
for k,f in enumerate(G2): Fa[k,:len(f)]=f
np.savez_compressed(out,V=V2,F=Fa); np.save(out.replace('.npz','_remap.npy'),np.array([remap.get(i,-1) for i in range(len(V))])); np.save(out.replace('.npz','_col.npy'),C2)
meta={'remap_old_max':int(len(V)),'O':[remap[v] for v in O],'M':[remap[v] for v in M],'M1':[remap[v] for v in M1],'crotch':[[remap[v] for v in c] for c in crotch],
      'rings':[[[remap[v] for v in r] for r in rs] for rs in dig_rings]}
json.dump(meta,open(out.replace('.npz','_meta.json'),'w'))
print('V',len(V2),'F',len(G2),'tris',sum(len(f)==3 for f in G2),'removed faces',len(z['F'])-len(keep))
