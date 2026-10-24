# sdf.py : vectorised SDF primitives (numpy), IQ-style
import numpy as np
def smin(a,b,k):
    if k<=0: return np.minimum(a,b)
    h=np.clip(0.5+0.5*(b-a)/k,0,1); return b+(a-b)*h-k*h*(1-h)
def smax(a,b,k): return -smin(-a,-b,k)
def round_cone(P,a,b,r1,r2):
    """P (n,3); segment a->b with radii r1 at a, r2 at b (IQ sdRoundCone, arbitrary orientation)"""
    ba=b-a; l2=ba@ba; rr=r1-r2; a2=l2-rr*rr; il2=1.0/l2
    pa=P-a; y=pa@ba; z=y-l2; x=pa*l2-y[:,None]*ba; x2=(x*x).sum(1); y2=y*y*l2; z2=z*z*l2
    k=np.sign(rr)*rr*rr*x2
    d=np.where(np.sign(z)*a2*z2>k, np.sqrt(x2+z2)*il2-r2,
       np.where(np.sign(y)*a2*y2<k, np.sqrt(x2+y2)*il2-r1, (np.sqrt(x2*a2*il2)+y*rr)*il2-r1))
    return d
def ellipsoid(P,c,R,rad):
    """rotation R (3x3, columns = local axes in world), radii rad"""
    q=(P-c)@R/np.asarray(rad); k0=np.linalg.norm(q,axis=1); k1=np.linalg.norm(q/np.asarray(rad),axis=1)
    return k0*(k0-1)/np.maximum(k1,1e-9)
def round_box(P,c,R,half,rnd):
    q=np.abs((P-c)@R)-(np.asarray(half)-rnd)
    return np.linalg.norm(np.maximum(q,0),axis=1)+np.minimum(q.max(1),0)-rnd
def flat_cone(P,a,b,r1,r2,dors,flat):
    """round cone with cross-section flattened along 'dors' (unit, perpendicular-ish to the bone) by factor flat (<1)"""
    t=(b-a)/np.linalg.norm(b-a); dd=dors-(dors@t)*t; dd/=np.linalg.norm(dd)
    q=P-a; s=q@dd; Q=P+((1.0/flat-1.0)*s)[:,None]*dd      # stretch along dors -> cone appears flattened
    A=a; B=b
    return round_cone(Q,A,B,r1,r2)*flat
def rot(axis,ang):
    axis=np.asarray(axis,float); axis/=np.linalg.norm(axis); c,s=np.cos(ang),np.sin(ang); x,y,z=axis
    return np.array([[c+x*x*(1-c),x*y*(1-c)-z*s,x*z*(1-c)+y*s],[y*x*(1-c)+z*s,c+y*y*(1-c),y*z*(1-c)-x*s],[z*x*(1-c)-y*s,z*y*(1-c)+x*s,c+z*z*(1-c)]])
