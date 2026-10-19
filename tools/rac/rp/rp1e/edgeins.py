# edgeins.py IN.npz IN_col.npy OUT.npz "x,y,z;x,y,z" [baseref "x,y,z;..."] : insert a vertex at each point on the cage edge nearest to its base ref
import numpy as np, sys, subprocess, os
pts=[list(map(float,p.split(','))) for p in sys.argv[4].split(';')]
refs=[list(map(float,p.split(','))) for p in sys.argv[5].split(';')] if len(sys.argv)>5 else pts
cur,curc=sys.argv[1],sys.argv[2]
for k,(p,r) in enumerate(zip(pts,refs)):
    z=np.load(cur); V=z['V']; F=z['F']; E=set()
    for f in F:
        f=[int(x) for x in f if x>=0]
        for i in range(len(f)): E.add(tuple(sorted((f[i],f[(i+1)%len(f)]))))
    r=np.array(r); best=None
    for a,b in E:
        A,B=V[a],V[b]; t=np.clip(np.dot(r-A,B-A)/max(np.dot(B-A,B-A),1e-12),0.15,0.85); d=np.linalg.norm(A+t*(B-A)-r)
        if best is None or d<best[0]: best=(d,a,b)
    out=sys.argv[3] if k==len(pts)-1 else '/tmp/claude-0/ei_%d.npz'%k
    print('point',p,'edge',best[1],best[2],'dist %.2f'%best[0])
    subprocess.run(['python3','slotN.py',cur,curc,out,str(best[1]),str(best[2]),','.join(map(str,p))],check=True)
    cur,curc=out,out.replace('.npz','_col.npy')
