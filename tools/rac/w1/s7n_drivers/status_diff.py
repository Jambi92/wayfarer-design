# S7 normalization: row-level result comparison between the committed evidence (ROOT_A) and the normalized re-run (ROOT_B).
# Usage: python3 status_diff.py ROOT_A ROOT_B OUT.json relpath...
import sys, json
def rows(d):
    if isinstance(d, dict) and "rows" in d: d = d["rows"]
    if isinstance(d, dict) and "checks" in d: d = d["checks"]
    return d if isinstance(d, list) else []
def label(r): return " | ".join(str(r.get(k)) for k in ("code", "cand", "check") if r.get(k) is not None)
def vals(r):
    for k in ("by_t", "va"):
        if k in r: return {"by_t": r.get("by_t"), "va": r.get("va"), "vb": r.get("vb"), "note": r.get("note")}
    return {}
A, B, OUT = sys.argv[1:4]; rep = {}
for rel in sys.argv[4:]:
    ra, rb = rows(json.load(open(A + "/" + rel))), rows(json.load(open(B + "/" + rel)))
    assert len(ra) == len(rb), rel
    ch, s7 = [], 0
    for x, y in zip(ra, rb):
        assert label(x) == label(y), (rel, label(x), label(y))
        dep = json.dumps(x, default=str) != json.dumps(y, default=str)
        if dep: s7 += 1
        if x.get("result") != y.get("result"): ch.append({"row": label(x), "old": x.get("result"), "new": y.get("result"), "old_values": vals(x), "new_values": vals(y)})
    rep[rel] = {"rows": len(ra), "rows_with_changed_values": s7, "status_changes": ch}
    print("%-58s rows %4d  value-changed %4d  status changes %d" % (rel, len(ra), s7, len(ch)))
    for c in ch: print("     %s: %s -> %s" % (c["row"][:120], c["old"], c["new"]))
json.dump(rep, open(OUT, "w"), indent=1, default=float)
