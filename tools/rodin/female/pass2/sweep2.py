import numpy as np, pickle, sys, json; sys.path.insert(0,'/tmp/claude-0/rodin/v1'); sys.path.insert(0,'/tmp/claude-0/rodin/v4')
import vary, metrics, evaluate as EV, fsets2, tissue
L=pickle.load(open('/tmp/claude-0/rodin/v1/Lbase.pkl','rb')); z=np.load(vary.REF_BASE); V=z['V'].astype(float); F=z['F'].astype(np.int64); L._u0=V[:,2]; L._f0=V[:,1]
sys.path.insert(0,'/tmp/claude-0/rb'); import wf_saurin_head63 as H; eye=(H.eye_centers()[0],H.eye_centers()[1])
lm=pickle.load(open('/tmp/claude-0/rodin/v1/lm.pkl','rb')); ref=json.load(open('/tmp/claude-0/rodin/v1/ref_metrics.json'))
x0,f0,u0=V.T; tor=L.torso>0.6
out={}
for jid,lab,sex,p in fsets2.JOBS:
    q=dict(p); P=tissue.fwarp(V,L,q,eye=eye); M=metrics.measure(P,F,L,q,lm,ref); M.pop('_A')
    x,f,u=P.T; s=q['_s']
    # extra measures: ventral projection (max f of torso, 112-150 band), lower-trunk length (hip 91 -> costal 123 ref landmarks), max chest width
    vb=tor&(u0>112)&(u0<150); M['ventral_f']=float(f[vb].max()-np.interp(130,np.arange(200),L.torso_cf)*s)
    i91=np.argmin(np.abs(u0-91)+100*(~tor)); i123=np.argmin(np.abs(u0-123)+100*(~tor)); M['lower_trunk']=float(u[i123]-u[i91])
    M['chest_w']=float(np.ptp(x[tor&(u0>128)&(u0<142)]))
    M['abd_w']=float(np.ptp(x[tor&(u0>104)&(u0<116)]))
    d,h,sft=EV.classify(M,p)
    out[jid]=dict(label=lab,sex=sex,params={k:v for k,v in p.items()},metrics={k:float(v) for k,v in M.items()},hard=h,soft=sft,derived={k:float(d[k]) for k in ('tail_RSI_n','d_lean','lean_req_deg')})
    print(jid,'H %.1f lt %.1f pel %.2f chw %.2f vf %.2f td %.2f dw %.3f dlean %+.2f hl %.4f tl %.1f RSI %.2f'%(M['height'],M['lower_trunk'],M['pelvis_w'],M['chest_w'],M['ventral_f'],M['thorax_d'],M['thorax_d_over_w'],d['d_lean'],M['head_len_ratio'],M['tail_len_pct'],d['tail_RSI_n']),h,flush=True)
json.dump(out,open('/tmp/claude-0/rodin/v4/sweep2.json','w'),indent=1)
