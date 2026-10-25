# make_landmarks.py SRC_LM PROD_LM OUT : production landmark package (analysis cm + Blender m, axes, method, v005 value,
# drift, and departure from the old Grask E3 prior seed where one was used)
import json, numpy as np, sys
A=json.load(open(sys.argv[1])); B=json.load(open(sys.argv[2]))
E3=np.load('/tmp/claude-0/rp2/GR5DE3_r6.npz',allow_pickle=True); J=json.loads(str(E3['joints']))
seed={'pelvis_root':'pelvis','spine_01':'spine_01','spine_02':'spine_02','spine_03':'spine_03','neck_base':'neck_01','head_pivot':'head'}
for s in 'lr':
    seed.update({'hip_'+s:'thigh_'+s,'knee_'+s:'calf_'+s,'ankle_'+s:'foot_'+s,'sternoclavicular_'+s:'clavicle_'+s,'glenohumeral_'+s:'upperarm_'+s,'elbow_'+s:'lowerarm_'+s})
bl=lambda p: [p[0]/100.0,-p[1]/100.0,p[2]/100.0]
blax=lambda a: [a[0],-a[1],a[2]]
out={}
for k,b in B.items():
    p=b['p']; e=dict(analysis_cm=[round(v,4) for v in p],blender_m=[round(v,6) for v in bl(p)],method=b['method'])
    if 'axis' in b: e['axis_analysis']=[round(v,5) for v in b['axis']]; e['axis_blender']=[round(v,5) for v in blax(b['axis'])]
    if 'note' in b: e['note']=b['note']
    e['v005_source_cm']=[round(v,4) for v in A[k]['p']]; e['drift_mm']=round(float(np.linalg.norm(np.array(p)-np.array(A[k]['p']))*10),3)
    if k in seed:
        sp=np.array(J[seed[k]][0]); e['prior_seed_E3_cm']=[round(v,3) for v in sp]; e['departure_from_E3_seed_cm']=round(float(np.linalg.norm(np.array(p)-sp)),3)
    out[k]=e
meta=dict(file='GR_U_REF_RP2_retopo_v001_landmarks.json',frames='analysis: cm, x=subject left, f=forward, u=up; blender: m, (x,-f,u)/100, Z up, faces -Y',
          methods='prior-seed+surface-fit = old Grask E3 joint used only as a diagnostic seed, moved by the section-centroid difference between E3 and this mesh; surface-fit = feature measured on this mesh; manual = exact v004/v005 construction point (hand/foot parametric model, v003 eye params) or estimate (jaw hinge)',
          note='landmarks re-measured on the production mesh with the same methods as on v005; drift = production vs v005 measurement',n=len(out))
json.dump(dict(meta=meta,landmarks=out),open(sys.argv[3],'w'),indent=1)
dep={k:v['departure_from_E3_seed_cm'] for k,v in out.items() if 'departure_from_E3_seed_cm' in v}
print('landmarks',len(out),'max drift mm',max(v['drift_mm'] for v in out.values()),'E3 departure cm max',max(dep.values()))
