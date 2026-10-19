import numpy as np, collections, subprocess
from scipy.spatial import cKDTree
subprocess.run(['/home/claude/stc/bin/python3','blendcage.py','--','/mnt/user-data/uploads/RaceBodies/production/Gorrund/RP1/GO_U_REF_RP1E_retopo_v006.blend','ui_cur.npz'],capture_output=True)
U=np.load('ui_cur.npz'); G=np.load('cage_g5b.npz')
F=[tuple(f[f>=0]) for f in U['F']]; e=collections.Counter()
for f in F:
    for i in range(len(f)): e[tuple(sorted((f[i],f[(i+1)%len(f)])))]+=1
print('UI V',len(U['V']),'F',len(F),'E',len(e),'bnd',sum(1 for v in e.values() if v==1),'nm',sum(1 for v in e.values() if v>2),'euler',len(U['V'])-len(e)+len(F))
d,i=cKDTree(G['V']).query(U['V']); print('max dist cm %.4f'%d.max(),'unique',len(set(i)))
FU=set(frozenset(i[f[f>=0]]) for f in U['F']); FG=set(frozenset(f[f>=0]) for f in G['F'])
print('faces only UI',len(FU-FG),'only g5b',len(FG-FU))
for f in FU-FG: print('  extra',np.round(G['V'][list(f)],2).tolist())
