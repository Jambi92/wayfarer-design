# growhole.py CAGE HOLE_IN HOLE_OUT INNER_RING_JSON idx : grow the hole by one face ring on the outer boundary only
import numpy as np, json, sys, collections
from holeloop import hole_loops
z=np.load(sys.argv[1]); V=z['V']; F=[list(map(int,f[f>=0])) for f in z['F']]
reg=set(json.load(open(sys.argv[2]))['reg']); inner=set(json.load(open(sys.argv[4]))[int(sys.argv[5])])
L=hole_loops(F,reg); outer=[l for l in L if set(l)!=inner][0]
v2f=collections.defaultdict(list)
for k,f in enumerate(F):
    for v in f: v2f[v].append(k)
add=set(k for v in outer for k in v2f[v] if not (set(F[k])&inner))
reg2=reg|add; L2=hole_loops(F,reg2); print('faces',len(reg2),'loops',[len(l) for l in L2],'nonquad',sum(len(F[k])!=4 for k in reg2))
json.dump(dict(reg=sorted(reg2)),open(sys.argv[3],'w'))
