# Compare evaluation JSON outputs between two reviews/ roots (deep, float tolerance). Usage: python3 compare.py ROOT_A ROOT_B relpath...
import sys, json
def walk(a, b, p, out):
    if isinstance(a, dict) and isinstance(b, dict):
        for k in set(a) | set(b):
            if k not in a or k not in b: out.append((p + "/" + str(k), a.get(k, "<missing>"), b.get(k, "<missing>"))); continue
            walk(a[k], b[k], p + "/" + str(k), out)
    elif isinstance(a, list) and isinstance(b, list) and len(a) == len(b):
        for i, (x, y) in enumerate(zip(a, b)): walk(x, y, p + "[%d]" % i, out)
    elif isinstance(a, (int, float)) and isinstance(b, (int, float)) and not isinstance(a, bool):
        if abs(a - b) > 1e-9 * max(1, abs(a)): out.append((p, a, b))
    elif a != b: out.append((p, a, b))
A, B = sys.argv[1], sys.argv[2]
for rel in sys.argv[3:]:
    out = []; walk(json.load(open(A + "/" + rel)), json.load(open(B + "/" + rel)), "", out)
    print("%-62s %s" % (rel, "IDENTICAL" if not out else "%d differences, e.g. %s" % (len(out), str(out[:2])[:300])))
