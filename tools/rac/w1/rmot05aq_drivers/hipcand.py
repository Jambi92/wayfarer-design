import sys; sys.path.insert(0,"/home/claude/aq")
import numpy as np, json, aqmetrics as Q
V0=Q.V0; M=np.load('mask_k250.npy')
S=np.load('simAQ_8_150.npz')['V']
def sphere(X):
    A=np.c_[2*X,np.ones(len(X))]; b=(X**2).sum(1); c=np.linalg.lstsq(A,b,rcond=None)[0]; return c[:3]
for s,i in Q.HB.items():
    mv=np.linalg.norm(S[i]-V0[i],axis=1)*1000
    print(s,'ring n',len(i),'mask==1',(M[i]>=0.999).sum(),'moved>0.01mm',(mv>0.01).sum(),'max',mv.max().round(2))
    print('  centroid',(V0[i].mean(0)*100).round(2),'sphere0',(sphere(V0[i])*100).round(2),'sphere drift mm',(np.linalg.norm(sphere(S[i])-sphere(V0[i]))*1000).round(3))
    # weight-symmetric: per-angle binned centroid around thigh axis (equal angular weight)
    c=V0[i].mean(0); X=V0[i]-c; _,_,vt=np.linalg.svd(X,full_matrices=False); ax=vt[2]
    u=vt[0]; v=vt[1]; ang=np.arctan2(X@v,X@u); b=((ang+np.pi)/(2*np.pi)*36).astype(int)%36
    cb=lambda Y: np.array([Y[b==k].mean(0) for k in range(36) if (b==k).any()]).mean(0)
    print('  angle-binned drift mm',(np.linalg.norm(cb(S[i])-cb(V0[i]))*1000).round(3))
jc=json.load(open('/home/claude/wayfarer-design/reviews/rac-rmot05ab-evidence/joints_C.json')); print(list(jc.keys())[:20])
print('bbox cm',(V0.min(0)*100).round(2),(V0.max(0)*100).round(2))
