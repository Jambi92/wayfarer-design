# orbital placement diagnostic: move each orbit (eye + lids + rim, smooth falloff) in the skull's own frame; brow/postorbital planes are NOT rebuilt
import numpy as np, sys; sys.path.insert(0,'/tmp/claude-0/rodin/v1'); sys.path.insert(0,'/tmp/claude-0/rb')
import vary, rv, wf_saurin_head63 as H
z=np.load(vary.REF_SURF); S=z['V'].astype(float); F=z['F'].astype(np.int64)
keep=S[:,2]>168; fk=keep[F].all(1); Fh=F[fk]; ids=np.unique(Fh); rm=-np.ones(len(S),int); rm[ids]=np.arange(len(ids)); Sh=S[ids]; Fh=rm[Fh]
E,r,_=H.eye_centers(); E=[np.array(e) for e in E]
L=vary.head_local(Sh)
def move(dx,du,R=2.6):
    Q=L.copy()
    for e in E:
        sx=np.sign(e[0]); d=np.linalg.norm(L-e,axis=1); w=1-vary.ss(d/R)
        Q[:,0]+=w*dx*sx; Q[:,2]+=w*du
    return vary.head_world(Q)
interorb=abs(E[0][0]-E[1][0]); print('interorbital (local) %.2f cm, eye r %.2f'%(interorb,r))
V="hF:0:3:0:10:180:24;hF34:40:12:0:8:181:26;oC:60:10:4.5:6:183:10;hT:0:89:0:5:184:30"
for nm,dx,du in (('ref',0,0),('sp_m3',-0.03*interorb/2*2,0),('sp_p3',0.03*interorb/2*2,0),('up',0,0.25),('dn',0,-0.25)):
    rv.render(move(dx,du),Fh,'/tmp/claude-0/rodin/v2/OR_'+nm,V,res=600); print(nm,dx,du,flush=True)
