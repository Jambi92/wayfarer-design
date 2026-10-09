# RAC W2I4 §7 scale-field continuity check. For each region the scale relief (normal displacement field) is sampled at base vertices and its
# autocorrelation length is measured along the local vertical tangent and the horizontal tangent (distance, in units of the local scale size R,
# at which the correlation of the displacement drops to 0.5; nearest-vertex lookup on the respective geometry). Compared:
#   frozen  = accepted frozen field on the frozen base (control);
#   before  = the accepted frozen field carried by vertex index onto the finished L1 + F2 base (what an un-regenerated asset would show);
#   after   = the W2I4 regenerated field on the finished base.
# A stretched field shows a vertical / horizontal length ratio departing from the frozen control (x1.5 thigh, compressed neck); a regenerated
# field should match the control. Also reports the seed nearest-neighbour spacing / R per region (regenerated field). Usage: python3 sa_fieldcheck.py OUT.json
import sys, os, json, numpy as np, igl
from scipy.spatial import cKDTree
D = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, D)
import sa_finish as FN
S = FN.C.S; L = FN.L; V0 = FN.V0; nb = len(V0)
up0 = np.load(S + '/w2i/rodin/c12/g15up.npz'); V0u = up0['V'].astype(float); F = up0['F'].astype(np.int64)
Vf = np.load(S + '/w2i4/surf/fin_up.npz')['V'].astype(float)
N0 = igl.per_vertex_normals(V0u, F); Nf = igl.per_vertex_normals(Vf, F)
s_froz = (np.load('/mnt/attach/outputs/racebodies_v35/saurin_final_surface_delta.npz')['d'].astype(float) * N0).sum(1)
s_new = (np.load(S + '/w2i4/surf/saurin_w2i4_surface_delta.npz')['d'].astype(float) * Nf).sum(1)
reg = np.load(S + '/w2i/rodin/c12/g15reg.npz'); R = reg['R'].astype(float); FAM = reg['FAM']
u0 = V0[:, 2]; ax = np.abs(V0[:, 0])
REG = dict(thigh=(L.leg > 0.6) & (u0 > 66) & (u0 < 84) & (L.tail < 0.05), knee=(L.leg > 0.6) & (u0 > 52) & (u0 < 63),
           shank=(L.leg > 0.6) & (u0 > 25) & (u0 < 45), pelvis=(u0 > 90) & (u0 < 100) & (L.leg < 0.2) & (L.tail < 0.05) & (L.arm < 0.1),
           thorax=(u0 > 128) & (u0 < 145) & (L.arm < 0.1) & (ax < 12), neck=(u0 > 155) & (u0 < 168) & (L.head < 0.3) & (L.arm < 0.1),
           shoulder=(u0 > 140) & (u0 < 152) & (ax > 14) & (L.arm < 0.6), upperarm=(L.arm > 0.6) & (u0 > 115) & (u0 < 135), forearm=(L.arm > 0.6) & (u0 > 92) & (u0 < 108))
DEL = np.array([0.02, 0.04, 0.06, 0.09, 0.12, 0.16, 0.2, 0.25, 0.3, 0.4, 0.5, 0.6])   # x local scale size R
def corrlen(V, Nrm, s, idx, rng):
    tr = cKDTree(V); out = {}
    smp = rng.choice(idx, min(6000, len(idx)), replace=False)
    n = Nrm[smp]; zt = np.array([0, 0, 1.0]) - n * n[:, 2:3]; zt /= np.linalg.norm(zt, axis=1, keepdims=True) + 1e-12; ht = np.cross(n, zt)
    for nm, t in (('vertical', zt), ('horizontal', ht)):
        c = []
        for dl in DEL:
            j = tr.query(V[smp] + (dl * R[smp])[:, None] * t)[1]; c.append(np.corrcoef(s[smp], s[j])[0, 1])
        c = np.array(c); k = np.where(c < 0.5)[0]
        out[nm] = float(np.interp(0.5, [c[k[0]], c[k[0] - 1]], [DEL[k[0]], DEL[k[0] - 1]])) if len(k) and k[0] > 0 else float('nan')
    out['v_over_h'] = out['vertical'] / out['horizontal']; return out
def main():
    res = {}; seeds = np.load(S + '/w2i4/surf/fin_seeds.npy'); ts = cKDTree(Vf[seeds]); dd, _ = ts.query(Vf[seeds], k=2); nn = dd[:, 1] / R[seeds]
    for nm, m in REG.items():
        idx = np.where(m & ((FAM[:nb] != 6) & (FAM[:nb] != 7)))[0]; rng = np.random.default_rng(3)
        r = dict(n=int(len(idx)), median_R_cm=float(np.median(R[idx])))
        for fld, V, Nrm, s in (('frozen', V0u, N0, s_froz), ('before', Vf, Nf, s_froz), ('after', Vf, Nf, s_new)): r[fld] = corrlen(V, Nrm, s, idx, np.random.default_rng(3))
        tb = cKDTree(V0[idx]); ins = seeds[seeds < nb]; ins = ins[np.isin(ins, idx)]
        r['after_seed_nn_over_R_median'] = float(np.median(nn[np.isin(seeds, ins)])) if len(ins) else None
        res[nm] = r; print(nm, {k: (round(v['v_over_h'], 3) if isinstance(v, dict) else v) for k, v in r.items()}, flush=True)
    res['all_seeds_nn_over_R'] = dict(p10=float(np.percentile(nn, 10)), p50=float(np.median(nn)), p90=float(np.percentile(nn, 90)))
    json.dump(res, open(sys.argv[1], 'w'), indent=1)
if __name__ == '__main__': main()
