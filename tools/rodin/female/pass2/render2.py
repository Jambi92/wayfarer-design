import numpy as np, pickle, sys, os, copy; sys.path.insert(0,'/tmp/claude-0/rodin/v1'); sys.path.insert(0,'/tmp/claude-0/rodin/v4')
import vary, rv, fsets2, tissue
sys.path.insert(0,'/tmp/claude-0/rb'); import wf_saurin_head63 as H; eye=(H.eye_centers()[0],H.eye_centers()[1])
MODE=sys.argv[1]; O='/tmp/claude-0/rodin/v4/R/'
BODY="front:0:0:0:0:104:216;profile:90:0:0:-52:104:268;rear34:150:0:0:-25:104:230;tq:40:5:0:0:129:70;tp:90:0:0:4:127:62;tf:0:0:0:0:128:62"
TORS="sq:40:5:0:0:129:70;sp:90:0:0:4:127:62;sf:0:0:0:0:128:62"
PEL="pR34:150:8:0:-14:96:52;pP:90:0:0:-12:96:52;pF:0:0:0:0:94:48;pV:0:-55:0:2:92:50"
J={j[0]:j for j in fsets2.JOBS}
ids=sys.argv[2:] or [j[0] for j in fsets2.JOBS]
if MODE=='body':
    L=pickle.load(open('/tmp/claude-0/rodin/v1/Lbase.pkl','rb')); z=np.load(vary.REF_BASE); V=z['V'].astype(float); Fb=z['F']
    for jid in ids:
        if os.path.exists(O+jid+'_tf.png'): continue
        P=tissue.fwarp(V,L,dict(J[jid][3]),eye=eye); rv.render(P,Fb,O+jid,BODY,res=600); print('B',jid,flush=True)
else:
    L=pickle.load(open('/tmp/claude-0/rodin/v1/Lsurf.pkl','rb')); z=np.load(vary.REF_SURF); S=z['V'].astype(float); Fs=z['F']
    N=len(S); top=np.where(S[:,2]>183)[0]
    def sub(ii):
        Lc=copy.copy(L)
        for k,v in L.__dict__.items():
            if isinstance(v,np.ndarray) and len(v)==N: setattr(Lc,k,v[ii])
        return Lc
    def warpc(p):
        q=dict(p); q['_hmeas']=1.0; q['height']=1.0; Lt=sub(top); St=S[top]+tissue.offset(S[top],Lt,q); h=vary.warp(St,Lt,q,eye=eye)[:,2].max()
        out=np.empty_like(S)
        for ii in np.array_split(np.arange(N),6):
            q=dict(p); q['_hmeas']=h; Li=sub(ii); out[ii]=vary.warp(S[ii]+tissue.offset(S[ii],Li,q),Li,q,eye=eye)
        return out
    for jid in ids:
        p=J[jid][3]; P=warpc(p); views=TORS+(';'+PEL if jid in ('m_ref','A','C') else '')
        rv.render(P,Fs,O+jid,views,res=700); print('S',jid,flush=True)
