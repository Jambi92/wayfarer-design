"""RAC RP1-A feasibility DIAGNOSTIC (not production): does 'coarse cage -> 3 subdivision levels -> projection onto the source'
meet the accepted T-1 / T-2 deviation tolerances at the planned density? The cage here is an automatic QEM decimation, a stand-in
for the manual cage (whose edge flow will be better); its output is discarded. Two-way deviation by zone.
Usage: python3 rp1_projsim.py weld_a.npz zones.npz TARGET_FACES LEVELS OUT.json"""
import sys, json, numpy as np, igl
z = np.load(sys.argv[1]); V = z['V'].astype(np.float64); F = z['F'].astype(np.int64)
Z = np.load(sys.argv[2]); zone = Z['zone']; names = list(Z['names']); nf = int(sys.argv[3]); lev = int(sys.argv[4])
Vc, Fc, _, _ = igl.decimate(V, F.astype(np.int32), nf); Fc = Fc.astype(np.int64)
Vs, Fs = Vc, Fc
for i in range(lev):
    Vs, Fs = igl.loop(Vs, Fs)
    d2, I, C = igl.point_mesh_squared_distance(Vs, V, F); Vs = C          # project every level (snap to surface)
# production -> source: sample face centroids and edge midpoints of the projected mesh
S = np.vstack([Vs[Fs].mean(1), (Vs[Fs[:, 0]] + Vs[Fs[:, 1]]) / 2])
dps, Ips, _ = igl.point_mesh_squared_distance(S, V, F); dps = np.sqrt(dps); zps = zone[F[Ips, 0]]
dsp, _, _ = igl.point_mesh_squared_distance(V, Vs, Fs); dsp = np.sqrt(dsp)
out = {'cage_faces': int(len(Fc)), 'levels': lev, 'final_vertices': int(len(Vs)), 'final_triangles': int(len(Fs)), 'zones': {}}
for i, nm in enumerate(names):
    a = dps[zps == i] * 10; b = dsp[zone == i] * 10
    if len(b) == 0: continue
    out['zones'][nm] = {'prod_to_src_mm': [round(float(x), 3) for x in (np.median(a), np.percentile(a, 95), a.max())],
                        'src_to_prod_mm': [round(float(x), 3) for x in (np.median(b), np.percentile(b, 95), b.max())]}
json.dump(out, open(sys.argv[5], 'w'), indent=1); np.savez_compressed(sys.argv[5].replace('.json', '_dist.npz'), dsp=dsp.astype(np.float32), Vs=Vs.astype(np.float32), Fs=Fs.astype(np.int32)); print(json.dumps(out, indent=1))
