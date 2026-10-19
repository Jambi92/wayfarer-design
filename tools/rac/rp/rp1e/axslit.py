# axslit.py SIDE IN.npz IN_col.npy RINGS.json OUT.npz
# Local redesign of an axilla junction band: replaces rings JA/J/JT (18 uniform columns) by M columns sampled
# on the junction polyline (axJ_SIDE.npz) with extra density on the creases, plus optional slit-wall rings.
# env: M (cols, default 30), WF (front-crease weight, 3), WB (back-crease weight, 1.5),
#      WALL (fractions lip->tip for wall rings, e.g. "0.5"), JNPZ (junction polyline file)
import numpy as np, sys, json, os
from scipy.spatial import cKDTree
from orient import orient_patch, check
side,inp,colp,rp,out=sys.argv[1:6]
z=np.load(inp); V=z['V'].astype(float).tolist(); F=[list(map(int,f[f>=0])) for f in z['F']]; cc=np.load(colp).tolist()
R=json.load(open(rp))[side]
S=np.load('/home/claude/stc/rp1/weld.npz')['V'].astype(float); scol=np.load(os.environ.get('SRCCOL','col_r2.npy'))
arm=int(os.environ.get('ARMCOL', 5 if side=='R' else 4)); trunk=1
SA=S[scol==arm]; kdA=cKDTree(SA); ST=S[scol==trunk]; kdT=cKDTree(ST)
Jd=np.load(os.environ.get('JNPZ','axJ_%s.npz'%side)); J,JA,JT=Jd['J'],Jd['JA'],Jd['JT']
Vn=np.array(V)
c2=Vn[R['A3']].mean(0); a=J.mean(0)-c2; a/=np.linalg.norm(a)
u=np.cross(a,[0,1.0,0]); u/=np.linalg.norm(u); v=np.cross(a,u)
ang=lambda P:np.arctan2((P-c2)@v,(P-c2)@u)
def orient(P):
    t=np.unwrap(ang(np.vstack([P,P[:1]]))); return P if t[-1]>t[0] else P[::-1]
def at_angle(P,th):
    P=orient(P); Q=np.vstack([P,P[:1]]); t=np.unwrap(ang(Q)); t0=t[0]; th=t0+((th-t0)%(2*np.pi))
    for k in range(len(Q)-1):
        if t[k]<=th<=t[k+1] or t[k]>=th>=t[k+1]:
            al=(th-t[k])/(t[k+1]-t[k]) if t[k+1]!=t[k] else 0; return Q[k]+(Q[k+1]-Q[k])*al
    k=int(np.argmin(np.abs(np.angle(np.exp(1j*(t-th)))))); return Q[k]
# weighted arc length on J: crease points get weight
Jo=orient(J); Q=np.vstack([Jo,Jo[:1]]); seg=np.linalg.norm(np.diff(Q,axis=0),axis=1)
mid=0.5*(Q[:-1]+Q[1:])
sg=1 if side=='R' else -1
front=(mid[:,1]<-35.5)&(mid[:,2]<153.8); back=(mid[:,1]>-27.5)&(mid[:,2]<155.5)
w=np.where(front,float(os.environ.get('WF','3')),np.where(back,float(os.environ.get('WB','1.5')),1.0))
s=np.r_[0,np.cumsum(seg*w)]
M=int(os.environ.get('M','30')); OFF=float(os.environ.get('JOFF','0.0'))
th=[]; nJ=[]; nA=[]; nT=[]
# lip offsets carried along J by arc length (keeps lips in J order)
same=np.allclose(orient(J)[0],J[0]) and np.allclose(orient(J)[1],J[1])
JAo=JA if same else JA[::-1]; JTo=JT if same else JT[::-1]
OA=np.vstack([JAo-Jo,(JAo-Jo)[:1]]); OT=np.vstack([JTo-Jo,(JTo-Jo)[:1]])
for x in (np.arange(M)+OFF)/M*s[-1]:
    k=int(np.clip(np.searchsorted(s,x),1,len(s)-1)); al=(x-s[k-1])/(s[k]-s[k-1]); p=Q[k-1]+(Q[k]-Q[k-1])*al; th.append(float(ang(p[None])[0]))
    nJ.append(p); nA.append(p+OA[k-1]+(OA[k]-OA[k-1])*al); nT.append(p+OT[k-1]+(OT[k]-OT[k-1])*al)
th=np.array(th); nJ=np.array(nJ); nA=np.array(nA); nT=np.array(nT)
nJ=S[cKDTree(S).query(nJ)[1]]
if os.environ.get('LIPPROJ','1')=='1': nA=SA[kdA.query(nA)[1]]; nT=ST[kdT.query(nT)[1]]
elif os.environ.get('LIPPROJ')=='2': _k=cKDTree(S); nA=S[_k.query(nA)[1]]; nT=S[_k.query(nT)[1]]
rings=[('JA',nA,arm)]
WALL=[float(x) for x in os.environ.get('WALL','').split(',') if x]
kdS=cKDTree(S)
cm=((nJ[:,1]<-35.5)&(nJ[:,2]<153.8))|((nJ[:,1]>-27.5)&(nJ[:,2]<155.5))
def wallp(L,f,kd,SS):
    P=L+f*(nJ-L); return np.where(cm[:,None],SS[kd.query(P)[1]],S[kdS.query(P)[1]])
for f in WALL: rings.append(('WA%g'%f,wallp(nA,f,kdA,SA),arm))
rings.append(('J',nJ,int(os.environ.get('JCOL',arm))))
for f in WALL[::-1]: rings.append(('WT%g'%f,wallp(nT,f,kdT,ST),trunk))
rings.append(('JT',nT,trunk))
# remove old band faces (strips A4-JA, JA-J, J-JT, JT-T1)
old=set(R['JA'])|set(R['J'])|set(R['JT'])
band=set(R['A4'])|old|set(R['T1'])
rm=[k for k,f in enumerate(F) if set(f)<=band and set(f)&old]
F=[f for k,f in enumerate(F) if k not in set(rm)]
ids={}
for nm,P,c in rings:
    ids[nm]=[]
    for p in P: V.append(np.asarray(p).tolist()); cc.append(int(c)); ids[nm].append(len(V)-1)
def frac_ang(l):
    P=np.array([V[i] for i in l]); t=np.unwrap(ang(np.vstack([P,P[:1]]))); return ((t[:-1]-t[0])/(t[-1]-t[0]))
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
# A4 -> JA (cells: absolute angle fractions about the same frame, so phase-aligned)
def fr(l):
    P=np.array([V[i] for i in l]); return ((ang(P)-th[0])/(2*np.pi))%1.0
A4=sorted_loop(R['A4']); T1=sorted_loop(R['T1'])
order=[r[0] for r in rings]
Fn=cells(A4,ids['JA'],fr(A4),fr(ids['JA']))
for k in range(len(order)-1):
    a_,b_=ids[order[k]],ids[order[k+1]]
    for i in range(M): Fn.append([a_[i],b_[i],b_[(i+1)%M],a_[(i+1)%M]])
Fn+=cells(T1,ids['JT'],fr(T1),fr(ids['JT']))
Fn=orient_patch(F,Fn); F2=F+Fn; dup,bnd=check(F2)
if dup or bnd:
    import collections
    de=collections.Counter((f[i],f[(i+1)%len(f)]) for f in F2 for i in range(len(f)))
    print('dup',[e for e,n in de.items() if n>1]); print('bnd',[e for e in de if (e[1],e[0]) not in de])
    raise SystemExit('topology dup %d bnd %d'%(dup,bnd))
used=sorted(set(i for f in F2 for i in f)); remap={o:n for n,o in enumerate(used)}
V2=np.array([V[i] for i in used]); F3=[[remap[i] for i in f] for f in F2]; cc2=np.array([cc[i] for i in used])
Fa=np.full((len(F3),4),-1)
for k,f in enumerate(F3): Fa[k,:len(f)]=f
np.savez_compressed(out,V=V2,F=Fa); np.save(out.replace('.npz','_col.npy'),cc2)
# carry ring ids
newR=json.load(open(rp))
for sd in newR:
    for k in list(newR[sd]): newR[sd][k]=[remap[i] for i in newR[sd][k] if i in remap]
newR[side]={**{k:newR[side][k] for k in ('A3','A4','T1')},**{k:[remap[i] for i in l] for k,l in ids.items()}}
json.dump(newR,open(out.replace('.npz','_rings.json'),'w'))
print(side,'V',len(V2),'F',len(F3),'tris',sum(len(f)==3 for f in F3),'removed faces',len(rm))
