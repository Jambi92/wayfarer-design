import numpy as np, sys, json, trimesh
s=sys.argv[1]
w=np.load('/home/claude/stc/rp1/weld.npz'); V=w['V'].astype(float); F=w['F'].astype(np.int64)
D=json.load(open('design_%s.json'%s))
d=np.array(D['rings']['P3']['d']); p=np.array(D['rings']['P3']['p'])
c=(d.mean(0)+p.mean(0))/2; m=(np.abs(V-c)<[12,12,12]).all(1); Fm=F[m[F].all(1)]
tm=trimesh.Trimesh(V,Fm,process=False)
for k in (1,2,3):
    a,b=d[k],p[k]; print('web',k,'d',a.round(1),'p',b.round(1))
    for t in np.linspace(-0.3,1.3,9):
        q=a+(b-a)*t; row=[]
        for dy in (-0.6,-0.3,0,0.3,0.6):
            o=np.array([q[0],q[1]+dy,92.0])
            loc,_,_=tm.ray.intersects_location([o],[[0,0,1.0]])
            zs=sorted(loc[:,2]) if len(loc) else []
            row.append(round(zs[0],1) if zs else None)
        print('  t=%.1f x=%.1f y=%.1f lowest hit z (dy -0.6..0.6): %s'%(t,q[0],q[1],row))
