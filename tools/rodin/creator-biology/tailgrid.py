import numpy as np, pickle, sys, json; sys.path.insert(0,'/tmp/claude-0/rodin/v1'); import vary, metrics
L=pickle.load(open('Lbase.pkl','rb')); z=np.load(vary.REF_BASE); V=z['V'].astype(float); F=z['F'].astype(np.int64); L._u0=V[:,2]; L._f0=V[:,1]
lm=pickle.load(open('lm.pkl','rb')); ref=json.load(open('ref_metrics.json'))
# restrict the warp/measure to the tail + pelvis for speed: tail metrics and whole-body COM need the full mesh, keep full
KS=[0.80,55/64.613,0.95,1.0,1.10,1.20,80/64.613,1.30]; BS=[0.80,0.85,0.92,1.0,1.08,1.15,1.22,1.30]; TS=[0.85,1.0,1.15]
out=[]
for t in TS:
  for k in KS:
    for b in BS:
        p={'tail_len':k,'tail_base':b,'tail_taper':t}; P=vary.warp(V,L,p); Mx=metrics.measure(P,F,L,p,lm,ref); Mx.pop('_A')
        out.append(dict(k=k,b=b,t=t,**{kk:float(Mx[kk]) for kk in ('tail_len_pct','tail_RSI','tail_taper','tail_A50','tail_A25','tail_A75','tail_vol_L','tail_root_area','tail_min_u','lean_req_deg','com_f','tail_mass_share')}))
        print(t,k,b,'%.3f %.3f %.3f %.2f'%(out[-1]['tail_RSI'],out[-1]['tail_taper'],out[-1]['tail_A50'],out[-1]['lean_req_deg']),flush=True)
json.dump(out,open('tailgrid.json','w'),indent=1)
