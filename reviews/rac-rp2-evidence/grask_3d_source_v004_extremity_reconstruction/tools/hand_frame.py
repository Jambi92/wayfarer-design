import numpy as np
FR={'L':dict(W=[30.9,1.2,105.0],tgt=[31.6,2.36,86.3],dors=[0.93,0.31,-0.18],tilt=4.5),
    'R':dict(W=[-31.2,1.0,105.0],tgt=[-33.0,2.3,85.1],dors=[-0.92,0.39,-0.09])}
def frame(side):
    f=FR[side]; W=np.array(f['W']); e0=np.array(f['tgt'])-W; e0/=np.linalg.norm(e0)
    e2=np.array(f['dors'],float); e2-= (e2@e0)*e0; e2/=np.linalg.norm(e2)
    e1=np.cross(e2,e0)
    if e1[1]<0: e1=-e1
    a=np.radians(f.get('tilt',0.0))
    e0,e2=np.cos(a)*e0+np.sin(a)*e2, -np.sin(a)*e0+np.cos(a)*e2
    return W,np.stack([e0,e1,e2],1)     # world = W + M @ local
