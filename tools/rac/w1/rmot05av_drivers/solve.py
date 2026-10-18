import numpy as np, sys, json; sys.path.insert(0,'/home/claude/av'); from avlib import *
from scipy.optimize import fsolve
YAW={'L':6.53,'R':-31.22}
def solve(side,za,zb,Lt=34.8,Wt_=15.3):
    w,P=scale_plan(side,za,zb)
    def f(x):
        m=measure(apply_scale(V0,w,P,YAW[side],x[0],x[1]),side); return [m['width_fp']-Wt_, m['length']-Lt]
    x=fsolve(f,[0.68,0.89],xtol=1e-6)
    V=apply_scale(V0,w,P,YAW[side],*x); return x,w,P,V,measure(V,side)
if __name__=='__main__':
    za,zb=float(sys.argv[1]),float(sys.argv[2])
    out={}
    for side in 'LR':
        x,w,P,V,m=solve(side,za,zb); r=ringmask(side)
        out[side]=dict(sx=x[0],sy=x[1],P=(P*100).tolist(),meas=m,ring_drift_mm=float(np.linalg.norm(V[r].mean(0)-V0[r].mean(0))*1000),max_move_cm=float(np.linalg.norm(V-V0,axis=1).max()*100))
    print(json.dumps(out,indent=0,default=float))
