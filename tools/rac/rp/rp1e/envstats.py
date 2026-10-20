# envstats.py GATEDIR DMASK_V1,DMASK_V2 : production-envelope T-1/T-2 (src->prod with the two frozen D masks excluded) + D area share
import sys,json,numpy as np
G=sys.argv[1]; D=np.load(G+'/deviation_arrays.npz'); r=json.load(open(G+'/rp1_gate.json'))
zz=np.load('/home/claude/stc/rp1/zones.npz'); zone=zz['zone']; names=list(zz['names'])
ex=np.zeros(len(zone),bool)
for f in sys.argv[2].split(','): ex[np.load(f)]=True
dsp=D['src_to_prod_mm']; out={}
for i,nm in enumerate(names):
    lim=(0.5,1.5,3.0) if nm=='general' else (0.3,0.8,1.5); b=dsp[(zone==i)&~ex]
    st=[round(float(v),3) for v in (np.median(b),np.percentile(b,95),b.max())]; pa=r['deviation'][nm]['prod_to_src_mm']
    ok=all(q[0]<=lim[0] and q[1]<=lim[1] and q[2]<=lim[2] for q in (pa,st))
    out[nm]=dict(limit=lim,prod_to_src_mm=pa,src_to_prod_envelope_mm=st,src_to_prod_raw_mm=r['deviation'][nm]['src_to_prod_mm'],excluded_D_vertices=int(((zone==i)&ex).sum()),within=ok)
    print(nm,out[nm])
json.dump(out,open(G+'/envelope.json','w'),indent=1)
