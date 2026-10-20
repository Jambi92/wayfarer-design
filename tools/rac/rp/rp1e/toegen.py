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
SRC=np.load('/home/claude/stc/rp1/weld.npz')['V'].astype(float); scol=np.load('/home/claude/stc/rp1e/col_r2.npy')
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
clefts=[]
for c in S['clefts']:
    levs=np.linspace(c['lev'][0],c['lev'][1],5)   # top .. bottom (5 crotch verts)
    rec=[]
    for lv in levs:
        pth=None
        cands=[tuple(s) for s in c['starts']]
        s0=np.array(c['starts'][0],float); dd0=np.array(c['dir'],float); dd0/=np.linalg.norm(dd0); nn0=np.array([-dd0[1],dd0[0]])
        cands+=[tuple(s0+u*nn0+w*dd0) for w in np.arange(-1.0,2.6,0.25) for u in np.arange(-1.2,1.21,0.15)]
        best=None
        for s in cands:
            p=trace(lv,s,c['dir'],axis=SL,ij=tuple(ij))
            if p and len(p)>=5:
                depth=(p[-1][0]-s0)@dd0
                if best is None or depth>best[0]+0.05: best=(depth,p)
                if s in [tuple(x) for x in c['starts']] and depth>0.5: break
        pth=None if best is None else best[1]
        assert pth, ('trace failed',c,lv)
        rec.append((lv,pth))
    clefts.append(rec)
_slc={}
def sl_loops(ax,lv):
    key=(ax,round(lv,4))
    if key not in _slc: _slc[key]=[P for P,c in slice_loops(ax,lv+1.3e-4) if c]
    return _slc[key]
from cleftfloor import ray as _ray
def wall_at(pth,lv,dist,side,d0):
    # wall point of the cleft at 'dist' back from the floor (towards the mouth, -d0), on the side*RT side
    f=pth[-1][0]; d0=np.asarray(d0,float); d0/=np.linalg.norm(d0); q=f-d0*dist
    n=np.array([-d0[1],d0[0]]); n3=to3(n,0)-to3(np.zeros(2),0)
    if n3@RT*side<0: n=-n
    L=sl_loops(SL,lv); segs=[(l[k][ij],l[(k+1)%len(l)][ij]) for l in L for k in range(len(l))]
    segs=[sg for sg in segs if np.linalg.norm(sg[0]-q)<3]
    l=_ray(segs,q,n)
    off=max(0.9*l,float(S.get('wallmin',0.15))) if l<3 else 0.3
    return to3(q+n*off,lv)
SUP=S['sup']
nd=len(S['digits'])
# crotch verts (shared): per cleft 5 floor verts [top..bottom]; support wall verts per cleft per sup per side
crotch=[]; wallL=[]; wallR=[]
for ci,rec in enumerate(clefts):
    ids=[]
    for lv,pth in rec:
        fp=to3(pth[-1][0],lv); ids.append(add(fp,srccol(fp) if not S.get('crotchcol') else S['crotchcol']))
    crotch.append(ids)
    wl=[];wr=[]
    for sd in SUP:
        wl.append([add(wall_at(pth,lv,sd,-1,S['clefts'][ci]['dir']),S['digits'][ci]['col']) for lv,pth in rec])
        wr.append([add(wall_at(pth,lv,sd,+1,S['clefts'][ci]['dir']),S['digits'][ci+1]['col']) for lv,pth in rec])
    wallL.append(wl); wallR.append(wr)
# ---------- digit outer sides (no cleft): medial side of digit 0, lateral side of last digit ----------
def side_col(ref_ids,side):
    # outer-side column: for each reference vertex, slice normal to D through it; among loop points at the same SL level
    # (+-0.2) take the extreme along side*RT
    row=[]; ax=int(np.argmax(np.abs(D)))
    for vid in ref_ids:
        p=np.array(NV[vid]); L=sl_loops(ax,p[ax]); Q=np.vstack(L)
        m=(np.abs(Q[:,SL]-p[SL])<0.2)&(np.linalg.norm(Q-p,axis=1)<S['sidesearch'])
        Qm=Q[m] if m.any() else Q[np.linalg.norm(Q-p,axis=1)<S['sidesearch']]
        row.append(Qm[np.argmax((Qm@RT)*side)])
    return row
def tb_point(pa,pb,sgn):
    # top (sgn=1) / bottom (-1) of the digit between side points pa,pb: slice normal to D at their mean, extreme along UP
    c=0.5*(pa+pb); ax=int(np.argmax(np.abs(D))); L=sl_loops(ax,c[ax]); Q=np.vstack(L)
    lo,hi=sorted([pa@RT,pb@RT]); m=((Q@RT)>lo)&((Q@RT)<hi)&(np.linalg.norm(Q-c,axis=1)<S['tbsearch'])
    Qm=Q[m] if m.any() else Q[np.linalg.norm(Q-c,axis=1)<S['tbsearch']]
    return Qm[np.argmax((Qm@UP)*sgn)]
dig_rings=[]
for di,dg in enumerate(S['digits']):
    # left side columns (L1,L2,L3 + TL, BL) and right side (TR,R1,R2,R3,BR) for ring0 and support rings
    rings=[]
    for r in range(len(SUP)+1):
        if di<nd-1: Rc=crotch[di] if r==0 else wallL[di][r-1]
        if di>0: Lc=crotch[di-1] if r==0 else wallR[di-1][r-1]
        if di==0: Lc=[add(p,dg['col']) for p in side_col(Rc,-1)]
        if di==nd-1: Rc=[add(p,dg['col']) for p in side_col(Lc,+1)]
        T=add(tb_point(np.array(NV[Lc[0]]),np.array(NV[Rc[0]]),1),dg['col'])
        B=add(tb_point(np.array(NV[Lc[-1]]),np.array(NV[Rc[-1]]),-1),dg['col'])
        rings.append([T,Rc[0],Rc[1],Rc[2],Rc[3],Rc[4],B,Lc[4],Lc[3],Lc[2],Lc[1],Lc[0]])
    # free rings from slices normal to D
    def dslice_ring(cen):
        cen=np.array(cen,float)
        ax=int(np.argmax(np.abs(D)))
        loops=[P for P,c in slice_loops(ax,cen[ax]+1.3e-4) if c]
        best=None
        for P in loops:
            dd=np.linalg.norm(P.mean(0)-cen)
            if best is None or dd<best[0]: best=(dd,P)
        P=best[1]
        # arc-length resample 12 starting at the top, going towards RT
        k0=int(np.argmax(P@UP)); P=np.roll(P,-k0,axis=0)
        if (P[min(3,len(P)-1)]-P[0])@RT<0: P=np.vstack([P[:1],P[1:][::-1]])
        Q=np.vstack([P,P[:1]]); s=np.r_[0,np.cumsum(np.linalg.norm(np.diff(Q,axis=0),axis=1))]
        pts=[]
        for u in np.arange(12)/12*s[-1]:
            k=int(np.clip(np.searchsorted(s,u),1,len(s)-1)); al=(u-s[k-1])/max(s[k]-s[k-1],1e-12); pts.append(Q[k-1]+(Q[k]-Q[k-1])*al)
        return pts, best[0]
    for t in dg['free']:
        pts,dd=dslice_ring(t); assert dd<dg.get('maxcen',2.5),('free ring off-axis',di,t,dd)
        rings.append([add(p,dg['col']) for p in pts])
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
for rings in dig_rings:
    for a,b in zip(rings[:-1],rings[1:]):
        for i in range(12): Fn.append([a[i],a[(i+1)%12],b[(i+1)%12],b[i]])
    l=rings[-1]
    if S.get('tipcap',True):
        P=np.array([NV[v] for v in l]); c=P.mean(0)
        idx=kS.query_ball_point(c,S.get('tipsearch',2.0)); Q=SRC[idx]
        hw=np.abs((P-c)@RT).max(); hh=np.abs((P-c)@UP).max()
        Q=Q[((Q-c)@D>0)&(np.abs((Q-c)@RT)<0.8*hw)&(np.abs((Q-c)@UP)<0.8*hh)] if len(Q) else Q
        tipP=Q[np.argmax(Q@D)] if len(Q) else c+D*0.3
        t=[]
        for k in range(4):
            dk=0.5*(P[(3*k+1)%12]+P[(3*k+2)%12])-c
            t.append(add(tipP-D*S.get('tipback',0.2)+S.get('tipspread',0.45)*dk,NC[l[0]]))
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
