# facering.py CAGE F0 E0a E0b : walk a quad face ring starting at face F0 across its edge (E0a,E0b) (rung), printing rungs
import numpy as np, sys, collections, json
z=np.load(sys.argv[1]); V=z['V']; F=[list(map(int,f[f>=0])) for f in z['F']]
e2f=collections.defaultdict(list)
for k,f in enumerate(F):
    for i in range(len(f)): e2f[frozenset((f[i],f[(i+1)%len(f)]))].append(k)
f0=int(sys.argv[2]); a,b=int(sys.argv[3]),int(sys.argv[4])
ring=[]; rungs=[(a,b)]; f=f0; e=frozenset((a,b))
while True:
    q=F[f]; assert len(q)==4, ('non-quad',f,q)
    i=[k for k in range(4) if frozenset((q[k],q[(k+1)%4]))==e][0]
    # opposite edge
    c,d=q[(i+2)%4],q[(i+3)%4]
    # keep orientation: rung (a,b) where a adjacent to q[i]...
    pa=q[i]; pb=q[(i+1)%4]
    # opposite: q[(i+3)%4] adjacent to pa, q[(i+2)%4] adjacent to pb
    na,nb=q[(i+3)%4],q[(i+2)%4]
    ring.append(f); e=frozenset((na,nb)); rungs.append((na,nb))
    nf=[g for g in e2f[e] if g!=f]
    if not nf or nf[0]==f0: break
    f=nf[0]
print('faces',len(ring)); 
for r in rungs: print(r, V[r[0]].round(1), V[r[1]].round(1))
json.dump(dict(faces=ring,rungs=rungs),open(sys.argv[5],'w'))
