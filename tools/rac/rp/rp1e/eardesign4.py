"""Ear sub-cage v4 = v3 crescent rings + concha canal pocket.
python3 eardesign4.py SIDE CAGE COL HOLEJSON OUT XS MI0 MI1 PYS   (env MY=mouth y, TA=lerp for T)
One transition ring T (lerp TA of B->R0). Mouth = faces between T and R0 for ring indices MI0..MI1-1 (removed);
T[MI0..MI1] are placed on the left (inner) edge of the canal mouth; pocket rings = source y-slice loops at PYS; zip cap."""
import numpy as np, sys, json, os
from earsl import slice_loops, resample, S
s,cin,colin,hj,out,xs,MI0,MI1,pys=sys.argv[1:10]; xs=[float(x) for x in xs.split(',')]; MI0=int(MI0); MI1=int(MI1); pys=[float(x) for x in pys.split(',')]
sg=1 if s=='L' else -1; MX=lambda x: x if s=='L' else 4-x; MY=float(os.environ.get('MY','-48')); TA=float(os.environ.get('TA','0.5'))
z=np.load(cin); V=z['V'].astype(float).tolist(); F=[list(map(int,f[f>=0])) for f in z['F']]; cc=np.load(colin).tolist()
H=json.load(open(hj)); hole=set(H['reg']); loop=list(H['loop']); NB=len(loop); B=np.array([V[i] for i in loop])
def area(P,i,j): a,b=P[:,i],P[:,j]; return 0.5*np.sum(a*np.roll(b,-1)-np.roll(a,-1)*b)
rings=[]
for x in xs:
    L=slice_loops(0,x if s=='L' else 4-x,lambda P:(P[:,2]>183)&(P[:,1]<-30)&(P[:,1]>-62))
    P=max([P for P,c in L if c],key=len)
    if np.sign(area(P,1,2))!=np.sign(area(B,1,2)): P=P[::-1]
    rings.append(resample(P,NB,int(np.argmin(P[:,1]))))
def align(R,ref,cols=(1,2)):
    c=list(cols); n=len(R); best=min(range(n),key=lambda sh:np.linalg.norm(np.roll(R,-sh,axis=0)[:,c]-ref[:,c],axis=1).sum()); return np.roll(R,-best,axis=0)
rings[0]=align(rings[0],B)
for k in range(1,len(rings)): rings[k]=align(rings[k],rings[k-1])
R0=rings[0]; T=(1-TA)*B+TA*R0
for it in range(int(os.environ.get('TS','0'))): T=0.5*T+0.25*(np.roll(T,1,axis=0)+np.roll(T,-1,axis=0))
# pocket loops
NM=2*(MI1-MI0+1)
PL=[]
for y in pys:
    L=slice_loops(1,y,lambda P:(P[:,2]>193)&(P[:,2]<202)&(MX(P[:,0])>9)&(MX(P[:,0])<16)); P=max([P for P,c in L if c],key=len); PL.append(P)
# mouth inner edge: from the first pocket loop, the half with smallest |x|
P0=resample(PL[0],64,0); m=P0.mean(0)
nI=MI1-MI0+1; zs=np.linspace(R0[MI0][2],R0[MI1][2],nI)
for k,i in enumerate(range(MI0,MI1+1)):
    zz=np.clip(zs[k],P0[:,2].min()+0.3,P0[:,2].max()-0.3)
    cand=P0[(sg*(P0[:,0]-m[0])<0)]; q=cand[np.argmin(abs(cand[:,2]-zz))].copy(); q[1]=MY; q[2]=zs[k]
    T[i]=q
col0=int(np.bincount([cc[i] for i in loop]).argmax())
F=[f for k,f in enumerate(F) if k not in hole]
def addring(R):
    cur=[]
    for p in R: V.append(np.asarray(p).tolist()); cc.append(col0); cur.append(len(V)-1)
    return cur
iT=addring(T); ids=[iT]
for i in range(NB): F.append([loop[i],loop[(i+1)%NB],iT[(i+1)%NB],iT[i]])
prev=iT
for k,R in enumerate(rings):
    cur=addring(R); ids.append(cur)
    for i in range(NB):
        if k==0 and MI0<=i<MI1: continue
        F.append([prev[i],prev[(i+1)%NB],cur[(i+1)%NB],cur[i]])
    prev=cur
Rl=rings[-1]; i0=int(np.argmax(np.linalg.norm(Rl-Rl.mean(0),axis=1))) if os.environ.get('CAPH','1')=='1' else 0
p=[prev[(i0+k)%NB] for k in range(NB)]; a_,b_=0,NB-1
while b_-a_>=3: F.append([p[a_],p[a_+1],p[b_-1],p[b_]]); a_+=1; b_-=1
if b_-a_==2: F.append([p[a_],p[a_+1],p[a_+2]])
# mouth loop: boundary of removed faces, oriented so that it is a hole boundary consistent with removed faces [T_i,T_i+1,R_i+1,R_i]
mouth=[iT[i] for i in range(MI0,MI1+1)]+[ids[1][i] for i in range(MI1,MI0-1,-1)]
M=np.array([V[i] for i in mouth])
pr=[]
for P in PL:
    if np.sign(area(P,0,2))!=np.sign(area(M,0,2)): P=P[::-1]
    pr.append(resample(P,NM,0))
pr[0]=align(pr[0],M,(0,2))
for k in range(1,len(pr)): pr[k]=align(pr[k],pr[k-1],(0,2))
prev=mouth; pids=[]
for R in pr:
    cur=addring(R); pids.append(cur)
    # removed face orientation: [T_i,T_i+1,R_i+1,R_i]; its edges T_i->T_i+1 ; so the hole boundary in the remaining mesh runs T_i+1->T_i. face along mouth edge (a->b) in the mouth list order must use b->a? decide by edge test below
    for i in range(NM): F.append([prev[i],prev[(i+1)%NM],cur[(i+1)%NM],cur[i]])
    prev=cur
p=prev; a_,b_=0,NM-1
while b_-a_>=3: F.append([p[a_],p[a_+1],p[b_-1],p[b_]]); a_+=1; b_-=1
if b_-a_==2: F.append([p[a_],p[a_+1],p[a_+2]])
# orientation check: every directed edge once
import collections
used=sorted(set(i for f in F for i in f)); remap={o:n for n,o in enumerate(used)}
V2=np.array([V[i] for i in used]); F2=[[remap[i] for i in f] for f in F]; cc2=np.array([cc[i] for i in used])
de=collections.Counter((f[i],f[(i+1)%len(f)]) for f in F2 for i in range(len(f)))
bad=sum(1 for e,n in de.items() if n>1); bnd=sum(1 for (a,b) in de if (b,a) not in de)
Fa=np.full((len(F2),4),-1)
for k,f in enumerate(F2): Fa[k,:len(f)]=f
np.savez_compressed(out,V=V2,F=Fa); np.save(out.replace('.npz','_col.npy'),cc2)
json.dump(dict(side=s,hole=sorted(hole),loop=[remap[i] for i in loop],loop_orig=loop,rings=[[remap[i] for i in r] for r in ids],pocket=[[remap[i] for i in r] for r in pids],
   mouth=[remap[i] for i in mouth],xs=xs,pys=pys,MI=[MI0,MI1],MY=MY,TA=TA,removed=[i for i in range(len(z['V'])) if i not in remap]),open(out.replace('.npz','_ear%s.json'%s),'w'))
print(s,'NB',NB,'V',len(V2),'F',len(F2),'dup-directed',bad,'boundary-edges',bnd)
