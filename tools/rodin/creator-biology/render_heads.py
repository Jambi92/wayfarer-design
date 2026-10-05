import numpy as np, pickle, sys, os; sys.path.insert(0,'/tmp/claude-0/rodin/v1'); import vary, rv, sets
sys.path.insert(0,'/tmp/claude-0/rb'); import wf_saurin_head63 as H
eye=(H.eye_centers()[0],H.eye_centers()[1])
MODE=sys.argv[1]
if MODE=='body': Lb=pickle.load(open('Lbase.pkl','rb')); zb=np.load(vary.REF_BASE); V=zb['V'].astype(float); Fb=zb['F']
else: Ls=pickle.load(open('Lsurf.pkl','rb')); zs=np.load(vary.REF_SURF); S=zs['V'].astype(float); Fs=zs['F']
BODY="front:0:0:0:0:104:216;profile:90:0:0:-52:104:268;rear34:150:0:0:-25:104:230"
TAIL="tprof:90:0:0:-72:90:182;ttop:0:89:0:-72:85:182;tr34:145:10:0:-70:85:160"
HEAD="hF:0:3:0:10:180:24;hP:90:0:0:8:181:32;hF34:40:12:0:8:181:26;hT:0:89:0:5:184:30"
HEADK=('ros_len','ros_w','ros_aw','ros_d','jaw_d','cran_len','cran_w','cran_d','orbit')
TAILK=('tail_len','tail_base','tail_taper','tail_curv','tail_lat','tail_fat_conc')
jobs=[('ref','Reference','ref',{})]+sets.SINGLE+[(a,b,'combo',c) for a,b,c in sets.COMBO]
only=sys.argv[2:]
O='/tmp/claude-0/rodin/v1/R3/'
import copy
def warp_chunks(X,L,p,eye,n=6):
    N=len(X); out=np.empty_like(X); idx=np.array_split(np.arange(N),n)
    top=np.where(X[:,2]>183.0)[0]
    def sub(ii):
        Lc=copy.copy(L)
        for k,v in L.__dict__.items():
            if isinstance(v,np.ndarray) and len(v)==N: setattr(Lc,k,v[ii])
        return Lc
    q=dict(p); q['_hmeas']=1.0; q['height']=1.0; h_ref=vary.warp(X[top],sub(top),q,eye=eye)[:,2].max()
    for ii in idx:
        q=dict(p); q['_hmeas']=h_ref; out[ii]=vary.warp(X[ii],sub(ii),q,eye=eye)
    return out
def head_follow(P,views):
    top=P[:,2].max(); dz=top-187.881
    out=[]
    for v in views.split(';'):
        n,y,e,cx,cf,cu,s=v.split(':'); out.append(':'.join([n,y,e,cx,cf,'%.2f'%(float(cu)+dz),s]))
    return ';'.join(out)
for jid,lab,grp,p in jobs:
    if only and jid not in only and grp not in only: continue
    keys=set(p)
    body = grp in ('body','frame','comp','ref','combo') or bool(keys & set(TAILK))
    tail = grp in ('tail','ref') or bool(keys & set(TAILK)) or 'fat' in keys or 'muscle' in keys
    head = grp in ('head','ref') or bool(keys & set(HEADK)) or 'head' in keys or 'height' in keys or grp=='frame'
    if grp=='head': body=False
    if os.path.exists(O+jid+'.h2'): continue
    if body and MODE=='body':
        q=dict(p); P=vary.warp(V,Lb,q,eye=eye); rv.render(P,Fb,O+jid,BODY,res=600)
    if head and MODE=='surf':
        q=dict(p); P0=vary.warp(S[::50],sub,dict(p),eye=eye) if False else None
        P=warp_chunks(S,Ls,p,eye)
        vw=[]
        pass
        if head: vw.append(head_follow(P,HEAD))
        rv.render(P,Fs,O+jid,';'.join(vw),res=600)
    open(O+jid+'.h2','w').write('1'); print('R',MODE,jid,flush=True)
