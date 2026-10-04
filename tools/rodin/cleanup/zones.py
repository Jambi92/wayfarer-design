# final cleanup: authorized correction zones (world cm, x f u) on the polished base mesh, as smooth weights 0..1
import numpy as np
def ss(a,b,x): t=np.clip((x-a)/(b-a),0,1); return t*t*(3-2*t)
def box(V,lo,hi,fall=1.5,absx=True):
    x,f,u=V.T; X=np.abs(x) if absx else x; P=np.stack([X,f,u],1); w=np.ones(len(V))
    for k in range(3): w*=ss(lo[k]-fall,lo[k],P[:,k])*ss(hi[k]+fall,hi[k],P[:,k])
    return w
def sph(V,c,r,fall):
    x,f,u=V.T; P=np.stack([np.abs(x),f,u],1); d=np.linalg.norm(P-np.array(c),axis=1); return ss(r+fall,r,d)
def zones(V,N):
    x,f,u=V.T; sg=np.sign(x)
    Z={}
    Z['sternum']=box(V,(0,6,118),(10,25,153),2.0)
    Z['dorsal_rod']=box(V,(0,-30,128),(5.0,-4,178),3.0)*ss(0.2,0.6,-N[:,1])
    Z['shoulder']=box(V,(16,-10,142),(28,10,157),2.0)*ss(0.0,0.5,N[:,2])
    Z['upper_arm']=box(V,(22,-12,114),(34,10,146),2.0)*ss(0.0,0.4,N[:,0]*sg)
    Z['inguinal_hip']=np.maximum(box(V,(4,-2,79),(20,16,99),2.0)*ss(-0.2,0.3,N[:,1]),sph(V,(17,-14,91.5),5.0,3.0))
    Z['heel']=box(V,(15,-9,5),(29,4,22),2.0)*ss(-0.45,0.05,-N[:,1])
    Z['ankle_front']=box(V,(16,3,7),(27,12,21),2.0)*ss(-0.2,0.3,N[:,1])          # anterior ankle tendon lump + step
    return Z
