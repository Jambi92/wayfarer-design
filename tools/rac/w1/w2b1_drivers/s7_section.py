# RAC W2B1 CANDIDATE (diagnostic, NOT adopted): femoral S7 (subtrochanteric, 20 % down the hip->knee axis) read as the composition infimum
# on an EXACT PLANE SECTION of the thigh faces (all three vertices thigh weight > 0.5), i.e. the accepted W1h trunk-station rule
# ("vertex slabs miss whole vertex rings where the mesh is stretched") extended to S7. The accepted reading (+/-0.8 cm vertex slab) is
# recomputed alongside on the same aligned bodies as a reproduction control.
# Usage: python3 s7_section.py OUT.json NAME=REF_REST.npz:GLOB[;GLOB...] ...   (the reference body is included in the infimum)
import sys, os, json, glob, tempfile, shutil, numpy as np
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from arm_measure import load
import skeletal_proxy as SP

def s7(d, section):
    V = d["V"].astype(float); keep = d["keep"]; J = d["joints"]; F = d["F"]; out = []
    for sd in ("l", "r"):
        hp, kn = np.asarray(J["thigh_" + sd][0], float), np.asarray(J["calf_" + sd][0], float); L = np.linalg.norm(kn - hp); ax = (kn - hp) / L
        on = keep & (d["w_thigh_" + sd] > 0.5)
        if section:
            TF = F[on[F].all(1)]; t = (V - hp) @ ax - 0.2 * L; pts = []
            for i, j in ((0, 1), (1, 2), (2, 0)):
                a, b = TF[:, i], TF[:, j]; m = t[a] * t[b] < 0; u = t[a[m]] / (t[a[m]] - t[b[m]])
                pts.append(V[a[m]] + (V[b[m]] - V[a[m]]) * u[:, None])
            P = np.vstack(pts) - hp
        else:
            tv = np.where(on)[0]; P = V[tv] - hp; tt = P @ ax; P = P[np.abs(tt - 0.2 * L) < 0.8]
        Q = P - np.outer(P @ ax, ax)
        out.append((np.ptp(Q[:, 0]), np.ptp(Q[:, 1])))
    return np.mean(out, axis=0)

def cib(ref, comps):
    rows = {}
    for p in [ref] + [c for c in comps if os.path.abspath(c) != os.path.abspath(ref)]:
        tmp = tempfile.mkdtemp(); a = os.path.join(tmp, "a.npz")
        if p == ref: shutil.copy(p, a)
        else: SP.align(p, ref, a)
        d = load(a); rows[os.path.basename(p)] = {"section": s7(d, True).tolist(), "vertex_slab": s7(d, False).tolist()}; shutil.rmtree(tmp, ignore_errors=True)
    res = {"n": len(rows), "per_body": rows}
    for k in ("section", "vertex_slab"):
        res[k] = [min(r[k][0] for r in rows.values()), min(r[k][1] for r in rows.values())]
        res[k + "_argmin"] = [min(rows, key=lambda n: rows[n][k][0]), min(rows, key=lambda n: rows[n][k][1])]
    return res

if __name__ == "__main__":
    out = {}
    for arg in sys.argv[2:]:
        n, spec = arg.split("=", 1); ref, g = spec.split(":", 1)
        out[n] = cib(ref, sorted(sum((glob.glob(x) for x in g.split(";")), []))); r = out[n]
        print(n, r["n"], "section b/d %.2f / %.2f" % tuple(r["section"]), "vertex b/d %.2f / %.2f" % tuple(r["vertex_slab"]), flush=True)
    json.dump(out, open(sys.argv[1], "w"), indent=1)
