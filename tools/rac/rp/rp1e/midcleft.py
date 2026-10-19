# midcleft.py IN.npz IN_col OUT.npz "lo,hi;..." heel [arc] [fracs] : insert verts on the crotch edge at fracs, split them (lips/tip) from source slices
import sys, numpy as np, json, subprocess, os
from earsl import slice_loops
inp,incol,out=sys.argv[1:4]; cl=[list(map(int,c.split(','))) for c in sys.argv[4].split(';')]
heel=np.array([float(t) for t in sys.argv[5].split(',')]); arc=float(sys.argv[6]) if len(sys.argv)>6 else 0.5
fracs=[float(t) for t in (sys.argv[7] if len(sys.argv)>7 else '0.5').split(',')]
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
for k,(lo,hi) in enumerate(cl):
    V=np.load(cur)['V']; c=0.5*(V[lo]+V[hi]); back=heel-c; back[2]=0; back/=np.linalg.norm(back); side=np.array([-back[1],back[0],0.0])
    a,b=lo,hi; mids=[]
    Fc=[[int(x) for x in f if x>=0] for f in np.load(cur)['F']]
    from collections import defaultdict
    nbd=defaultdict(set)
    for f in Fc:
        for i in range(len(f)): nbd[f[i]].add(f[(i+1)%len(f)]); nbd[f[(i+1)%len(f)]].add(f[i])
    if hi not in nbd[lo]:
        ms=[v for v in nbd[lo]&nbd[hi] if v>=int(os.environ.get('MINNEW','0')) and min(V[lo,2],V[hi,2])<V[v,2]<max(V[lo,2],V[hi,2])]
        mids=ms[:1]; fracs=[]
    for f in fracs:
        p=V[lo]+f*(V[hi]-V[lo]); tmp='/tmp/claude-0/mc_%d_%g.npz'%(k,f)
        subprocess.run(['python3','slotN.py',cur,curc,tmp,str(a),str(b),','.join(map(str,p.tolist()))],capture_output=True)
        n=len(np.load(cur)['V']); mids.append(n); cur,curc=tmp,tmp.replace('.npz','_col.npy'); a=n
    Vm=np.load(cur)['V']; path=[lo]+mids+[hi]; tips=[None];A=[];B=[]
    for v in mids:
        r=slit(Vm[v],back,side)
        if r is None or np.linalg.norm(r[0]-Vm[v])>float(os.environ.get('MAXMOVE','1.5')): tips.append(None); A.append('auto'); B.append('auto'); continue
        t,(wp,wm)=r; tips.append(t.tolist()); A.append(wp.tolist()); B.append(wm.tolist())
    tips.append(None)
    o=out if k==len(cl)-1 else '/tmp/claude-0/mc_%d.npz'%k; ok=False
    for flip in (False,True):
        spec=dict(path=path,tip=tips,A=B if flip else A,B=A if flip else B,lipoff=float(os.environ.get('LIPOFF','0.4')))
        json.dump(spec,open('/tmp/claude-0/mc.json','w'))
        os.path.exists(o) and os.remove(o)
        r=subprocess.run(['python3','pathbevel.py',cur,curc,o,'/tmp/claude-0/mc.json'],capture_output=True,text=True)
        if r.returncode: print('pathbevel failed',r.stderr[-200:]); continue
        s=subprocess.run(['/home/claude/stc/bin/python3','selfx_npz.py','--',o],capture_output=True,text=True).stdout
        nsx=int([l for l in s.splitlines() if l.startswith('SELFX')][0].split()[-1]); print('cleft',k,lo,hi,'flip',flip,'selfx',nsx,'tips',[None if t is None else np.round(t,2).tolist() for t in tips])
        if nsx==0: ok=True; break
    cur,curc=o,o.replace('.npz','_col.npy')
