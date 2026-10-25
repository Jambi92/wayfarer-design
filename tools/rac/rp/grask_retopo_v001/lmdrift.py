# lmdrift.py SRC_LM.json PROD_LM.json OUT.json : T-6 landmark drift (same methods re-run on the production mesh)
import json, numpy as np, sys
A=json.load(open(sys.argv[1])); B=json.load(open(sys.argv[2])); out={}
for k in A:
    d=float(np.linalg.norm(np.array(A[k]['p'])-np.array(B[k]['p']))*10); out[k]=dict(drift_mm=round(d,3),method=A[k]['method'])
v=np.array([o['drift_mm'] for o in out.values()])
R=dict(n=len(v),max_mm=float(v.max()),median_mm=float(np.median(v)),over_1mm={k:o for k,o in out.items() if o['drift_mm']>1.0},over_1_5mm=[k for k,o in out.items() if o['drift_mm']>1.5],all=out)
json.dump(R,open(sys.argv[3],'w'),indent=1)
print('n',R['n'],'max',round(R['max_mm'],3),'median',round(R['median_mm'],3),'>1.0',list(R['over_1mm']),'>1.5',R['over_1_5mm'])
