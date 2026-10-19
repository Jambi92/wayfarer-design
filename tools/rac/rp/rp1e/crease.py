import numpy as np, sys
w=np.load('/home/claude/stc/rp1/weld.npz'); V=w['V'].astype(float); F=w['F'].astype(np.int64)
s=sys.argv[1]; sg=-1 if s=='R' else 1
fn=np.cross(V[F[:,1]]-V[F[:,0]],V[F[:,2]]-V[F[:,0]]); fn/=np.linalg.norm(fn,axis=1,keepdims=True)+1e-12
fc=V[F].mean(1)
reg=(fc[:,0]*sg>10)&(fc[:,0]*sg<34)&(fc[:,2]>120)&(fc[:,2]<172)&(fc[:,1]>-55)&(fc[:,1]<-5)
idx=np.where(reg)[0]; Fr=F[idx]
import collections
ed=collections.defaultdict(list)
for k,f in zip(idx,Fr):
    for a,b in ((f[0],f[1]),(f[1],f[2]),(f[2],f[0])): ed[(min(a,b),max(a,b))].append(k)
cv=[]
for (a,b),fs in ed.items():
    if len(fs)!=2: continue
    f1,f2=fs; n1,n2=fn[f1],fn[f2]; ang=np.degrees(np.arccos(np.clip(n1@n2,-1,1)))
    if ang<35: continue
    # concave if the other face's centroid is on the positive side of face1 plane
    conc=(fc[f2]-fc[f1])@n1>0
    if conc: cv.append((a,b,ang))
cv=np.array(cv); print(s,'concave sharp edges',len(cv))
P=(V[cv[:,0].astype(int)]+V[cv[:,1].astype(int)])/2
np.save('crease_%s.npy'%s,np.c_[P,cv[:,2]]); np.save('creasev_%s.npy'%s,np.unique(cv[:,:2].astype(int)))
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
fig,ax=plt.subplots(1,3,figsize=(21,7))
for a,(i,j) in zip(ax,((0,2),(1,2),(0,1))):
    a.scatter(P[:,i],P[:,j],s=3,c=cv[:,2],cmap='viridis'); a.set_aspect('equal'); a.grid(alpha=.3)
plt.savefig('crease_%s.png'%s,dpi=55,bbox_inches='tight')
