# RM-OT-05V production chain: U8 cp1 (frozen) -> neutral ARM candidate GO-ARM-N1, in bounded groups with a verified
# checkpoint after each group. Every step template below is the FROZEN neutralization plan (committed before the production run);
# sets that depend on the current checkpoint are built by v_sets.py inside the chain (deterministic rules).
# Usage: python3 v_chain.py --u8 RETURN.npz --glb base.glb --params organism_params.json --work DIR [--from STEP] [--only STEP]
import argparse, json, os, subprocess, sys, hashlib, time, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); X0 = -0.5
sha = lambda p: hashlib.sha256(open(p, 'rb').read()).hexdigest()

def mirror(spec):
    sys.path.insert(0, HERE); from v_engine import mirror_spec; return mirror_spec(spec, X0)

def lower_leg(side, vb):
    reg = {"type": "box", "lo": [8, -34, -6], "hi": [47, 44, 57]}
    st = {"name": "C1_%s_lower_leg_wrap" % ('+X' if side > 0 else '-X'), "group_code": 3, "vid_base": vb, "region": reg,
          "box": [[5, -37, -4], [50, 47, 60]], "res": 0.8, "t": 3.0, "h": 1.2, "seam_g_max": 1.0,
          "field": {"blur_cm": 1.0, "blur_regions": [{"region": {"type": "box", "lo": [0, -40, 12], "hi": [60, 40, 54]}, "blur_cm": 2.6, "t": 4.0}],
                    "offset_regions": [{"region": {"type": "box", "lo": [0, -40, 13], "hi": [60, 40, 54]}, "extra_cm": 1.2, "t": 3.0}], "ground_z": 0.0}}
    if side < 0:
        st['region'] = mirror(reg); b = st['box']; st['box'] = [[2 * X0 - b[1][0], b[0][1], b[0][2]], [2 * X0 - b[0][0], b[1][1], b[1][2]]]
        for o in st['field']['blur_regions'] + st['field']['offset_regions']: o['region'] = mirror(o['region'])
    return st

PLAN = [
 ("A1", "A", lambda w: {"name": "A1_front_braids_necklace_teeth", "group_code": 1, "vid_base": 1000000,
   "region": {"type": "box", "lo": [-26, 4, 140], "hi": [26, 42, 183]}, "box": [[-31, 0, 136], [31, 46, 187]], "res": 0.7, "t": 2.5, "h": 1.0,
   "seam_g_max": 1.0, "seam_cm": 2.0, "debris_max_faces": 3000, "field": {"open_cm": 3.0, "blur_cm": 1.0}}),
 ("A2", "A", lambda w: {"name": "A2_back_braid", "group_code": 1, "vid_base": 1100000,
   "region": {"type": "box", "lo": [-10, -42, 143], "hi": [10, -12, 176]}, "box": [[-14, -46, 139], [14, -8, 180]], "res": 0.7, "t": 2.5, "h": 1.0,
   "seam_g_max": 1.0, "seam_cm": 2.0, "debris_max_faces": 3000, "field": {"open_cm": 3.0, "blur_cm": 1.0}}),
 ("B1", "B", lambda w: {"name": "B1_+X_forearm_bracer", "group_code": 2, "vid_base": 2000000,
   "region": {"type": "inter", "k": 1.0, "items": [{"type": "voronoi", "a": w + "/B1_A.npy", "b": w + "/B1_B.npy"}, {"type": "capsule", "a": [42.5, 11.5, 100], "b": [36.5, 1, 150], "r": 16}]},
   "box": [[25, -12, 96], [56, 26, 150]], "res": 0.6, "t": 3.0, "h": 0.9, "seam_g_max": 1.0, "seam_cm": 2.0, "debris_max_faces": 3000,
   "debris_keep_points": [[44, 8, 97], [35, 15, 101]],
   "field": {"blur_cm": 1.0, "blur_regions": [{"region": {"type": "capsule", "a": [42.0, 10.5, 110], "b": [36.5, 2, 143], "r": 12}, "blur_cm": 2.4, "t": 5.0}],
             "offset_regions": [{"region": {"type": "capsule", "a": [42.0, 10.5, 110], "b": [36.5, 2, 141], "r": 12}, "extra_cm": 1.0, "t": 5.0}]}}),
 ("B2", "B", lambda w: {"name": "B2_-X_arm_bilateral_counterpart", "group_code": 2, "vid_base": 2100000, "mode": "transplant",
   "region": {"type": "inter", "k": 1.0, "items": [{"type": "voronoi", "a": w + "/B2_A.npy", "b": w + "/B2_B.npy"}, {"type": "box", "lo": [-70, -40, 80], "hi": [-15, 45, 185]}]},
   "transplant": {"mirror_x": X0, "select": {"type": "voronoi", "a": w + "/B2_selA.npy", "b": w + "/B2_selB.npy", "bias": 0.0}},
   "t": 1.0, "h": 0.0, "seam_g_max": 2.0, "seam_cm": 3.5, "seam_iters": 8, "debris_max_faces": 8000, "max_loop_gap_cm": 5.0}),
 ("C1p", "C", lambda w: lower_leg(+1, 3000000)),
 ("C1m", "C", lambda w: lower_leg(-1, 3100000)),
 ("C2p", "C", None), ("C2m", "C", None),
 ("D", "D", lambda w: {"name": "D_pelvis_belt_loincloth_tail", "group_code": 4, "vid_base": 4000000,
   "region": {"type": "inter", "k": 1.0, "items": [{"type": "voronoi", "a": w + "/D_A.npy", "b": w + "/D_B.npy"}, {"type": "box", "lo": [-45, -55, 60], "hi": [45, 50, 152]}]},
   "box": [[-45, -52, 62], [45, 48, 151]], "res": 0.7, "t": 3.0, "h": 1.2, "seam_g_max": 1.0, "seam_cm": 2.5, "debris_max_faces": 8000,
   "field": {"open_cm": 4.5, "blur_cm": 2.5, "offset_cm": 0.0,
     "offset_regions": [{"region": {"type": "box", "lo": [-60, -60, 108], "hi": [60, 60, 141]}, "extra_cm": 1.6, "t": 8.0},
                        {"region": {"type": "box", "lo": [-60, -60, 60], "hi": [60, 60, 112]}, "extra_cm": 1.0, "t": 8.0},
                        {"region": {"type": "sub", "items": [{"type": "box", "lo": [-60, -60, 92], "hi": [60, 60, 122]}, {"type": "xprofile", "xc": X0, "z": [0, 300], "L": [22, 22]}]}, "extra_cm": 2.0, "t": 8.0}],
     "primitives": [{"op": "sub", "k": 1.5, "sdf": {"type": "ellcyl_y", "c": [X0, 66], "a": 9.5, "b": 39.0}},
                    {"op": "union", "k": 2.5, "mesh": {"file": w + "/tail_placed.obj", "blur_cm": 0.8}}]}}),
 ("E", "E", lambda w: {"name": "E_mane_neck_cranium", "group_code": 5, "vid_base": 5000000,
   "region": {"type": "inter", "k": 1.0, "items": [{"type": "voronoi", "a": w + "/E_A.npy", "b": w + "/E_B.npy"}, {"type": "box", "lo": [-45, -45, 160], "hi": [45, 50, 250]}]},
   "box": [[-42, -42, 162], [42, 48, 248]], "res": 0.45, "t": 4.0, "h": 1.3, "seam_g_max": 1.0, "seam_cm": 2.5, "debris_max_faces": 6000, "max_cap_loop": 120,
   "field": {"base": "none", "primitives": [
     {"op": "union", "k": 0.0, "source": {"open_cm": 0, "blur_cm": 0.25, "within": {"type": "ellipsoid", "c": [X0, 26, 207], "radii": [13.5, 22, 17]}, "k": 1.0},
      "note": "facial mask re-extracted from the source (frozen leonine head identity)"},
     {"op": "union", "k": 2.0, "source": {"open_cm": 0, "blur_cm": 0.4, "within": {"type": "capsule", "a": [X0, 13, 170], "b": [X0, 17, 191], "r": 9.0}, "k": 1.5},
      "note": "throat re-extracted from the source"},
     {"op": "union", "k": 4.0, "sdf": {"type": "ellipsoid", "c": [X0, 8, 212], "radii": [14.0, 20.0, 19.0]}, "note": "INFERRED cranial vault (builder value)"},
     {"op": "union", "k": 5.0, "sdf": {"type": "cone", "a": [X0, 3, 206], "b": [X0, 4, 174], "ra": 10.0, "rb": 12.5}, "note": "INFERRED neck (builder value)"},
     {"op": "union", "k": 6.0, "field": {"base": "source", "open_cm": 4.0, "blur_cm": 3.0,
        "offset_regions": [{"region": {"type": "box", "lo": [-60, -60, 171], "hi": [60, 2, 260]}, "extra_cm": 4.0, "t": 6.0}],
        "primitives": [{"op": "inter", "k": 5.0, "sdf": {"type": "halfspace", "n": [0, 0, 1], "d": 181}}]}, "note": "shoulders / upper back below the neck, mane shrunk 4 cm"},
     {"op": "union", "k": 3.0, "sdf": {"type": "union", "items": [{"type": "capsule", "a": [-17.5, 10, 229], "b": [-10, 9, 221], "r": 4.5},
                                                                {"type": "capsule", "a": [16.5, 10, 229], "b": [9, 9, 221], "r": 4.5}]}, "note": "INFERRED broad ear attachments"},
     {"op": "union", "k": 1.0, "mesh": {"file": w + "/E_ears.obj", "blur_cm": 0.3}, "note": "source -X pinna + its bilateral counterpart"}]}}),
]

def run(cmd, log):
    r = subprocess.run(cmd, capture_output=True, text=True); open(log, 'w').write(r.stdout + '\n' + r.stderr); return r.returncode

if __name__ == '__main__':
    ap = argparse.ArgumentParser(); [ap.add_argument(k) for k in ('--u8', '--glb', '--params', '--work', '--from', '--only')]; a = ap.parse_args()
    w = os.path.abspath(a.work); os.makedirs(w, exist_ok=True)
    s0 = os.path.join(w, 'N0.npz')
    if not os.path.exists(s0):
        R = np.load(a.u8); assert sha(a.u8) == '89c1def3f59bf677a7b4ad4eab6ea84d32ee6b4c67755209f1476338e031911d', 'U8 cp1 return.npz differs'
        np.savez_compressed(s0, V=R['V'], F=R['F'].astype(np.int64), vid=R['s3_vid1'].astype(np.int64), fgrp=np.zeros(len(R['F']), np.int8))
    if not os.path.exists(os.path.join(w, 'tail_placed.obj')):
        subprocess.run([sys.executable, os.path.join(HERE, 'v_tail.py'), '--glb', a.glb, '--params', a.params, '--x0', str(X0), '--out', os.path.join(w, 'tail_placed.obj')], check=True)
    prev = s0; started = a.__dict__['from'] is None; summary = []
    for i, (name, grp, tmpl) in enumerate(PLAN):
        out = os.path.join(w, 'S%02d_%s.npz' % (i + 1, name))
        if not started and name == a.__dict__['from']: started = True
        if (not started or (a.only and a.only != name)) and os.path.exists(out): prev = out; continue
        t0 = time.time()
        if name in ('B1', 'B2', 'D', 'E'):
            r = subprocess.run([sys.executable, os.path.join(HERE, 'v_sets.py'), name, prev, w], capture_output=True, text=True, check=True); sets = json.loads(r.stdout.strip().splitlines()[-1])
        else: sets = None
        if name in ('C2p', 'C2m'):
            sp = os.path.join(w, 'step_%s.json' % name)
            subprocess.run([sys.executable, os.path.join(HERE, 'v_feet.py'), '--state', prev, '--side', '1' if name == 'C2p' else '-1', '--out', sp], check=True, capture_output=True)
            st = json.load(open(sp)); st['vid_base'] = 3200000 if name == 'C2p' else 3300000
        else: st = tmpl(w)
        if sets: st['sets'] = sets
        sp = os.path.join(w, 'step_%s.json' % name); json.dump(st, open(sp, 'w'), indent=1)
        rc = run([sys.executable, os.path.join(HERE, 'v_rebuild.py'), '--state', prev, '--step', sp, '--out', out, '--log', out.replace('.npz', '_log.json')], out.replace('.npz', '_stdout.txt'))
        if rc != 0: print(json.dumps(dict(step=name, rebuild_exit=rc))); sys.exit(2)
        vc = run([sys.executable, os.path.join(HERE, 'v_verify.py'), '--prev', prev, '--new', out, '--step', sp, '--out', out.replace('.npz', '_verify.json')], out.replace('.npz', '_verify.txt'))
        v = json.load(open(out.replace('.npz', '_verify.json')))
        row = dict(step=name, group=grp, state=os.path.basename(out), state_sha256=sha(out), verdict=v['verdict'], failed=v['failed'], seconds=round(time.time() - t0, 1))
        summary.append(row); print(json.dumps(row), flush=True)
        if v['verdict'] != 'PASS': print(json.dumps(dict(stop='verification NOT MET', step=name))); sys.exit(3)
        prev = out
    json.dump(summary, open(os.path.join(w, 'chain_summary.json'), 'w'), indent=1)
