# blender-python cleft.py -- IN.npz IN_col OUT.npz "P,Q,Up,Ud;..." [tq] [lipoff] : web-floor crease per cleft via pathbevel
import sys, numpy as np, bpy, mathutils, json, subprocess
from mathutils.bvhtree import BVHTree
a_=sys.argv[sys.argv.index('--')+1:]; inp,incol,out=a_[0],a_[1],a_[2]; cl=[list(map(int,c.split(','))) for c in a_[3].split(';')]
tq=float(a_[4]) if len(a_)>4 else 1.25; lo=float(a_[5]) if len(a_)>5 else 0.6
w=np.load('/home/claude/stc/rp1/weld.npz'); S=w['V'].astype(float); SF=w['F']; bvh=BVHTree.FromPolygons(S.tolist(),SF.tolist())
def floor(x,y,z0):
    cur=mathutils.Vector((x,y,z0)); d=mathutils.Vector((0,0,-1))
    for k in range(8):
        h=bvh.ray_cast(cur,d,15.0)
        if h[0] is None: return None
        if h[1][2]<-0.2: return [h[0][0],h[0][1],h[0][2]]
        cur=h[0]+d*0.002
    return None
cur,curc=inp,incol
for k,(P,Q,Up,Ud) in enumerate(cl):
    V=np.load(cur)['V']; z0=max(V[P][2],V[Q][2])+1.5
    tp=floor(V[P][0],V[P][1],z0); q=V[P]+tq*(V[Q]-V[P]); tqp=floor(q[0],q[1],z0)
    if tp is not None and tp[2]<V[P][2]-0.2: tp=None
    if tqp is not None and tqp[2]<V[Q][2]-0.2: tqp=None
    print('cleft',k,'P',V[P].round(2).tolist(),'->',None if tp is None else np.round(tp,2).tolist(),' Q',V[Q].round(2).tolist(),'->',None if tqp is None else np.round(tqp,2).tolist())
    spec=dict(path=[Up,P,Q,Ud],tip=[None,tp,tqp,None],A=['auto','auto'],B=['auto','auto'],lipoff=lo)
    json.dump(spec,open('/tmp/claude-0/cl_%d.json'%k,'w'))
    o=out if k==len(cl)-1 else '/tmp/claude-0/cl_%d.npz'%k
    import os
    if os.path.exists(o): os.remove(o)
    r=subprocess.run(['python3','pathbevel.py',cur,curc,o,'/tmp/claude-0/cl_%d.json'%k],capture_output=True,text=True); print(r.stdout.strip(),r.stderr.strip()[-300:])
    if r.returncode: raise SystemExit('pathbevel failed for cleft %d'%k)
    cur,curc=o,o.replace('.npz','_col.npy')
