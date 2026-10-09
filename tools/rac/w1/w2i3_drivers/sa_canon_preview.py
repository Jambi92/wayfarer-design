# RAC W2I3 §16 canonicalization PREVIEW (no overwrite): writes the rebuilt candidate base (SA-M188 rebuilt L1 + F2, neutral carriage, C0
# contour) to the scratch area as {v, f} like saurin_final_base.npz, and reports SHA-256 of the file and of the vertex / face arrays beside the
# frozen reference; the §263 SA-F is a parameter state regenerated from the base (its rebuilt realization hash is reported for traceability).
# Usage: python3 sa_canon_preview.py OUT.json
import sys, os, json, hashlib, numpy as np
D = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, D)
import sa_rebuild as RB, sa_build as B
S = B.C.S + '/w2i3/canon_preview'; os.makedirs(S, exist_ok=True)
sha = lambda b: hashlib.sha256(b).hexdigest()
out = {"frozen": {"file": "saurin_final_base.npz", "sha256": sha(open('/mnt/attach/outputs/racebodies_v35/saurin_final_base.npz', 'rb').read()) if os.path.exists('/mnt/attach/outputs/racebodies_v35/saurin_final_base.npz') else None}}
for nm, p in (("SA-M188_rebuilt_base", {}), ("SA-F188_rebuilt_realization", B.CEN)):
    P = RB.build_r(p, RB.TARGET)[0].astype(np.float32); fn = S + '/%s.npz' % nm; np.savez_compressed(fn, v=P, f=RB.F0.astype(np.int32))
    out[nm] = dict(file=fn, file_sha256=sha(open(fn, 'rb').read()), v_sha256=sha(P.tobytes()), f_sha256=sha(RB.F0.astype(np.int32).tobytes()), n_vertices=int(len(P)), height=float(P[:, 2].max()))
    print(nm, out[nm]['file_sha256'][:16], flush=True)
json.dump(out, open(sys.argv[1], 'w'), indent=1)
