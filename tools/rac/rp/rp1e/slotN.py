# slotN.py IN.npz IN_col.npy OUT.npz a b c(face-side vertex lists) : insert vertex N on edge a-b at position P, splitting the two faces into quad+tri
import numpy as np, sys, json
from orient import check
z=np.load(sys.argv[1]); V=z['V'].tolist(); F=[list(map(int,f[f>=0])) for f in z['F']]; cc=np.load(sys.argv[2]).tolist()
a,b=int(sys.argv[4]),int(sys.argv[5]); P=[float(t) for t in sys.argv[6].split(',')]
V.append(P); N=len(V)-1; cc.append(cc[a])
G=[]
for f in F:
    n=len(f)
    if a in f and b in f:
        i=f.index(a); j=f.index(b)
        if (i+1)%n==j: k=i
        elif (j+1)%n==i: k=j
        else: G.append(f); continue
        g=f[:k+1]+[N]+f[k+1:]   # polygon with N inserted
        # split polygon (5) into quad + tri: tri = (prev(N), N, ...)? choose tri containing N and the vertex opposite the shorter side
        m=len(g); t=g.index(N)
        if m==4: G.append(g); continue
        # option: quad = N + next 3 verts; tri = N, vertex 3 ahead, vertex before N
        q=[g[(t+s)%m] for s in range(4)]; tr=[g[(t+3)%m],g[(t+4)%m],N]
        G+= [q,tr]
    else: G.append(f)
d,bn=check(G); print('dup',d,'bnd',bn)
Fa=np.full((len(G),4),-1)
for k,f in enumerate(G): Fa[k,:len(f)]=f
np.savez_compressed(sys.argv[3],V=np.array(V),F=Fa); np.save(sys.argv[3].replace('.npz','_col.npy'),np.array(cc)); print('N',N)
