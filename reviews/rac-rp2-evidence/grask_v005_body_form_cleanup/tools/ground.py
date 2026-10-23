# ground.py IN OUT : restore ground contact at z = 0 by a smooth local sole correction (soles only, fades out by z = 3 cm)
import sys, numpy as np
P=dict(np.load(sys.argv[1])); V=P['V'].astype(float); z0=V[:,2].min()
def ss(t): t=np.clip(t,0,1); return t*t*(3-2*t)
V[:,2]-=z0*(1-ss(V[:,2]/3.0)); P['V']=V; np.savez(sys.argv[2],**P); print('ground offset removed %.3f mm; new min %.5f'%(z0*10,V[:,2].min()))
