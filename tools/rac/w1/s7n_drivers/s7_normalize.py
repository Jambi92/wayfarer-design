# RAC S7 normalization (author ruling 2026-10-07, reviews/chatgpt-rac-w2b1-skarn-author-ruling-s7-normalization-order.md): re-read the femoral
# S7 station (subtrochanteric, 20 % down the hip->knee axis) as the composition infimum on an EXACT PLANE SECTION of the thigh faces, for an
# existing skeletal-proxy (SKP) directory, without rebuilding any body. In skeletal_proxy.py S7 enters the SKP output only as
# S7(t) = S7_bony - 2 t (t = the size-scaled tissue allowance) and through shaft_b/d_over_femur = S7(t) / femur length, so a normalized
# copy of the SKP directory is written with exactly those fields replaced. CONTROL: the old vertex-slab infimum is recomputed on the same
# resolved grid bodies and must reproduce the CIB json S7 (and the old SKP S7(t)) to 0.01 cm, otherwise the body is reported UNRESOLVED.
# Usage: python3 s7_normalize.py OUT_SKP_DIR SKP_DIR CIB_DIR_OR_JSON ROOTS(';'-separated search roots) [IDS(',')]
import sys, os, json, glob, shutil, itertools
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "w2b1_drivers"))
import s7_section as X

_IDX = {}
def index(root):
    if root not in _IDX:
        d = {}
        for p in glob.glob(os.path.join(root, "**", "*_rest.npz"), recursive=True): d.setdefault(os.path.basename(p)[:-9], []).append(p)
        _IDX[root] = d
    return _IDX[root]

def resolve(name, roots, prefer=None):
    for r in roots:
        c = index(r).get(name, [])
        if prefer: c = sorted(c, key=lambda p: (prefer not in p, len(p)))
        if c: return c
    return []

def cib_s7(cib, roots, hint):
    """Resolve the CIB grid bodies: reference x lean x composition-grid directory combinations (grid bodies taken together from one
    directory); the first combination whose vertex-slab infimum reproduces the CIB json S7 to 0.01 cm is used."""
    ref = cib["ref"][:-9] if cib["ref"].endswith("_rest.npz") else cib["ref"]
    names = [n for n in cib["per_body"] if n != ref]; grid = [n for n in names if "-C0" in n]; other = [n for n in names if n not in grid]
    tried = []
    gdirs = []
    for p in resolve(grid[0], roots, hint) if grid else [None]:
        d = os.path.dirname(p) if p else None
        if d is None or all(os.path.exists(os.path.join(d, n + "_rest.npz")) for n in grid): gdirs.append(d)
    for rp in resolve(ref, roots, hint)[:4]:
        for oc in itertools.product(*[resolve(n, [os.path.dirname(os.path.dirname(rp))] + roots, hint)[:4] for n in other]):
            for d in gdirs[:6]:
                comps = list(oc) + ([os.path.join(d, n + "_rest.npz") for n in grid] if d else [])
                res = X.cib(rp, comps)
                ok = all(abs(a - b) < 0.01 for a, b in zip(res["vertex_slab"], cib["bony"]["S7"]))
                tried.append((rp, list(oc), d, ok, res["vertex_slab"]))
                if ok: return res, rp, comps
    return None, tried, None

def main(out, skp, cibp, roots, ids=None):
    roots = [r for r in roots.split(";") if r]
    rep = {}
    ids = ids.split(",") if ids else sorted(os.path.basename(p)[:-9] for p in glob.glob(os.path.join(skp, "*_skp.json")))
    if os.path.exists(out): shutil.rmtree(out)
    shutil.copytree(skp, out)
    for i in ids:
        cj = cibp if cibp.endswith(".json") else os.path.join(cibp, i + "_cib.json")
        if not os.path.exists(cj): rep[i] = {"status": "NO CIB"}; continue
        if not all(os.path.exists(os.path.join(skp, "t%s" % t, i + "_meas.json")) for t in ("0.0", "0.5", "1.0")): rep[i] = {"status": "NO T FILES IN THIS DIR"}; continue
        C = json.load(open(cj)); sk = json.load(open(os.path.join(skp, i + "_skp.json")))
        res, rp, comps = cib_s7(C, roots, os.path.dirname(os.path.dirname(os.path.abspath(skp))))
        if res is None: rep[i] = {"status": "UNRESOLVED", "tried": rp}; continue
        tcm = sk["t_set_cm"]; old_new = {}
        for t, tc in zip(("0.0", "0.5", "1.0"), tcm):
            mp = os.path.join(out, "t%s" % t, i + "_meas.json"); m = json.load(open(mp)); c = m["combined"]
            old = list(c["alpc_stations"]["S7"]); chk = [v - 2 * tc for v in res["vertex_slab"]]
            ctrl = all(abs(a - b) < 0.01 for a, b in zip(old, chk))
            new = [v - 2 * tc for v in res["section"]]; fl = c["extra"]["femur_len"]
            c["alpc_stations"]["S7"] = new; c["ratio"]["shaft_b_over_femur"] = new[0] / fl; c["ratio"]["shaft_d_over_femur"] = new[1] / fl
            c["s7_method"] = "exact plane section (S7 normalization 2026-10-07)"; json.dump(m, open(mp, "w"), indent=1, default=float)
            sk["by_t"][t] = c; old_new[t] = {"old": old, "new": new, "control_reproduces_old": ctrl, "stature": c["stature"]}
        sk["s7_normalization"] = {"method": "exact plane section", "vertex_control": res["vertex_slab"], "section": res["section"], "ref": rp, "n": res["n"]}
        json.dump(sk, open(os.path.join(out, i + "_skp.json"), "w"), indent=1, default=float)
        rep[i] = {"status": "NORMALIZED" if all(v["control_reproduces_old"] for v in old_new.values()) else "CONTROL MISMATCH",
                  "ref": rp, "n": res["n"], "bony_vertex": res["vertex_slab"], "bony_section": res["section"], "by_t": old_new}
        print(i, rep[i]["status"], "vertex %.2f/%.2f -> section %.2f/%.2f" % (*res["vertex_slab"], *res["section"]), flush=True)
    json.dump(rep, open(os.path.join(out, "s7_normalization_report.json"), "w"), indent=1, default=float)

if __name__ == "__main__":
    main(*sys.argv[1:6])
