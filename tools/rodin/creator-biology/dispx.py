import numpy as np, sys, os, json; sys.path.insert(0,'/tmp/claude-0/rodin/v1'); import headpatch, rv
sys.path.insert(0,'/tmp/claude-0/rb'); import wf_saurin_head63 as H; eye=(H.eye_centers()[0],H.eye_centers()[1])
os.makedirs('/tmp/claude-0/rodin/v1/dx',exist_ok=True)
X={'x05':{'ros_len':1.20,'cran_w':0.92},'x06':{'ros_len':0.85,'cran_w':1.08}}
for dk,src in (('mx','dmx'),('sw','dsw'),('mr','d13')):
    z=np.load('/tmp/claude-0/rodin/v1/dv/hvs_%s.npz'%src); P=z['V'].astype(float); F=z['F']
    for xk,p in X.items():
        Q=headpatch.warp_patch(P,p,eye)
        rv.render(Q,F,'/tmp/claude-0/rodin/v1/dx/%s_%s'%(dk,xk),"hF:0:3:0:8:182:30;hP:90:0:0:2:182:34;hF34:40:12:0:6:183:32;hT:0:89:0:2:184:34",res=600); print(dk,xk,flush=True)
