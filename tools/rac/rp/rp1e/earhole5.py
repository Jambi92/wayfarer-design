import numpy as np, collections, sys, json
s=sys.argv[1]; X0=float(sys.argv[2]); Z0=float(sys.argv[3]); grow=int(sys.argv[4]); cg=sys.argv[5] if len(sys.argv)>5 else 'cage_g5b.npz'
z=np.load(cg); V=z['V']; F=[list(f[f>=0]) for f in z['F']]; sg=1 if s=='L' else -1
fc=np.array([V[f].mean(0) for f in F])
mx=lambda x: x if s=='L' else 4-x
reg=set(k for k in range(len(F)) if mx(fc[k][0])>X0 and fc[k][2]>Z0 and -62<fc[k][1]<-30 and fc[k][2]<206)
v2f=collections.defaultdict(list)
for k,f in enumerate(F):
    for i in f: v2f[i].append(k)
for g in range(grow):
    vs=set(i for k in reg for i in F[k]); reg|=set(k for i in vs for k in v2f[i])
import os
for i in [int(x) for x in os.environ.get('ADDV','').split(',') if x]: reg|=set(v2f[i])
ed=collections.Counter()
for k in reg:
    f=F[k]
    for i in range(len(f)): ed[(f[i],f[(i+1)%len(f)])]+=1
bnd={a:b for (a,b) in ed if (b,a) not in ed}; seen=set(); L=[]
for a in list(bnd):
    if a in seen: continue
    l=[a]; seen.add(a)
    while bnd.get(l[-1],a)!=a and len(l)<500: l.append(bnd[l[-1]]); seen.add(l[-1])
    L.append(l)
nv=len(set(i for k in reg for i in F[k]))
print(s,X0,Z0,grow,'faces',len(reg),'verts',nv,'loops',[len(l) for l in L],'euler(disk=1)',nv-len(ed)//1+0)
lp=max(L,key=len)
json.dump(dict(reg=sorted(int(k) for k in reg),loop=[int(x) for x in lp]),open('earhole5_%s.json'%s,'w'))
if len(sys.argv)>6:
  for i in lp: print(i,V[i].round(1))
