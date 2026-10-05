import numpy as np, pickle, sys, json; sys.path.insert(0,'/tmp/claude-0/rodin/v1'); sys.path.insert(0,'/tmp/claude-0/rodin/v3')
import vary, metrics, evaluate as EV, fsets
L=pickle.load(open('/tmp/claude-0/rodin/v1/Lbase.pkl','rb')); z=np.load(vary.REF_BASE); V=z['V'].astype(float); F=z['F'].astype(np.int64); L._u0=V[:,2]; L._f0=V[:,1]
sys.path.insert(0,'/tmp/claude-0/rb'); import wf_saurin_head63 as H; eye=(H.eye_centers()[0],H.eye_centers()[1])
lm=pickle.load(open('/tmp/claude-0/rodin/v1/lm.pkl','rb')); ref=json.load(open('/tmp/claude-0/rodin/v1/ref_metrics.json'))
out={}
for jid,lab,sex,p in fsets.JOBS:
    q=dict(p); P=vary.warp(V,L,q,eye=eye); M=metrics.measure(P,F,L,q,lm,ref); M.pop('_A')
    # extra: lower-trunk length (hip joint level 91 -> costal margin 123 mapped) and pelvic floor height
    x,f,u=P.T; tor=L.torso>0.6
    M['pelvic_floor_u']=float(np.percentile(u[(np.abs(x)<3)&(np.abs(f-2)<6)&tor&(V[:,2]>78)&(V[:,2]<95)],1)) if ((np.abs(x)<3)&tor).any() else -1
    d,h,s=EV.classify(M,p); out[jid]=dict(label=lab,sex=sex,params=p,metrics={k:float(v) for k,v in M.items()},hard=h,soft=s,derived={k:float(d[k]) for k in ('tail_RSI_n','d_lean','lean_req_deg')})
    print(jid,'H %.1f trunk? tl %.1f%% RSI %.2f tap %.2f A50 %.2f dlean %+.2f dw %.3f pel %.1f hl %.3f'%(M['height'],M['tail_len_pct'],d['tail_RSI_n'],M['tail_taper'],M['tail_A50'],d['d_lean'],M['thorax_d_over_w'],M['pelvis_w'],M['head_len_ratio']),h,flush=True)
json.dump(out,open('fsweep.json','w'),indent=1)
