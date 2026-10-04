# Gate 8 fix: limb/trunk pattern-system blend weight ramps over ~12 cm from each limb root (along the limb axis) and is then
# surface-smoothed, so no colour border appears where the limb coordinate system begins (was a ~1 cm blend -> visible line).
import sys, numpy as np
from scipy.sparse import coo_matrix, diags
fn=sys.argv[1]; base=sys.argv[2]
Fd=dict(np.load(fn)); B=np.load(base); F=B['F'].astype(np.int64); n=len(B['V'])
LID=Fd['LID']; LT=Fd['LT'].astype(np.float64)
def ss(a,b,x): t=np.clip((x-a)/(b-a),0,1); return t*t*(3-2*t)
w=np.where(LID>0, np.where(LID<=2, ss(3,15,LT), ss(2,14,LT)), 0.0).astype(np.float32)
E_=np.concatenate([F[:,[0,1]],F[:,[1,2]],F[:,[2,0]]]); A=coo_matrix((np.ones(len(E_)),(E_[:,0],E_[:,1])),shape=(n,n)).tocsr(); A=((A+A.T)>0).astype(np.float32)
L=diags(1/np.asarray(A.sum(1)).ravel())@A
for _ in range(300): w=L@w
Fd['LW']=np.clip(w,0,1).astype(np.float32); np.savez(fn,**Fd); print('LW fixed',float(Fd['LW'].mean()))
