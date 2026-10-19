# t1rebuild.py SIDE IN.npz IN_col.npy RINGS.json OUT.npz
# Rebuild the trunk-side ring T1 of an axilla band so it has the same column count as JT (quads JT->T1),
# then connect T1 -> outer loop with cells. Removes old T1 and the JT-T1 / T1-outer faces.
import numpy as np, sys, json, os
from scipy.spatial import cKDTree
from orient import orient_patch, check
from holeloop import hole_loops
side,inp,colp,rp,out=sys.argv[1:6]
z=np.load(inp); V=z['V'].astype(float).tolist(); F=[list(map(int,f[f>=0])) for f in z['F']]; cc=np.load(colp).tolist()
RR=json.load(open(rp)); R=RR[side]
S=np.load('/home/claude/stc/rp1/weld.npz')['V'].astype(float); scol=np.load('col_r2.npy'); ST=S[scol==1]; kdT=cKDTree(ST)
JT=R['JT']; T1=set(R['T1']); JTs=set(JT)
Vn=np.array(V)
# hole: faces touching old T1
hole=[k for k,f in enumerate(F) if set(f)&T1]
L=hole_loops(F,hole)
assert len(L)==2,[len(l) for l in L]
outer=[l for l in L if not (set(l)&JTs)][0]; inner=[l for l in L if set(l)&JTs][0]
assert set(inner)==JTs, ('inner loop is not JT', len(inner), len(JT))
c2=Vn[R['A3']].mean(0); Jc=Vn[R['J']].mean(0); a=Jc-c2; a/=np.linalg.norm(a)
u=np.cross(a,[0,1.0,0]); u/=np.linalg.norm(u); v=np.cross(a,u)
ang=lambda P:np.arctan2((P-c2)@v,(P-c2)@u)
def at_angle(P,th):
    Q=np.vstack([P,P[:1]]); t=np.unwrap(ang(Q))
    if t[-1]<t[0]: Q=Q[::-1]; t=np.unwrap(ang(Q))
    th=t[0]+((th-t[0])%(2*np.pi))
    for k in range(len(Q)-1):
        if t[k]<=th<=t[k+1]: al=(th-t[k])/(t[k+1]-t[k]) if t[k+1]!=t[k] else 0; return Q[k]+(Q[k+1]-Q[k])*al
    return Q[int(np.argmin(np.abs(np.angle(np.exp(1j*(t-th))))))]
PO=Vn[outer]; FT=float(os.environ.get('FT','0.5'))
newT=[]
for j in JT:
    th=float(ang(Vn[j][None])[0]); o=at_angle(PO,th); p=Vn[j]+FT*(o-Vn[j])
    if os.environ.get('OFFD'):
        i=JT.index(j); w=Vn[R['WT0.5'][i]] if 'WT0.5' in R else Vn[R['J'][i]]; dvec=Vn[j]-w; dvec/=np.linalg.norm(dvec)+1e-9; p=Vn[j]+float(os.environ['OFFD'])*dvec
    newT.append(ST[kdT.query(p)[1]])
F2=[f for k,f in enumerate(F) if k not in set(hole)]
ids=[]
for p in newT: V.append(np.asarray(p).tolist()); cc.append(1); ids.append(len(V)-1)
M=len(JT)
Fn=[[JT[i],JT[(i+1)%M],ids[(i+1)%M],ids[i]] for i in range(M)]
def fr(l):
    P=np.array([V[i] for i in l]); th0=float(ang(Vn[JT[0]][None])[0]); return ((ang(P)-th0)/(2*np.pi))%1.0
def sorted_loop(l):
    P=np.array([V[i] for i in l]); t=np.unwrap(ang(np.vstack([P,P[:1]]))); return l if t[-1]>t[0] else l[::-1]
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
def frac_arc(l):
    P=np.array([V[i] for i in l]); Q=np.vstack([P,P[:1]]); s_=np.r_[0,np.cumsum(np.linalg.norm(np.diff(Q,axis=0),axis=1))]; return s_[:-1]/s_[-1]
Ts=ids
Po=np.array([V[i] for i in outer]); k0=int(np.argmin(np.linalg.norm(Po-np.array(V[Ts[0]]),axis=1)))
o1=outer[k0:]+outer[:k0]; o2=[o1[0]]+o1[1:][::-1]
def corr(o):
    fo=frac_arc(o); f1=frac_arc(Ts); Pq=np.array([V[i] for i in o]); Pr=np.array([V[i] for i in Ts])
    return sum(np.linalg.norm(Pq[int(np.argmin(np.abs(((fo-f+0.5)%1)-0.5)))]-Pr[j]) for j,f in enumerate(f1))
Os=o1 if corr(o1)<corr(o2) else o2
if len(Ts)<=len(Os): Fn+=cells(Ts,Os,frac_arc(Ts),frac_arc(Os))
else: Fn+=cells(Os,Ts,frac_arc(Os),frac_arc(Ts))
Fn=orient_patch(F2,Fn); G=F2+Fn; d,b=check(G)
if d or b:
    import collections
    de=collections.Counter((f[i],f[(i+1)%len(f)]) for f in G for i in range(len(f)))
    dd=[e for e,c in de.items() if c>1][:5]; print('dup',dd)
    for e in dd[:2]: print([f for f in G if e[0] in f and e[1] in f], e[0] in ids, e[1] in ids, e[0] in JT, e[1] in JT)
    raise SystemExit('topology dup %d bnd %d'%(d,b))
used=sorted(set(i for f in G for i in f)); remap={o:n for n,o in enumerate(used)}
V2=np.array([V[i] for i in used]); G2=[[remap[i] for i in f] for f in G]; cc2=np.array([cc[i] for i in used])
Fa=np.full((len(G2),4),-1)
for k,f in enumerate(G2): Fa[k,:len(f)]=f
np.savez_compressed(out,V=V2,F=Fa); np.save(out.replace('.npz','_col.npy'),cc2)
for sd in RR:
    for k in list(RR[sd]): RR[sd][k]=[remap[i] for i in RR[sd][k] if i in remap]
RR[side]['T1']=[remap[i] for i in ids]
json.dump(RR,open(out.replace('.npz','_rings.json'),'w'))
print(side,'V',len(V2),'F',len(G2),'tris',sum(len(f)==3 for f in G2),'outer',len(outer),'removed',len(Vn)+M-len(V2))
