import numpy as np, json, os, sys
from scipy.spatial import cKDTree
sys.path.insert(0,'/tmp/claude-0/rodin/v1'); from meas import mass_props
D='/tmp/claude-0/rodin/v1/dv/'
base=np.load(D+'hvs_d00.npz'); B=base['V'].astype(float); BF=base['F'].astype(np.int64); tr=cKDTree(B)
volB,_=mass_props(B,BF)
AT=np.array([0.0,3.0,179.3])
neck=B[(B[:,2]<176)&(B[:,1]<-5)]; trn=cKDTree(neck)
headvol=None
# head mass proxy: baseline patch above the atlas plane u>172
V=[('d13',{}),('dlh',{}),('d01',{}),('d02',{'L':1.5}),('d03',{'L':0.7,'B':0.85}),('d04',{'L':1.5,'B':0.7}),('dsw',{}),('d05',{'L':0.75}),('d06',{'L':1.25}),('d07',{'SW':10}),('d08',{'SW':-12}),('d09',{'L':1.25,'B':0.8}),('dmx',{}),('d10',{'A':0.7}),('dcr',{}),('d11',{'CH':1.6}),('d12',{'CH':3.0})]
FAM={'d13':'ridges','dlh':'hornlets','d01':'hornlets','d02':'hornlets','d03':'hornlets','d04':'hornlets','dsw':'swept','d05':'swept','d06':'swept','d07':'swept','d08':'swept','d09':'swept','dmx':'mixed','d10':'mixed','dcr':'crest','d11':'crest','d12':'crest'}
RATIO={'hornlets':0.29,'swept':0.069,'mixed':0.135,'ridges':1.0,'crest':1.0}   # base radius / chord length of the main structure at reference (from head65 control points)
out={}
z=np.load(D+'hvs_d00.npz'); hm=B[:,2]>172; 
for k,par in V:
    fn=D+'hvs_%s.npz'%k
    if not os.path.exists(fn): continue
    z=np.load(fn); P=z['V'].astype(float); Fv=z['F'].astype(np.int64)
    vol,_=mass_props(P,Fv); dv=vol-volB
    d,_=tr.query(P); dp=P[d>0.4]
    r={}
    r['display_volume_cm3']=round(float(dv),1)
    if len(dp):
        r['max_height_above_skull_cm']=round(float(d.max()),2)
        r['top_u_gain_cm']=round(float(P[:,2].max()-B[:,2].max()),2)
        lever=np.linalg.norm(dp-AT,axis=1).mean(); r['moment_index']=round(float(dv*lever),0)
        far=P[d>1.0]
        r['neck_clearance_cm']=round(float(trn.query(far)[0].min()),2) if len(far) else None
        r['rear_extent_cm']=round(float(B[:,1].min()-dp[:,1].min()),2)
    fam=FAM[k]; L=par.get('L',1.0); Bs=par.get('B',1.0)
    r['footprint_ratio']=round(RATIO[fam]*Bs/L,3) if fam in ('hornlets','swept','mixed') else None
    r['family']=fam; r['params']=par
    out[k]=r; print(k,r)
json.dump(out,open('/tmp/claude-0/rodin/v1/display_metrics_raw.json','w'),indent=1)
