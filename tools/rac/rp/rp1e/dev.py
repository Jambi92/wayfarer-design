import numpy as np, sys, igl, json
w=np.load('/home/claude/stc/rp1/weld_a.npz'); S=w['V'].astype(float); SF=w['F'].astype(np.int64)
z=np.load('/home/claude/stc/rp1/zones.npz'); zone=z['zone']; names=list(z['names'])
for p in sys.argv[1:]:
    m=np.load(p); V=m['V'].astype(float); F=m['F'].astype(np.int64)
    dsp,_,_=igl.point_mesh_squared_distance(S,V,F); dsp=np.sqrt(dsp)*10
    C=V[F].mean(1); dps,I,_=igl.point_mesh_squared_distance(C,S,SF); dps=np.sqrt(dps)*10; zp=zone[SF[I,0]]
    np.save(p.replace('.npz','_dsp.npy'),dsp.astype(np.float32))
    print(p)
    for k,nm in enumerate(names):
        a=dsp[zone==k]; b=dps[zp==k]; lim=(0.5,1.5,3.0) if nm=='general' else (0.3,0.8,1.5)
        f=lambda x:'%.3f/%.3f/%.2f'%(np.median(x),np.percentile(x,95),x.max())
        print('  %-18s s2p %s  p2s %s  over %.2f%%'%(nm,f(a),f(b),(a>lim[2]).mean()*100))
