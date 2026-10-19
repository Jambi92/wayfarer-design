# footcleft2.py IN.npz IN_col OUT.npz "lo,hi[,ut];..." heel(x,y,z) [arc] : toe-cleft crease with tips/lips from source z-slices (slit tip + walls)
import sys, numpy as np, json, subprocess, os
from earsl import slice_loops
inp,incol,out=sys.argv[1:4]; cl=[list(map(int,c.split(','))) for c in sys.argv[4].split(';')]
heel=np.array([float(t) for t in sys.argv[5].split(',')]); arc=float(sys.argv[6]) if len(sys.argv)>6 else 0.5
def nbs(F,v):
    s=set()
    for f in F:
        if v in f: i=f.index(v); s|={f[i-1],f[(i+1)%len(f)]}
    return s
def slit(p,back,side,R=2.0):
    best=None
    for P,c in slice_loops(2,float(p[2])):
        d=np.linalg.norm(P[:,:2]-p[:2],axis=1); m=d<R
        if not m.any(): continue
        sc=np.where(m,(P[:,:2]-p[:2])@back[:2],-1e9); i=int(np.argmax(sc))
        if best is None or sc[i]>best[0]: best=(sc[i],P,i)
    if best is None: return None
    _,P,i=best; n=len(P)
    def walk(dd):
        s=0;k=i
        while s<arc: k2=(k+dd)%n; s+=np.linalg.norm(P[k2]-P[k]); k=k2
        return P[k]
    a,b=walk(1),walk(-1)
    # side: projection on 'side' axis
    return P[i],(a,b) if (a-b)[:2]@side[:2]>0 else (b,a)
cur,curc=inp,incol
for k,c_ in enumerate(cl):
    lo,hi=c_[0],c_[1]; z=np.load(cur); V=z['V']; F=[[int(x) for x in f if x>=0] for f in z['F']]
    c=0.5*(V[lo]+V[hi]); back=heel-c; back[2]=0; back/=np.linalg.norm(back); side=np.array([-back[1],back[0],0.0])
    dd=lambda a,n: np.dot((V[n]-V[a])/np.linalg.norm(V[n]-V[a]),back)
    ub=max([n for n in nbs(F,lo) if n!=hi],key=lambda n:dd(lo,n)); ub=ub if dd(lo,ub)>=0.4 else None
    if len(c_)>2: ut=c_[2] if c_[2]>=0 else None
    else:
        ut=max([n for n in nbs(F,hi) if n!=lo],key=lambda n:dd(hi,n)); ut=ut if dd(hi,ut)>=0.4 else None
    tmp='/tmp/claude-0/f2_m%d.npz'%k
    subprocess.run(['python3','slotN.py',cur,curc,tmp,str(lo),str(hi),','.join(map(str,c.tolist()))],capture_output=True)
    M=len(V); Vm=np.load(tmp)['V']; Fm=[[int(x) for x in f if x>=0] for f in np.load(tmp)['F']]
    path=[ub,lo,M,hi,ut]; keep=[x is not None for x in path]; path=[x for x in path if x is not None]
    # sides: determine which side (A/B) maps to +side by checking pathbevel's side faces later: we give A=+side, then verify
    tips=[];A=[];B=[]
    for v in path:
        if v in (ub,ut): tips.append(None); continue
        r=slit(Vm[v],back,side)
        if r is None: tips.append(None); A.append('auto'); B.append('auto'); continue
        t,(wp,wm)=r
        if np.linalg.norm(t-Vm[v])>float(os.environ.get('MAXMOVE','2.0')): tips.append(None); A.append('auto'); B.append('auto'); continue
        tips.append(t.tolist()); A.append(wp.tolist()); B.append(wm.tolist())
    spec=dict(path=path,tip=tips,A=A[:len(path)-2] if len(A)>=len(path)-2 else ['auto']*(len(path)-2),B=B[:len(path)-2] if len(B)>=len(path)-2 else ['auto']*(len(path)-2),lipoff=0.4)
    # interior verts only for A/B: path interior = path[1:-1]; tips/lips computed for lo,M,hi in order; if ub None, lo is path[0] (end) -> drop its lips
    inter=path[1:-1]; Ai=[];Bi=[]; j=0
    lipv=[v for v in path if v not in (ub,ut)]
    for v,a_,b_ in zip(lipv,A,B):
        if v in inter: Ai.append(a_); Bi.append(b_)
    spec['A']=Ai; spec['B']=Bi
    json.dump(spec,open('/tmp/claude-0/f2_%d.json'%k,'w'))
    o=out if k==len(cl)-1 else '/tmp/claude-0/f2_%d.npz'%k
    for flip in (False,True):
        if flip: spec['A'],spec['B']=spec['B'],spec['A']; json.dump(spec,open('/tmp/claude-0/f2_%d.json'%k,'w'))
        os.path.exists(o) and os.remove(o)
        r=subprocess.run(['python3','pathbevel.py',tmp,tmp.replace('.npz','_col.npy'),o,'/tmp/claude-0/f2_%d.json'%k],capture_output=True,text=True)
        if r.returncode: print('pathbevel failed',r.stderr[-200:]); continue
        s=subprocess.run(['/home/claude/stc/bin/python3','selfx_npz.py','--',o],capture_output=True,text=True).stdout
        nsx=int([l for l in s.splitlines() if l.startswith('SELFX')][0].split()[-1])
        print('cleft',k,lo,hi,'path',path,'flip',flip,'selfx',nsx)
        if nsx==0: break
    cur,curc=o,o.replace('.npz','_col.npy')
