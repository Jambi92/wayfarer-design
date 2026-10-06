# RAC W1g driver AS RUN (scratch paths = this session's working directories; kept for provenance).
"""Gorrund W1g stress bodies on the final W1g skeleton (gn4 parameters), all through the AD-G14 route with the CIB bony envelope:
frames GOR-BODY-04 / -12 / -14 (W1f frame writes on top of the W1g skeleton), GOR-BODY-02 (208 cm), GOR-BODY-03 (maximum
generator-reachable height), GO at 215 / 222 cm, and Broad Skarn (W1f frame write) at 215 / 222 cm (208 / 229 from W1f).
Usage: python3 stress.py params.json out_dir [names...]"""
import sys, os, json, shutil, subprocess
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); sys.path.insert(0, '/home/claude/wayfarer-design/tools/rac/w1')
import gn3, gn4, skeleton_envelope as SE, bony_envelope as BE, skeletal_proxy as SP
G, F, T = gn3.G, gn3.F, gn3.T
FR = {"GOR-BODY-04": {"bone_scales": {"LR:clavicle": [1, 0.92, 1], "pelvis": [0.91, 1, 1]}, "kb_nodes": [0.95, 0.93, 0.92, 0.83, 0.85, 0.92]},
      "GOR-BODY-12": {"bone_scales": {"LR:clavicle": [1, 0.88, 1], "pelvis": [0.865, 1, 1]}, "kb_nodes": [0.925, 0.895, 0.88, 0.75, 0.78, 0.88]},
      "GOR-BODY-14": {"ka": 0.88, "kp": 0.88, "kd_from": 0.44}}
HEIGHTS = {"GOR-BODY-02": (F + '/go/GO2080_build.json', F + '/go/GO2080', 'GO2080'),
           # donors at height macros 0.7438 / 0.7911 / 0.985 so that the GO skeleton lands at about 215 / 222 / 251 cm (first pass
           # with stature-resolved donors landed at 222.8 / 230.0 cm because the skeleton adds height; macro 1.0 gives 252.9 cm)
           "GO-H215": (G + '/h/GO0M215_build.json', G + '/h/GO0M215', 'GO0M215'),
           "GO-H222": (G + '/h/GO0M222_build.json', G + '/h/GO0M222', 'GO0M222'),
           "GOR-BODY-03": (G + '/h/GO0M251_build.json', G + '/h/GO0M251', 'GO0M251')}
SKB_OV = {"muscle": 0.0, "weight": 0.0, "bone_scales": {"LR:clavicle": [1.0, 1.08, 1.0], "spine_01": [1.08, 1.0, 1.0], "spine_02": [1.08, 1.0, 1.04],
          "spine_03": [1.08, 1.0, 1.04], "pelvis": [1.08, 1.0, 1.0], "LR:thigh": [1.05, 1.0, 1.05], "LR:calf": [1.05, 1.0, 1.05],
          "LR:upperarm": [1.05, 1.0, 1.05], "LR:lowerarm": [1.05, 1.0, 1.05]}}

def links(did, dref):
    for st in ("rest", "r6"):
        for t_, src in (("C050050", dref), ):
            p = G + '/donor/%s-%s_%s.npz' % (did, t_, st)
            if not os.path.lexists(p): os.symlink(src + '_%s.npz' % st, p)

def main(pfile, out, only=None):
    x = json.load(open(pfile))["x"]; os.makedirs(out, exist_ok=True)
    rp = out + '/stress_builds.json'; rec = json.load(open(rp)) if os.path.exists(rp) else {}
    for name, fr in FR.items():
        if only and name not in only: continue
        B, sc = gn4.unpack(x, frame=fr); links('GO0', F + '/go/GO0')
        r, C = gn3.build("GO", name, B, sc, wd=out); rec[name] = {"bone_scales": B, "sculpt": sc, "stature": r['r6']['stature'], "S5_argmin": C['argmin']['S5']}
        print(name, rec[name]['stature'], flush=True)
    B, sc = gn4.unpack(x)
    for name, (base, donor, did) in HEIGHTS.items():
        if only and name not in only: continue
        links(did, donor)
        r, C = gn3.build("GO", name, B, sc, wd=out, base=base, donor=donor, did=did); rec[name] = {"bone_scales": B, "sculpt": sc, "stature": r['r6']['stature'], "donor": did}
        print(name, rec[name]['stature'], flush=True)
    for h in (215, 222):
        if only and 'SKB%d' % h not in only: continue
        did = 'SKH%d' % h; links(did, G + '/h/' + did); name = 'SKB%d' % h
        json.dump(SKB_OV, open(out + '/%s_ov.json' % name, 'w'))
        subprocess.run(['python3', T + '/build_variant.py', G + '/h/%s_build.json' % did, out + '/%s_ov.json' % name, out, name + '-LEAN'], check=True, capture_output=True)
        r = SE.make(out + '/' + name + '-LEAN', G + '/h/' + did, G + '/h/' + did + '-LEAN', out + '/' + name, tag=name)
        gd = out + '/grid_' + name; os.makedirs(gd, exist_ok=True)
        comps = BE.assemble_grid(out + '/' + name + '-LEAN', G + '/donor', did, G + '/h/' + did + '-LEAN', gd, name) + [out + '/' + name + '_rest.npz']
        C = BE.cib(out + '/' + name + '_rest.npz', comps); cj = out + '/%s_cib.json' % name; json.dump(C, open(cj, 'w'), indent=1, default=float)
        SP.main(out, out, name, out + '/skp_' + name, cj); rec[name] = {"stature": r['r6']['stature']}
        print(name, rec[name]['stature'], flush=True)
    json.dump(rec, open(out + '/stress_builds.json', 'w'), indent=1, default=float)

if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2], sys.argv[3:] or None)
