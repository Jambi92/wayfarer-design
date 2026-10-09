# RAC W2I5 §4 thigh fine-relief metric (adds the W2I5 final); W2I4 header:
# RAC W2I4 §5 thigh fine-relief metric by sector: vertical / horizontal correlation length (cm) of the 1.5 cm high-pass relief on the
# mid-thigh (frozen base frame u 66-84), for the whole thigh, the anterior / lateral sector (where the W2I4 re-model is applied) and the
# medial / posterior sector (kept as the faired W2I3 form). Frozen (native) vs W2I3 rebuild vs W2I4 finished base. Usage: python3 sa_thighrelief.py OUT.json
import sys, os, json, numpy as np, igl
D = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, D); sys.path.insert(0, os.path.join(os.path.dirname(D), 'w2i4_drivers'))
import sa_sculpt as SC5; import sa_finish as FN; _BUILD4 = FN.build_f; FN.build_f = SC5.build_s   # W2I5: final route = W2I4 route + W2I5 sculpt delta
import sa_fieldcheck as FC
V0 = FN.V0.astype(float); L = FN.L; F0 = FN.F0; RB = FN.RB; ss = FN.ss
FC.R[:] = 1.0; FC.DEL[:] = np.array([0.15, 0.3, 0.5, 0.75, 1.0, 1.5, 2.0, 3.0, 4.0, 5.5, 7.0, 9.0])
mid = (L.leg > 0.6) & (V0[:, 2] > 66) & (V0[:, 2] < 84) & (L.tail < 0.05); al = np.zeros(len(V0))
for sd in (1, -1):
    m = np.where(mid & (L.side == sd))[0]; A0 = V0[m]
    cx = np.polyfit(A0[:, 2], np.abs(A0[:, 0]), 2); cf = np.polyfit(A0[:, 2], A0[:, 1], 2)
    ox = np.abs(A0[:, 0]) - np.polyval(cx, A0[:, 2]); of = A0[:, 1] - np.polyval(cf, A0[:, 2]); al[m] = (ox + of) / np.sqrt(2) / (np.hypot(ox, of) + 1e-9)
SECT = dict(whole=mid, anterolateral=mid & (al > 0.35), medial_posterior=mid & (al < -0.35))
out = {}
for nm, P in (('frozen', V0), ('W2I3', RB.build_r({}, RB.TARGET)[0]), ('W2I4', _BUILD4({})[0]), ('W2I5', FN.build_f({})[0])):
    idx = np.where(mid)[0]; N = igl.per_vertex_normals(P, F0); sm = FN.gsmooth(P, idx, 1.5); r = np.zeros(len(P)); r[idx] = np.einsum('ij,ij->i', P[idx] - sm, N[idx])
    out[nm] = {k: FC.corrlen(P, N, r, np.where(m)[0], np.random.default_rng(3)) for k, m in SECT.items()}
    print(nm, {k: round(v['vertical'], 2) for k, v in out[nm].items()}, flush=True)
json.dump(out, open(sys.argv[1], 'w'), indent=1)
