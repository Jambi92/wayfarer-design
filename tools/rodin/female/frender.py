import numpy as np, pickle, sys, os, copy; sys.path.insert(0,'/tmp/claude-0/rodin/v1'); sys.path.insert(0,'/tmp/claude-0/rodin/v3')
import vary, rv, fsets
sys.path.insert(0,'/tmp/claude-0/rb'); import wf_saurin_head63 as H; eye=(H.eye_centers()[0],H.eye_centers()[1])
MODE=sys.argv[1]; O='/tmp/claude-0/rodin/v3/R/'
BODY="front:0:0:0:0:104:216;profile:90:0:0:-52:104:268;rear34:150:0:0:-25:104:230;t34:45:0:0:0:118:105"
PEL="pR34:150:8:0:-14:96:52;pP:90:0:0:-12:96:52;pF:0:0:0:0:94:48;pV:0:-55:0:2:92:50"
HEAD="hF:0:3:0:10:180:24;hP:90:0:0:8:181:32;hF34:40:12:0:8:181:26;hT:0:89:0:5:184:30"
J={j[0]:j for j in fsets.JOBS}
if MODE=='body':
    L=pickle.load(open('/tmp/claude-0/rodin/v1/Lbase.pkl','rb')); z=np.load(vary.REF_BASE); V=z['V'].astype(float); Fb=z['F']
    for jid,lab,sex,p in fsets.JOBS:
        if os.path.exists(O+jid+'_t34.png'): continue
        P=vary.warp(V,L,dict(p),eye=eye); rv.render(P,Fb,O+jid,BODY,res=600); print('B',jid,flush=True)
else:
    L=pickle.load(open('/tmp/claude-0/rodin/v1/Lsurf.pkl','rb')); z=np.load(vary.REF_SURF); S=z['V'].astype(float); Fs=z['F']
    N=len(S); top=np.where(S[:,2]>183)[0]
    def sub(ii):
        Lc=copy.copy(L)
        for k,v in L.__dict__.items():
            if isinstance(v,np.ndarray) and len(v)==N: setattr(Lc,k,v[ii])
        return Lc
    def warpc(p):
        q=dict(p); q['_hmeas']=1.0; q['height']=1.0; h=vary.warp(S[top],sub(top),q,eye=eye)[:,2].max()
        out=np.empty_like(S)
        for ii in np.array_split(np.arange(N),6):
            q=dict(p); q['_hmeas']=h; out[ii]=vary.warp(S[ii],sub(ii),q,eye=eye)
        return out
    for jid in sys.argv[2:]:
        p=J[jid][3]; P=warpc(p); views=PEL+';'+HEAD
        rv.render(P,Fs,O+jid,views,res=600); print('S',jid,flush=True)
        if jid in ('f_ref','m_ref'):
            np.save(O+jid+'_disp.npy',(P-S)[S[:,2]>160].astype(np.float32)); np.save(O+'headidx.npy',np.where(S[:,2]>160)[0])
