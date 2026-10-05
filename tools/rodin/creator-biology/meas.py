import numpy as np
_EC={}
def tail_sections(V,F,C,rmax=24.0,step=2,E=None):
    """planar sections perpendicular to polyline C (C[0] = tip end). returns arc-length s (from C[0]) and area"""
    if E is None:
        key=(id(F),len(F))
        if key not in _EC: _EC[key]=np.unique(np.sort(np.concatenate([F[:,[0,1]],F[:,[1,2]],F[:,[2,0]]]),1),axis=0)
        E=_EC[key]
    seg=np.linalg.norm(np.diff(C,axis=0),axis=1); S=np.concatenate([[0],np.cumsum(seg)])
    out=[]
    for k in range(1,len(C)-1,step):
        c=C[k]; t=C[k+1]-C[k-1]; t/=np.linalg.norm(t)
        d=(V-c)@t; a,b=E[:,0],E[:,1]; cr=(d[a]*d[b]<0)
        ea,eb=a[cr],b[cr]; w=d[ea]/(d[ea]-d[eb]); P=V[ea]+w[:,None]*(V[eb]-V[ea])
        r=P-c; ok=np.linalg.norm(r,axis=1)<rmax; P=P[ok]; r=r[ok]
        if len(P)<20: out.append((S[k],np.nan)); continue
        e1=np.cross(np.array([1.0,0,0]),t); e1/=np.linalg.norm(e1); e2=np.cross(t,e1)
        x=r@e2; y=r@e1; ang=np.arctan2(y,x); o=np.argsort(ang); x=x[o]; y=y[o]
        out.append((S[k],0.5*abs(np.sum(x*np.roll(y,-1)-np.roll(x,-1)*y))))
    return np.array(out)
def mass_props(V,F):
    a,b,c=V[F[:,0]],V[F[:,1]],V[F[:,2]]; v=np.einsum('ij,ij->i',a,np.cross(b,c))/6.0
    vol=v.sum(); com=((a+b+c)*v[:,None]).sum(0)/4.0/vol; return vol,com
