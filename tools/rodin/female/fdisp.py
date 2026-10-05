import numpy as np, pickle, sys; sys.path.insert(0,'/tmp/claude-0/rodin/v1'); sys.path.insert(0,'/tmp/claude-0/rodin/v3')
import vary, rv, fsets
from scipy.spatial import cKDTree
sys.path.insert(0,'/tmp/claude-0/rb'); import wf_saurin_head63 as H; eye=(H.eye_centers()[0],H.eye_centers()[1])
O='/tmp/claude-0/rodin/v3/R/'; CUT=172.5
S=np.load(vary.REF_SURF)['V'].astype(float); hidx=np.load(O+'headidx.npy'); disp=np.load(O+'f_ref_disp.npy').astype(float)
tr=cKDTree(S[hidx])
L=pickle.load(open('/tmp/claude-0/rodin/v1/Lbase.pkl','rb')); zb=np.load(vary.REF_BASE); V=zb['V'].astype(float); Fb=zb['F']
p=dict(fsets.FEM); Pb=vary.warp(V,L,p,eye=eye)
keepb=~(V[Fb][:,:,2]>CUT).all(1); Fb2=Fb[keepb]
for dk,lab in (('d00','naked'),('d13','minimal'),('dsw','swept'),('dmx','mixed'),('dcr','crest')):
    z=np.load('/tmp/claude-0/rodin/v1/dv/hvs_%s.npz'%dk); Q=z['V'].astype(float); Fq=z['F'].astype(np.int64)
    d,j=tr.query(Q); Q2=Q+disp[j]
    kq=(Q[Fq][:,:,2]>CUT).all(1); Fq2=Fq[kq]+len(Pb)
    P=np.vstack([Pb,Q2]); FF=np.vstack([Fb2,Fq2])
    rv.render(P,FF,O+'fd_'+dk,"front34:45:0:0:0:104:216;hF34:40:12:0:8:181:30;hP:90:0:0:4:182:36",res=600); print(dk,flush=True)
