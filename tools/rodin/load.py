import numpy as np, re, time
t=time.time()
V=[];Fc=[]
with open('base.obj') as fh:
    for ln in fh:
        if ln.startswith('v '): V.append(ln[2:])
        elif ln.startswith('f '): Fc.append(ln[2:])
v=np.loadtxt(V,dtype=np.float64)
f=np.array([[int(p.split('/')[0]) for p in s.split()] for s in Fc],dtype=np.int64)-1
np.savez('mesh.npz',v=v,f=f)
print(v.shape,f.shape,v.min(0),v.max(0),round(time.time()-t,1))
