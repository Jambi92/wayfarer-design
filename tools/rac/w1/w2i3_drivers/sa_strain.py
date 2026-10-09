# RAC W2I3 §4: surface strain of the W2I2 diagnostic warp vs the W2I3 rebuild (per-edge length ratio vs the frozen as-built body at the same
# stature, by region) for SA-M188 / SA-F188, plus the rebuild's peak field densities. Usage: python3 sa_strain.py OUT.json
import sys, os, json
D = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, D)
import sa_rebuild as RB, sa_cand as SC, sa_build as B
out = {}
for bid, p in (("SA-M188", {}), ("SA-F188", B.CEN)):
    P0 = RB.build_r(p, {})[0]; Pd = SC.build_c(p, {'G': 9.2, 'FT': 0.4, 'fa_delta': 4.2})[0]; Pr, q, k, info = RB.build_r(p, RB.TARGET)
    out[bid] = {"W2I2_diagnostic": RB.strain(P0, Pd), "W2I3_rebuild": RB.strain(P0, Pr), "rebuild_fields": info}
    print(bid, {nm: out[bid][nm]['flipped_faces'] for nm in ('W2I2_diagnostic', 'W2I3_rebuild')}, flush=True)
json.dump(out, open(sys.argv[1], 'w'), indent=1, default=float)
