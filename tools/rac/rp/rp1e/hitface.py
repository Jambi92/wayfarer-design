import numpy as np,sys
z=np.load(sys.argv[1]);V=z['V'];F=[f[f>=0] for f in z['F']]
O=np.array(eval(sys.argv[2]));T=np.array(eval(sys.argv[3]));dvec=(O-T)/np.linalg.norm(O-T)
def tri(o,d,a,b,c):
    e1=b-a;e2=c-a;p=np.cross(d,e2);det=e1@p
    if abs(det)<1e-12: return None
    s=o-a;uu=(s@p)/det;q=np.cross(s,e1);vv=(d@q)/det;t=(e2@q)/det
    return t if (uu>=0 and vv>=0 and uu+vv<=1) else None
res=[]
for k,f in enumerate(F):
    P=V[f]
    if np.linalg.norm(P.mean(0)-O)>8: continue
    for i in range(1,len(f)-1):
        t=tri(O,dvec,P[0],P[i],P[i+1])
        if t is not None: res.append((abs(t),t,k,list(map(int,f))))
for r in sorted(res)[:3]: print(r)
