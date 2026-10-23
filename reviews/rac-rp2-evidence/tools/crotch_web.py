import sys; sys.path.insert(0,'/tmp/claude-0/rp2/tools'); sys.path.insert(0,'/tmp/claude-0/rp2'); import numpy as np, igl
import web; from web import make_web
from crotch_patch import build
from hidden import hidden_quads
g = float(sys.argv[1]) if len(sys.argv) > 1 else 0.3; eps = float(sys.argv[2]) if len(sys.argv) > 2 else 0.04; web.AIRSIGN = float(sys.argv[3]) if len(sys.argv) > 3 else -1.0
s=np.load('/tmp/claude-0/rp2/sstar.npz'); V=s['V']; Q=s['Q']; W2=np.load('/tmp/claude-0/rp2/w2_body.npz')['V']; m=np.load('/tmp/claude-0/rp2/mir_body.npy')
T=np.r_[Q[:,[0,1,2]],Q[:,[0,2,3]]]
w=np.abs(igl.winding_number(V,T,V)); box=(np.abs(V[:,0])<8)&(V[:,2]>100)&(V[:,2]<122)
side=np.where(W2[:,0]>0.05,1,np.where(W2[:,0]<-0.05,-1,0))
hidden=box&((w>1.0)|(side*V[:,0]<-1e-6))
bridge=hidden&(side==0); A=side>0; B=side<0
cr=build()['crease']
hq,sgn,ht=hidden_quads(V,Q)
fn=np.cross(V[T[:,1]]-V[T[:,0]],V[T[:,2]]-V[T[:,0]]); TN=sgn*fn/np.linalg.norm(fn,axis=1)[:,None]
labT=np.sign(np.round(W2[T][:,:,0].mean(1),2))
TA=np.where(~ht&(labT>0)&(V[T][:,:,0].min(1)>=-0.01))[0]; TB=np.where(~ht&(labT<0)&(V[T][:,:,0].max(1)<=0.01))[0]
def nfun(faces):
    def f(c):
        d,fi,cp=igl.point_mesh_squared_distance(c,V,T[faces]); return TN[faces[fi]]
    return f
P,rA,rB=make_web(V,Q,hidden,A,B,bridge,cr,nfun(TA),nfun(TB),g=g,eps=eps)
ok=m>=0; P[ok]=0.5*(P[ok]+P[m[ok]]*np.array([-1,1,1]))
np.savez('/tmp/claude-0/rp2/sstar_w.npz',V=P,Q=Q,hidden=hidden,mir=m)
print('hidden',hidden.sum())
