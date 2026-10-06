# RAC W1f driver script AS RUN (scratch paths are the session's working directories; kept for provenance of the AD-G14 construction)
import json, sys, shutil, subprocess; sys.path.insert(0,'.'); sys.path.insert(0,'/home/claude/wayfarer-design/tools/rac/w1')
import gn2
X = [1.10,1.045,1.28,1.20,0.90,1.186, 1.0,1.0,1.06,1.16,1.08,1.02, 1.25,1.50,1.65,1.35,1.0,0.97, 1.16,1.19,1.16,1.11,1.06,1.03]
FR = {"GOR-BODY-04": {"bone_scales": {"LR:clavicle": [1, 0.92, 1], "pelvis": [0.91, 1, 1]}, "kb_nodes": [0.95, 0.93, 0.92, 0.83, 0.85, 0.92]},
      "GOR-BODY-12": {"bone_scales": {"LR:clavicle": [1, 0.88, 1], "pelvis": [0.865, 1, 1]}, "kb_nodes": [0.925, 0.895, 0.88, 0.75, 0.78, 0.88]},
      "GOR-BODY-14": {"ka": 0.88, "kp": 0.88, "kd_from": 0.44}}
out = {"main": {"x": X, "unpack": gn2.unpack(X)}}
B, sc, r = gn2.build(X, 'GOFIN'); out["main"]["envelope"] = r
for k, fr in FR.items():
    B, sc, r = gn2.build(X, k, frame=fr); out[k] = {"frame_write": fr, "bone_scales": B, "sculpt": sc, "envelope": r}
B, sc, r = gn2.build(X, 'GOR-BODY-16', comp_donor=gn2.D + '/GO0-LOW'); out['GOR-BODY-16'] = {"composition": {"muscle": 0.25, "weight": 0.25}, "bone_scales": B, "sculpt": sc, "envelope": r}
json.dump(out, open(gn2.D + '/go_final_builds.json', 'w'), indent=1)
print(json.dumps({k: v.get('envelope', {}).get('r6', {}).get('stature') for k, v in out.items()}))
