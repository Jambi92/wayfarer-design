# tagloops.py CAGE.npz PROD.npz OUT.json : authored (tagged) cage loops -> exact production edge loops (vertex id paths),
# by replaying the Catmull-Clark topology (each cage edge u-v becomes u, mid(u,v), v at every level).
import numpy as np, sys, json
sys.path.insert(0,'/tmp/claude-0/rt')
from subproj import compact, cc
from common import PID
z=np.load(sys.argv[1]); V=z['V']; Q=z['Q']; FPn=z['FP']; tags=json.loads(str(z['tags']))
FP=np.array([PID[p] for p in FPn])
V,Q,cmap=compact(V,Q,True)
paths={k:[int(cmap[i]) for i in v] for k,v in tags.items()}
E0=set(map(tuple,np.unique(np.sort(np.concatenate([Q[:,[0,1]],Q[:,[1,2]],Q[:,[2,3]],Q[:,[3,0]]]),1),axis=0).tolist()))
bad=[k for k,p in paths.items() if min(p)<0 or any((min(p[i],p[(i+1)%len(p)]),max(p[i],p[(i+1)%len(p)])) not in E0 for i in range(len(p)))]
print('dropped (not closed edge loops in the final cage):',bad)
for k in bad: paths.pop(k)
for L in range(3):
    E=np.concatenate([Q[:,[0,1]],Q[:,[1,2]],Q[:,[2,3]],Q[:,[3,0]]]); Es=np.sort(E,1)
    ue=np.unique(Es,axis=0); nV=len(V)
    key={(int(a),int(b)):i for i,(a,b) in enumerate(ue)}
    for k,p in paths.items():
        q=[]
        for i in range(len(p)):
            a,b=p[i],p[(i+1)%len(p)]; q.append(a); q.append(nV+key[(min(a,b),max(a,b))])
        paths[k]=q
    V,Q,FP=cc(V,Q,FP)
P=np.load(sys.argv[2]); assert np.array_equal(P['Q'],Q),'topology mismatch'
json.dump(paths,open(sys.argv[3],'w'))
print(len(paths),'loops',sum(len(v) for v in paths.values()),'verts')
