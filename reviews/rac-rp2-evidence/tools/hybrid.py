# hybrid.py IN OUT [z0 z1] : Class C hybrid for the shoulder/neck band.
# Adds beta(z) * (E3 - S*) to a production mesh built on S*. E3 - S* is interpolated barycentrically at each vertex's
# closest point on S* (same topology as E3), beta ramps smoothly 0 -> 1 between z0 and z1 (cm) and stays 1 above.
# Also writes the matching hybrid reference H = S* + beta * (E3 - S*) on the 13k topology (hstar.npz).
import sys, numpy as np, igl
R='/tmp/claude-0/rp2/'
P=np.load(sys.argv[1]); V=P['V'].astype(float)
z0,z1=(float(sys.argv[3]),float(sys.argv[4])) if len(sys.argv)>4 else (162.0,170.0)
S=np.load(R+'sstar.npz'); SV=S['V'].astype(float); SQ=S['Q']; E=np.load(R+'e3_body.npz')['V'].astype(float)
ST=np.r_[SQ[:,[0,1,2]],SQ[:,[0,2,3]]]; D0=E-SV
def beta(z): t=np.clip((z-z0)/(z1-z0),0,1); return t*t*(3-2*t)
_,fi,cp=igl.point_mesh_squared_distance(V,SV,ST)
B=igl.barycentric_coordinates(cp,SV[ST[fi,0]],SV[ST[fi,1]],SV[ST[fi,2]])
D=(B[:,:,None]*D0[ST[fi]]).sum(1)
import os; sys.path.insert(0,R+'tools'); from lowpass import lowpass
DB=beta(cp[:,2])[:,None]*D; lp=float(os.environ.get('LP','0'))
if lp>0: DB=lowpass(P['Q'],len(V),DB,lp)
V2=V+DB
np.savez(sys.argv[2],**{k:P[k] for k in P.files if k!='V'},V=V2)
H=SV+beta(SV[:,2])[:,None]*D0; np.savez(R+'hstar.npz',V=H,Q=SQ,orig=S['orig'])
print('max move mm %.2f'%(np.linalg.norm(V2-V,axis=1).max()*10))
