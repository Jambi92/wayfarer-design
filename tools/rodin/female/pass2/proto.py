import numpy as np, pickle, sys, json; sys.path.insert(0,'/tmp/claude-0/rodin/v1'); sys.path.insert(0,'/tmp/claude-0/rodin/v4')
import vary, rv, tissue, fsets2, metrics
sys.path.insert(0,'/tmp/claude-0/rb'); import wf_saurin_head63 as H; eye=(H.eye_centers()[0],H.eye_centers()[1])
L=pickle.load(open('/tmp/claude-0/rodin/v1/Lbase.pkl','rb')); z=np.load(vary.REF_BASE); V=z['V'].astype(float); F=z['F']
J={j[0]:j for j in fsets2.JOBS}
V_="tq:40:5:0:0:129:70;tp:90:0:0:4:127:62;tf:0:0:0:0:128:62;front:0:0:0:0:104:216"
for jid in sys.argv[1:]:
    P=tissue.fwarp(V,L,dict(J[jid][3]),eye=eye); rv.render(P,F,'/tmp/claude-0/rodin/v4/R/pr_'+jid,V_,res=500); print(jid,flush=True)
