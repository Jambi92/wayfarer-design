# RAC W2D: composition state on an existing W2D Gorrund skeleton: envelope = that body's sculpted skeleton (-LEAN) + (donor at composition
# (m, w) - donor lean), donor = the same body's tissue donor (as w1k_drivers/gr_build.py 'comp' and the W1 GOR-BODY-16 route). Skin
# measurement only; the skeleton (every skeletal reading) is the source body's.   Usage: python3 go_comp.py NEW_NAME SOURCE_BODY MUSCLE WEIGHT
import sys, os, json, subprocess
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import go_body as GB, skeleton_envelope as SE
nm, body, m, w = sys.argv[1], sys.argv[2], float(sys.argv[3]), float(sys.argv[4])
rec = json.load(open(GB.W + '/b/%s/%s_w2d.json' % (body, body))); did = rec["donor"]; hd = GB.W + '/h'
cid = '%s-C%03d%03d' % (did, round(m * 100), round(w * 100)); src = GB.G + '/donor/' + cid
if not os.path.exists(src + '_rest.npz'): GB.bv(hd + '/%s_build.json' % did, {"muscle": m, "weight": w}, GB.G + '/donor', cid)
out = GB.W + '/b/' + nm; os.makedirs(out, exist_ok=True)
SE.make(GB.W + '/b/%s/%s-LEAN' % (body, body), src, hd + '/' + did + '-LEAN', out + '/' + nm, tag=nm)
subprocess.run(['python3', GB.T + '/run_candidate.py', out, nm, GB.F + '/final/MF-M-R_rest.npz'], capture_output=True, text=True, cwd=GB.T)
json.dump({"name": nm, "skeleton": body, "donor": cid, "muscle": m, "weight": w}, open(out + '/%s_w2d.json' % nm, 'w'), indent=1); print('BUILT', nm, flush=True)
