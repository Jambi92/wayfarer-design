# sxfaces.py CAGE.npz [box] : coarse-cage intersecting face pairs (triangulated quads; skip pairs sharing a vertex)
import numpy as np, sys
def tri_tri(a,b):
    # Moller-style via segment-triangle tests both ways
    def seg_tri(p,q,t):
        e1=t[1]-t[0]; e2=t[2]-t[0]; d=q-p; h=np.cross(d,e2); det=e1@h
        if abs(det)<1e-12: return False
        f=1/det; s=p-t[0]; u=f*(s@h)
        if u<0 or u>1: return False
        qq=np.cross(s,e1); v=f*(d@qq)
        if v<0 or u+v>1: return False
        tt=f*(e2@qq); return 0<tt<1
    for i in range(3):
        if seg_tri(a[i],a[(i+1)%3],b) or seg_tri(b[i],b[(i+1)%3],a): return True
    return False
def pairs(V,F,box=None):
    T=[];own=[]
    for k,f in enumerate(F):
        f=[x for x in f if x>=0]
        for i in range(1,len(f)-1): T.append((f[0],f[i],f[i+1])); own.append(k)
    T=np.array(T); own=np.array(own); P=V[T]; lo=P.min(1); hi=P.max(1)
    sel=np.arange(len(T)) if box is None else np.where(np.all((hi>box[0])&(lo<box[1]),axis=1))[0]
    out=set()
    for ii,i in enumerate(sel):
        js=sel[ii+1:]; m=np.all((lo[js]<=hi[i])&(hi[js]>=lo[i]),axis=1); js=js[m]
        for j in js:
            if own[i]==own[j] or set(T[i])&set(T[j]): continue
            if tri_tri(P[i],P[j]): out.add((min(own[i],own[j]),max(own[i],own[j])))
    return sorted(out)
if __name__=='__main__':
    z=np.load(sys.argv[1]); V=z['V']; F=z['F']; box=None
    if len(sys.argv)>2: b=eval(sys.argv[2]); box=(np.array(b[0]),np.array(b[1]))
    pp=pairs(V,F,box); print(len(pp))
    for a,b in pp: print(a,[int(x) for x in F[a] if x>=0],b,[int(x) for x in F[b] if x>=0])
