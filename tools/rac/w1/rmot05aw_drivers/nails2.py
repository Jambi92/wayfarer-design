# 05AW nail spec v2: nail plates located from the front/top orthographic grid renders (cm, foot frame v lateral, u along foot, z height).
import numpy as np, sys
sys.path.insert(0,'/home/claude/av'); from avlib import frame, ss
import scipy.sparse as sp
from scipy.sparse.csgraph import connected_components
YAW={'L':6.53,'R':-31.22}
# view, proximal (a,b), distal (a,b), width ; front view: (v,z) ; top view: (v,u)
NAILS={
 'L1':('top',(-5.6,8.3),(-5.6,11.3),2.5),
 'L2':('front',(-0.06,4.5),(-0.06,2.35),2.1),
 'L3':('front',(3.5,4.85),(3.5,2.45),1.7),
 'L4':('front',(6.1,4.05),(6.1,1.95),1.5),
 'R1':('top',(4.85,9.1),(4.85,11.3),2.5),
 'R2':('front',(-0.2,4.6),(-0.2,2.4),2.1),
 'R3':('front',(-3.65,3.95),(-3.65,1.75),1.7),
 'R4':('front',(-6.5,3.45),(-6.5,1.5),1.4)}
def frames(V):
    out={}
    for s in 'LR':
        fm,a,p=frame(V,s); out[s]=(fm,a,p,V[fm].mean(0))
    return out
def surf(V,fm,a,p,c,view,ab):
    u=(V-c)@a*100; v=(V-c)@p*100; z=V[:,2]*100
    if view=='front':
        m=fm&(np.abs(v-ab[0])<0.2)&(np.abs(z-ab[1])<0.2); i=np.flatnonzero(m)[np.argmax(u[m])]
    else:
        m=fm&(np.abs(v-ab[0])<0.2)&(np.abs(u-ab[1])<0.2); i=np.flatnonzero(m)[np.argmax(z[m])]
    return V[i]
def weld_adj(V,F):
    k,iv=np.unique(np.round(V,7),axis=0,return_inverse=True); iv=iv.ravel(); Fw=iv[F]
    E=np.vstack([Fw[:,[0,1]],Fw[:,[1,2]],Fw[:,[2,0]]]); A=sp.coo_matrix((np.ones(len(E)),(E[:,0],E[:,1])),shape=(len(k),)*2).tocsr(); A=A+A.T
    return iv,A
def nail_frame(V,name):
    view,pa,pb,W=NAILS[name]; s=name[0]; fm,a,p,c=frames(V)[s]
    Pp=surf(V,fm,a,p,c,view,pa); Pd=surf(V,fm,a,p,c,view,pb)
    e=Pd-Pp; L=np.linalg.norm(e); e/=L; lat=p-e*(p@e); lat/=np.linalg.norm(lat); n=np.cross(lat,e); 
    # outward: away from the toe interior (toward +a / +z)
    if n@(a+np.array([0,0,1.0]))<0: n=-n
    return dict(Pp=Pp,Pd=Pd,e=e,L=L,lat=lat,n=n,W=W/100,s=s,fm=fm,a=a,p=p)
def nail_weight(V,F,N,name,iv,A,ext=0.45,glat=(0.30,0.80),depth=0.006,smooth=0):
    fr=nail_frame(V,name); D=V-fr['Pp']; s=(D@fr['e'])/fr['L']; x=D@fr['lat']; d=D@fr['n']; W=fr['W']
    g=1-ss((np.abs(x)-glat[0]*W)/((glat[1]-glat[0])*W))
    h=ss(s/0.7)*(1-ss((s-1-ext*0.5)/(ext*0.5+1e-9)))
    k=ss((d+depth)/depth)*ss((N@fr['n']+0.1)/0.4)
    w=g*h*k; w[~fr['fm']]=0; w[(s<0)|(s>1+ext)]=0
    sup=np.zeros(A.shape[0],bool); sup[iv[w>0]]=True; idx=np.flatnonzero(sup)
    sub=A[idx][:,idx]; nn,l=connected_components(sub,directed=False)
    seed=iv[np.argmin(np.linalg.norm(V-(fr['Pp']+fr['e']*fr['L']*0.5),axis=1)+(w<=0)*10)]
    keep=np.zeros(A.shape[0],bool); keep[idx[l==l[np.searchsorted(idx,seed)]]]=True; w[~keep[iv]]=0
    gm=np.zeros(A.shape[0]); np.maximum.at(gm,iv,w)
    if smooth:
        deg=np.asarray(A.sum(1)).ravel()+1e-12
        from scipy.spatial import cKDTree
        sup=np.flatnonzero(gm>0); kpos=np.zeros((A.shape[0],3)); kpos[iv]=V
        dd,_=cKDTree(kpos[sup]).query(kpos,distance_upper_bound=0.0045); dom=np.isfinite(dd)
        for _ in range(smooth): gm=np.where(dom,0.5*gm+0.5*(A@gm)/deg,0)
    w=gm[iv]   # identical weight for duplicate-position copies
    return w,fr
def empty_mat(loc,rot_deg,scale):
    rx,ry,rz=np.radians(rot_deg); cx,sx=np.cos(rx),np.sin(rx); cz,sz=np.cos(rz),np.sin(rz); cy,sy=np.cos(ry),np.sin(ry)
    Rx=np.array([[1,0,0],[0,cx,-sx],[0,sx,cx]]); Ry=np.array([[cy,0,sy],[0,1,0],[-sy,0,cy]]); Rz=np.array([[cz,-sz,0],[sz,cz,0],[0,0,1]])
    M=np.eye(4); M[:3,:3]=Rz@Ry@Rx@np.diag(scale); M[:3,3]=loc; return M
def apply_hook(V,w,M0,M1):
    D=M1@np.linalg.inv(M0); X=V@D[:3,:3].T+D[:3,3]; return V+w[:,None]*(X-V)
