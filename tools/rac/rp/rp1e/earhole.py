import numpy as np, collections, sys, json
s=sys.argv[1]; R=float(sys.argv[2]); cg=sys.argv[3] if len(sys.argv)>3 else 'cage_g5b.npz'
z=np.load(cg); V=z['V']; F=[list(f[f>=0]) for f in z['F']]
w=np.load('/home/claude/stc/rp1/weld.npz'); S=w['V']; d=np.load('sim_b4_L3_dsp.npy')
e=np.load('ear_%s.npy'%s); P=S[e]; floor=P[d[e]>=np.percentile(d[e],95)].mean(0)
mouth=S[np.load('earroot_%s.npy'%s)].mean(0); A=mouth-floor; A/=np.linalg.norm(A); u=np.cross(A,[0,0,1.0]); u/=np.linalg.norm(u); v=np.cross(A,u)
fc=np.array([V[f].mean(0) for f in F]); X=fc-floor; h=X@A; rr=np.linalg.norm(X-np.outer(h,A),axis=1)
sg=1 if s=='L' else -1
reg=set(k for k in range(len(F)) if rr[k]<R and -14<h[k]<14 and (fc[k][0]*sg)>3 and fc[k][2]>184)
e2f=collections.defaultdict(list)
for k,f in enumerate(F):
    for i in range(len(f)): e2f[tuple(sorted((f[i],f[(i+1)%len(f)])))].append(k)
def loops_of(reg):
    ed=collections.Counter()
    for k in reg:
        f=F[k]
        for i in range(len(f)): ed[(f[i],f[(i+1)%len(f)])]+=1
    bnd={a:b for (a,b),n in ed.items() if (b,a) not in ed}; seen=set(); L=[]
    for a in list(bnd):
        if a in seen: continue
        l=[a]; seen.add(a)
        while bnd[l[-1]]!=a: l.append(bnd[l[-1]]); seen.add(l[-1])
        L.append(l)
    return L
# fill: flood the complement from a far face; anything not reached is interior -> add
comp=set(range(len(F)))-reg; far=max(comp,key=lambda k:np.linalg.norm(fc[k]-floor)); seen={far}; st=[far]
while st:
    k=st.pop(); f=F[k]
    for i in range(len(f)):
        for q in e2f[tuple(sorted((f[i],f[(i+1)%len(f)])))]:
            if q in comp and q not in seen: seen.add(q); st.append(q)
reg|=comp-seen
L=loops_of(reg); lp=max(L,key=len); B=V[lp]; X=B-floor; th=np.degrees(np.unwrap(np.arctan2(X@v,X@u))); hb=X@A; rb=np.linalg.norm(X-np.outer(hb,A),axis=1)
mono=np.all(np.diff(th)>0) or np.all(np.diff(th)<0)
print(s,'R',R,'faces',len(reg),'loops',[len(l) for l in L],'monotone',mono,'turn %.0f'%(th[-1]-th[0]),'r min %.1f'%rb.min(),'h range %.1f..%.1f'%(hb.min(),hb.max()))
json.dump(dict(reg=sorted(int(k) for k in reg),loop=[int(x) for x in lp]),open('earhole_%s.json'%s,'w'))
