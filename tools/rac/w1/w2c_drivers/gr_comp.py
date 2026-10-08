# RAC W2C: composition state on an existing W2C Grask skeleton (as w1k_drivers/gr_build.py 'comp'): envelope = that body's skeleton
# (-LEAN) + (donor at composition (m, w) - donor lean), donor = the same body's tissue donor. Skin measurement only (the skeleton,
# hence every skeletal reading, is the frame / stature body's).   Usage: python3 gr_comp.py NEW_NAME SKELETON_BODY MUSCLE WEIGHT
import sys, os, json, subprocess
T = '/home/claude/wayfarer-design/tools/rac/w1'; sys.path.insert(0, T); sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import skeleton_envelope as SE, gr_body as GB
nm, body, m, w = sys.argv[1], sys.argv[2], float(sys.argv[3]), float(sys.argv[4])
rec = json.load(open(GB.W + '/b/%s/%s_w2c.json' % (body, body))); did = rec["donor"]; dd = GB.W + '/donor'
cid = '%s-C%03d%03d' % (did, round(m * 100), round(w * 100))
if not os.path.exists(dd + '/%s_rest.npz' % cid): GB.bv(dd + '/%s_build.json' % did, {"muscle": m, "weight": w}, dd, cid)
out = GB.W + '/b/' + nm; os.makedirs(out, exist_ok=True)
SE.make(GB.W + '/b/%s/%s-LEAN' % (body, body), dd + '/' + cid, dd + '/' + did + '-LEAN', out + '/' + nm, tag=nm)
subprocess.run(['python3', T + '/run_candidate.py', out, nm, GB.F + '/final/MF-M-R_rest.npz'], capture_output=True, text=True, cwd=T)
json.dump({"name": nm, "skeleton": body, "donor": cid, "muscle": m, "weight": w}, open(out + '/%s_w2c.json' % nm, 'w'), indent=1); print('BUILT', nm, flush=True)
