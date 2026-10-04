# post-Gate-8 polish: tail taper continuity.
# Per-angle radial remap of the tail about the anatomical axis: for every direction around the tail the outline radius
# r(s,theta) is smoothed along the axis (removes the dorsal knob / ventral pinch), and the whole section is then scaled so the
# equivalent radius follows a smooth Hermite taper holding the SAME volume over s=12..98 cm (mass redistributed, not removed).
# Root (s>=98: sacral base, caudofemoral region) and terminal taper (s<=12) untouched; axis, path and length unchanged.
# argv: in.npz(V,F) out.npz
import numpy as np, sys, os
from scipy.optimize import brentq
from scipy.ndimage import gaussian_filter1d
from scipy.sparse import coo_matrix, diags
sys.path.insert(0,'/tmp/claude-0/rodin/p9'); from tailprof import profile
z=np.load(sys.argv[1]); V=z['V'].astype(np.float64); F=z['F']
C=np.load('/tmp/claude-0/rodin/g8/axis.npy'); P=np.load('/tmp/claude-0/rodin/p9/prof_g6.npy')
S=np.arange(0,108,0.5); rs=np.interp(S,P[:,0],P[:,2]); NB=72
s0,s1=12.0,98.0
r0=np.interp(s0,S,rs); r1=np.interp(s1,S,rs); d0=(np.interp(s0+3,S,rs)-np.interp(s0-3,S,rs))/6; d1=(np.interp(s1+3,S,rs)-np.interp(s1-3,S,rs))/6
m=(S>=s0)&(S<=s1); t=(S[m]-s0)/(s1-s0); L=s1-s0
H=(2*t**3-3*t**2+1)*r0+(t**3-2*t**2+t)*L*d0+(-2*t**3+3*t**2)*r1+(t**3-t**2)*L*d1; B=(t*(1-t))**2*16
V0=np.trapz(np.pi*rs[m]**2,S[m]); c=brentq(lambda c: np.trapz(np.pi*(H+c*B)**2,S[m])-V0,-10,10)
RT=np.interp(S,S[m],H+c*B); np.save('/tmp/claude-0/rodin/p9/taper_target.npy',np.stack([S,rs,RT],1))
nV=len(V); FF=np.asarray(F,np.int64); E_=np.concatenate([FF[:,[0,1]],FF[:,[1,2]],FF[:,[2,0]]])
A=coo_matrix((np.ones(len(E_)),(E_[:,0],E_[:,1])),shape=(nV,nV)).tocsr(); A=((A+A.T)>0).astype(np.float32); LAP=diags(1/np.asarray(A.sum(1)).ravel())@A
def grid(V):
    ci,th,R=profile(V,C); tail=(V[:,1]<-20)&(V[:,2]>40); G=np.full((len(S),NB),np.nan)
    b=((th+np.pi)/(2*np.pi)*NB).astype(int)%NB
    for kk in range(len(S)):
        mm=tail&(ci==kk)
        if mm.sum()<20: continue
        rb=np.zeros(NB); np.maximum.at(rb,b[mm],R[mm]); rb[rb==0]=np.nan; G[kk]=rb
    for j in range(NB):                                   # fill gaps along s
        col=G[:,j]; ok=~np.isnan(col); G[:,j]=np.interp(np.arange(len(S)),np.where(ok)[0],col[ok])
    return G,ci,th,R
V_in=V.copy(); W=np.clip(np.minimum((S-s0)/6.0,(s1-S)/6.0),0,1)[:,None]   # blend window: full effect inside, 0 at the ends
NIT=int(os.environ.get('NIT','3'))
for it in range(NIT):
    G,ci,th,R=grid(V)
    Gs=gaussian_filter1d(G,sigma=12.0,axis=0,mode='nearest')            # sigma 6 cm along the axis
    Gs=np.concatenate([Gs[:,-6:],Gs,Gs[:,:6]],1); Gs=gaussian_filter1d(Gs,1.5,axis=1)[:,6:-6]
    req=np.sqrt(0.5*np.sum(Gs**2,1)*(2*np.pi/NB)/np.pi); Gt=Gs*(RT/req)[:,None]
    Gt=G*(1-W)+Gt*W
    Kg=Gt/G
    ci2=np.clip(ci,1,len(C)-2); T=C[ci2+1]-C[ci2-1]; T/=np.linalg.norm(T,axis=1,keepdims=True)
    sf=ci*0.5+np.einsum('ij,ij->i',V-C[ci],T); r=V-C[ci]; r-=T*np.einsum('ij,ij->i',r,T)[:,None]
    tail=(V[:,1]<-26)&(V[:,2]>40)&(np.linalg.norm(r,axis=1)<22)&(sf<s1+1)
    fs=np.clip(sf/0.5,0,len(S)-1.001); i0=fs.astype(int); a=fs-i0
    fb=((th+np.pi)/(2*np.pi)*NB-0.5)%NB; j0=np.floor(fb).astype(int)%NB; j1=(j0+1)%NB; bb=fb-np.floor(fb)
    k=(Kg[i0,j0]*(1-a)*(1-bb)+Kg[i0+1,j0]*a*(1-bb)+Kg[i0,j1]*(1-a)*bb+Kg[i0+1,j1]*a*bb)
    k=np.where(tail,k,1.0)
    for _ in range(int(os.environ.get('KSM','200'))): k=LAP@k; k[~tail]=1.0
    V=V+(k-1)[:,None]*r
    rq=np.sqrt(0.5*np.sum(G**2,1)*(2*np.pi/NB)/np.pi); print('iter',it,'max |req/target-1| %.3f'%np.abs(rq[m]/RT[m]-1).max(),flush=True)
mv=np.linalg.norm(V-V_in,axis=1)
np.savez(sys.argv[2],V=V,F=F,MV=mv.astype(np.float32))
print('tail verts moved',int((mv>1e-6).sum()),'max %.2f cm; volume-preserving taper c=%.3f'%(mv.max(),c))
