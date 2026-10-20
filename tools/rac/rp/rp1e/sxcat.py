import sys; sys.path.insert(0,'/home/claude/stc/rp1e')
import numpy as np, json
from sxfaces import pairs
from collections import Counter
p=sys.argv[1]
z=np.load(p); V=z['V']; F=z['F']; m=json.load(open(p.replace('.npz','_meta.json')))
lab={}
for nm in ('O','M1','M'):
    for v in m[nm]: lab[v]=nm
for c in m['crotch']:
    for v in c: lab[v]='C'
for di,rs in enumerate(m['rings']):
    for k,r in enumerate(rs):
        for v in r: lab.setdefault(v,'t%d.%d'%(di,k))
def fl(f): return '/'.join(sorted(set(lab.get(int(x),'old') for x in f if x>=0)))
b=eval(sys.argv[2]) if len(sys.argv)>2 else ((15,-70,-3),(40,-40,12))
pp=pairs(V,F,(np.array(b[0]),np.array(b[1])))
print(len(pp)); print(Counter((fl(F[a]),fl(F[b])) for a,b in pp).most_common(40))
if len(sys.argv)>3:
    for a,bq in pp: print(fl(F[a]),fl(F[bq]),V[[x for x in F[a] if x>=0]].mean(0).round(1))
