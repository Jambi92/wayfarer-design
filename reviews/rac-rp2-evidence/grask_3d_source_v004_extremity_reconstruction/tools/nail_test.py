import sys, numpy as np
sys.path.insert(0,'/tmp/claude-0/src3d/v4/tools')
from hand_model import hand_sdf, DEF, scaled, finger_chain
from build_part import evaluate, polygonize
p=scaled(DEF)
for kv in sys.argv[2:]:
    k,v=kv.split('='); p['nail'][k]=float(v)
f=p['fingers']['middle']; J,_,_=finger_chain(f['mcp'],f['L'],f['splay'],f['flex'])
c=J[2]+0.4*(J[3]-J[2]); lo=c-2.6; hi=c+2.6
D,lo,h,cnt=evaluate(lambda P: hand_sdf(P,p),lo,hi,float(__import__("os").environ.get("H","0.05")))
V,F=polygonize(D,lo,h)
np.savez(sys.argv[1],V=V,Q=F); print(len(V), c.tolist())
