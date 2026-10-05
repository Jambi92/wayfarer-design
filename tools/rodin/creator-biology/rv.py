import numpy as np, subprocess, os, pickle, sys
sys.path.insert(0,'/tmp/claude-0/rodin/v1'); import vary
R='/tmp/claude-0/rodin/g1'
def render(P,F,tag,views,res=700,rgb=None):
    fn='/tmp/claude-0/rodin/v1/tmp_%s.npz'%os.path.basename(tag)
    if rgb is None: np.savez(fn,P=P.astype(np.float32),f=F.astype(np.int32))
    else: np.savez(fn,P=P.astype(np.float32),f=F.astype(np.int32),C=rgb.astype(np.float32))
    env=dict(os.environ,VIEWS=views,NPZ=fn,TAG=tag,RES=str(res))
    subprocess.run(['python3',R+('/rclose_rgb.py' if rgb is not None else '/rclose.py')],env=env,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
    os.remove(fn)
