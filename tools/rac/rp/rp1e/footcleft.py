# blender-python footcleft.py -- IN.npz IN_col OUT.npz "lo,hi;..." heel(x,y,z) [lipoff] : toe-cleft web-floor crease (vertical crotch edge)
import sys, numpy as np, bpy, mathutils, json, subprocess
from mathutils.bvhtree import BVHTree
a_=sys.argv[sys.argv.index('--')+1:]; inp,incol,out=a_[0],a_[1],a_[2]; cl=[list(map(int,c.split(','))) for c in a_[3].split(';')]
heel=np.array([float(t) for t in a_[4].split(',')]); lo_off=float(a_[5]) if len(a_)>5 else 0.5
w=np.load('/home/claude/stc/rp1/weld.npz'); S=w['V'].astype(float); SF=w['F']; bvh=BVHTree.FromPolygons(S.tolist(),SF.tolist())
def nbs(F,v):
    s=set()
    for f in F:
        if v in f: i=f.index(v); s|={f[i-1],f[(i+1)%len(f)]}
    return s
def floor(p,d,back=2.5):
    d=d/np.linalg.norm(d); cur=mathutils.Vector(p-back*d); dv=mathutils.Vector(d)
    for k in range(8):
        h=bvh.ray_cast(cur,dv,8.0)
        if h[0] is None: return None
        if h[1].dot(dv)>0.2: return [h[0][0],h[0][1],h[0][2]]
        cur=h[0]+dv*0.002
    return None
cur,curc=inp,incol
for k,(lo,hi) in enumerate(cl):
    z=np.load(cur); V=z['V']; F=[[int(x) for x in f if x>=0] for f in z['F']]
    c=0.5*(V[lo]+V[hi]); back=heel-c; back[2]=0; back/=np.linalg.norm(back); fwd=-back
    ub=max([n for n in nbs(F,lo) if n!=hi],key=lambda n:np.dot((V[n]-V[lo])/np.linalg.norm(V[n]-V[lo]),back))
    ut=max([n for n in nbs(F,hi) if n!=lo],key=lambda n:np.dot((V[n]-V[hi])/np.linalg.norm(V[n]-V[hi]),back))
    dd=lambda a,n: np.dot((V[n]-V[a])/np.linalg.norm(V[n]-V[a]),back)
    if dd(lo,ub)<0.4: ub=None
    if dd(hi,ut)<0.4: ut=None
    m=c.tolist(); tmp='/tmp/claude-0/fc_m%d.npz'%k
    r=subprocess.run(['python3','slotN.py',cur,curc,tmp,str(lo),str(hi),','.join(map(str,m))],capture_output=True,text=True)
    M=len(V)
    tips=[]
    for p in (V[lo],c,V[hi]):
        q=p.copy(); q[2]=p[2]*0.75+c[2]*0.25 if p is not c else c[2]
        t=floor(q,fwd); tips.append(t)
    # keep vertical position close to the original (only move along the toe direction)
    MX=float(__import__('os').environ.get('MAXMOVE','1.5'))
    tips=[t if (t is not None and np.linalg.norm(np.array(t)-p)<MX) else None for t,p in zip(tips,(V[lo],c,V[hi]))]
    tl,tm,th=tips
    print('cleft',k,lo,hi,'ub',ub,'ut',ut,'tips',[None if t is None else np.round(t,2).tolist() for t in tips])
    path=[ub,lo,M,hi,ut]; tip=[None,tl,tm,th,None]
    if ut is None: path=path[:-1]; tip=tip[:-1]
    if ub is None: path=path[1:]; tip=tip[1:]
    ni=len(path)-2
    spec=dict(path=path,tip=tip,A=['auto']*ni,B=['auto']*ni,lipoff=lo_off,lipsnap=__import__('os').environ.get('LIPSNAP','1')=='1')
    json.dump(spec,open('/tmp/claude-0/fc_%d.json'%k,'w'))
    o=out if k==len(cl)-1 else '/tmp/claude-0/fc_%d.npz'%k
    r=subprocess.run(['python3','pathbevel.py',tmp,tmp.replace('.npz','_col.npy'),o,'/tmp/claude-0/fc_%d.json'%k],capture_output=True,text=True); print(r.stdout.strip(),r.stderr.strip()[-300:])
    cur,curc=o,o.replace('.npz','_col.npy')
