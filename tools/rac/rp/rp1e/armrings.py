import numpy as np, json, sys
cg=sys.argv[1]; s=sys.argv[2]; nr=int(sys.argv[3])
z=np.load(cg); V=z['V']; F=z['F']; seg=json.load(open(cg.replace('.npz','_seg.json')))[s]
adj={}
for f in F:
    f=f[f>=0]
    for i in range(len(f)): a,b=f[i],f[(i+1)%len(f)]; adj.setdefault(int(a),set()).add(int(b)); adj.setdefault(int(b),set()).add(int(a))
arm=set(seg['arm']); cur=list(seg['junction']); seen=set(cur); rings=[cur]
for k in range(nr):
    nxt=[]
    for v in cur:
        # neighbour in arm, not seen, roughly 'next ring'
        for u in adj[v]:
            if u in arm and u not in seen: nxt.append(u); seen.add(u)
    # order nxt following cur order
    rings.append(nxt); cur=nxt
for k,r in enumerate(rings):
    print('ring',k,[(v,tuple(V[v].round(1))) for v in r])
json.dump(rings,open(cg.replace('.npz','_armrings_%s.json'%s),'w'))
