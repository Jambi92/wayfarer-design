# axdesign.py SIDE CAGE COL HOLE.json RING2.json(list of rings; index 2) OUT [N]
# Axilla annulus sub-cage: ring2 (arm, kept) -> A3, A4 (arm) -> JA (arm lip) -> J (crease/apex) -> JT (trunk lip) -> T1 -> outer loop (kept)
import numpy as np, sys, json, collections, os
from scipy.spatial import cKDTree
from holeloop import hole_loops
side,cg,colf,hj,rj,out=sys.argv[1:7]; N=int(sys.argv[7]) if len(sys.argv)>7 else 18
S=np.load('/home/claude/stc/rp1/weld.npz')['V']; scol=np.load(os.environ.get('SRCCOL','col_r1.npy')); arm=int(os.environ['ARMCOL']) if 'ARMCOL' in os.environ else (5 if side=='R' else 4)
kdA=cKDTree(S[scol==arm]); SA=S[scol==arm]; kdT=cKDTree(S[scol==1]); ST=S[scol==1]
z=np.load(cg); V=z['V'].astype(float).tolist(); F=[list(map(int,f[f>=0])) for f in z['F']]; cc=np.load(colf).tolist()
hole=json.load(open(hj))['reg']; ring2=json.load(open(rj))[2]
L=hole_loops(F,hole); inner=[l for l in L if set(l)==set(ring2)][0]; outer=[l for l in L if set(l)!=set(ring2)][0]
Jd=np.load(os.environ.get('RINGNPZ','axJ_%s.npz'%side)); J,JA,JT=Jd['J'],Jd['JA'],Jd['JT']
Vn=np.array(V)
c2=Vn[inner].mean(0); cJ=J.mean(0); a=cJ-c2; a/=np.linalg.norm(a)
u=np.cross(a,[0,1.0,0]); u/=np.linalg.norm(u); v=np.cross(a,u)
ang=lambda P:np.arctan2((P-c2)@v,(P-c2)@u)
def orient(P):  # make polyline angle increasing
    t=np.unwrap(ang(np.vstack([P,P[:1]])))
    return P if t[-1]>t[0] else P[::-1]
def at_angle(P,th):
    P=orient(P); Q=np.vstack([P,P[:1]]); t=np.unwrap(ang(Q)); t0=t[0]
    # shift th into [t0, t0+2pi)
    th=t0+((th-t0)%(2*np.pi))
    for k in range(len(Q)-1):
        if t[k]<=th<=t[k+1] or t[k]>=th>=t[k+1]:
            al=(th-t[k])/(t[k+1]-t[k]) if t[k+1]!=t[k] else 0; return Q[k]+(Q[k+1]-Q[k])*al
    k=int(np.argmin(np.abs(np.angle(np.exp(1j*(t-th)))))); return Q[k]
# angles: uniform arc length on J
Jo=orient(J); Q=np.vstack([Jo,Jo[:1]]); s=np.r_[0,np.cumsum(np.linalg.norm(np.diff(Q,axis=0),axis=1))]
OFF=float(os.environ.get('JOFF','0.0'))
sv=(np.arange(N)+OFF)/N*s[-1]; th=[]
for x in sv:
    k=int(np.clip(np.searchsorted(s,x),1,len(s)-1)); al=(x-s[k-1])/(s[k]-s[k-1]); p=Q[k-1]+(Q[k]-Q[k-1])*al; th.append(float(ang(p[None])[0]))
th=np.array(th)
R2=Vn[inner]
rings={}
rings['JA']=np.array([at_angle(JA,t) for t in th]); rings['J']=np.array([at_angle(J,t) for t in th]); rings['JT']=np.array([at_angle(JT,t) for t in th])
r2=np.array([at_angle(R2,t) for t in th]); ro=np.array([at_angle(Vn[outer],t) for t in th])
f3=float(os.environ.get('F3','0.34')); f4=float(os.environ.get('F4','0.67')); ft=float(os.environ.get('FT','0.5'))
A3=r2+f3*(rings['JA']-r2); A4=r2+f4*(rings['JA']-r2); T1=rings['JT']+ft*(ro-rings['JT'])
if os.environ.get('PROJ','1')=='1':
    A3=SA[kdA.query(A3)[1]]; A4=SA[kdA.query(A4)[1]]
    if os.environ.get('TPROJ','1')=='1': T1=S[cKDTree(S).query(T1)[1]]
if os.environ.get('T1CLEFT'):
    # natal-cleft override: bottom columns of T1 placed on the cleft (tip at x=xc, walls beside)
    zc,yt,yw,xc=[float(t) for t in os.environ['T1CLEFT'].split(',')]
    Jr=rings['J']
    for k in range(N):
        if Jr[k][2]<105.6:
            dx=Jr[k][0]-xc; y=yt if abs(dx)<0.6 else yw+0.0*dx
            T1[k]=S[cKDTree(S).query([Jr[k][0],y,zc])[1]]
order=[('A3',A3,arm),('A4',A4,arm),('JA',rings['JA'],arm),('J',rings['J'],int(os.environ.get('JCOL',arm))),('JT',rings['JT'],1),('T1',T1,1)]
F=[f for i,f in enumerate(F) if i not in set(hole)]
ids={}
for nm,P,c in order:
    ids[nm]=[]
    for p in P: V.append(np.asarray(p).tolist()); cc.append(int(c)); ids[nm].append(len(V)-1)
def frac_ang(l):
    P=np.array([V[i] for i in l]); t=np.unwrap(ang(np.vstack([P,P[:1]]))); return ((t[:-1]-t[0])/(t[-1]-t[0]))
def frac_arc(l):
    P=np.array([V[i] for i in l]); Q=np.vstack([P,P[:1]]); s_=np.r_[0,np.cumsum(np.linalg.norm(np.diff(Q,axis=0),axis=1))]; return s_[:-1]/s_[-1]
def cells(small,big,fs,fb):
    m=len(small); n=len(big)
    d=lambda x,y: abs(((x-y+0.5)%1.0)-0.5)
    own=[int(np.argmin([d(fs[i],fb[j]) for i in range(m)])) for j in range(n)]
    Fs=[]
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
def sorted_loop(l):
    P=np.array([V[i] for i in l]); t=np.unwrap(ang(np.vstack([P,P[:1]])))
    return l if t[-1]>t[0] else l[::-1]
inner_s=sorted_loop(inner); outer_s=sorted_loop(outer)
# rotate so that ordering by angle is consistent (start anywhere is fine for cells())
Fn=cells(inner_s,ids['A3'],frac_ang(inner_s),frac_ang(ids['A3']))
seq=['A3','A4','JA','J','JT','T1']
for k in range(len(seq)-1):
    a_,b_=ids[seq[k]],ids[seq[k+1]]
    for i in range(N): Fn.append([a_[i],b_[i],b_[(i+1)%N],a_[(i+1)%N]])
# outer: align start + direction by arc length
T1l=ids['T1']; P1=np.array([V[i] for i in T1l]); Po=np.array([V[i] for i in outer])
k0=int(np.argmin(np.linalg.norm(Po-P1[0],axis=1))); o1=outer[k0:]+outer[:k0]; o2=[o1[0]]+o1[1:][::-1]
def corr(o,ref):
    fo=frac_arc(o); f1=frac_arc(ref); Po_=np.array([V[i] for i in o]); Pr=np.array([V[i] for i in ref])
    return sum(np.linalg.norm(Po_[int(np.argmin(np.abs(((fo-f+0.5)%1)-0.5)))]-Pr[j]) for j,f in enumerate(f1))
oo=o1 if corr(o1,T1l)<corr(o2,T1l) else o2
N2=int(os.environ.get('N2','0'))
if N2:
    # intermediate trunk ring T2 with N2 verts: arc-fraction correspondence between T1 and the outer loop
    fo=frac_arc(oo); f1=frac_arc(T1l); Pr=np.array([V[i] for i in oo]); Pt=np.array([V[i] for i in T1l])
    def at_frac(P,fr,f):
        Q=np.vstack([P,P[:1]]); fq=np.r_[fr,1.0]; k=int(np.clip(np.searchsorted(fq,f),1,len(fq)-1)); al=(f-fq[k-1])/max(fq[k]-fq[k-1],1e-9); return Q[k-1]+(Q[k]-Q[k-1])*al
    T2=[]
    for j in range(N2):
        f=j/N2; T2.append(0.5*(at_frac(Pt,f1,f)+at_frac(Pr,fo,f)))
    T2=S[cKDTree(S).query(np.array(T2))[1]]
    ids['T2']=[]
    for p in T2: V.append(np.asarray(p).tolist()); cc.append(1); ids['T2'].append(len(V)-1)
    Fn+=cells(T1l,ids['T2'],frac_arc(T1l),frac_arc(ids['T2']))
    Fn+=cells(ids['T2'],oo,frac_arc(ids['T2']),frac_arc(oo))
else:
    Fn+=cells(T1l,oo,frac_arc(T1l),frac_arc(oo))
from orient import orient_patch, check
Fn=orient_patch(F,Fn); F2=F+Fn; dup,bnd=check(F2)
if dup or bnd: raise SystemExit('topology dup %d bnd %d'%(dup,bnd))
used=sorted(set(i for f in F2 for i in f)); remap={o:n for n,o in enumerate(used)}
V2=np.array([V[i] for i in used]); F3=[[remap[i] for i in f] for f in F2]; cc2=np.array([cc[i] for i in used])
Fa=np.full((len(F3),4),-1)
for k,f in enumerate(F3): Fa[k,:len(f)]=f
np.savez_compressed(out,V=V2,F=Fa); np.save(out.replace('.npz','_col.npy'),cc2)
json.dump(dict(side=side,rings={k:[remap[i] for i in l] for k,l in ids.items()},inner=[remap[i] for i in inner],outer=[remap[i] for i in outer],
   removed=[i for i in range(len(z['V'])) if i not in remap]),open(out.replace('.npz','_ax%s.json'%side),'w'))
print(side,'V',len(V2),'F',len(F3),'tris',sum(len(f)==3 for f in F3))
