import numpy as np, pickle, sys, json; sys.path.insert(0,'/tmp/claude-0/rodin/v1'); import vary, metrics, sets
L=pickle.load(open('Lbase.pkl','rb')); z=np.load(vary.REF_BASE); V=z['V'].astype(float); F=z['F'].astype(np.int64); L._u0=V[:,2]; L._f0=V[:,1]
sys.path.insert(0,'/tmp/claude-0/rb'); import wf_saurin_head63 as H
eye=(H.eye_centers()[0],H.eye_centers()[1])
lm=pickle.load(open('lm.pkl','rb')); ref=json.load(open('ref_metrics.json'))
out={}; prof={}
jobs=[('ref','Reference','ref',{})]+sets.SINGLE+[(a,b,'combo',c) for a,b,c in sets.COMBO]
for jid,lab,grp,p in jobs:
    q=dict(p); P=vary.warp(V,L,q,eye=eye); Mx=metrics.measure(P,F,L,q,lm,ref)
    prof[jid]=Mx.pop('_A'); out[jid]=dict(label=lab,group=grp,params={k:v for k,v in p.items()},metrics={k:float(v) for k,v in Mx.items()})
    print(jid, ' '.join('%s=%.3f'%(k,Mx[k]) for k in ('height','tail_len_pct','tail_RSI','tail_taper','tail_A50','tail_min_u','lean_req_deg','rostral_index','head_len_ratio','thorax_d_over_w') if k in Mx), flush=True)
json.dump(out,open('sweep.json','w'),indent=1); pickle.dump(prof,open('profiles.pkl','wb'))
